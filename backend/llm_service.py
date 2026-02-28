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

    def generate_rag_response(self, query: str, context: str,
                            conversation_history: Optional[List[Dict[str, str]]] = None,
                            language: str = 'en') -> str:
        """
        Generate a response using RAG context

        Args:
            query: User query
            context: Retrieved context from vector store
            conversation_history: Previous conversation turns
            language: Language for response ('en' for English, 'ur' for Roman Urdu)

        Returns:
            Generated response
        """
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

FORMATTING RULES:
- Write in Roman Urdu using Latin alphabet (a-z)
- Use a natural, conversational tone in Roman Urdu
- Use simple paragraphs separated by blank lines
- DO NOT use markdown headers (##, ===, ---)
- DO NOT use bold (**text**) or italic formatting
- DO NOT reference sources explicitly like [Source 1] or [Source 5] in the response

EXAMPLES of Roman Urdu responses:
- "Diabetes ya sugar ki bimari aik aisi bemari hai jis mein khoon mein sugar ki miqdar bohat zyada barh jati hai."
- "Ye bemari do qisam ki hoti hai - Type 1 aur Type 2. Type 1 diabetes mein jism insulin nahi bana pata."
- "Is ki wajah se aap ko ye alamat ho sakti hain: zyada pyas lagna, bar bar peshab ana, aur kamzori mehsoos hona."
- "Behtar hoga ke aap kisi doctor se salah karein aur apna check-up zaroor karwayen."

Remember: Write your COMPLETE response in Roman Urdu. Every word, every sentence must be in Roman Urdu, NOT English."""
        else:
            system_message = """You are Juniper, an AI-powered medical research assistant. Your role is to provide accurate, helpful, and clear medical information based on the knowledge provided to you.

IMPORTANT GUIDELINES:
1. Base your answers primarily on the provided CONTEXT
2. Provide clear, concise, and professional responses without excessive formatting
3. Use medical terminology appropriately but explain complex terms
4. If the context doesn't fully answer the question, provide what information is available and acknowledge limitations
5. Always remind users to consult healthcare professionals for medical advice
6. Be empathetic and supportive in your responses

FORMATTING RULES:
- Write in a natural, conversational tone
- Use simple paragraphs separated by blank lines
- DO NOT use markdown headers (##, ===, ---)
- DO NOT use bold (**text**) or italic formatting
- DO NOT reference sources explicitly like [Source 1] or [Source 5] in the response
- DO NOT create artificial sections with headers
- Present information in a flowing, readable manner

Remember: You are a research and educational tool, not a substitute for professional medical advice."""

        # Build user message with context and query
        if language == 'ur':
            user_message = f"""CONTEXT (Retrieved Medical Knowledge):
{context}

USER QUESTION (in Roman Urdu):
{query}

IMPORTANT: You MUST respond in ROMAN URDU ONLY. Do NOT write in English. Write your complete answer in Roman Urdu (Urdu language using English alphabet). Start your response immediately in Roman Urdu without any English words. Use simple Roman Urdu that is easy to understand."""
        else:
            user_message = f"""CONTEXT (Retrieved Medical Knowledge):
{context}

USER QUESTION:
{query}

Please provide a clear and professional answer based on the context above. Write in a natural, conversational style without markdown formatting, headers, or source citations."""

        # Build messages list
        messages = [{"role": "system", "content": system_message}]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Last 3 exchanges

        # Add current query
        messages.append({"role": "user", "content": user_message})

        return self.generate_response(messages)

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
