#!/usr/bin/python3

import copy
import sys
import time

from bike import Bike
from config_parser import Parser
from partitioned_genetic_search import PartitionedGeneticSearch
from simulation_params import SimulationParams
from unpartitioned_genetic_search import UnpartitionedGeneticSearch

## Class to sample a given search space, looking for the optimum parameter set
## that produces the results with the lowest overall error.
class SamplingTuner():

  def __init__(self, simulation_params, output_filename, ga_log_filename,\
               ga_platform, sampling_attributes):
    self._simulation_params = copy.deepcopy(simulation_params)
    self._output_filename = output_filename
    self._ga_log_filename = ga_log_filename
    self._ga_platform = ga_platform
    self._sampling_attributes = copy.deepcopy(sampling_attributes)

    ## Set the sample count here arbitrarily
    self._simulation_params.sample_count = 25

  def _build_square(self, num_attributes):
    ga_config = self._simulation_params.ga_config
    square = None
    if num_attributes == 3:
      square = self._build_3_attribute_square(self._sampling_attributes, ga_config)
    elif num_attributes == 4:
      square = self._build_4_attribute_square(self._sampling_attributes, ga_config)
    else:
      square = self._build_5_attribute_square(self._sampling_attributes, ga_config)
    return square

  def _build_3_attribute_square(self, sampling_attributes, ga_config):
    square = [[0, 0, 0], [1, 0, 1], [2, 0, 2], [3, 0, 3], [4, 0, 4],
              [0, 1, 1], [1, 1, 2], [2, 1, 3], [3, 1, 4], [4, 1, 0],
              [0, 2, 2], [1, 2, 3], [2, 2, 4], [3, 2, 0], [4, 2, 1],
              [0, 3, 3], [1, 3, 4], [2, 3, 0], [3, 3, 1], [4, 3, 2],
              [0, 4, 4], [1, 4, 0], [2, 4, 1], [3, 4, 2], [4, 4, 3]]
    return square

  def _build_4_attribute_square(self, sampling_attributes, ga_config):
    square = [[0, 0, 0, 0], [1, 0, 1, 3], [2, 0, 2, 1], [3, 0, 3, 4], [4, 0, 4, 2],
              [0, 1, 1, 1], [1, 1, 2, 4], [2, 1, 3, 2], [3, 1, 4, 1], [4, 1, 0, 3],
              [0, 2, 2, 2], [1, 2, 3, 0], [2, 2, 4, 3], [3, 2, 0, 2], [4, 2, 1, 4],
              [0, 3, 3, 3], [1, 3, 4, 1], [2, 3, 0, 4], [3, 3, 1, 3], [4, 3, 2, 0],
              [0, 4, 4, 4], [1, 4, 0, 2], [2, 4, 1, 0], [3, 4, 2, 4], [4, 4, 3, 1]]
    return square

  def _build_5_attribute_square(self, sampling_attributes, ga_config):
    square = [[0, 0, 0, 0, 0], [1, 0, 1, 1, 1], [2, 0, 2, 2, 2], [3, 0, 3, 3, 3], [4, 0, 4, 4, 4],
              [0, 1, 1, 2, 3], [1, 1, 2, 3, 4], [2, 1, 3, 4, 0], [3, 1, 4, 0, 1], [4, 1, 0, 1, 2],
              [0, 2, 2, 4, 1], [1, 2, 3, 0, 2], [2, 2, 4, 1, 3], [3, 2, 0, 2, 4], [4, 2, 1, 3, 0],
              [0, 3, 3, 1, 4], [1, 3, 4, 2, 0], [2, 3, 0, 3, 1], [3, 3, 1, 4, 2], [4, 3, 2, 0, 3],
              [0, 4, 4, 3, 2], [1, 4, 0, 4, 3], [2, 4, 1, 0, 4], [3, 4, 2, 1, 0], [4, 4, 3, 2, 1]]
    return square

  ## Returns a dictionary of {attribute -> [{value, error}]}, that is a
  ## dictionary of attributes names to a list of attribute value to error
  ## tuples.
  def _run_square(self, square, sampling_attributes, ga_config):
    ## Grab all the attribute values.
    attribute_lists = []
    attribute_results = {}
    for attribute in sampling_attributes:
      attribute_lists.append(copy.deepcopy(ga_config[attribute]))
      attribute_results[attribute] = {}

    ## Build a search algorithm object. 
    ga_search = None
    if self._ga_platform == 'unpartitioned':
      print('running unpartitioned')
      ga_search = UnpartitionedGeneticSearch()
    else:
      print('running partitioned')
      ga_search = PartitionedGeneticSearch()

    simulation_params = copy.deepcopy(self._simulation_params)

    ## For every cell in the square.
    for entry in square:
      ## Build the ga_config for each run.
      for index in range(0, len(entry)):
        attribute_name = sampling_attributes[index]
        attribute_value = ga_config[attribute_name][entry[index]] 
        simulation_params.ga_config[attribute_name] = [attribute_value]

      print('gen_count: ' + str(simulation_params.ga_config['generation_count']))
      print('pop_size: ' + str(simulation_params.ga_config['population_size']))

      ## Run the genetic search with this cell's ga_config.
      search_results = ga_search.run(simulation_params, self._ga_log_filename)

      ## If unpartitioned, then the results are a dictionary of
      ## {error -> bike_params}.
      if self._ga_platform == 'unpartitioned':
        min_error = sorted(search_results.keys())[0]

      ## If partitioned, then the results are a list of dictionaries of
      ## {error -> bike_params}.
      else:
        min_error = float('inf')
        for partition in search_results:
          partition_error = sorted(partition.keys())[0]
          if min_error > partition_error:
            min_error == partition_error

      ## Populate the output results for each attribute name and value in this
      ## cell.
      for index in range(0, len(entry)):
        attribute_name = sampling_attributes[index]
        attribute_value = ga_config[attribute_name][entry[index]] 

        ## Add a placeholder here for the output results.
        if attribute_value not in attribute_results[attribute_name]:
          attribute_results[attribute_name][attribute_value] = {}
          attribute_results[attribute_name][attribute_value]['min_error'] = min_error
          attribute_results[attribute_name][attribute_value]['max_error'] = min_error
          attribute_results[attribute_name][attribute_value]['avg_error'] = (min_error / 5)

        else:
          dictionary = attribute_results[attribute_name][attribute_value]
          dictionary['avg_error'] += (min_error / 5)

          if dictionary['min_error'] > min_error:
            dictionary['min_error'] = min_error
          if dictionary['max_error'] < min_error:
            dictionary['max_error'] = min_error

    return attribute_results

  ## Does a quick sampling of the design space using the appropriate
  ## Greaco-Latin square.
  ## Returns a dictionary of {attribute -> [{value, error}]}, that is a
  ## dictionary of attributes names to a list of attribute value to error
  ## tuples.
  def sample(self):
    ga_config = self._simulation_params.ga_config
    sampling_attributes = self._sampling_attributes

    ## Ensure that the proper number of attributes was specified.
    num_attributes = len(sampling_attributes)
    if num_attributes < 3 or num_attributes > 5:
      raise Exception('Must specifiy between 3 and 5 attributes to sample.')

    ## Ensure that all of the attributes have 5 values.
    for attribute in sampling_attributes:
      if attribute not in ga_config.keys():
        raise Exception('All sampling parameters must be present in ga_config.')

      if len(ga_config[attribute]) != 5:
        raise Exception('All sampling parameters must have the same number of values.')

    ## Build the Greaco-Latin square.
    square = self._build_square(len(sampling_attributes))

    ## Run the experiments in the square.
    return self._run_square(square, sampling_attributes, ga_config)

  def tune(self):
    pass

