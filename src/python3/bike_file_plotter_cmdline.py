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

  def plot(self, simulation_params, bikes_to_plot, output_filename):
    json_data = open(bikes_to_plot).read()
    bike_data = json.loads(json_data)

    ## Open a file to save all these plots to.
    pp = PdfPages(output_filename)

    ## Setup figure.
    fig = plt.figure(figsize=(15, 20), dpi=50)
    gs = gridspec.GridSpec(4, 2)

    ## Setup axes within the figure.
    axes = []
    axes.append(fig.add_subplot(gs[0,0]))
    axes.append(fig.add_subplot(gs[0,1]))
    axes.append(fig.add_subplot(gs[1,0]))
    axes.append(fig.add_subplot(gs[1,1]))
    axes.append(fig.add_subplot(gs[2,0]))
    axes.append(fig.add_subplot(gs[2,1]))
    axes.append(fig.add_subplot(gs[3,0]))
    axes.append(fig.add_subplot(gs[3,1]))

    ## Set overall title for first column.
    axes[0].set_title('Bike Dimensions')

    ## Set overall title for second column.
    axes[1].set_title('Control Sensitivity')

    ## Adjust plot to ensure that things fit correctly.
    plt.subplots_adjust(wspace=0.2, hspace=0.2)

    target_control_sensitivity = simulation_params.target_control_sensitivity
    top_speed = len(target_control_sensitivity)
    colors = ['b', 'g', 'k', 'm', 'y', 'c']
    axes_index = 0

    ## Mapping of error -> bike_params for each bicycle design, where the error
    ## is the average error across all the riders that are fit to the bike.
    bikes_to_plot = {}

    ## Sort the list by error.
    bike_errors = sorted(bike_data.keys())

    ## For each bike in bikes_to_plot JSON
    counter = 0
    for error in bike_data.keys():
      counter += 1
      color_index = 0

      ## For each rider
      riders_to_plot = []
      for rider in simulation_params.riders:
        control_spring = []
        control_sensitivity = []

        ## Make temporary bike for each bike/rider configuration
        bike = Bike()

        ## Parse the bike params into a Bike object
        bike_params = bike_data[error]
        bike.update_geometry(bike_params)

        ## Get the formatting color for each rider.
        rider_color = colors[color_index]
        color_index += 1
        if color_index >= len(colors):
          color_index = 0

        bike_plot_axis = axes[axes_index]
        bike_curve_axis = axes[axes_index + 1]

        ## Fit the rider to the bike.
        if bike.fit_rider(rider):
          ## Compute the Patterson Curve values.
          bike.compute_patterson_curves(control_spring, control_sensitivity, top_speed) 

          bike.plot_bike(bike_plot_axis, rider_color)

          ## Plot the curves for this bike and rider combination.
          bike.plot_control_sensitivity(bike_curve_axis,
                                        control_sensitivity,
                                        rider_color, rider['rider_name'])

      ## Add the total error to the plot.
      print(error)
      bike_curve_axis.annotate('Error: ' + str(error), xy=(0.5, 0.01),
                               xycoords='axes fraction', fontsize=16,
                               ha='center', va='bottom')

      ## Pot the target control sensitivity curve for reference.
      bike.plot_control_sensitivity(bike_curve_axis,target_control_sensitivity,
                                    'ro', 'Target')

      axes_index += 2

      ## If we ran out of axes to plot on this page, save that page to disk and
      ## start fresh on a new page.
      if axes_index >= 8:
        axes_index = 0

        ## Save the plot
        pp.savefig(fig)
        ##plt.show()

        ## Clear all axes for next set of plots
        for axis in axes:
          axis.clear()

    ## Save the last plot if it didn't get fully finished.
    if axes_index != 0:
      ## Save the plot
      pp.savefig(fig)

    ## Close the plots file.
    print('closing pdf')
    pp.close()

# Prints the usage string to stdout.
def print_usage():
    print('Improper arguments!\n'
          'Run as python3 bike_file_plotter_cmd.py <output_filename.pdf>'
          ' <bikes_to_plot.txt> <top_speed> <target_control_sensitivity.txt>'
          ' <rider_params>+\n'
          '|  output_filename.pdf = the file to write the bike plots to\n'
          '|  bikes_to_plot.txt = JSON file containing bike parameters to plot\n'
          '|  target_control_sensitivity.txt = a sensitivity curve that this '
                                              'model is trying to build towards\n'
          '|  rider_params.txt = one or more files containing rider params\n')

## Parses the command line arguments, returning the following triple:
##
##      (simulation_params, bikes_to_plot, output_filename)
## 
## where:
##   simulation_params = a population SimulationParams object (from input data)
##   bikes_to_plot = name of a JSON file of bikes to analyze/plot.
##   output_filename = the name of the final file to print all results to.
def parse_input(command_line_args):
  if len(command_line_args) < 5:
    print_usage()
    sys.exit(1)

  ## Create a Parser to parse the input files.
  parser = Parser()

  ## Create a SimulationParams object to hold the params for each run.
  simulation_params = SimulationParams()

  ## Grab the output filename.
  output_filename = command_line_args[1]

  ## Grab the name of the JSON file containing all of the bikes to plot.
  bikes_to_plot = command_line_args[2]

  ## Grab the name of the target_control_sensitivity curve file.
  curve_filename = command_line_args[3]

  ## Grab the name of the rider config file.
  rider_config_filename = command_line_args[4]

  ## Parse the target control sensitivity curve from the input.
  parser.parse_curve_file(simulation_params.target_control_sensitivity,
                          curve_filename) 

  ## Parse in the rider_params, resulting in a list of [{param -> [values]}].
  parser.parse_riders(simulation_params.riders, rider_config_filename)

  return simulation_params, bikes_to_plot, output_filename

def main():
  ## Parse the command line arguments
  simulation_params, bikes_to_plot, output_filename = parse_input(sys.argv)

  ## Create a BikeFilePlotter object to plot with.
  bike_plotter = BikeFilePlotter()

  ## Plot each bike configuration and write to output file.
  bike_plotter.plot(simulation_params, bikes_to_plot, output_filename)

if __name__ == '__main__':
    main()

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
