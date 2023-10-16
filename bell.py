import matplotlib.pyplot as plt
import matplotlib.scale as scl
import random as rng
import pandas as pd
import math

from numpy import arange, logspace
from matplotlib import rcParams
from tqdm import tqdm

xls = pd.ExcelWriter('bell.xlsx')

def confusion(a, b):
    pp = sum(    p and     q for p, q in zip(a, b))
    pn = sum(    p and not q for p, q in zip(a, b))
    np = sum(not p and     q for p, q in zip(a, b))
    nn = sum(not p and not q for p, q in zip(a, b))

    return pp, pn, np, nn

def filter(alpha, beta):
    # Probability amplitude is determined by the cosine of the angle difference
    return rng.random() < math.cos(math.radians(abs(alpha - beta)))**2

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
    passes_b = filter(beta, alpha + 90 * (not passes_a))
    
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

def passes_hidden(alpha, beta, photon):
    # Does photon 1 pass through the polarizer?
    passes_a = filter(alpha, photon)

    # Probability of photon 2 coinciding with 1 is linear with respect to the angle difference
    passes_b = passes_a
    diff = abs((alpha % 180) - (beta % 180))
    if diff > 90: diff = 180 - diff
    if rng.random() < diff / 90:
        passes_b = not passes_b
    
    return (passes_a, passes_b)

def bell_hidden(alpha, beta, samples):
    # Assume a photon source generating pairs of entangled photons with
    # a uniform polarization distribution
    photons = [rng.random() * 360 for _ in range(samples)]

    # Do the photons pass filter 1? do they pass filter 2?
    passes_a, passes_b = zip(*(passes_hidden(alpha, beta, p) for p in photons))

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
        result_lo = bell_test(1000000, bell_qm, a0=a0, a1=a0+sample_lo, b0=b0, b1=b0+sample_lo)
        result_hi = bell_test(1000000, bell_qm, a0=a0, a1=a0+sample_hi, b0=b0, b1=b0+sample_hi)
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
        result_lo = bell_test(1000000, bell_qm, a0=a0, a1=a0+diff, b0=sample_lo, b1=sample_lo+diff)
        result_hi = bell_test(1000000, bell_qm, a0=a0, a1=a0+diff, b0=sample_hi, b1=sample_hi+diff)
        if result_lo > result_hi: hi = mid
        else: lo = mid
    
    b0 = (hi + lo) / 2

    print(a0, a0+diff, b0, b0+diff)

def single_experiment():
    result = bell_test(10000000, bell_hidden)
    expected = 2 * math.sqrt(2)
    print(f'Result: {result}  Expected: {expected}  Err: {abs(result - expected)}')
    print(f'This test could{" not" if result > 2.1 else ""} be described by local hidden variable theories.')

def plot_angles():
    rcParams.update({'font.size': 38})

    x = list(arange(0, 360.1, 1))
    resultsa = [bell_test(1000, bell_qm, a0=0, a1=45, b0=a, b1=a+45) for a in tqdm(x)]
    resultsb = [bell_test(1000, bell_qm, a0=0, a1=a, b0=22.5, b1=22.5+a) for a in tqdm(x)]

    #f = pd.read_excel('bbell.xlsx', sheet_name='angles')
    #resultsa = list(f['baseB'])
    #resultsb = list(f['diff'])

    cont = arange(0, math.tau, 0.1)
    plt.plot(cont, [math.sin(a * 2 + math.pi / 4) * 2 * 2**0.5 for a in cont], c='#01c1fd', ls='--')
    plt.plot(cont, [math.sin(a * 2) * 2**0.5 + 2**0.5 for a in cont], c='#7030a0' , ls='--')

    plt.axhline(y= 2*2**0.5, c='tab:green', ls=':', lw='5')
    plt.axhline(y= 2, c='red', ls='-', lw='5')
    plt.axhline(y=-2*2**0.5, c='tab:green', ls=':', lw='5')
    plt.axhline(y=-2, c='red', ls='-', lw='5')

    rads = [a / 180 * math.pi for a in x]
    plt.plot(rads, resultsa, '+', c='#01c1fd')
    plt.plot(rads, resultsb, 'x', c='#7030a0' )

    #frame = pd.DataFrame({'x': x, 'rads': rads, 'baseB': resultsa, 'diff': resultsb})
    #frame.to_excel(xls, sheet_name='angles', index=False)

    plt.xticks([0, math.pi / 2, math.pi, 3/2*math.pi, math.tau, math.radians(22.5), math.radians(45)], [0, "$\pi/2$", "$\pi$", "$3\pi/2$", "$2\pi$", "$\pi/8$", "$\pi/4$"])
    plt.axvline(x=math.radians(22.5), c='#01c1fd', ls=':')
    plt.axvline(x=math.radians(45.0), c='#7030a0' , ls=':')

    plt.xlabel('θ (radians)')
    plt.ylabel('S')

    plt.legend(['Varying beam splitter diff.', 'Varying setting diff.', 'QM limit', 'Inequality limit'])

    #plt.grid()
    plt.show()

def plot_converge():
    rcParams.update({'font.size': 35})

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    x = [int(a) for a in logspace(2, 6, 300)]
    resultsa = [bell_test(a, bell_qm) for a in tqdm(x)]
    resultsb = [bell_test(a, bell_classical) for a in tqdm(x)]
    resultsc = [bell_test(a, bell_hidden) for a in tqdm(x)]

    #f = pd.read_excel('bbell.xlsx', sheet_name='converge')
    #resultsa = list(f['qm'])
    #resultsb = list(f['classical'])
    #resultsc = list(f['hidden'])

    #frame = pd.DataFrame({'x': x, 'qm': resultsa, 'classical': resultsb, 'hidden': resultsc})
    #frame.to_excel(xls, sheet_name='converge', index=False)

    ax1.plot(x, resultsa, c='tab:blue')
    ax1.axhline(y=2*2**0.5, c='tab:pink', ls=':', lw='5')
    ax1.legend(['Quantum results','Quantum theoretical limit'], loc='upper right', fontsize="25")
    ax1.set_xscale(scl.LogScale('x', base = 10))

    ax2.plot(x, resultsb, c='tab:red')
    ax2.axhline(y=2**0.5, c='tab:purple', ls=':', lw='5')
    ax2.legend(['Classic results', 'Classic theoretical limit'], loc='lower right', fontsize="25")
    ax2.set_xscale(scl.LogScale('x', base = 10))

    ax3.plot(x, resultsc, c='tab:orange')
    ax3.axhline(y=2, c='tab:green', ls=':', lw='5')
    ax3.legend(['Hidden variable results', 'Hidden variable theoretical limit'], loc='upper right', fontsize="25")
    ax3.set_xscale(scl.LogScale('x', base = 10))

    #ax1.grid()
    #ax2.grid()
    #ax3.grid()

    fig.text(0.005, 0.5, 'S', va='center', rotation='vertical')
    plt.xlabel('Sample size (photon pairs)')

    plt.show()

#find_best() # Binary search for bell test angles
single_experiment() # Run a single experiment
#plot_angles() # Graph varying angles
#plot_converge() # Graph increasing sample size, qm vs classical

xls.close()
