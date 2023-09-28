import random as rng
import math

def confusion(a, b):
    pp = sum(    p and     q for p, q in zip(a, b))
    pn = sum(    p and not q for p, q in zip(a, b))
    np = sum(not p and     q for p, q in zip(a, b))
    nn = sum(not p and not q for p, q in zip(a, b))

    return pp, pn, np, nn

def filter(alpha, beta):
    return rng.random() < math.cos(math.radians(alpha - beta))**2

def bell_hidden(alpha, beta, samples):
    photons = [rng.random() * 360 for _ in range(samples)]

    passes_a = [filter(alpha, p) for p in photons]
    passes_b = [filter( beta, p) for p in photons]

    pp, pn, np, nn = confusion(passes_a, passes_b)

    e = (pp - pn - np + nn) / (pp + pn + np + nn)

    return e

def passes_qm(alpha, beta, photon):
    order = rng.randint(0, 1) == 1
    if order: alpha, beta = beta, alpha

    passes_a = filter(alpha, photon)
    passes_b = filter( beta, alpha + 90 * (not passes_a))

    return (passes_a, passes_b) if order else (passes_b, passes_a)

def bell_qm(alpha, beta, samples):
    photons = [rng.random() * 360 for _ in range(samples)]
    passes_a, passes_b = zip(*(passes_qm(alpha, beta, p) for p in photons))

    pp, pn, np, nn = confusion(passes_a, passes_b)

    e = (pp - pn - np + nn) / (pp + pn + np + nn)

    return e

def bell_test(samples, test):
    ab = test( 0, 22.5, samples)
    aB = test( 0, 67.5, samples)
    Ab = test(45, 22.5, samples)
    AB = test(45, 67.5, samples)

    s = ab - aB + Ab + AB

    return s

result = bell_test(1000000, bell_qm)
expected = 2 * math.sqrt(2)
print(f'Result: {result}  Expected: {expected}  Err: {abs(result - expected)}')
print(f'This test could{" not" if result > 2 else ""} be described by local hidden variable theories.')
