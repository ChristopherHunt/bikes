bikes
=====

A project to iteratively explore the design space of recumbent bicycles
leveraging the *Patterson Control Model* for bicycle design as well as Genetic
Algorithm search techniques with the intention of helping bicycle enthusiasts
discover useable bicycle designs given a set of geometric and physical
constraints that they define up front. Note that this project was designed with
recumbent bicycle design in mind -- it can still help design safety bikes but in
general it is less robust in this arena.

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
This project currently runs on the user's local machine with the front-end being
supplied via a series of Jupyter Notebooks. As such, the steps to run this are:

* Download this source code.
* Install the software on your machine as outlined in the *Required Software*
  section above.
* Start the Jupyter Notebook application locally on your machine. This will
  launch your brower with a view of your filesystem.
* Navigate to one of the example notebooks provided in the
  **bikes/src/notebook** directory of this codebase and select it. This will
  bring up that notebook in your brower and will allow you to run it
  interactively.

There are two primary notebook types to choose from under the
**bikes/src/notebooks** directory and there are **demo notebooks** for each of
them under **bikes/src/notebooks/demos** which also includes some general
templates showing their extended functionality.

__Bike Plotting:__

The bike plotting notebook (*bike_plotter.ipynb*) allows users to visualize
bicycle/rider geometries while computing their Patterson Control Sensitivity
Curve. The model requires the user to specify the following input parameters:
* the bicycle's frame geometry
* a series of riders to fit to the bicycle frame
* a datum control sensitivity curve to compare rider's against.

The model then outputs the following:
* each rider's Control Sensitivity Curve
* an plot of the bicycle with each rider superimposed on the bicycle frame

Note that this notebook expects an input Patterson Control Sensitivity Curve and
reports errors relative to this in the output. This was done to allow a designer
to compare a known "good handling" design to the new experimental designs, and
also to drive the *Bike Search* notebook (discussed below).

__Bike Searching:__

The bike searching notebook (*bike_search.ipynb*) is designed to search a
specified bicycle geometry space in an attempt to find suitable designs that
match the user's handling expectations. The model requires the user to specify
the following inputs:
* a range of values for each of the frame's components
* a set of riders
* a target sensitivity curve
* other search configuration parameters (if they want to tweak the defaults)

From there, the user can select between the following search algorithms via a
drop down button in the notebook (which will appear after the button cell is
run by the notebook):
* Brute Force
* Unpartitioned Genetic Search
* Partitioned Genetic Search

The model will then iterate to the final solution and will return a series of
bicycle designs, with each being reported via a plot of the bicycle/riders as
well as each rider's Patterson Control Sensitivity Curves.

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
