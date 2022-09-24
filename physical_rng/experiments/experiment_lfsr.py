"""
尝试LFSR算法和采到的随机数相结合
"""
import bitarray
import numpy as np
import matplotlib.pyplot as plt

def lfsr_8_bit(N, seed):
    seq = bitarray.bitarray(seed)
    assert(N > len(seq))
    for i in range(N-len(seq)):
        seq.append(seq[-1]^seq[-3]^seq[-4]^seq[-6]^1)
    return np.frombuffer(seq.tobytes(), dtype='uint8')

seq = lfsr_8_bit(1024, 7)

plt.plot(seq)
plt.figure()
plt.hist(seq, bins=256)
plt.show()
