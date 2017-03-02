#!/usr/bin/python3

import copy
import json
import random
import sys
import time

from bike import Bike
from bike_search_base import BikeSearchBase
from config_parser import Parser
from simulation_params import SimulationParams
from unpartitioned_genetic_operators import UnpartitionedGeneticOperators

class UnpartitionedGeneticSearch(BikeSearchBase):
  'Class to implement unpartitioned genetic algorithm bike search.'

  def __init__(self):
    self._simulation_params = {}
    self._ga_log_filename = ''

  ## Runs a genetic algorithm simulation given the specified parameters and
  ## returns the set containing the best bikes.
  def run(self, simulation_params, ga_log_filename):
    self._simulation_params = copy.deepcopy(simulation_params)
    self._ga_log_filename = ga_log_filename
    return self._run_full_simulation()

## Appends the follow header contents to the output_string:
##
##  ---
##  num_runs = #
##  selection_percentage = #
##  cross_over_percentage = #
##  mutation_percentage = #
##  cross_over_gene_count = #
##  mutation_gene_count = #
##  Run Data [gen_count, pop_size, error, runtime]'
  def _add_ga_config_header(self, current_ga_config, num_runs):
    output_string = '---\n'
    output_string += 'num_runs = ' + str(num_runs) + '\n'
    output_string += 'selection_percentage = ' +\
                     str(current_ga_config['selection_percentage']) + '\n'
    output_string += 'cross_over_percentage = ' +\
                     str(current_ga_config['cross_over_percentage']) + '\n'
    output_string += 'mutation_percentage = ' +\
                     str(current_ga_config['mutation_percentage']) + '\n'
    output_string += 'cross_over_gene_count = ' +\
                     str(current_ga_config['cross_over_gene_count']) + '\n'
    output_string += 'mutation_gene_count = ' +\
                     str(current_ga_config['mutation_gene_count']) + '\n'
    output_string += 'Run Data [gen_count, pop_size, error, runtime]\n'
    return output_string

  ## Adds bikes to the population which are randomly chosen from the possible
  ## bike space.
  def _add_random_bikes_to_pop(self, population, num_bikes_to_add):
    bike = Bike()

    for count in range(0, int(num_bikes_to_add)):
      ## Create a random bike and add its indexed array to the population.
      population.append(bike.generate_random_bike(self._simulation_params.bike_params))

  ## Ranks all the bikes in the unranked_bike_params_population, putting each
  ## bike_param from the population into the ranked_population as follows:
  ## 
  ##    rank --> bike_params for a single bike
  def _rank_bikes_by_score(self, unranked_bike_params_population, ranked_population):
    bike = Bike() 

    for single_bike_params_indexes in unranked_bike_params_population:
      ## Configure the bike with the current geometry.
      bike.update_geometry_from_indexes(self._simulation_params.bike_params,
                                        single_bike_params_indexes)

      ## Get the score for the bike as a whole based on the input riders.
      score = bike.compute_error(self._simulation_params.riders,
                                 self._simulation_params.target_control_sensitivity,
                                 self._simulation_params.top_speed)

      ## Add the current bike's to the old_poperation.
      ranked_population[score] = single_bike_params_indexes

  def _run_full_simulation(self):
    ## Store a copy of the ga_config for later manipulation.
    ga_config = copy.deepcopy(self._simulation_params.ga_config)

    output_string = ''
    aggregate_error = 0.0

    ## Container to hold the parameters for each GA config run.
    current_ga_config = {}

    ## Container to hold the best bike designs at the end of the run.
    best_bikes_per_run = {}

    ## The number of runs to do per configuration (to gather some sense of
    ## statistical certainty about the results).
    num_runs = int(ga_config['num_runs'][0])
    start_time = time.time()
    beginning = time.time()

    ## Open the log file once to clear it.
    ga_log_file = open(self._ga_log_filename, 'w')
    ga_log_file.close()

    for selection_percentage in ga_config['selection_percentage']:
      current_ga_config['selection_percentage'] = selection_percentage
      for cross_over_percentage in ga_config['cross_over_percentage']:
        current_ga_config['cross_over_percentage'] = cross_over_percentage
        for mutation_percentage in ga_config['mutation_percentage']:
          current_ga_config['mutation_percentage'] = mutation_percentage
          for cross_over_gene_count in ga_config['cross_over_gene_count']:
            current_ga_config['cross_over_gene_count'] = cross_over_gene_count
            for mutation_gene_count in ga_config['mutation_gene_count']:
              current_ga_config['mutation_gene_count'] = mutation_gene_count

              ## Open the log file to write the final results to.
              ga_log_file = open(self._ga_log_filename, 'a')

              ## Add the initial header to the output_string for this run.
              output_string = self._add_ga_config_header(current_ga_config,
                                                         num_runs)
              for gen_count in ga_config['generation_count']:
                current_ga_config['generation_count'] = gen_count
                for pop_size in ga_config['population_size']:
                  current_ga_config['population_size'] = pop_size

                  ## Add the current GA config to the simulation params so we can
                  ## run this test configuration.
                  self._simulation_params.ga_config = copy.deepcopy(current_ga_config)

                  ## Start timing the run.
                  start = time.time()

                  ## Reset error to 0.0 for the new trial
                  aggregate_error = 0.0
                  min_error = float('inf')
                  max_error = 0
                  for run in range(0, num_runs):
                    ## Run the simulation for the given configuration and record
                    ## the error of the best bike in each case.
                    run_error = self._run_single_simulation(self._simulation_params,
                                                            best_bikes_per_run)
                    if run_error < min_error:
                      min_error = run_error

                    if run_error > max_error:
                      max_error = run_error

                    aggregate_error += run_error

                  ## Average the error for each run
                  avg_error = aggregate_error / num_runs

                  ## Comptute the runtime for this trial
                  runtime = time.time() - start

                  ## Append that error to the output_string
                  output_string += str(gen_count) + ',' +\
                                   str(pop_size) + ',' +\
                                   str(avg_error) + ',' +\
                                   str(runtime) + '\n'

                  ## Print the output to the specified file. Do it this way to
                  ## ensure that if the trial dies part way through we still have
                  ## some data saved.
                  ga_log_file = open(self._ga_log_filename, 'a')
                  ga_log_file.write(output_string)
                  ga_log_file.close()

              print('Selection %: ' + str(selection_percentage) + ', ' +
                    'Cross Over %: ' + str(cross_over_percentage) + ', ' +
                    'Mutation %: ' + str(mutation_percentage) + ' -- ' +
                    'Runtime: ' + str(time.time() - beginning))

    ## Add final deliminter to the file for later parsing.
    output_string = '---\n'

    ## Print the output to the specfied file.
    ga_log_file = open(self._ga_log_filename, 'a')
    ga_log_file.write(output_string)
    ga_log_file.close()

    ## Extract the best ranked designs from all of the runs.
    best_bikes_overall = {}
    counter = 0
    for error in sorted(best_bikes_per_run.keys()):
      counter += 1
      if counter > self._simulation_params.sample_count:
        break

      ## Add the error -> bike_param mapping to the output dictionary.
      best_bikes_overall[error] = best_bikes_per_run[error]
  
    ## Return the top bikes from the experiments.
    return best_bikes_overall

  ## Runs the genetic algorithm simulation based on what the current member
  ## variables are for this object.
  def _run_single_simulation(self, simulation_params, best_bikes):
    ## Grab initial references.
    bike_params = simulation_params.bike_params
    ga_config = simulation_params.ga_config
    score = float('inf')

    ## Build the dictionaries to hold the old and the new bike generations.
    old_pop = []
    new_pop = []
    selected_pop = []

    ## Create a bike to act as a container for building other bikes.
    bike = Bike()

    ## Create a GA object.
    pop_size = ga_config['population_size']
    ga_operators = UnpartitionedGeneticOperators(pop_size)

    ## Populate the old_pop with a random set of of bikes.
    self._add_random_bikes_to_pop(new_pop, pop_size)

    ## Create a dictionary for ranking the populations.
    ranked_pop = {}

    ## Rank all the bikes.
    self._rank_bikes_by_score(new_pop, ranked_pop)

    ## Compute counts for each opertor
    selection_percentage = ga_config['selection_percentage']
    selection_count = int(abs(pop_size * (selection_percentage / 100.0)))
    cross_over_percentage = ga_config['cross_over_percentage']
    cross_over_count = int(abs(pop_size * (cross_over_percentage / 100.0)))
    mutation_percentage = ga_config['mutation_percentage']
    mutation_count = int(abs(pop_size * (mutation_percentage / 100.0)))
    random_selection_count = pop_size - selection_count - cross_over_count - mutation_count
    gen_count = int(ga_config['generation_count'])

    ## For each generation
    for gen in range(0, int(ga_config['generation_count'])):
      ## Update the old population to be the previous one.
      new_pop.clear()
      selected_pop.clear()

      ## Perform selection
      ga_operators.selection(ranked_pop, selected_pop, selection_count)

      ## Error if too many individuals exist.
      if random_selection_count < 0:
        print('Cannot have more individuals than the specified population size.')
        sys.exit(1)

      ## Perform random selection if needed.
      if random_selection_count > 0:
        self._select_random_individuals_from_pop(ranked_pop, selected_pop,
                                                 random_selection_count)

      ## Now add the selected individuals to the new population, while keeping
      ## the selected designs separate so they can be used in the other genetic
      ## operations.
      new_pop = copy.deepcopy(selected_pop)

      ## Perform cross_over
      ga_operators.cross_over(selected_pop,
                              new_pop,
                              bike_params,
                              ga_config['cross_over_gene_count'],
                              cross_over_count)

      ## Perform mutation
      ga_operators.mutate(selected_pop,
                          new_pop,
                          bike_params,
                          ga_config['mutation_gene_count'],
                          mutation_count)

      ## Rank all the bikes in the new population.
      ranked_pop.clear()
      self._rank_bikes_by_score(new_pop, ranked_pop)

    ## Copy the final list of bike params into the caller's out dictionary, with
    ## a mapping of each bike_param's error -> bike_param.
    counter = 0
    for error in sorted(ranked_pop.keys()):
      counter += 1
      if counter > self._simulation_params.sample_count:
        break

      ## Add the error -> bike_param mapping to the output dictionary.
      best_bikes[error] =\
         bike.convert_bike_params_from_indexes(bike_params,
                                               ranked_pop[error])

    ## Return the score of the best bike.
    score = sorted(ranked_pop.keys())[0]
    return float(score)

  def _select_random_individuals_from_pop(self, old_pop, new_pop, count):
    while old_pop and count > 0:
      key = random.choice(list(old_pop.keys()))
      new_pop.append(old_pop[key])
      del old_pop[key]
      count -= 1

    self._add_random_bikes_to_pop(new_pop, count)

