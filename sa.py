import numpy as np
import matplotlib.pyplot as plt
import random
import os

class library_scanning_strategy:
  def __init__(self, nBooks, nLibraries, nDays, bookScores, libraryList, filename):
    self.nBooks = nBooks
    self.nLibraries = nLibraries
    self.nDays = nDays
    self.bookScores = bookScores
    self.libraryList = libraryList
    self.librarySignupDays = [library['signupDays'] for library in self.libraryList]
    self.libraryBookspDay = [library['books/day'] for library in self.libraryList]
    self.filename_short = filename.split('/')[1][0]
  @classmethod
  def from_file(cls, filename):
    with open(filename) as f:
      lines = f.read().split('\n')
      nBooks, nLibraries, nDays = map(lambda x: int(x), lines[0].split(' '))
      bookScores = np.array(list(map(lambda x: int(x), lines[1].split(' '))))
      libraryList = []
      for i in range(nLibraries):
        tempDict = {}
        tempDict['nBooks'], tempDict['signupDays'], tempDict['books/day'] = map(lambda x: int(x), lines[(2*i)+2].split(' '))
        tempDict['booksList'] = np.array(list(map(lambda x: int(x), lines[(2*i)+3].split(' '))))
        libraryList.append(tempDict)
      return cls(nBooks, nLibraries, nDays, bookScores, libraryList, filename)
  def book_occurence_matrix(self, strategy):
    """ 
      A generator to yield book occurence matrix for a given strategy,
      in the order of libraries as given by the strategy list.
    """
    for i, library in enumerate(strategy):
      occurence_matrix = np.zeros([self.nBooks], dtype=bool)
      occurence_matrix[np.array(library['books_to_scan'])] = True
      yield i, library, occurence_matrix
  def scanning_days(self, strategy):
    signUpdays = np.array([self.librarySignupDays[library['id']] for library in strategy])
    readyOnDay = np.cumsum(signUpdays)
    temp_sd = (self.nDays - readyOnDay)
    return (temp_sd > 0)*temp_sd
  def redundancy(self, strategy):
    library_id_list = [library['id'] for library in strategy]
    scanning_days_list = self.scanning_days(strategy)
    scanning_days_dict = dict(zip(library_id_list, scanning_days_list))
    scan_array = np.zeros([len(self.bookScores)])
    for i, (library_id, scanning_days) in enumerate(scanning_days_dict.items()):
      books_to_scan = strategy[i]['books_to_scan']
      max_books_that_can_be_scanned = self.libraryList[library_id]['books/day']*scanning_days
      N = min([max_books_that_can_be_scanned, len(books_to_scan)])
      books_scanned = books_to_scan[:N]
      if len(books_scanned) > 0:
        scan_array[np.array(books_scanned)] += 1
    return scan_array
  def score(self, strategy):
    scan_array = self.redundancy(strategy)
    return (scan_array != 0)@self.bookScores
  def generate_random_strategy(self):
    random_strategy = []
    sequence = [i for i in range(len(self.libraryList))]
    np.random.shuffle(sequence)
    for i in sequence:
      temp_dict = {}
      temp_dict['id'] = i
      book_sequence = self.libraryList[i]['booksList']
      np.random.shuffle(book_sequence)
      temp_dict['books_to_scan'] = book_sequence
      random_strategy.append(temp_dict)
    return random_strategy
  def sort_books_by_score(self, strategy):
    book_sorted_strategy = strategy
    oneup_books_array = np.arange(1, self.nBooks + 1)
    for _, library, o_matrix in self.book_occurence_matrix(book_sorted_strategy):
      book_array = oneup_books_array*o_matrix
      sorted_book_array = book_array[np.argsort(-self.bookScores)]
      library['books_to_scan'] = list(sorted_book_array[sorted_book_array != 0] - 1)
    return book_sorted_strategy
  def generate_sorted_strategy(self):
    sorted_strategy = []
    signup_days = np.array([library['signupDays'] for library in self.libraryList])
    sorted_library_order = np.argsort(signup_days)
    for i in sorted_library_order:
      temp_dict = {}
      temp_dict['id'] = i
      book_sequence = self.libraryList[i]['booksList']
      np.random.shuffle(book_sequence)
      temp_dict['books_to_scan'] = book_sequence
      sorted_strategy.append(temp_dict)
    return sorted_strategy
  def random_swap_strategy(self, strategy, swap_item):
    if swap_item is 'library':
      return np.random.permutation(strategy)
    if swap_item is 'book':
      random_library = np.random.randint(len(strategy))
      strategy[random_library]['books_to_scan'] = np.random.permutation(strategy[random_library]['books_to_scan'])
      return strategy
  def remove_redundancy_and_sort_by_score(self, strategy):
    non_redundant_strategy = strategy
    csum_o_matrix = np.zeros(self.nBooks)
    oneup_books_array = np.arange(1, self.nBooks + 1)
    for i, library, o_matrix in self.book_occurence_matrix(non_redundant_strategy):
      csum_o_matrix += o_matrix
      masked_csum_o_matrix = o_matrix*csum_o_matrix
      repeated_books = oneup_books_array*(masked_csum_o_matrix > 1)
      non_repeated_books = oneup_books_array*(masked_csum_o_matrix == 1)
      sorted_non_repeated_books = non_repeated_books[np.argsort(-self.bookScores)]
      library['books_to_scan'] = \
        list(sorted_non_repeated_books[sorted_non_repeated_books != 0] - 1) + \
        list(repeated_books[repeated_books != 0] - 1)
    return non_redundant_strategy
  def output_strategy(self, filename, strategy):
    with open(filename, 'w') as f:
      f.write(str(len(strategy)))
      for library in strategy:
        f.write('\n')
        f.write(str(library['id']) + ' ' + str(len(library['books_to_scan'])))
        f.write('\n')
        books_to_scan_list_as_string = list(map(lambda x: str(x), library['books_to_scan']))
        f.write(' '.join(books_to_scan_list_as_string))

