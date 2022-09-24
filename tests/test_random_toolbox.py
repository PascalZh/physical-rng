import numpy as np
from bitarray import bitarray
from numpy.random import default_rng
import matplotlib.pyplot as plt
from random_toolbox import pack_bits

rng = default_rng()

print(pack_bits(b'\xa1\xfe\xff', bit_width=1))
print(pack_bits(b'\xa1\xfe\xff', bit_width=2))
print(pack_bits(b'\xa1\xfe\xff', bit_width=3))
print(pack_bits(b'\xa1\xfe\xff', bit_width=4))
print(pack_bits(b'\xa1\xfe\xff', bit_width=8))


def generate_random_bit_sequence():

    #vals = rng.integers(0, 2**8, size=10000).astype('uint8')
    vals = rng.normal(128, 40, size=10000).astype('uint8')
    print('Generated pseudo-random values\nFirst 20:',
          vals[:20], '\nLast 20:', vals[-20:], '\n')
    f_bit_dump = open('tmp_bit_dump.txt', 'w')
    f_bin = open('tmp_bin.bin', 'wb')
    for x in vals:
        f_bit_dump.write(f'{x:08b}')
        f_bin.write(x)

    f_bit_dump.close()
    f_bin.close()

    plt.hist(vals, bins=2**8)


generate_random_bit_sequence()

plt.show()
