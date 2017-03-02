#!/usr/bin/python3

search_algorithm = button.value
if search_algorithm == 'Brute Force Search':
    print('Running Brute Force Search')
    %run -i brute_force_search bikes.txt 25 target_control_curve.txt bike_params.txt rider_params.txt
elif search_algorithm == 'Unpartitioned Genetic Search':
    print('Running Unpartitioned Genetic Search')
    %run -i unpartitioned_genetic_search bikes.txt bikes_log.txt genetic_params.txt 200 target_control_curve.txt bike_params.txt rider_params.txt
elif search_algorithm == 'Partitioned Genetic Search':
    print('Running Partitioned Genetic Search')
    %run -i partitioned_genetic_search bikes.txt bikes_log.txt genetic_params.txt partitioning_params.txt target_control_curve.txt bike_params.txt rider_params.txt
else:
    print('Unknown search algorithm: ' + str(search_algorithm))
    
%run -i bike_file_plotter bikes.txt target_control_curve.txt rider_params.txt

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
