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

# Global RAG engine instance
rag_engine = None


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

        # Validate message
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400

        if len(user_message) > Config.MAX_MESSAGE_LENGTH:
            return jsonify({
                'error': f'Message too long. Maximum {Config.MAX_MESSAGE_LENGTH} characters'
            }), 400

        logger.info(f"Processing chat request: '{user_message[:100]}...'")

        # Process query through RAG engine
        result = rag_engine.query(
            user_query=user_message,
            conversation_id=conversation_id
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
    print("\n" + "=" * 60)
    print("JUNIPER - Medical Research Assistant")
    print("=" * 60)
    print(f"\nEnvironment: {Config.FLASK_ENV}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Model: {Config.LLM_MODEL}")

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
