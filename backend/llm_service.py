"""
LLM Service Module
Handles integration with Groq API for text generation
"""

from groq import Groq
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with Groq LLM API
    """

    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile",
                 temperature: float = 0.3, max_tokens: int = 1024):
        """
        Initialize LLM service

        Args:
            api_key: Groq API key
            model: Model name
            temperature: Temperature for generation (0-2)
            max_tokens: Maximum tokens to generate
        """
        if not api_key:
            raise ValueError("Groq API key is required")

        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        logger.info(f"Initialized LLM service with model: {model}")

    def generate_response(self, messages: List[Dict[str, str]],
                         temperature: Optional[float] = None,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the LLM

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Returns:
            Generated response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                top_p=1,
                stream=False
            )

            generated_text = response.choices[0].message.content.strip()
            logger.info(f"Generated response ({len(generated_text)} chars)")

            return generated_text

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def _build_rag_messages(self, query: str, context: str,
                            conversation_history: Optional[List[Dict[str, str]]] = None,
                            language: str = 'en') -> List[Dict[str, str]]:
        """Build the message list for a RAG completion (shared by stream + non-stream)."""
        # Build system message with instructions based on language
        if language == 'ur':
            system_message = """You are Juniper, an AI-powered medical research assistant who speaks ONLY in Roman Urdu.

CRITICAL RULE - RESPOND IN ROMAN URDU ONLY:
⚠️ DO NOT write in English
⚠️ You MUST write your ENTIRE response in Roman Urdu (Urdu language written using English alphabet)
⚠️ Every single sentence must be in Roman Urdu
⚠️ DO NOT mix English and Roman Urdu - use ONLY Roman Urdu

IMPORTANT GUIDELINES:
1. Base your answers primarily on the provided CONTEXT
2. Use simple Roman Urdu that is easy to understand
3. Explain medical terms in Roman Urdu when possible (e.g., "diabetes" = "sugar ki bimari")
4. If the context doesn't fully answer the question, provide what information is available
5. Always remind users to consult healthcare professionals (doctor se mashwara zaroor lein)
6. Be empathetic and supportive in your responses

FORMATTING (use clean, light Markdown — it will be rendered):
- Write the WORDS in Roman Urdu, but you MAY use Markdown structure
- Use short **bold** for key terms (e.g., **Diabetes**)
- Use bullet points (-) for lists of symptoms, causes, or tips
- Use a short bold mini-heading like **Alamaat:** or **Ilaaj:** where helpful
- End with a brief reminder line: "Doctor se mashwara zaroor karein."
- DO NOT reference sources explicitly like [Source 1] in the text
- Keep it concise and easy to read — avoid long dense paragraphs

Remember: Write your COMPLETE response in Roman Urdu. Every word must be in Roman Urdu, NOT English."""
        else:
            system_message = """You are Juniper, an AI-powered medical research assistant. Your role is to provide accurate, helpful, and clear medical information based on the knowledge provided to you.

IMPORTANT GUIDELINES:
1. Base your answers primarily on the provided CONTEXT
2. Be accurate, clear, and professional; explain medical terms in plain language
3. If the context doesn't fully answer the question, share what is available and acknowledge the limitation
4. Be empathetic and supportive
5. When relevant, include a brief "When to see a doctor" note for warning signs

HANDLING VAGUE QUESTIONS:
- If the question is clear, answer it directly and fully.
- ONLY if the question is too vague to answer well (e.g., just "I feel unwell" or "I have pain"),
  briefly acknowledge it, give safe general guidance, AND ask ONE short clarifying question
  (e.g., "How long have you had this, and where exactly is the pain?"). Do not ask more than one.

ANSWER STRUCTURE (use clean Markdown — it is rendered for the user):
- Open with a 1-2 sentence plain-language **summary** answering the core question
- Then use short bold mini-headings where they help: **Symptoms**, **Causes**, **Treatment / Management**, **When to see a doctor**
- Use bullet points (-) for lists; keep paragraphs short and scannable
- **Bold** key terms and warning signs
- Do NOT use giant headers (#), and do NOT add inline source citations like [Source 1]
- End with a short, non-alarming reminder to consult a healthcare professional

Remember: You are a research and educational tool, not a substitute for professional medical advice."""

        # Build user message with context and query
        if language == 'ur':
            user_message = f"""CONTEXT (Retrieved Medical Knowledge):
{context}

USER QUESTION (in Roman Urdu):
{query}

IMPORTANT: Respond in ROMAN URDU ONLY (Urdu using English alphabet). You may use light Markdown (bold, bullets) for structure, but every word must be Roman Urdu, not English."""
        else:
            user_message = f"""CONTEXT (Retrieved Medical Knowledge):
{context}

USER QUESTION:
{query}

Answer using the context above. Format with clean Markdown (short bold headings, bullet points, bold key terms) so it is easy to read. Do not include inline source citations."""

        messages = [{"role": "system", "content": system_message}]
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Last 3 exchanges
        messages.append({"role": "user", "content": user_message})
        return messages

    def generate_rag_response(self, query: str, context: str,
                            conversation_history: Optional[List[Dict[str, str]]] = None,
                            language: str = 'en') -> str:
        """
        Generate a (non-streamed) response using RAG context.
        Kept for the legacy /api/chat endpoint and as a fallback.
        """
        messages = self._build_rag_messages(query, context, conversation_history, language)
        return self.generate_response(messages)

    def stream_rag_response(self, query: str, context: str,
                            conversation_history: Optional[List[Dict[str, str]]] = None,
                            language: str = 'en'):
        """
        Stream a RAG response token-by-token. Yields text chunks as they arrive.

        Args:
            query: User query
            context: Retrieved context from vector store
            conversation_history: Previous conversation turns
            language: Response language

        Yields:
            str: incremental text chunks
        """
        messages = self._build_rag_messages(query, context, conversation_history, language)
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise

    def generate_followup_questions(self, query: str, answer: str,
                                    language: str = 'en') -> List[str]:
        """
        Generate up to 3 short, relevant follow-up questions a user might ask next.
        Returns a list of strings (empty list on any failure — never fatal).
        """
        try:
            if language == 'ur':
                instruction = (
                    "User ne ye sawal poocha aur ye jawab mila. 3 chhote, relevant follow-up "
                    "sawal Roman Urdu mein do jo user aage pooch sakta hai. Sirf sawal, har aik "
                    "nai line par, bina number ke."
                )
            else:
                instruction = (
                    "Based on the question and answer below, suggest 3 short, natural follow-up "
                    "questions the user might ask next. Output ONLY the questions, one per line, "
                    "no numbering, no extra text. Keep each under 12 words."
                )
            prompt = f"{instruction}\n\nQUESTION: {query}\n\nANSWER: {answer[:1500]}"
            raw = self.generate_response(
                [{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=120,
            )
            # Parse lines, strip bullets/numbering, keep up to 3 non-empty.
            questions = []
            for line in raw.splitlines():
                line = line.strip().lstrip("-*0123456789.) ").strip()
                if line and line.endswith("?") and len(line) <= 120:
                    questions.append(line)
            return questions[:3]
        except Exception as e:
            logger.warning(f"Follow-up generation failed (non-fatal): {e}")
            return []

    def test_connection(self) -> bool:
        """
        Test connection to Groq API

        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_messages = [
                {"role": "user", "content": "Say 'Hello' if you're working."}
            ]
            response = self.generate_response(test_messages, max_tokens=50)
            logger.info("LLM connection test successful")
            return True
        except Exception as e:
            logger.error(f"LLM connection test failed: {e}")
            return False
