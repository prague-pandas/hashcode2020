from load_file import load_libraries
from main import score
import numpy as np


def order_libraries(libraries, scores_of_books, num_of_days):
    ordered_libraries = []
    available_libraries_indices = set(range(len(libraries)))
    excluded_books = set()
    num_of_remaining_days = num_of_days
    best_score = 1
    while available_libraries_indices and num_of_remaining_days and best_score:
        scores_of_libraries = {}
        books_of_libraries = {}
        for i in available_libraries_indices:
            _, signup_days, books_per_day, list_of_books = libraries[i]
            scores_of_libraries[i], books_of_libraries[i] = score_library(list_of_books,
                                                     signup_days,
                                                     books_per_day,
                                                     excluded_books,
                                                     scores_of_books,
                                                     num_of_remaining_days)
        best_library = max(scores_of_libraries, key=scores_of_libraries.get)
        best_score = scores_of_libraries[best_library]
        print(best_library, scores_of_libraries[best_library])
        ordered_libraries.append((best_library,
                                  books_of_libraries[best_library]))
        _, signup_days, books_per_day, list_of_books = libraries[best_library]
        excluded_books.update(list_of_books)
        num_of_remaining_days -= signup_days
        available_libraries_indices.remove(best_library)
    return ordered_libraries


def score_library(list_of_books,
                  signup_days,
                  books_per_day,
                  excluded_books,
                  scores_of_books,
                  num_of_days):
    books = set(list_of_books) - set(excluded_books)
    books_scores = [(b, scores_of_books[b]) for b in books]
    books_scores.sort(key=lambda x: x[1])
    days_for_scanning = num_of_days - signup_days
    num_books_to_scan = books_per_day * days_for_scanning
    scores_cut = [x[1] for x in books_scores[:num_books_to_scan]]
    score = sum(scores_cut)
    return score, [x[0] for x in books_scores[:num_books_to_scan]]






if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    n_books, n_libs, n_days, scores_of_books, libs = load_libraries(args.file)
    scores_of_books_dict = dict(enumerate(scores_of_books))

    #print(n_books)
    #print(n_libs)
    #print(n_days)
    #print(book_scores)
    #print(libs[:10])

    #lib = libs[0]
    #n = lib[0]
    #signup_days = lib[1]
    #bs_per_day = lib[2]
    #bs = lib[3]
    #score = score_library(bs, signup_days, bs_per_day, [], scores_of_books, n_days)
    #print(score)

    library_signup_times = [lib[1] for lib in libs]
    library_ship_capacities = [lib[2] for lib in libs]
    solution = order_libraries(libs, scores_of_books_dict, n_days)
    print(solution)
    print(scores_of_books)
    scores_of_books = np.asarray(scores_of_books, dtype=np.uint)
    s = score(solution, n_days, scores_of_books,
          library_signup_times,
          library_ship_capacities)
    print(s)