## Parses the inputs for the sampling tuner, returning them as a tuple of
## simulation_params, output_filename, ga_log_filename, ga_platform.
def parse_inputs(command_line_args):
  num_command_line_args = len(command_line_args)
  if num_command_line_args < 8 or num_command_line_args > 10:
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

  ## Grab the ga_platform name.
  ga_platform = sys.argv[3]

  ## Ensure that the name is either 'unpartitioned' or 'partitioned'.
  if ga_platform != 'unpartitioned' and ga_platform != 'partitioned':
    raise Exception('ga_platform must be set to partitioned or unpartitioned')

  ## Next, ensure that the proper number of arguements were supplied for the
  ## given run. Specifically, if this is for a partitioned run then there needs
  ## to be a partitioned config present, if not then the partitioned config
  ## should not be present.
  if ga_platform == 'unpartitioned' and num_command_line_args != 8:
    raise Exception('improper number of arguements for unpartitioned sampling')

  if ga_platform == 'partitioned' and num_command_line_args != 9:
    raise Exception('improper number of arguements for partitioned sampling')

  ## Grab the name of the genetic algorithm's config file.
  ga_config_filename = sys.argv[4]

  ## Grab the name of the target_control_sensitivity curve file.
  curve_filename = sys.argv[5]

  ## Grab the name of the bike_params file.
  bike_params_filename = sys.argv[6]

  ## Grab rider config filename.
  rider_config_filename = sys.argv[7]

  ## Parse the genetic algorithm config file.
  parser.parse_genetic_algorithm_config_file(simulation_params.ga_config,
                                             ga_config_filename)

  if ga_platform == 'partitioned':
    ## Grab the name of the partitioning config file.
    partitioning_config_filename = sys.argv[8]

    ## Parse the partitioning config file.
    partitioning_config = {}
    parser.parse_partitioning_config_file(partitioning_config,
                                          partitioning_config_filename)

    ## Add the partitioning config components to the simulation_params object.
    simulation_params.partitioning_radius = partitioning_config['radius'][0]
    simulation_params.partitioning_attributes = copy.deepcopy(partitioning_config['attributes'])

  ## Parse the target control sensitivity curve from the input.
  parser.parse_curve_file(simulation_params.target_control_sensitivity,
                          curve_filename) 

  ## Parse in the bike_params, resulting in a dictionary of {param -> [values]}.
  parser.parse_bike(simulation_params.bike_params, bike_params_filename)

  ## Parse in the rider_params, resulting in a list of [{param -> [values]}].
  parser.parse_riders(simulation_params.riders, rider_config_filename)

  ## Compute the top speed to test all bikes at given the input curve.
  simulation_params.top_speed = len(simulation_params.target_control_sensitivity)

  return simulation_params, output_filename, ga_log_filename, ga_platform

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 sampling_tuner.py <output_filename> <ga_log_filename>'
          ' <ga_platform> <ga_config_file.txt> <partitioning_config.txt>'
          ' <target_control_sensitivity.txt> <bike_params.txt> <rider_params>\n'
          '|  output_filename = the file to write the results to\n'
          '|  ga_log_filename = the name of the output file to dump GA results to\n'
          '|  ga_platform = [unpartitioned, partitioned] -- the search platform to sample\n'
          '|  ga_config_file.txt = the GA configuration file for this run\n'
          '|  target_control_sensitivity.txt = a sensitivity curve that this '
                                              'model is trying to build towards\n'
          '|  bike_params.txt = a file containing all the bike params\n'
          '|  rider_params.txt = one or more files containing rider params\n'
          '|  partitioning_config.txt = the config file describing the '
                                        'partitioning parameter values.\n')

def main():
  try:
    ## Parse the input.
    simulation_params, output_filename, ga_log_filename, ga_platform =\
       parse_inputs(sys.argv)

    ## Set the sampling attributes here to make things easy for now.
    sampling_attributes = ['generation_count', 'population_size',
                           'selection_percentage', 'mutation_percentage',\
                           'cross_over_percentage']

    ## Create a SamplingTuner object.
    tuner = SamplingTuner(simulation_params, output_filename, ga_log_filename,
                          ga_platform, sampling_attributes)

    ## Sample the design space.
    start_time = time.time()
    attribute_results = tuner.sample()
    end_time = time.time()
    print('Total sampling time: ' + str(end_time - start_time))
    print(attribute_results)

    ## tune the design space based on that sampling.
    tuner.tune()

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
