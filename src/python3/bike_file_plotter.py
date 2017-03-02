from bike import Bike

import copy
import json
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl

from matplotlib import gridspec
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import sys
import time

from bike import Bike
from config_parser import Parser
from simulation_params import SimulationParams

class BikeFilePlotter:
  def __init__(self):
    pass

  def plot(self, simulation_params, bikes_to_plot):
    json_data = open(bikes_to_plot).read()
    bike_data_strings = json.loads(json_data)

    target_control_sensitivity = simulation_params.target_control_sensitivity
    top_speed = len(target_control_sensitivity)
    colors = ['b', 'g', 'k', 'm', 'y', 'c']

    ## Mapping of error -> bike_params for each bicycle design, where the error
    ## is the average error across all the riders that are fit to the bike.
    bikes_to_plot = {}

    ## Check that there are bikes to plot, print error and exit if the list is
    ## empty.
    if not bike_data_strings.items():
      print('No useable bike designs to plot.')
      return

    ## Convert all string errors into float errors.
    bike_data = {}
    for key, value in bike_data_strings.items():
      bike_data[float(key)] = value 

    ## Sort the list by error.
    bike_errors = sorted(bike_data.keys())

    ## For each bike in bikes_to_plot JSON
    counter = 0
    for error in bike_errors:
      counter += 1
      color_index = 0

      ## Setup figure.
      fig = plt.figure(figsize=(15, 20), dpi=70)
      gs = gridspec.GridSpec(4, 2)

      ## Setup axes within the figure.
      bike_axis = fig.add_subplot(gs[0,0])
      curve_axis = fig.add_subplot(gs[0,1])

      ## Set overall title for first column.
      bike_axis.set_title('Bike Dimensions')

      ## Set overall title for second column.
      curve_axis.set_title('Control Sensitivity')

      ## Get the bike configuration to plot.
      bike_params = bike_data[error]

      ## Print bike configuration.
      print('\n')
      print('Bike Params:')
      print(bike_params)
      print('\n')

      ## For each rider
      riders_to_plot = []
      for rider in simulation_params.riders:
        control_spring = []
        control_sensitivity = []

        ## Make temporary bike for each bike/rider configuration
        bike = Bike()

        ## Parse the bike params into a Bike object
        bike.update_geometry(bike_params)

        ## Get the formatting color for each rider.
        rider_color = colors[color_index]
        color_index += 1
        if color_index >= len(colors):
          color_index = 0

        ## Fit the rider to the bike.
        if bike.fit_rider(rider):
          ## Compute the Patterson Curve values.
          bike.compute_patterson_curves(control_spring, control_sensitivity, top_speed) 

          bike.plot_bike(bike_axis, rider_color)

          ## Plot the curves for this bike and rider combination.
          bike.plot_control_sensitivity(curve_axis,
                                        control_sensitivity,
                                        rider_color, rider['rider_name'])

        print('Rider: ' + str(rider['rider_name']))
        print(rider)
        print('\n')
        print('Control Sensitivity Values:')
        print(control_sensitivity)
        print('\n')

      ## Add the total error to the plot.
      curve_axis.annotate('Error: ' + str(error), xy=(0.5, 0.01),
                          xycoords='axes fraction', fontsize=16,
                          ha='center', va='bottom')

      ## Pot the target control sensitivity curve for reference.
      bike.plot_control_sensitivity(curve_axis,target_control_sensitivity,
                                    'ro', 'Target')


      ## Show this configuration.
      plt.show()
      plt.close(fig)

# Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 bike_file_plotter.py <bikes_to_plot.txt> '
          '<target_control_sensitivity.txt> <rider_params>+\n'
          '|  bikes_to_plot.txt = JSON file containing bike parameters to plot\n'
          '|  target_control_sensitivity.txt = a sensitivity curve that this '
                                              'model is trying to build towards\n'
          '|  rider_params.txt = one or more files containing rider params\n')

## Parses the command line arguments, returning the following triple:
##
##      (simulation_params, bikes_to_plot)
## 
## where:
##   simulation_params = a population SimulationParams object (from input data)
##   bikes_to_plot = name of a JSON file of bikes to analyze/plot.
def parse_input(command_line_args):
  if len(command_line_args) < 4:
    print_usage()
    sys.exit(1)

  ## Create a Parser to parse the input files.
  parser = Parser()

  ## Create a SimulationParams object to hold the params for each run.
  simulation_params = SimulationParams()

  ## Grab the name of the JSON file containing all of the bikes to plot.
  bikes_to_plot = command_line_args[1]

  ## Grab the name of the target_control_sensitivity curve file.
  curve_filename = command_line_args[2]

  ## Grab the name of the rider config file.
  rider_config_filename = command_line_args[3]

  ## Parse the target control sensitivity curve from the input.
  parser.parse_curve_file(simulation_params.target_control_sensitivity,
                          curve_filename) 

  ## Parse in the rider_params, resulting in a list of [{param -> [values]}].
  parser.parse_riders(simulation_params.riders, rider_config_filename)

  return simulation_params, bikes_to_plot

def main():
  ## Parse the command line arguments
  simulation_params, bikes_to_plot = parse_input(sys.argv)

  ## Create a BikeFilePlotter object to plot with.
  bike_plotter = BikeFilePlotter()

  ## Plot each bike configuration and write to output file.
  bike_plotter.plot(simulation_params, bikes_to_plot)

if __name__ == '__main__':
    main()

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
