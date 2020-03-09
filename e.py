from sa import library_scanning_strategy, simulated_annealing, file_dict

e = library_scanning_strategy.from_file(file_dict['e'])

# sort it
sorted_strategy = e.generate_sorted_strategy()
print("Sort Library: {}".format(e.score(sorted_strategy)))
special_strategy = e.sort_books_by_score(sorted_strategy)
print("Remove redundancy: {}".format(e.score(special_strategy)))
strategy_at_end_of_stage = special_strategy
strategy_at_end_of_stage, score_history = simulated_annealing(
  e, 
  strategy_at_end_of_stage, 
  e.score(special_strategy), 
  swap_step = 2, 
  library_swap_prob = 1,
  reduce_interval = 500,
  iteration = 1000000)