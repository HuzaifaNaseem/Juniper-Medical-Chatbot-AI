#!/usr/bin/env bash
#
# Load the public-domain MedlinePlus health-topics compendium into Juniper's
# knowledge base, expanding it from the 53 built-in topics to ~1,000.
#
# Run this ON THE DROPLET (it needs internet to download the compendium):
#     cd /var/www/juniper && bash scripts/load_medlineplus.sh
#
# Optionally pass an explicit compendium URL or a local file to skip auto-discovery:
#     bash scripts/load_medlineplus.sh https://medlineplus.gov/xml/mplus_topics_YYYY-MM-DD.xml
#     bash scripts/load_medlineplus.sh ./data/mplus_topics.xml
#
# The script stops the app while it rebuilds the vector store (so the live
# workers don't read a half-written database), then restarts it and runs the
# evaluation harness to confirm retrieval didn't regress.

set -euo pipefail

cd "$(dirname "$0")/.."   # repo root
DATA_DIR="./data"
mkdir -p "$DATA_DIR"

# --- pick the Python interpreter (venv if present, else python3) ---
if [ -x "./venv/bin/python" ]; then
    PY="./venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PY="python3"
else
    echo "ERROR: no python3 / venv found." >&2
    exit 1
fi
echo "Using Python: $PY"

# --- resolve the compendium source (arg, or auto-discover the latest) ---
SOURCE="${1:-}"
if [ -z "$SOURCE" ]; then
    echo "Discovering latest MedlinePlus health-topics compendium..."
    LISTING="$(curl -fsSL https://medlineplus.gov/xml.html)"
    # Links look like /xml/mplus_topics_YYYY-MM-DD.xml (or .zip). Take the newest.
    FNAME="$(printf '%s' "$LISTING" \
        | grep -oiE 'mplus_topics_[0-9-]+\.(xml|zip)' \
        | sort -u | tail -1 || true)"
    if [ -z "$FNAME" ]; then
        echo "ERROR: couldn't find the compendium link on https://medlineplus.gov/xml.html" >&2
        echo "       Open that page, copy the 'Health Topic XML' file URL, and pass it as an argument." >&2
        exit 1
    fi
    SOURCE="https://medlineplus.gov/xml/${FNAME}"
    echo "Latest compendium: $SOURCE"
fi

# --- stop the app so the rebuild has exclusive access to the vector store ---
echo "Stopping juniper..."
supervisorctl stop juniper || echo "(supervisorctl stop failed — continuing)"

# --- rebuild the knowledge base: built-in topics + MedlinePlus ---
echo "Rebuilding knowledge base (built-in + MedlinePlus). This takes a few minutes..."
if AUTO_INIT=1 "$PY" initialize_kb.py --source all --medlineplus-file "$SOURCE"; then
    echo "Knowledge base rebuilt."
else
    echo "ERROR: knowledge base rebuild failed. Restarting app on the previous data." >&2
    supervisorctl start juniper || true
    exit 1
fi

# --- restart the app ---
echo "Starting juniper..."
supervisorctl start juniper

# --- sanity-check retrieval quality (non-fatal) ---
echo "Running retrieval evaluation..."
"$PY" -m eval.run_eval || echo "(eval reported below-threshold metrics — review the output above)"

echo
echo "Done. Juniper now answers from the expanded knowledge base."
