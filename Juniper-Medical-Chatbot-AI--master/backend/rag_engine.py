"""
RAG Engine Module
Coordinates retrieval and generation for RAG chatbot
"""

from typing import List, Dict, Optional, Any
import logging
from .vector_store import VectorStore
from .llm_service import LLMService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGEngine:
    """
    Main RAG (Retrieval-Augmented Generation) engine
    Coordinates document retrieval and response generation
    """

    def __init__(self, vector_store: VectorStore, llm_service: LLMService, top_k: int = 5):
        """
        Initialize RAG engine

        Args:
            vector_store: Vector store instance
            llm_service: LLM service instance
            top_k: Number of documents to retrieve
        """
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.top_k = top_k

        # Conversation memory
        self.conversations = {}

        logger.info("RAG Engine initialized")

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

            # Step 1: Retrieve relevant documents
            retrieved_docs = self.vector_store.search(user_query, top_k=self.top_k)

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

        for doc in retrieved_docs:
            metadata = doc.get('metadata', {})
            sources.append({
                'title': metadata.get('title', 'Unknown'),
                'category': metadata.get('category', 'general'),
                'similarity': round(doc.get('similarity', 0), 3)
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

"""
Juniper Medical AI
Author: Huzaifa Naseem
Original GitHub Repository: https://github.com/HuzaifaNaseem/Juniper-Medical-Chatbot-AI
This file is part of the original Juniper project.
Unauthorized redistribution is prohibited.
"""

