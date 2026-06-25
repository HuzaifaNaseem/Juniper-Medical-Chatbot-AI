"""
Juniper Configuration Module
Manages environment variables and application settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'

    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

    # RAG Configuration
    EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    # Chunking is measured in words. 300/50 splits longer multi-section topics
    # (and large external summaries like MedlinePlus) into focused, overlapping
    # passages while keeping short topics whole.
    CHUNK_SIZE = 300
    CHUNK_OVERLAP = 50
    TOP_K_RESULTS = 5            # final docs used for context/citations

    # Retrieval re-ranking (Tier 2). Pull more candidates, re-rank with a
    # lexical boost, then keep only the genuinely relevant ones.
    RETRIEVAL_CANDIDATES = 10    # how many to fetch before re-ranking
    MIN_RELEVANCE = 0.18         # absolute cosine-similarity floor
    RELEVANCE_RATIO = 0.5        # keep docs within this fraction of the top score

    # LLM Configuration
    LLM_MODEL = "llama-3.3-70b-versatile"  # Groq's Llama 3.3 70B model (latest)
    LLM_TEMPERATURE = 0.3
    LLM_MAX_TOKENS = 1024

    # Vision model (multimodal) for photo analysis. Overridable via env in case
    # Groq renames/deprecates the model. Confirm the current id at console.groq.com.
    VISION_MODEL = os.getenv('VISION_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')
    VISION_MAX_TOKENS = 1024
    MAX_IMAGE_BYTES = 4 * 1024 * 1024  # 4 MB cap on uploaded images

    # ChromaDB Configuration
    CHROMA_DB_PATH = './data/chroma_db'
    COLLECTION_NAME = 'medical_knowledge'

    # Application Settings
    MAX_MESSAGE_LENGTH = 2000
    CONVERSATION_TIMEOUT = 3600  # 1 hour in seconds

    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # Admin token guarding the /api/debug diagnostics endpoint. If unset, the
    # endpoint is disabled entirely (returns 404) rather than leaking internals.
    ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', '')

    # Rate limiting (flask-limiter). Per-IP caps to curb abuse of the LLM-backed
    # endpoints. Storage defaults to in-process memory; set RATELIMIT_STORAGE_URI
    # (e.g. redis://...) to share limits across workers.
    RATELIMIT_STORAGE_URI = os.getenv('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '200 per hour')
    RATELIMIT_CHAT = os.getenv('RATELIMIT_CHAT', '20 per minute')
    RATELIMIT_VISION = os.getenv('RATELIMIT_VISION', '10 per minute')
    RATELIMIT_AUTH = os.getenv('RATELIMIT_AUTH', '10 per minute')

    @staticmethod
    def validate():
        """Validate critical configuration"""
        if not Config.GROQ_API_KEY:
            print("⚠️  WARNING: GROQ_API_KEY not set. Please add it to your .env file")
            print("   Get your free API key at: https://console.groq.com")
            return False
        return True


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


# Configuration dictionary
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': Config
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'production')
    return config_dict.get(env, Config)
