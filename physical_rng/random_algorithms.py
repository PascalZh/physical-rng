from bitarray import bitarray
import numpy as np


def identity(x):
    return x


def delayed_xor(x, delay=101):

    x_bytes = x.tobytes()
    ba = bitarray()
    ba.frombytes(x_bytes)
    ba_ret = bitarray()
    for i in range(delay, len(ba)//8):
        i_ = i - delay  # index for delayed values
        res = [ba[i*8+j] ^ ba[i_*8+j] for j in range(8)]

        for j in range(8):
            ba_ret.append(res[j])

    return np.frombuffer(ba_ret.tobytes(), dtype='uint8')


def delayed_reversed_xor(x, delay=101):

    x_bytes = x.tobytes()
    ba = bitarray()
    ba.frombytes(x_bytes)
    ba_ret = bitarray()
    for i in range(delay, len(ba)//8):
        i_ = i - delay  # index for delayed values
        res = [ba[i*8+j] ^ ba[i_*8+7-j] for j in range(8)]

        for j in range(8):
            ba_ret.append(res[j])

    return np.frombuffer(ba_ret.tobytes(), dtype='uint8')


def delayed_reversed_xor_then_select_4bits(x, delay=101):

    x_bytes = x.tobytes()
    ba = bitarray()
    ba.frombytes(x_bytes)
    ba_ret = bitarray()
    for i in range(delay, len(ba)//8):
        i_ = i - delay  # index for delayed values
        res = [ba[i*8+j] ^ ba[i_*8+7-j] for j in range(8)]

        for j in [0, 1, 6, 7]:
            ba_ret.append(res[j])

    return np.frombuffer(ba_ret.tobytes(), dtype='uint8')


def delayed_reversed_xor_then_mLSB(x, delay=101, m=4):

    x_bytes = x.tobytes()
    ba = bitarray()
    ba.frombytes(x_bytes)
    ba_ret = bitarray()
    for i in range(delay, len(ba)//8):
        i_ = i - delay  # index for delayed values
        res = [ba[i*8+j] ^ ba[i_*8+7-j] for j in range(8)]

        for j in range(m):
            ba_ret.append(res[7-j])

    return np.frombuffer(ba_ret.tobytes(), dtype='uint8')


def cdf_method(x, cdf):
    return (cdf(x) * 256).astype('uint8')


def box_muller(x_bytes, delay=101):
    x_ = np.frombuffer(x_bytes, dtype='uint8')
    x = (x_[delay:] - 128)/40
    y = (x_[:-delay] - 128)/40
    b = np.exp(- (x**2+y**2)/2) * 256
    # plt.figure('Box-Muller time series')
    # plt.plot(b)
    return b.astype('uint8')


def diff(x, n=1):
    return np.diff(x, n=n).astype('uint8')


def subtract_delayed(x, delay):
    return x[delay:] - x[:-delay]


def diff_delayed_reversed_xor(x):
    return delayed_reversed_xor(np.diff(x))

def subtract_delayed(x):
    delays = [0, 137, 487, 547, 1321, 1559, 2531, 61, 2161, 829, 1487, 647, 887, 3373, 2879, 3413, 457, 23]
    ba_ret = bitarray()

    for i in range(7549, len(x)):
        res = [np.uint8(0) for j in range(8)]
        # for j in range(8):
            # print(ba[i*8+j], end=' ')
        # print()
        # for j in range(8):
            # print(ba[i_*8+j], end=' ')
        # print()

        for j in range(8):
            # print(f'{c1[j]:08b}, {c2[j]:08b}')

            res[j] = (((x[i-delays[2*j]] - x[i-delays[2*j+1]]) % (2 ** (j+1))) >> j) & 1
            # print(f'{c1[j] - c2[j]:08b} {res[j]:08b}')
        # print()

        # for j in range(8):
            # print(res[7-j], end=' ')
        # print()

        for j in range(8):
            ba_ret.append(res[7-j])

    return np.frombuffer(ba_ret.tobytes(), dtype='uint8')


def lfsr8_with_perturbation(perturb: np.ndarray, N, seed):
    perturb_bitarray = bitarray()
    perturb_bitarray.frombytes(perturb.tobytes())
    seq = bitarray(seed)
    assert(N > len(seq) and (N-len(seq)) < len(perturb_bitarray))
    for i in range(N-len(seq)):
        seq.append(seq[-1]^seq[-3]^seq[-4]^seq[-6]^1 ^ perturb_bitarray[i])
    return np.frombuffer(seq.tobytes(), dtype='uint8')