def simulated_annealing(library_set, start_strategy, T, reduce_interval=100, library_swap_prob=0.9, swap_step=1, iteration=1000, plot=True):
  max_strategy_history = []
  current_strategy = start_strategy
  current_score = library_set.score(current_strategy)
  max_score = current_score
  for i in range(iteration):
    # reduce temperature
    T = T * (np.exp((-10)/iteration))
    # swap
    temp_new_strategy = current_strategy
    for j in range(swap_step):
      swap_type = random.choices(['book', 'library'], weights=[1-library_swap_prob,library_swap_prob])[0]
      temp_new_strategy = library_set.random_swap_strategy(temp_new_strategy, swap_type)
    new_strategy = temp_new_strategy
    new_score = library_set.score(new_strategy)
    # accept/reject change
    deltaE = (new_score - current_score)
    metropolis_factor = min([1, np.exp(deltaE/T)])
    p = np.random.random()
    if (p < metropolis_factor):
      # update
      if new_score > max_score:
        library_set.output_strategy('output/output_'+library_set.filename_short+str(new_score)+'.txt', new_strategy)
        max_score = new_score
        max_strategy_history.append(new_strategy)
      current_strategy = new_strategy
      current_score = new_score
    # reduce the best strategies
    if ((i%reduce_interval == 0 and i != 0) or (i == iteration - 1)) and (len(max_strategy_history) != 0):
      max_score_history = list(map(lambda x: library_set.score(x), max_strategy_history))
      max_strategy = max_strategy_history[np.argsort(-np.array(max_score_history))[0]]
      reduced_max_strategy = library_set.remove_redundancy_and_sort_by_score(max_strategy)
      reduced_max_score = library_set.score(reduced_max_strategy)
      print("Max score {} reduced to {}".format(max_score, reduced_max_score))
      library_set.output_strategy('output/output_'+library_set.filename_short+str(reduced_max_score)+'.txt', reduced_max_strategy)
    if (i%100 == 0):
      print("Step {} for example {}".format(i,library_set.filename_short))
  pass


list_of_filenames = os.listdir('input')
input_keys = [filename[0] for filename in list_of_filenames]
list_of_filepaths = ['input/' + filename for filename in list_of_filenames]
file_dict = dict(zip(input_keys, list_of_filepaths))
