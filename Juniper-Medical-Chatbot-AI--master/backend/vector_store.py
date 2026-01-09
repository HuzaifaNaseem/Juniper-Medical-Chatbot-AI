"""
Vector Store Module
Manages ChromaDB for semantic search and retrieval
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """
    Vector store implementation using ChromaDB and sentence-transformers
    """

    def __init__(self, db_path: str, collection_name: str, embedding_model_name: str):
        """
        Initialize vector store

        Args:
            db_path: Path to ChromaDB storage
            collection_name: Name of the collection
            embedding_model_name: Name of the sentence-transformer model
        """
        self.db_path = db_path
        self.collection_name = collection_name

        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model_name}")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()

        # Initialize ChromaDB
        self._initialize_chromadb()

    def _initialize_chromadb(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.db_path, exist_ok=True)

            # Initialize ChromaDB client with persistent storage
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            # Get or create collection
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                logger.info(f"Loaded existing collection: {self.collection_name}")
                logger.info(f"Collection contains {self.collection.count()} documents")
            except:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}  # Use cosine similarity
                )
                logger.info(f"Created new collection: {self.collection_name}")

        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]], batch_size: int = 100):
        """
        Add documents to the vector store

        Args:
            documents: List of documents with 'id', 'text', and 'metadata'
            batch_size: Number of documents to process at once
        """
        try:
            logger.info(f"Adding {len(documents)} documents to vector store...")

            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]

                ids = [doc['id'] for doc in batch]
                texts = [doc['text'] for doc in batch]
                metadatas = [doc.get('metadata', {}) for doc in batch]

                # Generate embeddings
                embeddings = self.embedding_model.encode(
                    texts,
                    show_progress_bar=True,
                    convert_to_numpy=True
                ).tolist()

                # Add to collection
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas
                )

                logger.info(f"Added batch {i // batch_size + 1}/{(len(documents) - 1) // batch_size + 1}")

            logger.info(f"Successfully added {len(documents)} documents")
            logger.info(f"Total documents in collection: {self.collection.count()}")

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using semantic similarity

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of dictionaries containing document information
        """
        try:
            # Refresh collection reference to avoid stale object
            self.collection = self.client.get_collection(name=self.collection_name)

            # Generate query embedding
            query_embedding = self.embedding_model.encode(
                query,
                convert_to_numpy=True
            ).tolist()

            # Query collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=['documents', 'metadatas', 'distances']
            )

            # Format results
            formatted_results = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for idx in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][idx],
                        'document': results['documents'][0][idx],
                        'metadata': results['metadatas'][0][idx],
                        'distance': results['distances'][0][idx],
                        'similarity': 1 - results['distances'][0][idx]  # Convert distance to similarity
                    })

            logger.info(f"Found {len(formatted_results)} results for query: '{query[:50]}...'")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    def delete_collection(self):
        """Delete the entire collection (use with caution)"""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise

    def reset_collection(self):
        """Reset collection (delete and recreate)"""
        try:
            self.delete_collection()
            self._initialize_chromadb()
            logger.info("Collection reset successfully")
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            raise

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        return {
            'collection_name': self.collection_name,
            'document_count': self.collection.count(),
            'embedding_model': self.embedding_model.get_sentence_embedding_dimension(),
            'embedding_dimension': self.embedding_dim
        }
