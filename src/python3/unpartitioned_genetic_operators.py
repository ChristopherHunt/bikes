#!/usr/bin/python3

import copy
import random

from genetic_operator_base import GeneticOperatorBase

class UnpartitionedGeneticOperators(GeneticOperatorBase):
  'Implementation of the unpartitioned genetic operators.'

  def __init__(self, pop_size):
    GeneticOperatorBase.__init__(self, pop_size)

  ## This operator selects the top 'selection_count' individuals from the
  ## ranked_pop, removing them from that dictionary and adding them to the
  ## new_pop dictionary.
  def selection(self, ranked_pop, new_pop, selection_count):
    count = 0
    for key in sorted(ranked_pop.keys()):
      if selection_count == count:
        break
      new_pop.append(copy.deepcopy(ranked_pop.pop(key, None)))
      count += 1

  def cross_over(self, old_pop, new_pop, bike_params, num_traits, cross_over_count):
    traits = bike_params.keys()

    trait_count = 0
    cross_over_traits = []

    ## Create the traits list to cross_over with
    while trait_count < num_traits:
      trait = random.choice(list(traits))
      ## Ensure all the traits are unique
      if trait not in cross_over_traits and len(cross_over_traits) < len(traits):
        cross_over_traits.append(trait)
        trait_count += 1
    
    ## Create children via cross_over
    for count in range(0, cross_over_count):
      ## Get the two parents
      first_parent = random.choice(old_pop)
      second_parent = random.choice(old_pop)

      ## Create the child from the second parent
      child = copy.deepcopy(second_parent)

      ## Cross over traits from the other parent to the child
      for trait in cross_over_traits:
        ## The child here should have a mapping of trait --> index of param
        child[trait] = first_parent[trait]

      ## Add the child to the new population
      new_pop.append(copy.deepcopy(child))

  def mutate(self, old_pop, new_pop, bike_params, num_traits, mutation_count):
    traits = bike_params.keys()

    trait_count = 0
    mutation_traits = []

    ## Create the traits list to cross_over with
    while trait_count < num_traits:
      trait = random.choice(list(traits))
      ## Ensure all the traits are unique
      if trait not in mutation_traits and len(mutation_traits) < len(traits):
        mutation_traits.append(trait)
        trait_count += 1
    
    for count in range(0, mutation_count):
      ## Get random parent from the population
      parent = random.choice(old_pop)

      ## Create the child from the parent
      child = copy.deepcopy(parent)

      ## Mutate the specified traits
      for trait in mutation_traits:
        ## The child here should have a mapping of trait --> index of param
        child[trait] = random.choice(range(0, len(bike_params[trait])))

      ## Add the child to the new population
      new_pop.append(copy.deepcopy(child))

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
