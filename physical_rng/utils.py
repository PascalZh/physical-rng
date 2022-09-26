import numpy as np
import matplotlib.pyplot as plt
from bitarray import bitarray


class NBitSequence(object):
    def __init__(self, data: bytes, *, bit_width: int, big_endian=True):
        self._buffer = data
        self.bit_width = bit_width
        self.big_endian = big_endian


    def tobytes(self):
        return self._buffer


    def to_array(self, dtype='int') -> np.ndarray:
        """Notice: ensure a variable of dtype can contain any integer number of width `bit_width`.
        
        Extra bits will be discarded when the number of all bits is not dividable by bit_width"""
        ba = bitarray()
        ba.frombytes(self._buffer)
        bit_width = self.bit_width
        big_endian = self.big_endian

        N = len(ba)
        N -= N % bit_width

        seq = np.zeros(N // bit_width, dtype=dtype)
        for i in range(N // bit_width):
            for j in range(bit_width):
                if big_endian:
                    seq[i] += ba[i*bit_width+j] << (bit_width - j - 1)
                else:  # little-endian
                    seq[i] += ba[i*bit_width+j] << j
        return seq

    
    @classmethod
    def from_ndarray(cls, arr: np.ndarray, **kwargs):
        return cls(arr.tobytes(), **kwargs)


def read_osc_data(filename: str) -> np.ndarray:
    with open(filename, 'r') as f:
        return np.array([float(x) for x in f.read().splitlines()])


def generate_cdf(x: np.ndarray):
    hist = np.bincount(x, minlength=256).astype(float)
    hist /= len(x)
    hist = np.cumsum(hist)
    plt.figure('CDF')
    plt.plot(hist)
    assert(len(hist) == 256)

    def cdf(y):
        return hist[int(y) % 256]

    return np.vectorize(cdf)


def calculate_biases(seq: bytes):
    ba = bitarray()
    ba.frombytes(seq)
    N = len(ba)//8
    biases = np.array([0 for _ in range(8)], dtype=float)

    for i in range(N):
        for j in range(8):
            biases[j] += ba[i*8+7-j]

    biases /= N
    biases = np.abs(biases - 0.5)
    return biases # [LSB, ..., MSB]


def plot_biases(ax, seq: bytes, label=None):
    biases = calculate_biases(seq)
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
