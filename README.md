bikes
=====

A project to iteratively explore the design space of recumbent bicycles
leveraging the *Patterson Control Model* for bicycle design as well as Computer
Science AI search techniques, with the intention of helping engineers and
enthusiasts discover good bicycle designs given a set of geometric and physical
constraints that they define up front.

Required Software:
------------------
* Python 3.6
* NumPy 1.11.3
* Matplotlib 2.0.0
* Jupyter Notebook 4.2.1

Note that the above versions are only those which the project has been tested
with, other versions may work as well. Additionally, all of this software can be
installed via [Anaconda](https://www.continuum.io/downloads).

To Run:
-------
This project runs via a series of Jupyter Notebooks. There are two primary
notebooks to choose from under the src/notebooks directory.

__Bike Plotting:__

The bike plotting notebook (bike_plotter.ipynb) allows users to visualize
bicycle/rider geometries while computing a configurations Patterson Control
Sensitivity Curve. The model requires the user to specify a bicycle's frame
geometry, a series of riders and a datum control sensitivity curve as inputs,
and outputs each rider's Control Sensitivity Curve as well as an illustration
of the bicycle as outputs.

__Bike Searching:__

The bike searching notebook (bike_search.ipynb) is designed to search a
specified bicycle geometry space in an attempt to find suitable designs that
match the user's handling expectations. The model requires the user to specify
a range of frame geometries as well as a set of riders, a target sensitivity
curve and other search configuration parameters. From there, the user can select
between the following search algorithms:

* Brute Force
* Unpartitioned Genetic Search
* Partitioned Genetic Search

The model will then iterate to the final solution and will return a series of
bicycle designs (both an illustration of the bicycle as well as its Control
Sensitivity Curves).

     _____________________________________________________
    ( Get a bicycle. You will not regret it, if you live. )
    (                                  -- Mark Twain      )
    (_____________________________________________________)
       o
        o
            .--.
           |o_o |
           |:_/ |
          //   \ \
         (|     | )
        /'\_   _/`\
        \___)=(___/
