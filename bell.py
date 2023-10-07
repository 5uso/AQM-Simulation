import random as rng
import math
import matplotlib.pyplot as plt
from numpy import arange

def confusion(a, b):
    pp = sum(    p and     q for p, q in zip(a, b))
    pn = sum(    p and not q for p, q in zip(a, b))
    np = sum(not p and     q for p, q in zip(a, b))
    nn = sum(not p and not q for p, q in zip(a, b))

    return pp, pn, np, nn

def filter(alpha, beta):
    # Probability amplitude is determined by the cosine of the angle difference
    return rng.random() < math.cos(math.radians(alpha - beta))**2

def bell_classical(alpha, beta, samples):
    # Uniform photon source
    photons = [rng.random() * 360 for _ in range(samples)]

    # Measurements are independent
    passes_a = [filter(alpha, p) for p in photons]
    passes_b = [filter( beta, p) for p in photons]

    # Count coincidences
    pp, pn, np, nn = confusion(passes_a, passes_b)

    # Estimate for test setup
    e = (pp - pn - np + nn) / (pp + pn + np + nn)

    return e

def passes_qm(alpha, beta, photon):
    # Randomly determine which photon of the pair to simulate first,
    # to avoid bias
    order = rng.randint(0, 1) == 1
    if order: alpha, beta = beta, alpha

    # Does photon 1 pass through the polarizer?
    passes_a = filter(alpha, photon)

    # Photon's b measurement is affected by the collapse of the wave
    # function. Its angle is either equivalent to that of the first
    # polarizer, or orthogonal to it.
    passes_b = filter( beta, alpha + 90 * (not passes_a))

    return (passes_a, passes_b) if order else (passes_b, passes_a)

def bell_qm(alpha, beta, samples):
    # Assume a photon source generating pairs of entangled photons with
    # a uniform polarization distribution
    photons = [rng.random() * 360 for _ in range(samples)]

    # Do the photons pass filter 1? do they pass filter 2?
    passes_a, passes_b = zip(*(passes_qm(alpha, beta, p) for p in photons))

    # Count coincidences
    pp, pn, np, nn = confusion(passes_a, passes_b)

    # Estimate for test setup
    e = (pp - pn - np + nn) / (pp + pn + np + nn)

    return e

def bell_test(samples, test, a0=0, a1=45, b0=22.5, b1=67.5):
    # Run tests for four different setups.
    # alpha is the angle for polarizer 1, beta plarizer 2
    # samples indicated the number of photon pairs fired
    ab = test(a0, b0, samples)
    aB = test(a0, b1, samples)
    Ab = test(a1, b0, samples)
    AB = test(a1, b1, samples)

    # Estimate the CHSH metric
    s = ab - aB + Ab + AB

    return s

def find_best():
    # Start off with a base angle 0
    a0 = 0
    # Arbitrarily choose 45 as polarizer difference, will be optimized later
    b0 = 45

    # Binary search to find the optimal difference between the two angles of the
    # same polarizer (diff)
    lo = 0
    hi = 90
    while hi - lo > 0.5:
        mid = (lo + hi) / 2
        sample_lo = (lo + mid) / 2
        sample_hi = (hi + mid) / 2
        result_lo = bell_test(100000, bell_qm, a0=a0, a1=a0+sample_lo, b0=b0, b1=b0+sample_lo)
        result_hi = bell_test(100000, bell_qm, a0=a0, a1=a0+sample_hi, b0=b0, b1=b0+sample_hi)
        if result_lo > result_hi: hi = mid
        else: lo = mid
    
    diff = (hi + lo) / 2 
    
    # Binary search to find the optimal base angle for polarizer b (b0)
    lo = 0
    hi = 90
    while hi - lo > 0.5:
        mid = (lo + hi) / 2
        sample_lo = (lo + mid) / 2
        sample_hi = (hi + mid) / 2
        result_lo = bell_test(100000, bell_qm, a0=a0, a1=a0+diff, b0=sample_lo, b1=sample_lo+diff)
        result_hi = bell_test(100000, bell_qm, a0=a0, a1=a0+diff, b0=sample_hi, b1=sample_hi+diff)
        if result_lo > result_hi: hi = mid
        else: lo = mid
    
    b0 = (hi + lo) / 2

    print(a0, a0+diff, b0, b0+diff)

find_best()

result = bell_test(1000000, bell_qm)
expected = 2 * math.sqrt(2)
print(f'Result: {result}  Expected: {expected}  Err: {abs(result - expected)}')
print(f'This test could{" not" if result > 2 else ""} be described by local hidden variable theories.')

x = list(arange(0, 90.1, 0.5))
results = [bell_test(10000, bell_qm, a0=0, a1=a, b0=22.5, b1=22.5+a) for a in x]
plt.plot(x, results)
plt.show()
