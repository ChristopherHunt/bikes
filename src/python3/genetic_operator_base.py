#!/usr/bin/python3

class GeneticOperatorBase(object):
  'Interface for all genetic operator implementations to extend.'

  ## The pop_size is the number of individuals in a given generation for the
  ## genetic algorithm implementation.
  def __init__(self, pop_size):
    self.pop_size = pop_size

  ## Selects the members of the old_poperation (represented as a list of
  ## single_bike_params (dictionaries of param -> value)) to be copied into the
  ## new_poperation. Percentage refers to the percent of the old_pop to be
  ## selected to form the base for the new gen.
  def selection(self, ranked_pop, new_pop, percentage):
    raise NotImplementedError('selection operation was not defined by subclass.')

  ## Selects the members of the old_poperation (represented as a list of
  ## single_bike_params (dictionaries of param -> value)) to be crossed_over
  ## with members from the new_population. Percentage refers to the percent of
  ## the old_population to be selected to cross_over, and num_traits specifies
  ## the number of traits to cross_over using.
  def cross_over(self, old_pop, new_pop, bike_params, num_traits, percentage):
    raise NotImplementedError('cross_over operation was not defined by subclass.')

  ## Selects the members of the old_poperation (represented as a list of
  ## single_bike_params (dictionaries of param -> value)) to be mutated
  ## and placed in the new_population. Percentage refers to the percent of
  ## the old_population to be selected to mutate, and num_traits specifies
  ## the number of traits to mutate.
  def mutate(self, old_pop, new_pop,  bike_params, num_traits, percentage):
    raise NotImplementedError('mutate operation was not defined by subclass.')

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
