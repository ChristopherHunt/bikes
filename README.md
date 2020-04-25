bikes
=====

A project to iteratively explore the design space of recumbent bicycles. This
work leverages the *Patterson Control Model* for bicycle design as well as Genetic
Algorithm search techniques to help aid bicycle enthusiasts discover new designs
for their set of geometric and physical constraints. Note that this project was
designed with recumbent bicycle design in mind -- it can still help design safety
bikes but in general it is less robust in this arena. See the included paper for
more details on the project's background, development and test results.

This project is written in Python3 and uses Jupyter Notebooks for data visualization.
There are notebooks for computing bike sensitivity curves for a given set of bike
and rider inputs, as well as notebooks that will propose bike geometry given a
range of rider and bike design constraints. Base templates are included for each
notebook style, as well as some demo notebooks to serve as examples.

Bike Plotting:
--------------

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

Bike Searching:
---------------

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

Running this Software
---------------------

This project is built upon several python libraries and uses the Jupyter notebook
framework for script execution and data visualization. This guide outlines two
separate ways to run this project:

* Online via Google Colab
* Locally on your own machine

Running on Google Colab shouldn't require any special configuration of your
machine and is free to use, making it the ideal choice for most users. However,
if you want to modify the source code iteratively then downloading the repo and
running it locally will be what you'll want to do.

Running on Google Colab
-----------------------

Google Colab is an online service which we'll use to run our Jupyter notebooks.
The service is free to use so just follow the following steps to import this
project so you can start running it:

* Create a Google account if you haven't already (if you use gmail then you already
  have a Google account).
* Go to [https://colab.research.google.com/](https://colab.research.google.com/).
* Upon loading this website it should prompt you with a window to create a new
  notebook. If it does not then you can navigate to the `File -> Upload notebook...`
  dropdown menu.

![Image of Opening Notebook Uploader](https://github.com/ChristopherHunt/bikes/blob/master/src/notebooks/img/google_colab_launch_uploader.png)

* Select the `GitHub` tab from the file upload window.
* Then enter the bikes GitHub reposity URL (`https://github.com/ChristopherHunt/bikes.git`)
  to get a list of Jupyter notebook files to upload to Google Colab.

![Image of Choosing GitHub Upload](https://github.com/ChristopherHunt/bikes/blob/master/src/notebooks/img/google_colab_upload_from_git.png)

* Click on the notebook you want to run and it will open up within Google Colab.
  At this point you can modify any of the fields within the notebook as well as run
  the simulation.

![Image of Running Simulation](https://github.com/ChristopherHunt/bikes/blob/master/src/notebooks/img/google_colab_run_notebook.png)

There are two primary notebook types to choose from under the
**bikes/src/notebooks** directory and there are **demo notebooks** for each of
them under **bikes/src/notebooks/demos** which also includes some general
templates showing their extended functionality.

Running Locally
---------------

__Required Software:__

* Python 3.6
* NumPy 1.11.3
* Matplotlib 2.0.0
* Jupyter Notebook 4.2.1

Note that the above versions are only those which the project has been tested
with, other versions may work as well. Additionally, all of this software can be
installed via the `Anaconda` python installer.

__To Run Locally:__

Follow these steps to run this project on your local machine:

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
