#!/usr/bin/env python3
"""This is a command line script.
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import functools
import random
import statsmodels.api as sm
from bitarray import bitarray
from ..utils import NBitSequence


class ArgumentParserWithDefaultsHelpFormatter(argparse.ArgumentParser):
    def __init__(self, *args, formatter_class=argparse.ArgumentDefaultsHelpFormatter, **kwargs):
        kwargs['formatter_class'] = formatter_class
        super().__init__(*args, **kwargs)


def load_bit_sequence(filename) -> bytes:
    with open(filename, 'rb' if filename.endswith('.bin') else 'r') as f:
        b = f.read()
        if filename.endswith('.txt'):
            b = bytes.fromhex(b[:len(b)//2*2])
    return b


def parse_bit_sequence(seq_bytes, bit_width=8, big_endian=True):
    b = seq_bytes
    # truncate to a multiple of bit_width bits, so that np.frombuffer and pack_bits work properly
    trunc_len = len(b) // bit_width * bit_width
    b = b[:trunc_len]

    if bit_width == 8:
        return np.frombuffer(b, dtype='>u1')  # big-endian
    elif bit_width == 16:
        return np.frombuffer(b, dtype='>u2')
    elif bit_width == 32:
        return np.frombuffer(b, dtype='>u4')
    elif bit_width == 64:
        return np.frombuffer(b, dtype='>u8')
    else:
        seq = NBitSequence(b, bit_width=bit_width, big_endian=big_endian)
        return seq.to_array()


def analyze_rng(args):

    bit_width = args.bit_width
    file = args.FILE
    file_without_ext = os.path.splitext(file)[0]

    x = parse_bit_sequence(load_bit_sequence(file), bit_width=bit_width)

    if args.plot_histogram:
        plt.figure()
        plt.title('Histogram')

        bins = 2**bit_width
        plt.hist(x, bins=bins)
        if args.save_fig:
            plt.savefig(file_without_ext+'_hist.png')

    if args.plot_time_series:
        plt.figure()
        plt.title('Time series (part)')

        start = random.randint(0, (len(x) - 2000))
        plt.plot(np.arange(start, start+2000), x[start:start+2000])
        # plt.plot(x)
        # plt.ylim(0, 256)
        if args.save_fig:
            plt.savefig(file_without_ext+'_time_series_part.png')

    if args.plot_psd:
        plt.figure()
        plt.title('PSD')
        plt.psd(x, NFFT=1024)
        if args.save_fig:
            plt.savefig(file_without_ext+'_psd.png')

    if args.plot_acf:
        plt.figure()
        plt.title('ACF')
        plt.plot(sm.tsa.acf(x))
        if args.save_fig:
            plt.savefig(file_without_ext+'_acf.png')

    if args.show:
        plt.show()


def main(args):

    # fig2 = plt.figure()
    # ax2 = fig2.add_subplot()
    # x = read_osc_data('1S.txt')
    # x_binary, x_compare = demodulate_osc_data(x, compare=True)
    # ax2.hist(np.packbits(x_binary), bins=2**8)
    plt.show()


def demodulate_osc_data(x, T=64, compare=True):
    L = x.shape[0] // T
    bin_seq = np.array([(x[i*T:(i+1)*T] > 0).sum() for i in range(L)])
    bin_seq = (bin_seq > T/2)

    if compare:
        bin_seq_for_plot = np.amin(x) + (np.amax(x) - np.amin(x)) * functools.reduce(
            lambda a, b: np.concatenate((a, b)), [np.repeat(bin_seq[i], T) for i in range(L)])
        return bin_seq, bin_seq_for_plot
    return bin_seq, None


def main():
    parser = ArgumentParserWithDefaultsHelpFormatter(
        description='Random number generation lab toolbox')
    subparsers = parser.add_subparsers(description='subcommands contains various tools',
                                       required=True,
                                       parser_class=type(parser))

    p1 = subparsers.add_parser('analyze_rng',
                               help='analyze a random bit sequence, parsing as W-bit number (big-endian)')
    p1.add_argument('FILE', default='test.bin',
                    help='inputted random sequence file')
    p1.add_argument('--plot_time_series', action='store_true')
    p1.add_argument('--plot_histogram', action='store_true')
    p1.add_argument('--plot_psd', action='store_true')
    p1.add_argument('--plot_acf', action='store_true')
    p1.add_argument('--show', action='store_true',
                    help='show figures (by default plt.show() is not called)')
    p1.add_argument('--save_fig', action='store_true',
                    help='save figures when ploting')
    p1.add_argument('--bit_width', metavar='W', type=int, default=8,
                    help='random bit sequence will be viewed as W-bit number sequence (big-endian)')
    p1.set_defaults(func=analyze_rng)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    main()
