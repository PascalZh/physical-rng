#!/usr/bin/env python3
import sys
import os
from subprocess import Popen, PIPE

if len(sys.argv) < 2:
    print('Usage: ./rbg_nist_sp_800_22_test <file> <ascii | bin>')
    exit(1)

SEQ_LEN = 1000000

file = sys.argv[1]
is_ascii = True if sys.argv[2] == 'ascii' else False

file_bit_len = os.path.getsize(file) * (1 if is_ascii else 8)

num_of_seq = file_bit_len // SEQ_LEN

if num_of_seq < 1:
    print(f'Error: inputted sequence must have at least {SEQ_LEN} bits')
    exit(1)

print('Creating directories for saving the results')


for dname in 'AlgorithmTesting BBS CCG G-SHA1 LCG MODEXP MS QCG1 QCG2 XOR'.split():
    for dname_sub in 'Frequency BlockFrequency Runs LongestRun Rank FFT NonOverlappingTemplate OverlappingTemplate Universal LinearComplexity Serial ApproximateEntropy CumulativeSums RandomExcursions RandomExcursionsVariant'.split():
        p = os.path.join('experiments', dname, dname_sub)
        os.makedirs(p, exist_ok=True)

print(f'Assessing {num_of_seq} sequences, each sequence has {SEQ_LEN} bits\n')

p = Popen(['assess', str(SEQ_LEN)], stdin=PIPE, text=True)

p.communicate(input=f'0\n{file}\n1\n0\n{num_of_seq}\n{1-int(is_ascii)}\n')

if p.returncode == 1:  # somehow `assess` return 1 for success
    os.system('cat experiments/AlgorithmTesting/finalAnalysisReport.txt')
    os.system('cat experiments/AlgorithmTesting/freq.txt')
