import numpy as np
import matplotlib.pyplot as plt
from bitarray import bitarray


def read_osc_data(filename) -> np.ndarray:
    with open(filename, 'r') as f:
        return np.array([float(x) for x in f.read().splitlines()])


def generate_cdf(x):
    hist = np.bincount(x, minlength=256).astype(float)
    hist /= len(x)
    hist = np.cumsum(hist)
    plt.figure('CDF')
    plt.plot(hist)
    assert(len(hist) == 256)

    def cdf(y):
        return hist[int(y) % 256]

    return np.vectorize(cdf)


def calculate_biases(x_bytes):
    ba = bitarray()
    ba.frombytes(x_bytes)
    N = len(ba)//8
    biases = np.array([0 for _ in range(8)], dtype=float)

    for i in range(N):
        for j in range(8):
            biases[j] += ba[i*8+7-j]

    biases /= N
    biases = np.abs(biases - 0.5)
    return biases # [LSB, ..., MSB]


def plot_biases(ax, x_bytes, label=None):
    biases = calculate_biases(x_bytes)
    print(f'cnt = {biases}')
    ax.plot(range(1,9), biases, label=label)
    ax.set_yscale('log')
    ax.set_title('Bias for every bits')
    ax.legend(fontsize=6)


def H_min(pdf: np.ndarray):
    """Calculate min entropy
    Unit: bit
    See the article: Real-time fast physical random number generator with a photonic integrated circuit
    """
    return -np.log2(np.max(pdf))
