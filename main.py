import argparse
import glob
import itertools
import logging

import numpy as np

import greedy


def load_libraries(filename):
    with open(filename) as f:
        b, l, d = map(int, f.readline().split(' '))
        s = list(map(int, f.readline().split(' ')))
        libraries = list()
        for _ in range(l):
            n, t, m = map(int, f.readline().split(' '))
            books = list(map(int, f.readline().split(' ')))
            libraries.append((n, t, m, books))
        return b, l, d, s, libraries


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
    total = np.uint(0)
    current_time = np.uint(0)
    days = np.uint(days)
    book_scores = book_scores.copy()
    for library, books in solution:
        signup_time = np.uint(library_signup_times[library])
        ship_capacity = np.uint(library_ship_capacities[library])
        current_time += signup_time
        if current_time >= days:
            break
        remaining_time = days - current_time
        n_books_to_be_scanned = remaining_time * ship_capacity
        books_to_be_scanned = books[:n_books_to_be_scanned]
        cur_scores = book_scores[books_to_be_scanned]
        total += np.sum(cur_scores)
        book_scores[books_to_be_scanned] = 0
    return int(total)


def solve_random(name, d, s, libraries, iterations=None):
    library_signup_times = np.asarray([lib[1] for lib in libraries], dtype=np.uint)
    library_ship_capacities = np.asarray([lib[2] for lib in libraries], dtype=np.uint)
    best_score = 0
    if iterations is None or iterations < 0:
        i_generator = itertools.count()
    else:
        i_generator = range(iterations)
    for i in i_generator:
        library_order = np.random.permutation(len(libraries))
        solution = list()
        for library_i in library_order:
            n, t, m, books = libraries[library_i]
            books = np.asarray(books, dtype=np.uint)
            solution.append((library_i, np.random.permutation(books)))
        scor = score(solution, d, s, library_signup_times, library_ship_capacities)
        if scor > best_score:
            logging.info(f'New best score in iteration {i}: {scor}')
            save_result(f'{name}_{str(scor).zfill(8)}_random.out', solution)
            best_score = scor
    return best_score


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='input/*.txt')
    parser.add_argument('--random', action='store_true')
    parser.add_argument('--greedy', action='store_true')
    parser.add_argument('--iterations', type=int, default=1, help='-1: run forever')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    np.seterr(all='raise')

    np.random.seed(0)

    for f in sorted(glob.iglob(args.input)):
        print(f)
        b, l, d, s, libraries = load_libraries(f)
        s = np.asarray(s, dtype=np.uint)
        print(f'Score upper bound: {np.sum(s)}')
        library_signup_times = np.asarray([lib[1] for lib in libraries], dtype=np.uint)
        library_ship_capacities = np.asarray([lib[2] for lib in libraries], dtype=np.uint)
        if args.random:
            solve_random(f, d, s, libraries, args.iterations)
        if args.greedy:
            solution = greedy.order_libraries(libraries, s, d)
            scor = score(solution, d, s, library_signup_times, library_ship_capacities)
            print(f'Greedy score: {scor}')
            save_result(f'{f}_{str(scor).zfill(8)}_greedy.out', solution)
