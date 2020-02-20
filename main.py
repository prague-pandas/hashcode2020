import argparse
import glob
import logging

import numpy as np

import load_file


def pizza_load(f):
    with open(f) as fp:
        line0 = fp.readline()
        m, n = tuple(map(int, line0.split(' ')))
        s = list(map(int, fp.readline().split(' ')))
        return s, m


def save_result(filename, libraries):
    with open(filename, 'w') as f:
        f.write(f'{len(libraries)}\n')
        for library, books in libraries:
            f.write(f'{library} {len(books)}\n')
            f.write(' '.join(map(str, books)))
            f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=100)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    np.random.seed(0)

    for f in glob.glob('input/*.txt'):
        print(f)
        b, l, d, s, libraries = load_file.load_libraries(f)
        save_result(f'{f}.out', [(1, [5, 2, 3]), (0, [0, 1, 2, 3, 4])])
