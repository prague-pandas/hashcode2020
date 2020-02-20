import argparse
import glob
import logging

import numpy as np


def pizza_load(f):
    with open(f) as fp:
        line0 = fp.readline()
        m, n = tuple(map(int, line0.split(' ')))
        s = list(map(int, fp.readline().split(' ')))
        return s, m


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=100)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    np.random.seed(0)

    for f in glob.glob('pizza/*.in'):
        logging.debug(f)
        s, m = pizza_load(f)
        print(m)
