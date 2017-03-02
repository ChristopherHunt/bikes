#!/usr/bin/python3

import copy
import random

from genetic_operator_base import GeneticOperatorBase

class PartitionedGeneticOperators(GeneticOperatorBase):
  'Implementation of genetic operators that support partitioning during selection.'

  def __init__(self, pop_size):
    GeneticOperatorBase.__init__(self, pop_size)

  ## partitions = a list of dictionaries of score --> array of bike param indexes
  ## new_pop = a list of 
  def selection(self, partitions, new_pop, selection_count):
    count = 0

    num_partitions = len(partitions)
    partition_index = 0

    for count in range(0, selection_count):
      if partition_index >= num_partitions:
        partition_index = 0

      current_partition = partitions[partition_index]
      if len(current_partition) > 0:
        key = sorted(current_partition.keys())[0]
        new_pop.append(current_partition.pop(key, None))
        count += 1

      partition_index += 1

  def cross_over(self, old_pop, new_pop, bike_params, num_attributes, cross_over_count):
    attributes = bike_params.keys()

    attribute_count = 0
    cross_over_attributes = []

    ## Create the attributes list to cross_over with
    while attribute_count < num_attributes:
      attribute = random.choice(list(attributes))
      ## Ensure all the attributes are unique
      if attribute not in cross_over_attributes and len(cross_over_attributes) < len(attributes):
        cross_over_attributes.append(attribute)
        attribute_count += 1
    
    ## Create children via cross_over
    for count in range(0, cross_over_count):
      ## Get the two parents
      first_parent = random.choice(old_pop)
      second_parent = random.choice(old_pop)

      ## Create the child from the second parent
      child = copy.deepcopy(second_parent)

      ## Cross over attributes from the other parent to the child
      for attribute in cross_over_attributes:
        ## The child here should have a mapping of attribute --> index of param
        child[attribute] = first_parent[attribute]

      ## Add the child to the new population
      new_pop.append(copy.deepcopy(child))

  def mutate(self, old_pop, new_pop, bike_params, num_attributes, mutation_count):
    attributes = bike_params.keys()

    attribute_count = 0
    mutation_attributes = []

    ## Create the attributes list to cross_over with
    while attribute_count < num_attributes:
      attribute = random.choice(list(attributes))
      ## Ensure all the attributes are unique
      if attribute not in mutation_attributes and len(mutation_attributes) < len(attributes):
        mutation_attributes.append(attribute)
        attribute_count += 1
    
    for count in range(0, mutation_count):
      ## Get random parent from the population
      parent = random.choice(old_pop)

      ## Create the child from the parent
      child = copy.deepcopy(parent)

      ## Mutate the specified attributes
      for attribute in mutation_attributes:
        ## The child here should have a mapping of attribute --> index of param
        child[attribute] = random.choice(range(0, len(bike_params[attribute])))

      ## Add the child to the new population
      new_pop.append(copy.deepcopy(child))

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
