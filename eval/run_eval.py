"""
Retrieval Evaluation Harness
Measures how well Juniper's retrieval + citation layer performs against a fixed,
hand-labelled set of medical queries (eval/eval_set.json).

It exercises the *real* retrieval path (RAGEngine._retrieve) and the *real*
citation path (RAGEngine._format_sources) — no LLM/Groq call needed, so it runs
offline and fast. This lets us tune retrieval and citation filtering against
numbers instead of eyeballing screenshots.

Metrics
-------
Retrieval (does the right topic come back?)
  - hit@1 / hit@3 / hit@5 : expected topic is the top / within top-3 / top-5 result
  - MRR                    : mean reciprocal rank of the expected topic

Citations (is the sources panel clean?)
  - citation precision     : fraction of cited sources that are on-topic
                             (title == expected, or category in acceptable_categories)
  - off-topic citations    : average number of irrelevant sources shown per query
  - expected cited         : fraction of queries where the expected topic is cited

Usage
-----
  python -m eval.run_eval            # human-readable report
  python -m eval.run_eval --json     # machine-readable (for CI / before-after diffs)

A non-zero exit code is returned if hit@3 or citation precision fall below the
thresholds below, so this can gate changes in CI.
"""

import os
import sys
import json
import argparse

# Use cached embedding model; avoid slow/failing network round-trips offline.
os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_OFFLINE', '1')

# Allow running as a script from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config                                    # noqa: E402
from backend.vector_store import VectorStore                 # noqa: E402
from backend.rag_engine import RAGEngine                     # noqa: E402

# CI gate thresholds.
MIN_HIT_AT_3 = 0.80
MIN_CITATION_PRECISION = 0.80

EVAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_set.json')


def _title_of(doc):
    return (doc.get('metadata', {}) or {}).get('title', '')


def _build_engine():
    """RAGEngine wired to the live vector store; LLM service is never invoked."""
    vs = VectorStore(Config.CHROMA_DB_PATH, Config.COLLECTION_NAME, Config.EMBEDDING_MODEL)
    # LLM service isn't needed for retrieval/citation eval — pass a stand-in.
    engine = RAGEngine.__new__(RAGEngine)
    engine.vector_store = vs
    engine.top_k = Config.TOP_K_RESULTS
    engine.retrieval_candidates = Config.RETRIEVAL_CANDIDATES
    engine.min_relevance = Config.MIN_RELEVANCE
    engine.relevance_ratio = Config.RELEVANCE_RATIO
    # Citation knobs (added with the citation cleanup); fall back if absent.
    engine.citation_relevance_ratio = getattr(Config, 'CITATION_RELEVANCE_RATIO', 0.0)
    engine.citation_min_relevance = getattr(Config, 'CITATION_MIN_RELEVANCE', 0.0)
    engine.max_sources = getattr(Config, 'MAX_SOURCES', 5)
    return engine


def evaluate(engine, cases):
    n = len(cases)
    hits1 = hits3 = hits5 = 0
    rr_sum = 0.0
    cited_total = cited_good = 0
    offtopic_total = 0
    expected_cited = 0
    per_case = []

    for case in cases:
        query = case['query']
        expected = case['expected_title']
        acceptable = set(case.get('acceptable_categories', []))

        docs = engine._retrieve(query)
        titles = [_title_of(d) for d in docs]

        # Rank of the expected topic among retrieved docs (1-based; 0 = absent).
        rank = next((i + 1 for i, t in enumerate(titles) if t == expected), 0)
        if rank == 1:
            hits1 += 1
        if rank and rank <= 3:
            hits3 += 1
        if rank and rank <= 5:
            hits5 += 1
        if rank:
            rr_sum += 1.0 / rank

        # Citation quality on the actually-shown sources.
        sources = engine._format_sources(docs)
        good = sum(1 for s in sources
                   if s['title'] == expected or s.get('category') in acceptable)
        off = [s['title'] for s in sources
               if s['title'] != expected and s.get('category') not in acceptable]
        cited_total += len(sources)
        cited_good += good
        offtopic_total += len(off)
        if any(s['title'] == expected for s in sources):
            expected_cited += 1

        per_case.append({
            'query': query,
            'expected': expected,
            'rank': rank,
            'top': titles[0] if titles else None,
            'sources': [s['title'] for s in sources],
            'offtopic': off,
        })

    metrics = {
        'cases': n,
        'hit@1': hits1 / n,
        'hit@3': hits3 / n,
        'hit@5': hits5 / n,
        'mrr': rr_sum / n,
        'citation_precision': (cited_good / cited_total) if cited_total else 0.0,
        'avg_offtopic_citations': offtopic_total / n,
        'expected_cited_rate': expected_cited / n,
        'avg_sources_shown': cited_total / n,
    }
    return metrics, per_case


def _print_report(metrics, per_case):
    print("=" * 70)
    print("JUNIPER RETRIEVAL EVALUATION")
    print("=" * 70)
    print(f"Cases: {metrics['cases']}\n")
    print("Retrieval")
    print(f"  hit@1 : {metrics['hit@1']:.0%}")
    print(f"  hit@3 : {metrics['hit@3']:.0%}")
    print(f"  hit@5 : {metrics['hit@5']:.0%}")
    print(f"  MRR   : {metrics['mrr']:.3f}")
    print("\nCitations")
    print(f"  precision (on-topic)      : {metrics['citation_precision']:.0%}")
    print(f"  expected topic cited      : {metrics['expected_cited_rate']:.0%}")
    print(f"  avg off-topic per query   : {metrics['avg_offtopic_citations']:.2f}")
    print(f"  avg sources shown         : {metrics['avg_sources_shown']:.2f}")

    # Show the cases that retrieved the wrong top topic or cited noise.
    problems = [c for c in per_case if c['rank'] != 1 or c['offtopic']]
    if problems:
        print("\n" + "-" * 70)
        print(f"NEEDS ATTENTION ({len(problems)} cases)")
        print("-" * 70)
        for c in problems:
            rank_str = f"rank={c['rank']}" if c['rank'] else "MISSED"
            print(f"\n  Q: {c['query']}")
            print(f"     expected: {c['expected']}  ({rank_str}, top='{c['top']}')")
            if c['offtopic']:
                print(f"     off-topic citations: {', '.join(c['offtopic'])}")
    print("=" * 70)


def main(argv=None):
    p = argparse.ArgumentParser(description="Run Juniper retrieval evaluation")
    p.add_argument('--json', action='store_true', help="Emit metrics as JSON")
    p.add_argument('--eval-file', default=EVAL_PATH)
    args = p.parse_args(argv if argv is not None else sys.argv[1:])

    with open(args.eval_file, encoding='utf-8') as f:
        cases = json.load(f)['cases']

    engine = _build_engine()
    metrics, per_case = evaluate(engine, cases)

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        _print_report(metrics, per_case)

    # CI gate.
    ok = metrics['hit@3'] >= MIN_HIT_AT_3 and metrics['citation_precision'] >= MIN_CITATION_PRECISION
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
