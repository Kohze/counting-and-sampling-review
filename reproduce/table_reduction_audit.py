"""Exhaustive finite audit of the table/common-polymatroid bijection.

Run: python reproduce/table_reduction_audit.py
This regression check supports, and does not replace, the proof in the review.
The implementation uses no external packages.
"""
import itertools
import json
import math
from fractions import Fraction


def check_instance(rows, cols, caps):
    nr, nc = len(rows), len(cols)
    cells = list(itertools.product(range(nr), range(nc)))
    total, dimension = sum(rows), len(cells)

    def rank(subset, axis, margins):
        return sum(
            min(
                margin,
                sum(
                    caps[i][j]
                    for k, (i, j) in enumerate(cells)
                    if k in subset and (i if axis == 0 else j) == group
                ),
            )
            for group, margin in enumerate(margins)
        )

    subsets = [
        {k for k in range(dimension) if mask >> k & 1}
        for mask in range(1 << dimension)
    ]
    row_ranks = [rank(s, 0, rows) for s in subsets]
    col_ranks = [rank(s, 1, cols) for s in subsets]
    direct, bases = [], []
    for vector in itertools.product(
        *[range(caps[i][j] + 1) for i, j in cells]
    ):
        is_table = all(
            sum(vector[k] for k, (i, j) in enumerate(cells) if i == a) == rows[a]
            for a in range(nr)
        ) and all(
            sum(vector[k] for k, (i, j) in enumerate(cells) if j == b) == cols[b]
            for b in range(nc)
        )
        if is_table:
            direct.append(vector)
        is_base = (
            row_ranks[-1] == total
            and col_ranks[-1] == total
            and sum(vector) == total
            and all(
                sum(vector[k] for k in subset) <= rr
                and sum(vector[k] for k in subset) <= cr
                for subset, rr, cr in zip(subsets, row_ranks, col_ranks)
            )
        )
        if is_base:
            bases.append(vector)
    assert direct == bases, (rows, cols, caps, direct, bases)
    return len(direct)


def main():
    instances = nonempty = maximum_count = 0
    for flat_caps in itertools.product(range(3), repeat=4):
        caps = [flat_caps[:2], flat_caps[2:]]
        for rows in itertools.product(range(5), repeat=2):
            for col0 in range(5):
                cols = (col0, sum(rows) - col0)
                if not 0 <= cols[1] <= 4:
                    continue
                count = check_instance(rows, cols, caps)
                instances += 1
                nonempty += count > 0
                maximum_count = max(maximum_count, count)
    unnormalised = [
        Fraction(1, math.factorial(a) ** 2 * math.factorial(2-a) ** 2)
        for a in range(3)
    ]
    normaliser = sum(unnormalised)
    fisher = [w / normaliser for w in unnormalised]
    total_variation = sum(abs(w-Fraction(1, 3)) for w in fisher) / 2
    report = {
        "instances": instances,
        "nonempty": nonempty,
        "maximum_count": maximum_count,
        "fisher_probabilities": [str(w) for w in fisher],
        "tv_from_uniform": str(total_variation),
        "scope": "2 by 2, cell capacities 0..2, row and column margins 0..4",
        "arithmetic": "integer and fractions.Fraction",
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

