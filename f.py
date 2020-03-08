from sa import library_scanning_strategy, simulated_annealing, file_dict

f = library_scanning_strategy.from_file(file_dict['f'])

# sort it
sorted_strategy = f.generate_sorted_strategy()
print("Sort Library: {}".format(f.score(sorted_strategy)))
special_strategy = f.remove_redundancy_and_sort_by_score(sorted_strategy)
print("Remove redundancy: {}".format(f.score(special_strategy)))
strategy_at_end_of_stage = special_strategy
for i in range(100):
  strategy_at_end_of_stage, score_history = simulated_annealing(
    f, 
    strategy_at_end_of_stage, 
    400000, 
    objective_fn='score', 
    swap_step = 1, 
    library_swap_prob = 1,
    sort_book_at_end = False,
    iteration=10000,
    plot=False)
  strategy_at_end_of_stage = f.remove_redundancy_and_sort_by_score(strategy_at_end_of_stage)
  final_score_at_end_of_stage = f.score(strategy_at_end_of_stage)
  print("Score at stage {}: {} ".format(i, final_score_at_end_of_stage))
  f.output_strategy('output/outputf_{}.txt'.format(final_score_at_end_of_stage), strategy_at_end_of_stage)