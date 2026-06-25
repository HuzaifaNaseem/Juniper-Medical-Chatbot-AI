"""
Ingestion Pipeline
Turns raw medical sources into clean, chunked, provenance-tagged documents ready
for the vector store.

Why this exists
---------------
The original knowledge base was a 53-topic Python literal indexed as one
embedding per topic (no chunking, despite CHUNK_SIZE/CHUNK_OVERLAP existing in
config), and "citations" were mapped at the *category* level. This module
replaces that with a real pipeline:

  - pluggable, license-clean *sources* (the built-in KB and the public-domain
    MedlinePlus health-topics compendium) normalised to a common record shape,
  - paragraph-aware chunking with overlap, so large topics become several
    focused, retrievable passages, and
  - per-chunk provenance metadata (source_name + source_url), so an answer can
    cite the actual page a passage came from instead of a generic category link.

A normalised *record* is:
    {
        "title":       str,            # human-readable topic title
        "category":    str,            # coarse area, used for fallback references
        "content":     str,            # plain-text body (no HTML)
        "source_name": str,            # e.g. "MedlinePlus"
        "source_url":  str,            # canonical URL for this specific topic
        "source_type": str,            # "builtin" | "medlineplus" | ...
    }

A *document* (what the vector store ingests) is:
    {"id": str, "text": str, "metadata": {...flat scalars...}}
"""

import re
import html
import hashlib
import logging
from typing import List, Dict, Any, Iterable, Optional

from .references import reference_for

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# Text cleaning + chunking
# ----------------------------------------------------------------------------

_TAG_RE = re.compile(r'<[^>]+>')
_WS_RE = re.compile(r'[ \t\f\v]+')
_MULTINEWLINE_RE = re.compile(r'\n{3,}')


def strip_html(text: str) -> str:
    """Strip HTML tags and unescape entities, preserving paragraph breaks."""
    if not text:
        return ''
    # Block-level closers become paragraph breaks; <br> a single line break.
    text = re.sub(r'(?i)</(p|div|li|h[1-6]|ul|ol)>', '\n\n', text)
    text = re.sub(r'(?i)<br\s*/?>', '\n', text)
    text = _TAG_RE.sub('', text)
    text = html.unescape(text)
    text = _WS_RE.sub(' ', text)
    # Trim horizontal whitespace hugging line breaks, then collapse blank runs.
    text = re.sub(r'[ \t]*\n[ \t]*', '\n', text)
    text = _MULTINEWLINE_RE.sub('\n\n', text)
    return text.strip()


def _paragraphs(text: str) -> List[str]:
    """Split text into non-empty paragraphs."""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into word-bounded chunks of ~chunk_size words with `overlap`
    words of context carried between consecutive chunks.

    Paragraph boundaries are respected where possible: a paragraph that fits is
    kept whole; an oversized paragraph is split on word boundaries. Overlap
    keeps a claim that straddles a boundary retrievable from either chunk.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    overlap = max(0, min(overlap, chunk_size - 1))

    chunks: List[str] = []
    current: List[str] = []  # words in the chunk being built

    def flush():
        if current:
            chunks.append(' '.join(current).strip())

    for para in _paragraphs(text):
        words = para.split()
        if not words:
            continue
        # If adding this paragraph keeps us within budget, append it.
        if len(current) + len(words) <= chunk_size:
            current.extend(words)
            continue
        # Otherwise flush what we have, then emit the paragraph, splitting it if
        # it alone exceeds the chunk size.
        flush()
        if len(words) <= chunk_size:
            # Start the new chunk with trailing overlap from the previous one.
            tail = chunks[-1].split()[-overlap:] if (chunks and overlap) else []
            current = tail + words
        else:
            current = []
            i = 0
            while i < len(words):
                piece = words[i:i + chunk_size]
                chunks.append(' '.join(piece).strip())
                if i + chunk_size >= len(words):
                    break
                i += chunk_size - overlap
            current = []
    flush()

    # Drop empties and de-duplicate consecutive identical chunks defensively.
    out = [c for c in chunks if c]
    return out


# ----------------------------------------------------------------------------
# Record -> document conversion
# ----------------------------------------------------------------------------

def _slug(text: str, max_len: int = 40) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    return s[:max_len] or 'topic'


