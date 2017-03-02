#!/usr/bin/python3

class RPartitionBase(object):
  'Class to define the interface for implementations of this partitioning algorithm.'

  def __init__(self):
    pass

  ## Performs the partitioning of inputs based on the specified partition_attributes
  ## as well as the partition_radius. The input data_points are expected to be a
  ## mapping of {score --> {attributes}}, where the score is a decimal number
  ## and the attributes are a dictionary of attribute --> value. Additionally,
  ## the min_max parameter specifies if the partitioning algorithm should try to
  ## partition about minima or maxima in the input data_points. For minima, set
  ## min_max = 'min', and for maxima set min_max = 'max'.
  ## 
  ## Outputs a list of partitions, where each partition contains the data_points
  ## that are within partition_radius distance from one another.
  def partition(self, data_points, partition_attributes, partition_radius, min_max):
    raise NotImplementedError('partition operation was not defined by subclass.')

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
