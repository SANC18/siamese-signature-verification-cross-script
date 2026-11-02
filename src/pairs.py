"""Writer-disjoint splitting and pair generation.

Expected data format (build it with a small loader for each dataset):

    data = {
        "writer_001": {"genuine": ["a.png", "b.png", ...], "forged": ["c.png", ...]},
        "writer_002": {...},
    }
"""

import random
from typing import Dict, List, Tuple

Data = Dict[str, Dict[str, List[str]]]
Pair = Tuple[str, str, int]  # (path_a, path_b, label) with label 1 = same writer
Triplet = Tuple[str, str, str]  # (anchor, positive, negative)


def make_triplets(data: Data, writers: List[str], n_triplets: int, seed: int = 0) -> List[Triplet]:
    """Make triplets: anchor and positive are genuine signatures of one writer.

    The negative is a skilled forgery of that writer (half of the time, when
    forgeries exist) or a genuine signature of another writer.
    """
    rng = random.Random(seed)
    usable = [w for w in writers if len(data[w]["genuine"]) >= 2]
    if len(usable) < 2:
        raise ValueError("Need at least two writers with two genuine signatures each.")
    out: List[Triplet] = []
    for _ in range(n_triplets):
        w = rng.choice(usable)
        a, p = rng.sample(data[w]["genuine"], 2)
        forged = data[w].get("forged", [])
        if forged and rng.random() < 0.5:
            n = rng.choice(forged)
        else:
            other = rng.choice(usable)
            while other == w:
                other = rng.choice(usable)
            n = rng.choice(data[other]["genuine"])
        out.append((a, p, n))
    return out


def split_writers(writers, train=0.7, val=0.15, seed=42):
    """Split WRITERS (not images) into train, validation and test lists.

    Splitting by writer guarantees no person appears in more than one set.
    """
    writers = sorted(writers)
    random.Random(seed).shuffle(writers)
    n_train = int(len(writers) * train)
    n_val = int(len(writers) * val)
    return (
        writers[:n_train],
        writers[n_train:n_train + n_val],
        writers[n_train + n_val:],
    )


def check_disjoint(*writer_lists):
    """Raise an error if any writer appears in more than one list."""
    seen = set()
    for lst in writer_lists:
        overlap = seen & set(lst)
        if overlap:
            raise ValueError(f"Writers appear in more than one split: {sorted(overlap)[:5]}")
        seen |= set(lst)


def make_pairs(data: Data, writers: List[str], n_pairs: int, seed: int = 0) -> List[Pair]:
    """Make a balanced list of positive and negative pairs from the given writers.

    Positive (label 1): two different genuine signatures of one writer.
    Negative (label 0): a genuine signature against either a skilled forgery of
    the same writer or a genuine signature of another writer.
    """
    rng = random.Random(seed)
    usable = [w for w in writers if len(data[w]["genuine"]) >= 2]
    if len(usable) < 2:
        raise ValueError("Need at least two writers with two genuine signatures each.")

    pairs: List[Pair] = []
    for i in range(n_pairs):
        writer = rng.choice(usable)
        genuine = data[writer]["genuine"]
        if i % 2 == 0:
            a, b = rng.sample(genuine, 2)
            pairs.append((a, b, 1))
        else:
            a = rng.choice(genuine)
            forged = data[writer].get("forged", [])
            if forged and rng.random() < 0.5:
                b = rng.choice(forged)  # skilled forgery
            else:
                other = rng.choice([w for w in usable if w != writer])
                b = rng.choice(data[other]["genuine"])  # random forgery
            pairs.append((a, b, 0))
    return pairs
