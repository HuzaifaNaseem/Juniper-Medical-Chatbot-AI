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
    SECRET_KEY = os.getenv('SECRET_KEY', 'juniper-medical-assistant-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'

    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

    # RAG Configuration
    EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K_RESULTS = 5

    # LLM Configuration
    LLM_MODEL = "llama-3.3-70b-versatile"  # Groq's Llama 3.3 70B model (latest)
    LLM_TEMPERATURE = 0.3
    LLM_MAX_TOKENS = 1024

    # ChromaDB Configuration
    CHROMA_DB_PATH = './data/chroma_db'
    COLLECTION_NAME = 'medical_knowledge'

    # Application Settings
    MAX_MESSAGE_LENGTH = 2000
    CONVERSATION_TIMEOUT = 3600  # 1 hour in seconds

    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

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
