from sa import library_scanning_strategy, simulated_annealing, file_dict

d = library_scanning_strategy.from_file(file_dict['d'])

# sort it
sorted_strategy = d.generate_sorted_strategy()
print("Sort Library: {}".format(d.score(sorted_strategy)))
special_strategy = d.sort_books_by_score(sorted_strategy)
print("Remove redundancy: {}".format(d.score(special_strategy)))
strategy_at_end_of_stage = special_strategy
strategy_at_end_of_stage, score_history = simulated_annealing(
  d, 
  strategy_at_end_of_stage, 
  d.score(special_strategy), 
  swap_step = 2, 
  library_swap_prob = 1,
  reduce_interval = 100000,
  iteration = 10000000000000)