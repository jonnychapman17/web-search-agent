from __future__ import annotations


def score_relevance(
    *,
    source_authority: int,
    recency: int,
    direct_relevance: int,
    novelty: int,
    discussion_signal: int,
) -> int:
    score = source_authority + recency + direct_relevance + novelty + discussion_signal
    return max(0, min(100, score))
