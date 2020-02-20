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


def score(solution, days, book_scores, library_signup_times, library_ship_capacities):
    total = 0
    current_time = 0
    for library, books in solution:
        signup_time = library_signup_times[library]
        ship_capacity = library_ship_capacities[library]
        current_time += signup_time
        remaining_time = days - current_time
        n_books_to_be_scanned = remaining_time * ship_capacity
        books_to_be_scanned = books[:n_books_to_be_scanned]
        cur_scores = book_scores[books_to_be_scanned]
        total += np.sum(cur_scores)
        book_scores[books_to_be_scanned] = 0
    return total


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=100)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    np.random.seed(0)

    for f in glob.glob('input/*.txt'):
        print(f)
        b, l, d, s, libraries = load_file.load_libraries(f)
        s = np.asarray(s, dtype=np.uint)
        library_signup_times = [lib[1] for lib in libraries]
        library_ship_capacities = [lib[2] for lib in libraries]
        solution = [(1, [5, 2, 3]), (0, [0, 1, 2, 3, 4])]
        print(score(solution, d, s, library_signup_times, library_ship_capacities))
        save_result(f'{f}.out', solution)
