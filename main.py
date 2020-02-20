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
    book_scores = book_scores.copy()
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
    return int(total)


def solve_random(name, d, s, libraries, iterations=None):
    library_signup_times = [lib[1] for lib in libraries]
    library_ship_capacities = [lib[2] for lib in libraries]
    best_score = 0
    for i in range(iterations):
        library_order = np.random.permutation(len(libraries))
        solution = list()
        for library_i in library_order:
            n, t, m, books = libraries[library_i]
            solution.append((library_i, np.random.permutation(books)))
        scor = score(solution, d, s, library_signup_times, library_ship_capacities)
        if scor > best_score:
            logging.info(f'New best score in iteration {i}: {scor}')
            save_result(f'{name}_{str(scor).zfill(8)}.out', solution)
            best_score = scor
    return best_score


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=100)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    np.random.seed(0)

    for f in sorted(glob.glob('input/*.txt')):
        print(f)
        b, l, d, s, libraries = load_file.load_libraries(f)
        s = np.asarray(s, dtype=np.uint)
        print(f'Score upper bound: {np.sum(s)}')
        library_signup_times = [lib[1] for lib in libraries]
        library_ship_capacities = [lib[2] for lib in libraries]
        solve_random(f, d, s, libraries, args.iterations)
