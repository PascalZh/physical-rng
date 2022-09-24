import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored, cprint
from numpy.random import default_rng
from random_algorithms import *
from random_utils import *


rng = default_rng()
bit_width = 8
mu = 120
sigma = 40
cprint(f'mu = {mu}\nsigma = {sigma}', 'blue')
x = rng.normal(mu, sigma, size=2000).astype('uint8')
# the length of the post-processed 8 bit number sequence to be analyzed
N = x.shape[0]
bins = 2**bit_width

y = delayed_reversed_xor(x)

def analyze_xcf(y, n):
  N = y.shape[0]
  first_bit = ((y >> (n-1)) & 1).astype('float')
  last_bit = ((y >> (8-n)) & 1).astype('float')
  c = np.correlate(first_bit, last_bit[:N//2], mode='valid')
  c /= N//2
  plt.plot(c)
  plt.title(str(n))
  plt.ylim(0, 1)

for i in range(1, 4+1):
  plt.subplot(2, 2, i)
  analyze_xcf(y, i)
  analyze_xcf(x, i)
  plt.legend(['XOR', 'Original'])

plt.show()
