"""
Juniper Medical AI
Author: Huzaifa Naseem
Original GitHub Repository: https://github.com/HuzaifaNaseem/Juniper-Medical-Chatbot-AI
This file is part of the original Juniper project.
Unauthorized redistribution is prohibited.
"""


"""
Juniper - Medical Research Assistant
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import os

from config import get_config, Config
from backend.vector_store import VectorStore
from backend.llm_service import LLMService
from backend.rag_engine import RAGEngine
from backend.user_auth import UserAuth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
config_class = get_config()
app.config.from_object(config_class)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": config_class.CORS_ORIGINS}})

# Global RAG engine and auth instances
rag_engine = None
user_auth = None


def initialize_rag_engine():
    """Initialize RAG engine with vector store and LLM service"""
    global rag_engine

    try:
        logger.info("Initializing RAG engine...")

        # Validate configuration
        if not Config.validate():
            logger.error("Configuration validation failed")
            return False

        # Initialize vector store
        logger.info("Loading vector store...")
        vector_store = VectorStore(
            db_path=Config.CHROMA_DB_PATH,
            collection_name=Config.COLLECTION_NAME,
            embedding_model_name=Config.EMBEDDING_MODEL
        )

        # Check if vector store has documents
        if vector_store.collection.count() == 0:
            logger.error("Vector store is empty. Please run 'python initialize_kb.py' first")
            return False

        # Initialize LLM service
        logger.info("Initializing LLM service...")
        llm_service = LLMService(
            api_key=Config.GROQ_API_KEY,
            model=Config.LLM_MODEL,
            temperature=Config.LLM_TEMPERATURE,
            max_tokens=Config.LLM_MAX_TOKENS
        )

        # Test LLM connection
        if not llm_service.test_connection():
            logger.error("Failed to connect to Groq API. Please check your API key")
            return False

        # Initialize RAG engine
        rag_engine = RAGEngine(
            vector_store=vector_store,
            llm_service=llm_service,
            top_k=Config.TOP_K_RESULTS
        )

        logger.info("✓ RAG engine initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Error initializing RAG engine: {e}")
        return False


# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if rag_engine is None:
            return jsonify({
                'status': 'error',
                'message': 'RAG engine not initialized'
            }), 503

        stats = rag_engine.get_stats()

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'stats': stats
        }), 200

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Expects JSON: {"message": "user query", "conversation_id": "optional_id"}
    """
    try:
        # Validate RAG engine
        if rag_engine is None:
            return jsonify({
                'error': 'System not initialized. Please contact administrator.'
            }), 503

        # Get request data
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message'
            }), 400

        user_message = data['message'].strip()
        conversation_id = data.get('conversation_id')
        language = data.get('language', 'en')  # Get language, default to English

        # Validate message
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400

        if len(user_message) > Config.MAX_MESSAGE_LENGTH:
            return jsonify({
                'error': f'Message too long. Maximum {Config.MAX_MESSAGE_LENGTH} characters'
            }), 400

        logger.info(f"Processing chat request (lang: {language}): '{user_message[:100]}...'")

        # Process query through RAG engine with language parameter
        result = rag_engine.query(
            user_query=user_message,
            conversation_id=conversation_id,
            language=language
        )

        # Build response
        response_data = {
            'response': result['response'],
            'conversation_id': result.get('conversation_id'),
            'sources': result.get('sources', []),
            'timestamp': datetime.utcnow().isoformat()
        }

        logger.info("Chat request processed successfully")
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'An error occurred processing your request. Please try again.'
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')

        if not conversation_id:
            return jsonify({
                'error': 'Missing conversation_id'
            }), 400

        if rag_engine:
            rag_engine.clear_conversation(conversation_id)

        return jsonify({
            'message': 'Conversation cleared successfully'
        }), 200

    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        return jsonify({
            'error': 'Failed to clear conversation'
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        if rag_engine is None:
            return jsonify({
                'error': 'System not initialized'
            }), 503

        stats = rag_engine.get_stats()

        return jsonify({
            'stats': stats,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'error': 'Failed to retrieve statistics'
        }), 500


# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        result = user_auth.register_user(email, username, password)

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({
            'success': False,
            'message': 'Registration failed'
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()

        email = data.get('email', '').strip()
        password = data.get('password', '')

        result = user_auth.login_user(email, password)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': 'Login failed'
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        data = request.get_json()
        session_token = data.get('session_token', '')

        user_auth.logout_user(session_token)

        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200

    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({
            'success': False,
            'message': 'Logout failed'
        }), 500


@app.route('/api/auth/validate', methods=['POST'])
def validate_session():
    """Validate session token"""
    try:
        data = request.get_json()
        session_token = data.get('session_token', '')

        user = user_auth.validate_session(session_token)

        if user:
            return jsonify({
                'success': True,
                'user': user
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired session'
            }), 401

    except Exception as e:
        logger.error(f"Session validation error: {e}")
        return jsonify({
            'success': False,
            'message': 'Validation failed'
        }), 500


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error'
    }), 500


# ==========================================
# APPLICATION STARTUP
# ==========================================

def startup():
    """Application startup tasks"""
    global user_auth

    print("\n" + "=" * 60)
    print("JUNIPER - Medical Research Assistant")
    print("=" * 60)
    print(f"\nEnvironment: {Config.FLASK_ENV}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Model: {Config.LLM_MODEL}")

    # Initialize user authentication
    try:
        user_auth = UserAuth()
        print("✓ User authentication initialized")
    except Exception as e:
        logger.error(f"Failed to initialize user authentication: {e}")
        print("⚠ User authentication initialization failed (continuing without auth)")

    # Initialize RAG engine
    if not initialize_rag_engine():
        print("\nWARNING: RAG engine initialization failed")
        print("\nPlease ensure:")
        print("  1. You have created a .env file with your GROQ_API_KEY")
        print("  2. You have run 'python initialize_kb.py' to set up the knowledge base")
        print("\n" + "=" * 60)
        return False

    print("\nSystem initialized successfully")
    print("=" * 60)
    return True


if __name__ == '__main__':
    # Run startup tasks
    if startup():
        # Start Flask server
        port = int(os.environ.get('PORT', 5000))
        print(f"\nStarting server on http://localhost:{port}")
        print("Press CTRL+C to stop\n")

        app.run(
            host='0.0.0.0',
            port=port,
            debug=Config.DEBUG
        )
    else:
        print("\nServer startup aborted due to initialization errors")
        exit(1)
