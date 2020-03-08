from sa import library_scanning_strategy, simulated_annealing, file_dict

d = library_scanning_strategy.from_file(file_dict['d'])

# sort it
sorted_strategy = d.generate_sorted_strategy()
print("Sort Library: {}".format(d.score(sorted_strategy)))
special_strategy = d.remove_redundancy_and_sort_by_score(sorted_strategy)
print("Remove redundancy: {}".format(d.score(special_strategy)))
strategy_at_end_of_stage = special_strategy
for i in range(100):
  strategy_at_end_of_stage, score_history = simulated_annealing(
    d, 
    strategy_at_end_of_stage, 
    400000, 
    objective_fn='score', 
    swap_step = 1, 
    library_swap_prob = 1,
    sort_book_at_end = False,
    iteration=10000,
    plot=False)
  strategy_at_end_of_stage = d.remove_redundancy_and_sort_by_score(strategy_at_end_of_stage)
  final_score_at_end_of_stage = d.score(strategy_at_end_of_stage)
  print("Score at stage {}: {} ".format(i, final_score_at_end_of_stage))
  d.output_strategy('output/outputd_{}.txt'.format(final_score_at_end_of_stage), strategy_at_end_of_stage)