def parse_inputs(command_line_args):
  if len(command_line_args) < 8:
    print_usage()
    raise Exception()

  ## Create a SimulationParams object to hold all the parsed input data.
  simulation_params = SimulationParams()

  ## Create a Parser to parse the input files.
  parser = Parser()

  ## Grab the output filename.
  output_filename = sys.argv[1]

  ## Grab the name of the output file.
  ga_log_filename = sys.argv[2]

  ## Grab the name of the genetic algorithm's config file.
  ga_config_filename = sys.argv[3]

  ## Grab the sample count from the input.
  simulation_params.sample_count = int(sys.argv[4])

  ## Grab the name of the target_control_sensitivity curve file.
  curve_filename = sys.argv[5]

  ## Grab the name of the bike_params file.
  bike_params_filename = sys.argv[6]

  ## Grab rider config filename.
  rider_config_filename = sys.argv[7]

  ## Parse the genetic algorithm config file.
  if not parser.parse_genetic_algorithm_config_file(simulation_params.ga_config,
                                                    ga_config_filename):
    raise Exception()

  ## Parse the target control sensitivity curve from the input.
  if not parser.parse_curve_file(simulation_params.target_control_sensitivity,
                                curve_filename):
    raise Exception()

  ## Parse in the bike_params, resulting in a dictionary of {param -> [values]}.
  if not parser.parse_bike(simulation_params.bike_params, bike_params_filename):
    raise Exception()

  ## Parse in the rider_params, resulting in a list of [{param -> [values]}].
  if not parser.parse_riders(simulation_params.riders, rider_config_filename):
    raise Exception()

  ## Compute the top speed for testing bikes to.
  simulation_params.top_speed = len(simulation_params.target_control_sensitivity)

  return simulation_params, output_filename, ga_log_filename

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 unpartitioned_genetic_search.py <output_filename>'
          ' <ga_log_filename> <ga_config_file.txt> <sample_count>'
          ' <target_control_sensitivity.txt> <bike_params.txt>  <rider_params>\n'
          '|  output_filename = the file to write the results to\n'
          '|  ga_log_filename = the name of the output file to dump GA results to\n'
          '|  ga_config_file.txt = the GA configuration file for this run\n'
          '|  sample_count = the number optimum bike samples to output\n'
          '|  target_control_sensitivity.txt = a sensitivity curve that this '
                                              'model is trying to build towards\n'
          '|  bike_params.txt = a file containing all the bike params\n'
          '|  rider_params.txt = one or more files containing rider params\n')

def main():
  try:
    ## Parse the command line argumements.
    simulation_params, output_filename, ga_log_filename  = parse_inputs(sys.argv)

    ## Build the simulation object.
    ga_search = UnpartitionedGeneticSearch()

    ## Run the simulation and get back the resulting partitions.
    start_time = time.time()
    best_bikes_overall = ga_search.run(simulation_params, ga_log_filename)
    end_time = time.time()
    print('Total time: ' + str(end_time - start_time))

    ## Write the top bikes to an output file.
    try:
      with open(output_filename, 'w') as output:
        ## Write all the top bikes to disk.
        output.write(json.dumps(best_bikes_overall))
    except IOError:
      print('Could not open ' + str(output_filename) + ' for writing.')
      sys.exit(1)

  except BaseException as e:
    print(str(e))

if __name__ == '__main__':
    main()

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
