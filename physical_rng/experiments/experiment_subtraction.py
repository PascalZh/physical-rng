import numpy as np
import matplotlib.pyplot as plt
from random import randint

dpi = 150

sigma = 60
mu = 140


def gen_random():
    x = sigma * np.random.randn(100000) + mu
    x = x.astype('uint8')
    return x


def hist(x, title=None, bins=256):
    plt.hist(x, bins=bins, range=(0, bins-1))
    plt.title(title)


x1 = gen_random()
x2 = gen_random()
x3 = gen_random()
x4 = gen_random()


def plot_m_lsb_cut(x, title):
    print(f'{title}: std = {np.std(x)}')
    for i in range(5):
        plt.subplot(2, 3, i+1)
        hist(x % 2**(8-i), f'({title}) % 2**{8-i}', bins=2**(8-i))
    plt.subplot(2, 3, 6)
    idx = randint(0, len(x) - 200)
    plt.plot(x[idx:idx+200], linewidth=0.5)
    plt.ylim(0, 255)


plt.figure(dpi=dpi)
plot_m_lsb_cut(x1, 'x1')

plt.figure(dpi=dpi)
plot_m_lsb_cut(x1 - x2, 'x1 - x2')

plt.figure(dpi=dpi)
plot_m_lsb_cut(x1 + x2, 'x1 + x2')

plt.figure(dpi=dpi)
plot_m_lsb_cut(x1 - x2 - x3 + x4, 'x1 - x2 - x3 + x4')

plt.show()
