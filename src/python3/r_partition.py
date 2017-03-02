#!/usr/bin/python3

import copy
import math
from r_partition_base import RPartitionBase

class RPartition(RPartitionBase):
  'Class to implement the RPartition algorithm. Note that this implementation \
   uses Euclidean distance to compute the distance between different data \
   points, & uses the average data_points score as the partition threshold.'

  def __init__(self):
    RPartitionBase.__init__(self)

  ## Parses data_points (which is a mapping of {score --> {attributes}}, and
  ## creates a new dictionary of {score --> {attribute}} which contains members
  ## of the input data_points that are within the specified partition_radius from
  ## the partition_seed_score. Note that this method computes the distance between
  ## points using the Euclidean distance, and only computes this distance using
  ## the attributes specified in the partition_attributes parameter.
  ## Returns the resulting dictionary (the partition) to the caller.
  def _build_partition_around_seed(self, data_points, partition_seed_score,
                                 partition_attributes, partition_radius):
    ## The partition to fill and return to the caller.
    partition = {}

    ## Begin by getting the seed point for the partition.
    partition_seed_point = data_points[partition_seed_score]

    ## Iterate over all data_points, comparing the distance between each point
    ## and the partition's seed point.
    for score, point in data_points.items():
      distance = self._compute_euclidean_distance(point,
                                                  partition_seed_point,
                                                  partition_attributes)
      ## If the distance is low enough, include this point in the new partition.
      if distance <= partition_radius:
        partition[score] = point

    return partition

  ## Computes the average score from the input list of scores, returning that
  ## value to the caller.
  def _compute_average_score(self, scores, threshold_factor):
    average_score = 0.0
    for score in scores:
      if score < float('inf'):
        average_score += score
    return average_score * threshold_factor

  ## Computes the Euclidean distance between point_a and point_b based soley
  ## around the distance between the attributes_to_compare. Returns this
  ## distance to the caller.
  def _compute_euclidean_distance(self, point_a, point_b, attributes_to_compare):
    summation = 0.0
    for attribute in attributes_to_compare:
      summation += (point_a[attribute] - point_b[attribute]) *\
                   (point_a[attribute] - point_b[attribute])
    return math.sqrt(summation)

  ## Scans scores, creating and returning a list of scores to the caller, where
  ##  the entries all have a score greater than or equal to the threshold (if
  ## min_max == 'max'), or less than or equal to the threshold (if
  ## min_max == 'min'). If min_max is not 'min' or 'max', an exception is raisd.
  def _compute_ordered_candidate_scores(self, scores, threshold, min_max):
    if min_max == 'min':
      scores = self._compute_ordered_list_below_threshold(scores, threshold)    
      return scores
    elif min_max == 'max':
      return self._compute_ordered_list_above_threshold(scores, threshold)    
    else:
      raise AttributeError('min_max must be \'min\' or \'max\'.')

  ## Scans scores, creating and returning a list of scores to the caller, where
  ## the entries all have a score greater than or equal to the threshold.
  def _compute_ordered_list_above_threshold(self, scores, threshold):
    outputs = []
    for score in scores:
      if score >= threshold:
        outputs.append(score)
    sorted(outputs).reverse()
    return outputs

  ## Scans scores, creating and returning a list of scores to the caller, where
  ## the entries all have a score less than or equal to the threshold.
  def _compute_ordered_list_below_threshold(self, scores, threshold):
    outputs = []
    for score in scores:
      if score <= threshold:
        outputs.append(score)
    sorted(outputs)
    return outputs

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
  def partition(self, data_points, partition_attributes, partition_radius, min_max, threshold_factor=0.50):
    ## List of scores for the input data_points.
    scores = data_points.keys()

    ## Compute the average score of the input data points to act as the
    ## threshold (the cutoff to stop partitioning).
    threshold = self._compute_average_score(scores, threshold_factor)

    ## Compute a list of ordered candidate scores, where each score in the list
    ## is ordered based on the value of min_max, and only scores that fall to
    ## the correct side of the threshold are included.
    ordered_candidate_scores = self._compute_ordered_candidate_scores(scores,
                                                                threshold,
                                                                min_max)
    ## Resultant partitions to output.
    partitions = []

    ## While there are still candidates to partition, partition.
    while ordered_candidate_scores:
      ## Get the next score to investiage.
      partition_seed_score = ordered_candidate_scores.pop(0)

      ## Build the partition around the seed_score.
      partition = self._build_partition_around_seed(data_points,
                                                partition_seed_score,
                                                partition_attributes,
                                                partition_radius)

      ## Remove any candidates from the ordered_candidate_scores list if they
      ## were included in the most recent partition. This prevents us from
      ## partitioning on points that have already been "consumed" by another
      ## partition.
      ordered_candidate_scores = [score for score in ordered_candidate_scores if score not in partition.keys()]

      ## Add this partition to the list of partitions.
      partitions.append(partition)

    return partitions

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
