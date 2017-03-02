#!/usr/bin/python3

import sys

from bike import Bike
from config_parser import Parser

from matplotlib import gridspec
import matplotlib.pyplot as plt

## Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 single_bike_gen.py <target_control_sensitivity.txt>'
          ' <bike_params.txt> <rider_params>\n'
          '|  target_control_sensitivity.txt = a file containing the reference'
                                             ' control sensitivity graph'
                                             ' values.\n'
          '|  bike_params.txt = a file containing the bike params\n'
          '|  rider_params.txt = a file containing the rider params\n')

def main():
  if len(sys.argv) != 4:
    print_usage()
    return

  target_control_sensitivity_file = sys.argv[1]
  bike_params_file = sys.argv[2]
  rider_params_file = sys.argv[3]

  ## Create a Parser to parse the input files.
  parser = Parser()

  ## Parse the target control sensitivity curve from the input.
  target_control_sensitivity = []
  parser.parse_curve_file(target_control_sensitivity,
                          target_control_sensitivity_file) 

  ## Read in the bike_params, resulting in a dictionary of {param -> [values]}.
  temp_bike_params = {}
  parser.parse_bike(temp_bike_params, bike_params_file)

  ## Read in the rider_params, resulting in a list of [{param -> [values]}].
  rider_params = []
  parser.parse_riders(rider_params, rider_params_file)

  ## Reduce the original bike_params dictionary to {param -> value} since we
  ## only have a single value per param.
  bike_params = {}
  for key, value in temp_bike_params.items():
    bike_params[key] = value[0] 

  ## Build a Bike
  bike = Bike()
  bike.update_geometry(bike_params)

  ## Setup figure.
  fig = plt.figure(figsize=(15, 20), dpi=70)
  gs = gridspec.GridSpec(4, 2)

  ## Setup axes within the figure.
  ax1 = fig.add_subplot(gs[0,0])
  ax2 = fig.add_subplot(gs[0,1])
  ax1.grid()

  ## Adjust plot to ensure that things fit correctly.
  plt.subplots_adjust(wspace=0.3)

  error = 0
  color_index = 0
  colors = ['b', 'g', 'k', 'm', 'y', 'c']
  for rider in rider_params:
    control_spring = []
    control_sensitivity = []
    top_speed = len(target_control_sensitivity)

    ## Fit the rider to the bike.
    bike.fit_rider(rider)

    ## Compute the Patterson Curve values.
    bike.compute_patterson_curves(control_spring, control_sensitivity, top_speed) 

    ## Compute the error.
    error += bike.compute_sum_of_diff_of_squares(control_sensitivity,
                                                 target_control_sensitivity)

    print(rider['rider_name'] + '\'s Control Sensitivity:')
    print(control_sensitivity)
    print('')

    rider_color = colors[color_index]
    color_index += 1
    if color_index >= len(colors):
      color_index = 0

    bike.plot_bike(ax1, rider_color)
    bike.plot_control_sensitivity(ax2, control_sensitivity, rider_color,
                                  rider['rider_name'])

  ## Pot the target control sensitivity curve for reference.
  bike.plot_control_sensitivity(ax2, target_control_sensitivity, 'ro', 'Target')

  ## Print the rider data.
  print('Rider data:')
  for rider in rider_params:
    print(rider)

  '''
  ## Add the names of each rider to the plot.
  rider_names = ', '.join(rider['rider_name'] for rider in rider_params)
  ax1.annotate('Riders: ' + rider_names, xy=(0.05, 0.95),
                xycoords='axes fraction', fontsize=16, ha='left', va='top')
  '''

  ## Add the total error to the plot.
  ax2.annotate('Error: ' + str(error), xy=(0.5, 0.01), xycoords='axes fraction',
                fontsize=16, ha='center', va='bottom')
  
  ## Show the figure.
  plt.show()

if __name__ == '__main__':
    main()

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
