"""
Knowledge Base Initialization Script
Builds the ChromaDB vector store from one or more medical sources using the
ingestion pipeline (chunking + per-chunk provenance).

Examples
--------
  # Default: rebuild from the built-in 53-topic knowledge base (chunked).
  python initialize_kb.py

  # Ingest the public-domain MedlinePlus compendium (download it first from
  # https://medlineplus.gov/xml.html), in addition to the built-in KB.
  python initialize_kb.py --source all --medlineplus-file ./data/mplus_topics.xml

  # Add to the existing collection instead of resetting it.
  python initialize_kb.py --source medlineplus --medlineplus-file URL --append

Re-ingesting the same source upserts (stable ids), so it won't create duplicates.
"""

import sys
import os
import argparse

from backend.vector_store import VectorStore
from backend.ingest import load_records, build_documents
from config import Config


def _parse_args(argv):
    p = argparse.ArgumentParser(description="Initialize Juniper's vector knowledge base")
    p.add_argument('--source', default='builtin',
                   choices=['builtin', 'medlineplus', 'all'],
                   help="Which source(s) to ingest (default: builtin)")
    p.add_argument('--medlineplus-file', default=os.getenv('MEDLINEPLUS_FILE'),
                   help="Path or URL to the MedlinePlus health-topics XML compendium")
    p.add_argument('--limit', type=int, default=None,
                   help="Cap number of MedlinePlus topics (useful for testing)")
    p.add_argument('--append', action='store_true',
                   help="Add to the existing collection instead of resetting it")
    p.add_argument('--reset', action='store_true',
                   help="Force-reset the collection before ingesting")
    return p.parse_args(argv)


def main(argv=None):
    """Initialize the knowledge base. Returns True on success."""
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    config = Config()

    print("=" * 60)
    print("JUNIPER - Medical Knowledge Base Initialization")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Database Path:   {config.CHROMA_DB_PATH}")
    print(f"  Collection:      {config.COLLECTION_NAME}")
    print(f"  Embedding Model: {config.EMBEDDING_MODEL}")
    print(f"  Source(s):       {args.source}")
    print(f"  Chunk size/overlap: {config.CHUNK_SIZE}/{config.CHUNK_OVERLAP} words")

    # [1/4] Load + normalise source records.
    print("\n[1/4] Loading source records...")
    try:
        records = load_records(args.source, medlineplus_path=args.medlineplus_file,
                               limit=args.limit)
    except Exception as e:
        print(f"Error loading sources: {e}")
        return False
    print(f"  Loaded {len(records)} topic records")

    # [2/4] Chunk into provenance-tagged documents.
    print("\n[2/4] Chunking into documents...")
    documents = build_documents(records, chunk_size=config.CHUNK_SIZE,
                                overlap=config.CHUNK_OVERLAP)
    if not documents:
        print("No documents produced — nothing to ingest.")
        return False
    print(f"  Produced {len(documents)} chunks "
          f"(avg {len(documents) / max(1, len(records)):.1f} chunks/topic)")

    # [3/4] Open the vector store, optionally resetting.
    print("\n[3/4] Initializing vector store...")
    try:
        vector_store = VectorStore(
            db_path=config.CHROMA_DB_PATH,
            collection_name=config.COLLECTION_NAME,
            embedding_model_name=config.EMBEDDING_MODEL,
        )
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        return False

    current = vector_store.collection.count()
    should_reset = args.reset or (not args.append and current > 0)
    if current > 0 and not args.append and not args.reset and os.environ.get('AUTO_INIT') == '1':
        # In automated (re)deploys with AUTO_INIT=1, default to a clean rebuild.
        should_reset = True
    if should_reset and current > 0:
        print(f"  Resetting collection ({current} existing documents)...")
        vector_store.reset_collection()
    elif args.append:
        print(f"  Appending to existing collection ({current} documents)...")

    # [4/4] Embed + add.
    print("\n[4/4] Embedding and adding documents (this can take a while)...\n")
    try:
        vector_store.add_documents(documents, batch_size=64)
    except Exception as e:
        print(f"Error adding documents: {e}")
        return False

    stats = vector_store.get_stats()
    print("\n" + "=" * 60)
    print("INITIALIZATION COMPLETE")
    print("=" * 60)
    print(f"  Total documents (chunks): {stats['document_count']}")
    print(f"  Embedding dimension:      {stats['embedding_dimension']}")
    print("\nJuniper knowledge base is ready!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
