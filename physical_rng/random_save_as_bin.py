#!/usr/bin/env python3
import glob

data_path = 'data4_0325'

random_files = glob.glob(data_path+'/*.txt')
save_bytes = b''

for filename in random_files:
    with open(filename, 'r') as f:
        print('converting %s...' % filename)
        s = f.read()
        if (len(s) % 2 == 1):  # make len(s) even
            s = s[0:-1]
        save_bytes += bytes.fromhex(s)

with open(data_path+'.bin', 'wb') as f:
    print('saving as a whole binary file: '+data_path+'.bin')
    f.write(save_bytes)

