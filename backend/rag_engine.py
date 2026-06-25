"""
RAG Engine Module
Coordinates retrieval and generation for RAG chatbot
"""

from typing import List, Dict, Optional, Any
import re
import logging
from .vector_store import VectorStore
from .llm_service import LLMService
from . import safety
from .references import reference_for

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common English words that carry little retrieval signal — ignored when
# computing the lexical re-rank boost.
_STOPWORDS = {
    'the', 'and', 'for', 'are', 'what', 'how', 'why', 'when', 'who', 'can',
    'does', 'with', 'about', 'tell', 'have', 'has', 'this', 'that', 'from',
    'your', 'you', 'they', 'them', 'there', 'here', 'into', 'out', 'get',
    'should', 'would', 'could', 'may', 'might', 'will', 'his', 'her', 'its',
    'their', 'some', 'any', 'all', 'more', 'most', 'such', 'than', 'then',
    'between', 'symptoms', 'symptom', 'causes', 'cause', 'treatment', 'disease',
}


class RAGEngine:
    """
    Main RAG (Retrieval-Augmented Generation) engine
    Coordinates document retrieval and response generation
    """

    def __init__(self, vector_store: VectorStore, llm_service: LLMService, top_k: int = 5,
                 retrieval_candidates: int = 10, min_relevance: float = 0.18,
                 relevance_ratio: float = 0.5):
        """
        Initialize RAG engine

        Args:
            vector_store: Vector store instance
            llm_service: LLM service instance
            top_k: Final number of documents to keep for context/citations
            retrieval_candidates: How many candidates to fetch before re-ranking
            min_relevance: Absolute cosine-similarity floor to keep a doc
            relevance_ratio: Keep docs within this fraction of the top score
        """
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.top_k = top_k
        self.retrieval_candidates = max(retrieval_candidates, top_k)
        self.min_relevance = min_relevance
        self.relevance_ratio = relevance_ratio

        # Conversation memory
        self.conversations = {}

        logger.info("RAG Engine initialized")

    def _retrieve(self, user_query: str) -> List[Dict[str, Any]]:
        """
        Retrieve, re-rank, and filter documents for a query.

        Fetches a wider candidate set from the vector store, then re-ranks with a
        lexical boost (query terms appearing in a document's title are a strong
        signal) and drops weakly-related documents so the context and citations
        stay clean and on-topic.
        """
        candidates = self.vector_store.search(user_query, top_k=self.retrieval_candidates)
        if not candidates:
            return []

        query_terms = {
            t for t in re.findall(r'[a-z]{3,}', user_query.lower())
            if t not in _STOPWORDS
        }

        for doc in candidates:
            similarity = doc.get('similarity', 0) or 0
            title = (doc.get('metadata', {}) or {}).get('title', '').lower()
            content = (doc.get('document', '') or '').lower()

            title_hits = sum(1 for t in query_terms if t in title)
            content_hits = sum(1 for t in query_terms if t in content)
            # Title matches are weighted much more heavily than body matches.
            boost = 0.10 * title_hits + 0.015 * min(content_hits, 4)
            doc['rerank_score'] = similarity + boost

        candidates.sort(key=lambda d: d['rerank_score'], reverse=True)

        # Relative + absolute relevance filtering.
        top_sim = max((d.get('similarity', 0) or 0) for d in candidates)
        cutoff = max(self.min_relevance, top_sim * self.relevance_ratio)
        filtered = [d for d in candidates if (d.get('similarity', 0) or 0) >= cutoff]

        # Always keep at least the single best match so we never go empty.
        result = (filtered or candidates[:1])[:self.top_k]
        logger.info(
            f"Retrieval: {len(candidates)} candidates -> {len(result)} kept "
            f"(cutoff={cutoff:.3f})"
        )
        return result

    def query(self, user_query: str, conversation_id: Optional[str] = None, language: str = 'en') -> Dict[str, Any]:
        """
        Process a user query using RAG pipeline

        Args:
            user_query: User's question
            conversation_id: Optional conversation ID for context
            language: Language for response ('en' for English, 'ur' for Roman Urdu)

        Returns:
            Dictionary containing response and metadata
        """
        try:
            logger.info(f"Processing query (lang: {language}): '{user_query[:100]}...'")

            # Step 0: Safety guardrail — intercept emergencies / self-harm BEFORE
            # the LLM is ever involved, returning safe hard-coded guidance instead.
            safety_result = safety.screen_message(user_query, language)
            if safety_result is not None:
                logger.warning(
                    f"Query intercepted by safety guardrail: {safety_result['safety_flag']}"
                )
                return {
                    'response': safety_result['response'],
                    'sources': [],
                    'conversation_id': conversation_id,
                    'safety_flag': safety_result['safety_flag'],
                }

            # Step 1: Retrieve, re-rank, and filter relevant documents
            retrieved_docs = self._retrieve(user_query)

            if not retrieved_docs:
                logger.warning("No relevant documents found")
                return {
                    'response': self._generate_fallback_response(user_query, language),
                    'sources': [],
                    'conversation_id': conversation_id
                }

            # Step 2: Build context from retrieved documents
            context = self._build_context(retrieved_docs)

            # Step 3: Get conversation history
            conversation_history = self._get_conversation_history(conversation_id)

            # Step 4: Generate response using LLM
            response = self.llm_service.generate_rag_response(
                query=user_query,
                context=context,
                conversation_history=conversation_history,
                language=language
            )

            # Step 5: Update conversation history
            if conversation_id:
                self._update_conversation(
                    conversation_id,
                    user_query,
                    response
                )

            # Step 6: Format sources
            sources = self._format_sources(retrieved_docs)

            logger.info("Query processed successfully")

            return {
                'response': response,
                'sources': sources,
                'conversation_id': conversation_id,
                'retrieved_docs_count': len(retrieved_docs)
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            error_msg = "I apologize, but I encountered an error processing your request. Please try again." if language == 'en' else "Maafi, mujhe aapke sawal ka jawab dene mein masla ho raha hai. Mehrbani karke dobara koshish karein."
            return {
                'response': error_msg,
                'sources': [],
                'conversation_id': conversation_id,
                'error': str(e)
            }

    def query_stream(self, user_query: str, conversation_id: Optional[str] = None,
                     language: str = 'en'):
        """
        Streaming version of query(). Yields event dicts that the API layer
        converts to Server-Sent Events:
          {"type": "meta", "conversation_id", "safety_flag"}
          {"type": "token", "text"}
          {"type": "sources", "data": [...]}
          {"type": "suggestions", "data": [...]}
          {"type": "done"}
          {"type": "error", "error"}
        """
        try:
            logger.info(f"Streaming query (lang: {language}): '{user_query[:100]}...'")

            # Step 0: Safety guardrail — intercept before any LLM/retrieval.
            safety_result = safety.screen_message(user_query, language)
            if safety_result is not None:
                logger.warning(
                    f"Stream intercepted by safety guardrail: {safety_result['safety_flag']}"
                )
                yield {"type": "meta", "conversation_id": conversation_id,
                       "safety_flag": safety_result['safety_flag']}
                yield {"type": "token", "text": safety_result['response']}
                yield {"type": "sources", "data": []}
                yield {"type": "done"}
                return

            yield {"type": "meta", "conversation_id": conversation_id, "safety_flag": None}

            # Step 1: Retrieve, re-rank, and filter
            retrieved_docs = self._retrieve(user_query)

            if not retrieved_docs:
                fallback = self._generate_fallback_response(user_query, language)
                yield {"type": "token", "text": fallback}
                yield {"type": "sources", "data": []}
                yield {"type": "done"}
                return

            # Step 2-4: Build context, history, then stream the answer.
            context = self._build_context(retrieved_docs)
            conversation_history = self._get_conversation_history(conversation_id)

            full_answer_parts = []
            for chunk in self.llm_service.stream_rag_response(
                query=user_query,
                context=context,
                conversation_history=conversation_history,
                language=language,
            ):
                full_answer_parts.append(chunk)
                yield {"type": "token", "text": chunk}

            full_answer = "".join(full_answer_parts).strip()

            # Step 5: Persist conversation + emit sources.
            if conversation_id:
                self._update_conversation(conversation_id, user_query, full_answer)

            yield {"type": "sources", "data": self._format_sources(retrieved_docs)}

            # Step 6: Follow-up suggestions (best-effort, never fatal).
            suggestions = self.llm_service.generate_followup_questions(
                user_query, full_answer, language
            )
            if suggestions:
                yield {"type": "suggestions", "data": suggestions}

            yield {"type": "done"}
            logger.info("Streaming query completed successfully")

        except Exception as e:
            logger.error(f"Error in streaming query: {e}")
            yield {"type": "error", "error": str(e)}

    def _build_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Build context string from retrieved documents

        Args:
            retrieved_docs: List of retrieved documents

        Returns:
            Formatted context string
        """
        context_parts = []

        for idx, doc in enumerate(retrieved_docs, 1):
            document_text = doc.get('document', '')
            context_parts.append(document_text.strip())

        return "\n\n".join(context_parts)

    def _get_conversation_history(self, conversation_id: Optional[str]) -> List[Dict[str, str]]:
        """
        Get conversation history for a conversation ID

        Args:
            conversation_id: Conversation identifier

        Returns:
            List of message dictionaries
        """
        if not conversation_id or conversation_id not in self.conversations:
            return []

        return self.conversations[conversation_id]

    def _update_conversation(self, conversation_id: str, user_message: str, assistant_message: str):
        """
        Update conversation history

        Args:
            conversation_id: Conversation identifier
            user_message: User's message
            assistant_message: Assistant's response
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_message}
        ])

        # Keep only last 10 exchanges (20 messages)
        if len(self.conversations[conversation_id]) > 20:
            self.conversations[conversation_id] = self.conversations[conversation_id][-20:]

    def _format_sources(self, retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format source information for response

        Args:
            retrieved_docs: Retrieved documents

        Returns:
            List of formatted source dictionaries
        """
        sources = []
        seen_titles = set()

        for doc in retrieved_docs:
            metadata = doc.get('metadata', {})
            title = metadata.get('title', 'Unknown')

            # De-duplicate by title so the same topic isn't cited twice.
            if title in seen_titles:
                continue
            seen_titles.add(title)

            category = metadata.get('category', 'general')
            reference = reference_for(category)

            sources.append({
                'title': title,
                'category': category,
                'similarity': round(doc.get('similarity', 0), 3),
                # Whole-number relevance percentage for clean display.
                'relevance': max(0, min(100, round(doc.get('similarity', 0) * 100))),
                'reference_name': reference['name'],
                'reference_url': reference['url'],
            })

        return sources

    def _generate_fallback_response(self, query: str, language: str = 'en') -> str:
        """
        Generate fallback response when no documents are retrieved

        Args:
            query: User query
            language: Language for response

        Returns:
            Fallback response
        """
        if language == 'ur':
            return """Maafi chahta hoon, lekin mujhe apne medical knowledge base mein aapke sawal ka koi khaas jawab nahi mila.

Ye is wajah se ho sakta hai:
1. Ye topic bohat specialized hai ya mere current knowledge ke bahar hai
2. Sawal ko doosre tareeqe se poochna behtar hoga

Meri taraf se mashwara:
- Apne sawal ko medical terms ke sath dobara likhein
- Mushkil sawalo ko chhote chhote hisson mein taqseem karein
- Kisi doctor ya healthcare professional se mashwara zaroor lein

Kya main aapki kisi aur medical topic mein madad kar sakta hoon?"""
        else:
            return """I apologize, but I couldn't find specific information in my medical knowledge base to answer your question.

This could be because:
1. The topic is very specialized or outside my current knowledge scope
2. The question needs to be rephrased for better matching

I recommend:
- Rephrasing your question with more specific medical terms
- Breaking down complex questions into simpler parts
- Consulting with healthcare professionals for specialized medical advice

How can I help you with another medical topic?"""

    def clear_conversation(self, conversation_id: str):
        """
        Clear conversation history for a conversation ID

        Args:
            conversation_id: Conversation identifier
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Cleared conversation: {conversation_id}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get RAG engine statistics

        Returns:
            Dictionary with statistics
        """
        return {
            'vector_store_stats': self.vector_store.get_stats(),
            'active_conversations': len(self.conversations),
            'top_k': self.top_k
        }
