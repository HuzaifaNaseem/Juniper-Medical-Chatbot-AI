"""
Knowledge Base Initialization Script
Loads medical knowledge into ChromaDB vector store
Run this once to initialize the knowledge base
"""

import sys
import os
from backend.knowledge_base import MEDICAL_KNOWLEDGE
from backend.vector_store import VectorStore
from config import Config

def main():
    """Initialize the knowledge base"""
    print("=" * 60)
    print("JUNIPER - Medical Knowledge Base Initialization")
    print("=" * 60)

    # Load configuration
    config = Config()

    print(f"\nConfiguration:")
    print(f"  Database Path: {config.CHROMA_DB_PATH}")
    print(f"  Collection Name: {config.COLLECTION_NAME}")
    print(f"  Embedding Model: {config.EMBEDDING_MODEL}")
    print(f"  Total Medical Topics: {len(MEDICAL_KNOWLEDGE)}")

    # Initialize vector store
    print("\n[1/3] Initializing vector store...")
    try:
        vector_store = VectorStore(
            db_path=config.CHROMA_DB_PATH,
            collection_name=config.COLLECTION_NAME,
            embedding_model_name=config.EMBEDDING_MODEL
        )
        print("Vector store initialized")
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        sys.exit(1)

    # Check if collection already has documents
    current_count = vector_store.collection.count()
    if current_count > 0:
        print(f"\nCollection already contains {current_count} documents")
        response = input("Do you want to reset and reinitialize? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            print("Resetting collection...")
            vector_store.reset_collection()
        else:
            print("Skipping initialization.")
            return

    # Prepare documents for indexing
    print("\n[2/3] Preparing documents...")
    documents = []

    for idx, knowledge_item in enumerate(MEDICAL_KNOWLEDGE):
        # Create document ID
        doc_id = f"doc_{idx:04d}"

        # Combine title and content for better embedding
        text = f"Title: {knowledge_item['title']}\n\n{knowledge_item['content']}"

        # Create metadata
        metadata = {
            'title': knowledge_item['title'],
            'category': knowledge_item['category'],
            'doc_index': idx
        }

        documents.append({
            'id': doc_id,
            'text': text,
            'metadata': metadata
        })

    print(f"Prepared {len(documents)} documents")

    # Add documents to vector store
    print("\n[3/3] Adding documents to vector store...")
    print("This may take a few minutes depending on your hardware...\n")

    try:
        vector_store.add_documents(documents, batch_size=50)
        print("Documents added successfully")
    except Exception as e:
        print(f"Error adding documents: {e}")
        sys.exit(1)

    # Display statistics
    print("\n" + "=" * 60)
    print("INITIALIZATION COMPLETE")
    print("=" * 60)

    stats = vector_store.get_stats()
    print(f"\nVector Store Statistics:")
    print(f"  Collection: {stats['collection_name']}")
    print(f"  Total Documents: {stats['document_count']}")
    print(f"  Embedding Dimension: {stats['embedding_dimension']}")
    print(f"  Embedding Model: {config.EMBEDDING_MODEL}")

    print("\nJuniper knowledge base is ready!")
    print("\nYou can now run the application with: python app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
