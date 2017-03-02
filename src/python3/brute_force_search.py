#!/usr/bin/python3

import copy
import sys
import time

from bike import Bike
from bike_search_base import BikeSearchBase
from config_parser import Parser
from simulation_params import SimulationParams

class BruteForceSearch(BikeSearchBase):
  'Implements a brute force search to find the optimimal bike design.'

  def __init__(self):
    pass

  def run(self, simulation_params, best_bikes):

    ## Grab the top speed from the input.
    top_speed = simulation_params.top_speed

    ## Grab the target control sensitivity curve from the input.
    target_control_sensitivity = simulation_params.target_control_sensitivity

    ## Read in the bike_params, resulting in a dictionary of {param -> [values]}.
    bike_params = simulation_params.bike_params

    ## Read in the rider_params, resulting in a list of [{param -> [values]}].
    riders = simulation_params.riders

    ## Create a Bike object to hold all bike_params in the following iterations.
    bike = Bike()

    ## Create a Bike object to hold the best bike configuration.
    best_bike = Bike()

    ## Container to represent the bike parameter set to build and test each bike
    ## from.
    current_bike_params = {}

    ## List of the top bike params to print to the output file.
    best_bike_params = []

    ## Initialize the min_error to be infinity to start.
    min_error = float('inf')

    ## Lists to hold the control spring and control sensitivity values in the
    ## following iterations.
    control_spring = []
    control_sensitivity = []

    counter = 0

    start_time = time.time()
    checkpoint = start_time
    for wheelbase in bike_params['wheelbase']:
     current_bike_params['wheelbase'] = wheelbase
     for hip_angle in bike_params['hip_angle']:
      current_bike_params['hip_angle'] = hip_angle
      for headtube_angle in bike_params['headtube_angle']:
       current_bike_params['headtube_angle'] = headtube_angle
       for crank_radius in bike_params['crank_radius']:
        current_bike_params['crank_radius'] = crank_radius
        for crank_x_offset in bike_params['crank_x_offset']:
         current_bike_params['crank_x_offset'] = crank_x_offset
         for crank_z_offset in bike_params['crank_z_offset']:
          current_bike_params['crank_z_offset'] = crank_z_offset
          for fork_offset in bike_params['fork_offset']:
           current_bike_params['fork_offset'] = fork_offset
           for seat_height in bike_params['seat_height']:
            current_bike_params['seat_height'] = seat_height
            for handlebar_radius in bike_params['handlebar_radius']:
             current_bike_params['handlebar_radius'] = handlebar_radius
             for front_wheel_radius in bike_params['front_wheel_radius']:
              current_bike_params['front_wheel_radius'] = front_wheel_radius
              for rear_wheel_radius in bike_params['rear_wheel_radius']:
               current_bike_params['rear_wheel_radius'] = rear_wheel_radius
               for frame_mass in bike_params['frame_mass']:
                current_bike_params['frame_mass'] = frame_mass
                for crank_mass in bike_params['crank_mass']:
                 current_bike_params['crank_mass'] = crank_mass
                 for front_wheel_mass in bike_params['front_wheel_mass']:
                  current_bike_params['front_wheel_mass'] = front_wheel_mass
                  for rear_wheel_mass in bike_params['rear_wheel_mass']:
                   current_bike_params['rear_wheel_mass'] = rear_wheel_mass

                   ## For Debugging.
                   counter += 1
                   if counter % 10000 == 0:
                     print(str(counter) + ' - min_error: ' + str(min_error) +\
                           ' - current runtime: ' +\
                            str(checkpoint - start_time) + ' sec')
                     checkpoint = time.time()

                   ## Update the current bike with the current geometry.
                   bike.update_geometry(current_bike_params)

                   rider_didnt_fit = False
                   error = 0.0

                   ## Try and fit each rider in the bike and sum the errors.
                   for rider in riders:
                     if bike.fit_rider(rider):
                       bike.compute_patterson_curves(control_spring,\
                                                     control_sensitivity, top_speed)
                       error +=\
                         bike.compute_sum_of_diff_of_squares(control_sensitivity,\
                                                            target_control_sensitivity)
                     else:
                       rider_didnt_fit = True
                       break

                   ## If a rider doesn't fit, abandon this design.
                   if rider_didnt_fit:
                     continue

                   ## If this is a better design than any previous design,
                   ## record it.
                   if error < min_error:
                     min_error = error
                     current_bike_params['error'] = error
                     if len(best_bike_params) >= simulation_params.sample_count:
                       ## Remove the param configuration with the worst error.
                       best_bike_params = best_bike_params[:-1]

                     ## Add new param configuration to the front of the list.
                     best_bike_params = [copy.deepcopy(current_bike_params)] + best_bike_params

                     #bike.plot()
                     best_bike.update_geometry(current_bike_params)

    ## Prints the best bike.
    best_bike.fit_rider(riders[0])
    best_bike.compute_patterson_curves(control_spring, control_sensitivity, top_speed)
    best_bike.plot()

    ## Copy the final list of bike params into the caller's out dictionary, with
    ## a mapping of each bike_param's error -> bike_param.
    for bike_params in best_bike_params:
      error = bike_params['error']
      best_bikes[error] = bike_params

    ## Return the score of the best bike.
    return error

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 brute_force_search.py <output_filename>'
          ' <sample_count> <target_control_sensitivity> <bike_params.txt>'
          ' <rider_params>+\n'
          '|  output_filename = the file to write the results to\n'
          '|  sample_count = the number optimum bike samples to output\n'
          '|  target_control_sensitivity = a sensitivity curve that this model'
                                          'is trying to build towards\n'
          '|  bike_params.txt = a file containing all the bike params\n'
          '|  rider_params.txt = one or more files containing rider params\n')

def parse_inputs(command_line_args):
  ## Create a SimulationParams object to hold all the parsed input data.
  simulation_params = SimulationParams()

  ## Create a Parser to parse the input files.
  parser = Parser()

  ## Grab the output filename.
  output_filename = sys.argv[1]

  ## Grab the sample count from the input.
  simulation_params.sample_count = int(sys.argv[2])

  ## Grab the target control sensitivity curve from the input.
  parser.parse_curve_file(simulation_params.target_control_sensitivity,
                          sys.argv[3]) 

  ## Read in the bike_params, resulting in a dictionary of {param -> [values]}.
  parser.parse_bike(simulation_params.bike_params, sys.argv[4])

  ## Read in the rider_params, resulting in a list of [{param -> [values]}].
  parser.parse_riders(simulation_params.riders, sys.argv[5])

  ## Compute the top speed.
  simulation_params.top_speed = len(simulation_params.target_control_sensitivity)

  return simulation_params

def main():
  if len(sys.argv) < 6:
    print_usage()
    return

  ## Parse all the inputs.
  simulation_params = parse_inputs(sys.argv)

  ## Create a BruteForceSearch object to run the simulation with.
  simulation = BruteForceSearch()

  ## A dictionary of error -> bike_params to be populated with the best bikes
  ## from the simulation.
  best_bikes = {}

  ## Run the simulation
  start = time.time()
  simulation.run(simulation_params, best_bikes)
  end = time.time()
  print('Brute Force runtime: ' + str(end - start))

  ## Write the top bikes to an output file.
  try:
    with open(output_filename, 'w') as output:
      output.write(json.dumps(best_bikes))

  except IOError:
    print('Could not open ' + str(output_filename) + ' for writing.')
    sys.exit(1)

if __name__ == '__main__':
    main()

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
