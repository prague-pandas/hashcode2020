from sa import library_scanning_strategy, simulated_annealing, file_dict

c = library_scanning_strategy.from_file(file_dict['c'])

# sort it
sorted_strategy = c.generate_sorted_strategy()
print("Sort Library: {}".format(c.score(sorted_strategy)))
special_strategy = c.sort_books_by_score(sorted_strategy)
print("Remove redundancy: {}".format(c.score(special_strategy)))
strategy_at_end_of_stage = special_strategy
strategy_at_end_of_stage, score_history = simulated_annealing(
  c, 
  strategy_at_end_of_stage, 
  c.score(special_strategy), 
  objective_fn='score', 
  swap_step = 2, 
  library_swap_prob = 1,
  iteration = 1000000)