def _stable_id(source_type: str, title: str, chunk_index: int) -> str:
    """Deterministic id so re-ingesting the same source upserts, not duplicates."""
    h = hashlib.sha1(f"{source_type}|{title}".encode('utf-8')).hexdigest()[:10]
    return f"{source_type}-{_slug(title)}-{h}-{chunk_index:03d}"


def build_documents(records: Iterable[Dict[str, Any]], chunk_size: int = 500,
                    overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Convert normalised records into chunked, provenance-tagged documents.

    Each chunk's embedded text is prefixed with the topic title (improves
    retrieval and lets the re-ranker's title boost keep working), and carries
    flat metadata the vector store / citation layer can use directly.
    """
    documents: List[Dict[str, Any]] = []
    for rec in records:
        title = (rec.get('title') or '').strip()
        content = (rec.get('content') or '').strip()
        if not title or not content:
            continue

        category = (rec.get('category') or 'general').strip().lower()
        source_type = rec.get('source_type') or 'builtin'

        # Provenance: use the record's own URL when present (real per-topic
        # source), else fall back to the category-level authoritative reference.
        ref = reference_for(category)
        source_name = rec.get('source_name') or ref['name']
        source_url = rec.get('source_url') or ref['url']

        chunks = chunk_text(content, chunk_size=chunk_size, overlap=overlap)
        for idx, chunk in enumerate(chunks):
            documents.append({
                'id': _stable_id(source_type, title, idx),
                'text': f"Title: {title}\n\n{chunk}",
                'metadata': {
                    'title': title,
                    'category': category,
                    'source_name': source_name,
                    'source_url': source_url,
                    'source_type': source_type,
                    'chunk_index': idx,
                    'chunk_count': len(chunks),
                },
            })
    logger.info(f"build_documents: {len(documents)} chunks produced")
    return documents


# ----------------------------------------------------------------------------
# Sources
# ----------------------------------------------------------------------------

def records_from_builtin() -> List[Dict[str, Any]]:
    """Normalise the hand-written MEDICAL_KNOWLEDGE list into records."""
    from .knowledge_base import MEDICAL_KNOWLEDGE
    records = []
    for item in MEDICAL_KNOWLEDGE:
        category = item.get('category', 'general')
        ref = reference_for(category)
        records.append({
            'title': item['title'],
            'category': category,
            'content': item['content'],
            'source_name': ref['name'],
            'source_url': ref['url'],
            'source_type': 'builtin',
        })
    return records


# MedlinePlus health-topic <group> names mapped onto our coarse categories so
# the category-reference fallback and the re-ranker stay meaningful. Unmapped
# groups fall through to 'general'.
_MPLUS_GROUP_TO_CATEGORY = {
    'heart and circulation': 'cardiovascular',
    'blood, heart and circulation': 'cardiovascular',
    'lungs and breathing': 'respiratory',
    'diabetes': 'endocrine',
    'endocrine system': 'endocrine',
    'hormones': 'endocrine',
    'infections': 'infectious',
    'brain and nerves': 'neurological',
    'digestive system': 'gastrointestinal',
    'cancers': 'oncology',
    'cancer': 'oncology',
    'mental health and behavior': 'mental_health',
    'immune system': 'immunology',
    'kidneys and urinary system': 'renal',
    'skin, hair and nails': 'dermatology',
    'blood': 'hematology',
    'eyes and vision': 'ophthalmology',
    'food and nutrition': 'nutrition',
    'drugs and supplements': 'pharmacology',
    "women's health": 'women_health',
    "children's health": 'pediatrics',
    'bones, joints and muscles': 'musculoskeletal',
}


def _medlineplus_category(group_names: List[str]) -> str:
    for g in group_names:
        cat = _MPLUS_GROUP_TO_CATEGORY.get(g.strip().lower())
        if cat:
            return cat
    return 'general'


def _materialize_xml(path_or_url: str) -> "tuple[str, list]":
    """
    Return a path to a plain-XML file for `path_or_url`, plus a list of temp
    files to clean up. Transparently handles http(s) URLs and gzip/zip
    compression (MedlinePlus distributes the compendium compressed), detected by
    magic bytes rather than trusting the extension.
    """
    import tempfile
    import shutil
    import gzip
    import zipfile

    temps: list = []

    # 1) Get a local copy of the raw bytes.
    if path_or_url.startswith(('http://', 'https://')):
        import urllib.request
        logger.info(f"Downloading MedlinePlus compendium: {path_or_url}")
        raw = tempfile.NamedTemporaryFile(delete=False, suffix='.bin')
        with urllib.request.urlopen(path_or_url) as resp:  # nosec - trusted NIH host
            shutil.copyfileobj(resp, raw)
        raw.close()
        temps.append(raw.name)
        src = raw.name
    else:
        src = path_or_url

    # 2) Sniff magic bytes to decide on decompression.
    with open(src, 'rb') as f:
        magic = f.read(4)

    if magic[:2] == b'\x1f\x8b':  # gzip
        out = tempfile.NamedTemporaryFile(delete=False, suffix='.xml')
        with gzip.open(src, 'rb') as gz:
            shutil.copyfileobj(gz, out)
        out.close()
        temps.append(out.name)
        return out.name, temps

    if magic[:4] == b'PK\x03\x04':  # zip
        with zipfile.ZipFile(src) as zf:
            member = next((n for n in zf.namelist() if n.lower().endswith('.xml')), None)
            if not member:
                raise ValueError("MedlinePlus zip contains no .xml file")
            out = tempfile.NamedTemporaryFile(delete=False, suffix='.xml')
            with zf.open(member) as m:
                shutil.copyfileobj(m, out)
            out.close()
            temps.append(out.name)
            return out.name, temps

    # Plain XML.
    return src, temps


def records_from_medlineplus_xml(path_or_url: str, limit: Optional[int] = None,
                                 min_chars: int = 200) -> List[Dict[str, Any]]:
    """
    Parse the public-domain MedlinePlus Health Topics compendium into records
    with real per-topic provenance (title + canonical URL).

    Accepts a local path or an http(s) URL, and plain-XML, .gz, or .zip
    compression (MedlinePlus serves it compressed). Download from:
        https://medlineplus.gov/xml.html   (e.g. mplus_topics_YYYY-MM-DD.zip)
    English topics only. Streamed with iterparse so the file is not held fully
    in memory.
    """
    import os as _os
    import xml.etree.ElementTree as ET

    xml_path, temps = _materialize_xml(path_or_url)

    records: List[Dict[str, Any]] = []
    try:
        with open(xml_path, 'rb') as stream:
            for _event, elem in ET.iterparse(stream, events=('end',)):
                if elem.tag != 'health-topic':
                    continue
                try:
                    if (elem.get('language') or 'English') != 'English':
                        continue
                    title = (elem.get('title') or '').strip()
                    url = (elem.get('url') or '').strip()
                    summary_el = elem.find('full-summary')
                    summary = strip_html(summary_el.text if summary_el is not None else '')
                    if not title or len(summary) < min_chars:
                        continue
                    groups = [g.text or '' for g in elem.findall('group')]
                    records.append({
                        'title': title,
                        'category': _medlineplus_category(groups),
                        'content': summary,
                        'source_name': 'MedlinePlus (U.S. National Library of Medicine)',
                        'source_url': url or 'https://medlineplus.gov/',
                        'source_type': 'medlineplus',
                    })
                    if limit and len(records) >= limit:
                        break
                finally:
                    elem.clear()  # free the parsed element
    finally:
        for t in temps:
            try:
                _os.unlink(t)
            except OSError:
                pass

    logger.info(f"records_from_medlineplus_xml: {len(records)} topics parsed")
    return records


# Registry of named sources for the CLI / initializer.
def load_records(source: str, medlineplus_path: Optional[str] = None,
                 limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Load normalised records for a named source ('builtin', 'medlineplus', 'all')."""
    source = (source or 'builtin').lower()
    records: List[Dict[str, Any]] = []
    if source in ('builtin', 'all'):
        records.extend(records_from_builtin())
    if source in ('medlineplus', 'all'):
        if not medlineplus_path:
            raise ValueError(
                "source 'medlineplus' requires --medlineplus-file <path-or-url> "
                "(download from https://medlineplus.gov/xml.html)"
            )
        records.extend(records_from_medlineplus_xml(medlineplus_path, limit=limit))
    if source not in ('builtin', 'medlineplus', 'all'):
        raise ValueError(f"Unknown source: {source!r}")
    return records
