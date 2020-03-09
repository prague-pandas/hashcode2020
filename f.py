from sa import library_scanning_strategy, simulated_annealing, file_dict

f = library_scanning_strategy.from_file(file_dict['f'])

# sort it
sorted_strategy = f.generate_sorted_strategy()
print("Sort Library: {}".format(f.score(sorted_strategy)))
special_strategy = f.sort_books_by_score(sorted_strategy)
print("Remove redundancy: {}".format(f.score(special_strategy)))
strategy_at_end_of_stage = special_strategy
strategy_at_end_of_stage, score_history = simulated_annealing(
  f, 
  strategy_at_end_of_stage, 
  f.score(special_strategy), 
  swap_step = 10, 
  library_swap_prob = 1,
  reduce_interval = 500,
  iteration = 1000000)