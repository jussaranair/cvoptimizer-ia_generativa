"""Módulo para simular análises de currículos (CV).

Fornece funções para gerar scores aleatórios e uma lista de palavras-chave ausentes.
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional


DEFAULT_KEYWORDS_POOL: List[str] = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "communication",
    "leadership",
    "project management",
    "docker",
    "aws",
    "git",
    "testing",
    "nlp",
    "pandas",
    "numpy",
    "linux",
    "tensorflow",
    "keras",
]


def generate_missing_keywords(pool: Optional[List[str]] = None, count: Optional[int] = None) -> List[str]:
    """Return a list of `count` unique missing keywords sampled from `pool`.

    - `pool`: optional source list of keywords; defaults to `DEFAULT_KEYWORDS_POOL`.
    - `count`: number of keywords to return; if None, chooses randomly between 3 and 5.
    """
    pool = pool or DEFAULT_KEYWORDS_POOL
    if not pool:
        return []
    if count is None:
        count = random.randint(3, 5)
    count = max(0, min(count, len(pool)))
    return random.sample(pool, count)


def simulate_analysis(
    seed: Optional[int] = None,
    keywords_pool: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Simulate an analysis and return a dictionary with the required keys.

    Keys:
      - summary_score: int 0-100
      - experience_score: int 0-100
      - skills_score: int 0-100
      - education_score: int 0-100
      - keywords_missing: list[str] (3-5 items)

    If `seed` is provided, the random generator will be seeded for reproducible results.
    """
    rnd = random.Random(seed)

    def _rand_score() -> int:
        return rnd.randint(0, 100)

    # generate keywords_missing using the module-level pool but with the same RNG
    pool = keywords_pool or DEFAULT_KEYWORDS_POOL
    km_count = rnd.randint(3, 5)
    km_count = max(0, min(km_count, len(pool)))
    keywords_missing = rnd.sample(pool, km_count) if pool else []

    return {
        "summary_score": _rand_score(),
        "experience_score": _rand_score(),
        "skills_score": _rand_score(),
        "education_score": _rand_score(),
        "keywords_missing": keywords_missing,
    }


__all__ = ["simulate_analysis", "generate_missing_keywords", "DEFAULT_KEYWORDS_POOL"]


if __name__ == "__main__":
    # Demo run
    print(simulate_analysis())
