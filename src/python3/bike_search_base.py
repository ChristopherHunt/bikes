#!/usr/bin/python3

from simulation_params import SimulationParams

class BikeSearchBase:
  'Interface for bicycle design search algorithms.'

  def __init__(self):
    pass

  ## Runs a bicycle simulation given the set of simulation parameters,
  ## copying the top bike's bike_params into the "best_bikes" out parameters.
  def run(self, simulation_params, best_bikes):
    raise NotImplementedError('Run function was not defined by subclass.')

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
