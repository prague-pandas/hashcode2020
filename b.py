from sa import library_scanning_strategy, simulated_annealing, file_dict

b = library_scanning_strategy.from_file(file_dict['b'])

# sort it
sorted_strategy = b.generate_sorted_strategy()
print("Sort Library: {}".format(b.score(sorted_strategy)))
special_strategy = b.sort_books_by_score(sorted_strategy)
print("Remove redundancy: {}".format(b.score(special_strategy)))
strategy_at_end_of_stage = special_strategy
strategy_at_end_of_stage, score_history = simulated_annealing(
  b, 
  strategy_at_end_of_stage, 
  b.score(special_strategy)/10, 
  objective_fn='score', 
  swap_step = 2, 
  library_swap_prob = 1,
  iteration = 1000000)