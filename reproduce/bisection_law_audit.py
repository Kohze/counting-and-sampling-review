'''Exact finite-law audit of interval bisection; no FPRAS is implemented.

The toy counter laws below are prescribed exactly. Independent fresh calls
have controlled relative-error and failure parameters. This script checks
the complete finite output law, including failure, using Fraction arithmetic.
Run: python -B reproduce/bisection_law_audit.py
'''
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json

FAIL = 'failure'


def frac(x):
    return str(x.numerator) + '/' + str(x.denominator)


def tables(rows, cols, caps):
    out = []
    for x in product(*(range(u + 1) for u in caps)):
        a, b, c, d = x
        if (a + b, c + d) == rows and (a + c, b + d) == cols:
            out.append(x)
    return tuple(out)


def depth_bound(caps):
    return sum(u.bit_length() for u in caps)


def audit_case(name, rows, cols, caps, alpha, beta, bits):
    omega = tables(rows, cols, caps)
    if not omega:
        return {'case': name, 'status': 'empty_detected', 'states': 0}
    initial = tuple((0, u) for u in caps)
    depth = depth_bound(caps)
    worst_local = F(0)

    def compatible(intervals):
        return tuple(x for x in omega
                     if all(lo <= a <= hi
                            for a, (lo, hi) in zip(x, intervals)))

    def counter_law(z, side):
        good = F(z) * (1 + alpha if side == 0 else 1 - alpha)
        assert (1 - alpha) * z <= good <= (1 + alpha) * z
        if beta == 0:
            return ((good, F(1)),)
        bad = F(100 + 11 * z) if side == 0 else F(0)
        return ((good, 1 - beta), (bad, beta))

    @lru_cache(None)
    def law(intervals):
        nonlocal worst_local
        feasible = compatible(intervals)
        if not feasible:
            return {FAIL: F(1)}
        cell = next((i for i, (lo, hi) in enumerate(intervals)
                     if lo < hi), None)
        if cell is None:
            x = tuple(lo for lo, hi in intervals)
            assert x in omega
            return {x: F(1)}
        lo, hi = intervals[cell]
        mid = (lo + hi) // 2
        child0 = list(intervals)
        child1 = list(intervals)
        child0[cell] = (lo, mid)
        child1[cell] = (mid + 1, hi)
        child0, child1 = tuple(child0), tuple(child1)
        z0 = len(compatible(child0))
        z1 = len(compatible(child1))
        assert z0 + z1 == len(feasible)
        ideal_left = F(z0, z0 + z1)
        actual_left = F(0)
        for a0, p0 in counter_law(z0, 0):
            for a1, p1 in counter_law(z1, 1):
                q = a0 / (a0 + a1) if a0 + a1 else F(1, 2)
                if bits is not None:
                    denominator = 1 << bits
                    q = F((q.numerator * denominator) // q.denominator,
                          denominator)
                actual_left += p0 * p1 * q
        coin_error = F(0) if bits is None else F(1, 1 << bits)
        local_error = abs(actual_left - ideal_left)
        local_bound = alpha + 2 * beta + coin_error
        assert local_error <= local_bound
        worst_local = max(worst_local, local_error)
        out = {}
        for child, weight in ((child0, actual_left),
                              (child1, 1 - actual_left)):
            if weight:
                for x, mass in law(child).items():
                    out[x] = out.get(x, F(0)) + weight * mass
        assert sum(out.values()) == 1
        return out

    output = law(initial)
    target = {x: F(1, len(omega)) for x in omega}
    support = set(output) | set(target)
    tv = sum(abs(output.get(x, F(0)) - target.get(x, F(0)))
             for x in support) / 2
    coin_error = F(0) if bits is None else F(1, 1 << bits)
    bound = depth * (alpha + 2 * beta + coin_error)
    failure = output.get(FAIL, F(0))
    assert tv <= bound
    assert failure <= 2 * depth * beta
    assert all(x == FAIL or x in omega for x in output)
    if alpha == beta == 0 and bits is None:
        assert output == target
    # Replacing failure by a fixed feasible table is a pushforward,
    # not conditioning. Its TV distance cannot increase.
    replacement = dict(output)
    replacement.pop(FAIL, None)
    replacement[omega[0]] = replacement.get(omega[0], F(0)) + failure
    replacement_tv = sum(abs(replacement.get(x, F(0)) - target[x])
                         for x in omega) / 2
    assert replacement_tv <= tv
    return {
        'case': name, 'states': len(omega), 'depth_bound': depth,
        'relative_tolerance': frac(alpha),
        'failure_parameter_per_counter': frac(beta),
        'coin_bits_per_branch': bits,
        'tv': frac(tv), 'tv_bound': frac(bound),
        'failure_probability': frac(failure),
        'failure_bound': frac(2 * depth * beta),
        'replacement_tv': frac(replacement_tv),
        'worst_local_tv': frac(worst_local),
        'output_law': [
            {'state': list(x) if x != FAIL else FAIL,
             'probability': frac(mass)}
            for x, mass in sorted(output.items(),
                                  key=lambda item: str(item[0]))
        ],
        'checks_passed': True
    }


def main():
    base = ((2, 2), (2, 2), (2, 2, 2, 2))
    cases = [
        audit_case('three_states_ideal', *base, F(0), F(0), None),
        audit_case('three_states_K5', *base, F(0), F(0), 5),
        audit_case('three_states_K8', *base, F(0), F(0), 8),
        audit_case('three_states_relative', *base, F(1, 64), F(0), 8),
        audit_case('three_states_controlled_failure', *base,
                   F(1, 64), F(1, 1024), 8),
        audit_case('unique_binary_controlled_failure',
                   (2, 2), (2, 2), (1, 1, 1, 1),
                   F(1, 64), F(1, 1024), 8),
        audit_case('two_states_relative', (2, 1), (1, 2), (1, 2, 1, 2),
                   F(1, 64), F(0), 8),
        audit_case('zero_total_unique', (0, 0), (0, 0), (0, 0, 0, 0),
                   F(0), F(0), 8),
        audit_case('empty_support', (2, 2), (2, 2), (0, 0, 0, 0),
                   F(0), F(0), 8)
    ]
    print(json.dumps({
        'audit': 'exact finite output laws for interval bisection',
        'counter_model': 'prescribed fresh independent rational toy laws',
        'not_an_FPRAS_implementation': True,
        'cases': cases,
        'all_checks_passed': True
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
