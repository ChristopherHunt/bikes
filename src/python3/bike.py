# bike.py
#!/usr/bin/python3

import copy
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

class Bike:
  'Wrapped to hold all of the parameters for defining a bike.'

  def __init__(self):
    ## General constants
    self._g = 9.81 ## Gravity [m/s^2]

    ## Set all the bike parameters to be initially zero.
    self._clear_bike_params()

    ## Set all the rider parameters to be initially zero.
    self._clear_rider_params()

    ## Set all the Patterson parameters to be initially zero.
    self._clear_patterson_variables()

  def compute_patterson_curves(self, control_spring, control_sensitivity,\
                               top_speed):
    self._trail = self._Rf * math.sin(self._beta) - self._e / math.cos(self._beta)

    self._k1 = (self._m_bike * self._g * (self._m_bike_x / self._A) *\
               self._trail * math.cos(self._beta)) * (math.sin(self._beta) -\
               self._m_bike_z * self._trail * self._m_bike_x / (self._A *\
               (self._m_bike_z * self._m_bike_z + self._bike_Kxx * self._bike_Kxx)))

    self._k2 = self._trail * (math.cos(self._beta) * math.cos(self._beta)) *\
              self._m_bike * (self._m_bike_x / (self._A * self._A)) *\
              ((self._bike_Kxx * self._bike_Kxx) / (self._m_bike_z *\
              self._m_bike_z + self._bike_Kxx * self._bike_Kxx))

    self._k3 = 1 / 1500.0

    self._k4 = self._m_bike_x / (self._m_bike_z * self._A) * math.cos(self._beta)

    '''
    print('bike_Kxx: ' + str(self._bike_Kxx))
    print('m_bike: ' + str(self._m_bike))
    print('R_f: ' + str(self._Rf))
    print('e: ' + str(self._e))
    print('g: ' + str(self._g))

    print('A: ' + str(self._A))
    print('m_bike_x: ' + str(self._m_bike_x))
    print('m_bike_z: ' + str(self._m_bike_z))
    print('beta: ' + str(self._beta))

    print('trail: ' + str(self._trail))
    print('k1: ' + str(self._k1))
    print('k2: ' + str(self._k2))
    print('k3: ' + str(self._k3))
    print('k4: ' + str(self._k4))
    '''

    self._compute_control_spring(control_spring, top_speed)
    self._compute_control_sensitivity(control_sensitivity, top_speed)

  ## Attempts to fit each rider into the current bike geometry, and tests each
  ## version up to the specified top_speed. Returns the normalized score for the
  ## bike from all the rider fittings, or infinity if the bike geometry is
  ## invalid or one of the riders didn't fit.
  def compute_error(self, riders, target_control_sensitivity, top_speed):
    control_spring = []
    control_sensitivity = []
    error = 0.0

    ## Try and fit each rider
    for rider in riders:
      if self.fit_rider(rider):
        self.compute_patterson_curves(control_spring,\
                                      control_sensitivity, top_speed)
        error +=\
          self.compute_sum_of_diff_of_squares(control_sensitivity,\
                                              target_control_sensitivity)
      ## If the rider doesn't fit, return worst case score
      else:
        return float('inf')

    ## Normalize the error across riders.
    error = error / len(riders)
    return error

  ## Computes the sum of difference of sequares between the two input curves,
  ## returning the resulting error through the error out parameter. If the two
  ## curves have different lengths, then the comparison only happens on the
  ## first n elements, where n is the length of the shorter list.
  def compute_sum_of_diff_of_squares(self, curve, target_curve):
    error = 0.0
    for x, y in zip(curve, target_curve):
      error += (x - y) * (x - y)
    return error

  ## Attempts to fit the rider to the bike by adjusting the seat location. Also
  ## computes the radius of gyration of the entire system about the bike's wheel
  ## contact patch.
  ##
  ## Returns False if the rider cannot fit on the bike.
  def fit_rider(self, rider_params):
    ## Update the internal mapping of the rider's parameters.
    self._update_rider_params(rider_params)

    ## Attempt to fit the rider to the bike. This returns True if it succeeds.
    return self._fit_rider_to_bike()

  ## Generates a random bike from the input bike_params. Additionally, populates
  ## indexed_bike_params with the param -> array of indices of params that were
  ## chosen to create this random bike and returns a deepcopy of that dict to
  ## the caller.
  def generate_random_bike(self, bike_params):
    self._single_bike_params = {}
    indexed_bike_params = {}
    for key, value_list in bike_params.items():
      index = random.randint(0, len(value_list) - 1)
      indexed_bike_params[key] = index
      self._single_bike_params[key] = value_list[index]

    self.update_geometry(self._single_bike_params)
    return copy.deepcopy(indexed_bike_params)

  ## Plots the current bike geometry.
  def plot_bike(self, ax, color='b'):
    self._plot_bike(ax, color)

  ## Prints all the current bike and rider params that the bike is being built
  ## with.
  def print_params(self):
    print('=== Bike Params ===')
    print('A:' + str(self._A))
    print('alpha: ' + str(math.degrees(self._alpha)))
    print('beta: ' + str(math.degrees(self._beta)))
    print('C_r: ' + str(self._Cr))
    print('C_x: ' + str(self._Cx))
    print('C_z: ' + str(self._Cz))
    print('e: ' + str(self._e))
    print('H_z: ' + str(self._Hz))
    print('R_h: ' + str(self._Rh))
    print('R_f: ' + str(self._Rf))
    print('R_r: ' + str(self._Rr))
    print('m_frame: ' + str(self._m_frame))
    print('m_crank: ' + str(self._m_crank))
    print('self._m_front_wheel: ' + str(self._m_front_wheel))
    print('self._m_rear_wheel: ' + str(self._m_rear_wheel))
    print('\n')
    print('=== Current Rider Being Fit ===')
    print('self._m_rider: ' + str(self._m_rider))
    print('self._head_diameter: ' + str(self._head_diameter))
    print('self._torso_length: ' + str(self._torso_length))
    print('self._torso_depth: ' + str(self._torso_depth))
    print('self._torso_width: ' + str(self._torso_width))
    print('self._arm_length: ' + str(self._arm_length))
    print('self._arm_diameter: ' + str(self._arm_diameter))
    print('self._leg_length: ' + str(self._leg_length))
    print('self._leg_diameter: ' + str(self._leg_diameter))
    print('\n')

  ## Return a full copy of the current geometry parameters for this bike.
  def single_bike_params(self):
    return copy.deepcopy(self._single_bike_params)

  ## Updates the current bike with the specified single_bike_params, and clears
  ## out the information from the previous rider.
  def update_geometry(self, single_bike_params):
    ## Update the internal mapping of the bike's parameters.
    self._update_bike_params(single_bike_params)

    ## Clear out previous rider information.
    self._clear_rider_params()

  ## Converts the single_bike_params_indexes to the actual bike_param values and
  ## returns that dictionary to the caller.
  def convert_bike_params_from_indexes(self, bike_params, single_bike_params_indexes):
    single_bike_params = {}

    ## Construct the actual single_bike_params dictionary from the indexed dict.
    for key, value in single_bike_params_indexes.items():
      single_bike_params[key] = bike_params[key][value]

    return single_bike_params

  ## Updates the current bike with the specified single_bike_params_indexes,
  ## converting each parameter from an index into its actual value by
  ## referencing the bike_params dictionary. Additionally, clears out the
  ## information from the previous rider.
  def update_geometry_from_indexes(self, bike_params, single_bike_params_indexes):
    ## Convert from bike_param indexes to actual bike_param values.
    single_bike_params =\
       self.convert_bike_params_from_indexes(bike_params,
                                             single_bike_params_indexes)

    ## Update the internal mapping of the bike's parameters.
    self._update_bike_params(single_bike_params)

    ## Clear out previous rider information.
    self._clear_rider_params()

  def _clear_bike_params(self):
    ## Bike Parameters
    self._A              = 0.0
    self._alpha          = 0.0
    self._beta           = 0.0
    self._Cr            = 0.0
    self._Cx            = 0.0
    self._Cz            = 0.0
    self._e              = 0.0
    self._Hz            = 0.0
    self._Rh            = 0.0
    self._Rf            = 0.0
    self._Rr            = 0.0
    self._m_frame        = 0.0
    self._m_crank        = 0.0
    self._m_front_wheel  = 0.0
    self._m_rear_wheel   = 0.0

    ## Fork Positions
    self._fork_bottom_x  = 0.0
    self._fork_bottom_z  = 0.0
    self._fork_top_x     = 0.0
    self._fork_top_z     = 0.0

    ## Tube Centers of Gravity
    self._t1x = 0.0
    self._t1z = 0.0
    self._t2x = 0.0
    self._t2z = 0.0
    self._t3x = 0.0
    self._t3z = 0.0
    self._t4x = 0.0
    self._t4z = 0.0
    self._t5x = 0.0
    self._t5z = 0.0

    ## Tube Lengths
    self._t1l = 0.0 
    self._t2l = 0.0 
    self._t3l = 0.0 
    self._t4l = 0.0 
    self._t5l = 0.0 

    ## Tube Masses
    self._t1m = 0.0
    self._t2m = 0.0
    self._t3m = 0.0
    self._t4m = 0.0
    self._t5m = 0.0

    ## Seat Positions
    self._seat_back_start_x  = 0.0
    self._seat_back_start_z  = 0.0
    self._seat_back_end_x    = 0.0
    self._seat_back_end_z    = 0.0

    ## Lower Seat
    self._seat_bottom_start_x  = 0.0
    self._seat_bottom_start_z  = 0.0
    self._seat_bottom_end_x    = 0.0
    self._seat_bottom_end_z    = 0.0

    ## Frame CG Location
    self._frame_cg_x = 0.0
    self._frame_cg_z = 0.0

    ## Bike CG Location
    self._m_bike_x = 0.0
    self._m_bike_z = 0.0
    self._m_bike   = 0.0

  def _clear_rider_params(self):
    ## Rider Parameters
    self._m_rider        = 0.0
    self._head_diameter  = 0.0
    self._torso_length   = 0.0
    self._torso_depth    = 0.0
    self._torso_width    = 0.0
    self._arm_length     = 0.0
    self._arm_diameter   = 0.0
    self._leg_length     = 0.0
    self._leg_diameter   = 0.0

    ## 95% Male Body Mass Percentages
    self._body_segment_to_mass_percentage = {}
    self._body_segment_to_mass_percentage['arm']   = 0.06
    self._body_segment_to_mass_percentage['head']  = 0.07
    self._body_segment_to_mass_percentage['leg']   = 0.170
    self._body_segment_to_mass_percentage['torso'] = 0.47

    ## Total rider inertia relative to the rider's CG about the X axis
    self._rider_Ixx  = 0.0
    self._head_Ixx   = 0.0
    self._torso_Ixx  = 0.0
    self._leg_Ixx    = 0.0
    self._arm_Ixx    = 0.0

    self._rider_Kxx  = 0.0
    self._head_Kxx   = 0.0
    self._torso_Kxx  = 0.0
    self._leg_Kxx    = 0.0
    self._arm_Kxx    = 0.0

    self._bike_Kxx   = 0.0

    ## Angle between hip and crank
    self._theta = 0.0

    ## Supplemental angle used during torso computations
    self._phi = 0.0

    ## Supplemental angle used during arm computations
    self._zeta = 0.0

    ## Hip Center Delta off of Seat
    self._hip_center_delta_x = 0.0
    self._hip_center_delta_z = 0.0

    ## Distance between rear wheel center and hip in x-dimension
    self._Hx = 0.0

    ## Torso
    self._torso_start_x    = 0.0
    self._torso_start_z    = 0.0
    self._torso_end_x      = 0.0
    self._torso_end_z      = 0.0
    self._torso_cg_x       = 0.0
    self._torso_cg_z       = 0.0

    ## Head
    self._head_cg_x = 0.0
    self._head_cg_z = 0.0

    ## Legs
    self._leg_start_x  = 0.0
    self._leg_start_z  = 0.0
    self._leg_end_x    = 0.0
    self._leg_end_z    = 0.0
    self._leg_cg_x     = 0.0
    self._leg_cg_z     = 0.0

    ## Arms
    self._arm_start_x  = 0.0
    self._arm_start_z  = 0.0
    self._arm_end_x    = 0.0
    self._arm_end_z    = 0.0
    self._arm_cg_x     = 0.0
    self._arm_cg_z     = 0.0

    ## Rider CG
    self._rider_cg_x = 0.0
    self._rider_cg_z = 0.0

  def _clear_patterson_variables(self):
    ## Patterson variables
    self._trail  = 0.0
    self._k1     = 0.0
    self._k2     = 0.0
    self._k3     = 0.0
    self._k4     = 0.0

  def _compute_arms(self):
    self._zeta = math.atan((self._torso_end_z - self._fork_top_z) /\
                          (self._fork_top_x - self._torso_end_x))
    self._arm_start_x = self._torso_end_x
    self._arm_start_z = self._torso_end_z
    self._arm_end_x = self._arm_start_x + self._arm_length * math.cos(self._zeta)
    self._arm_end_z = self._arm_start_z - self._arm_length * math.sin(self._zeta)
    shoulder_offset_from_hip_x = self._torso_length *\
                                 math.cos(math.pi - self._alpha - self._theta)
    shoulder_offset_from_hip_z = self._torso_length *\
                                 math.sin(math.pi - self._alpha - self._theta)
    self._arm_cg_x = math.cos(self._zeta) *\
                    (self._arm_length / 2) + self._arm_start_x
    self._arm_cg_z = -math.sin(self._zeta) *\
                    (self._arm_length / 2) + self._arm_start_z

  def _compute_arm_inertia_about_global_x_axis(self):
    ## Compute the local inertia values in the x,y,z directions. Note that we
    ## are idealizing the leg as a cylinder of constant diameter (which is where
    ## the below equations come from).
    arm_local_Ixx = (1 / 4.0) * self._m_arm *\
                    ((self._arm_diameter / 2) ** 2) +\
                     (1 / 12.0) * self._m_arm * (self._arm_length ** 2)
    arm_local_Iyy = (1 / 4.0) * self._m_arm *\
                    ((self._arm_diameter / 2) ** 2) +\
                     (1 / 12.0) * self._m_arm * (self._arm_length ** 2)
    arm_local_Izz = (1 / 2.0) * self._m_arm * ((self._arm_diameter / 2) ** 2)

    ## Compute local torso inertia tensor.
    arm_local_inertia_tensor =\
                    np.matrix([[arm_local_Ixx,       0,              0      ],
                              [      0,        arm_local_Iyy,        0      ],
                              [      0,              0,        arm_local_Izz]])

    ## Define the global coordinate system for reference.
    global_ref = np.matrix([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]])

    ## Create rotation matrix to dot with the global reference to create the
    ## final rotation matrix which will take our local inertia tensor and rotate
    ## it to align with the global coordinate system.
    local_arm_ref = np.matrix([[math.sin(self._zeta), 0, math.cos(self._zeta)],
                               [         0,          1,          0         ],
                               [math.cos(self._zeta), 0, math.sin(self._zeta)]])

    ## Compute final inertia rotation matrix to rotate the local inertia tensor
    ## to align with the global coordinate system.
    arm_rotation_matrix = global_ref * (local_arm_ref.transpose())

    ## Rotate local inertia tensor to align with the global coordinate system.
    arm_rotated_inertia_tensor = arm_rotation_matrix *\
                                 arm_local_inertia_tensor *\
                                 (arm_rotation_matrix.transpose())

    ## Use parallel axis theorum to shift the rotated torso tensor to be about
    ## the global x-axis. Note that we are grabbing the 0th item in the tensor
    ## because we only care about Ixx.
    self._arm_Ixx = arm_rotated_inertia_tensor.item(0) +\
                   self._m_arm * ((((self._torso_width / 2) +\
                                   (self._arm_diameter / 2)) ** 2) +\
                                 (self._arm_cg_z ** 2))

    ## Radius of gyration about the wheel contact patch. Note that we don't
    ## have to multiple by 2 here because if we double the inertia we also
    ## double the mass (so it cancels out).
    self._arm_Kxx = math.sqrt(self._arm_Ixx / self._m_arm)

    ## Multiple by 2 because we have 2 arms.
    self._rider_Ixx += 2 * self._arm_Ixx

  def _compute_bike_cg(self):
    self._compute_frame_cg()
    self._compute_rider_cg()

    ## Compute the CG of the bike in the x-dimension
    self._m_bike_x = (self._frame_cg_x * self._m_frame +\
                     self._rider_cg_x * self._m_rider) /\
                    (self._m_frame + self._m_rider)

    ## Compute the CG of the bike in the y-dimension
    self._m_bike_z = (self._frame_cg_z * self._m_frame +\
                     self._rider_cg_z * self._m_rider) /\
                    (self._m_frame + self._m_rider)

  def _compute_bike_radius_of_gyration(self):
    ## First compute the rider's radius of gyration component.
    self._compute_rider_radius_of_gyration()

    self._bike_Kxx = math.sqrt(
      ((self._rider_Kxx ** 2) * (self._m_rider / self._m_bike)) + 
      ((self._frame_cg_z ** 2) * (self._m_frame / self._m_bike)) + 
      ((self._Rf ** 2) * (self._m_front_wheel / self._m_bike)) +
      ((self._Rr ** 2) * (self._m_rear_wheel / self._m_bike)) +
      ((self._Cz ** 2) * (self._m_crank / self._m_bike)))

    '''
    ## Adding this for now to make things match the findings of the team over
    ## the years.
    self._bike_Kxx = self._bike_Kxx / 2
    '''

  def _compute_chain_stays(self):
    '''
    chainstay_slope = (self._Cz - self._Rr) / (self._A + self._Cx)
    chainstay_bottom_x = 0
    chainstay_bottom_z = self._Rr
    chainstay_z_intercept = chainstay_bottom_z -\
                            chainstay_slope * chainstay_bottom_x

    a = chainstay_slope * chainstay_slope + 1
    b = 2 * (chainstay_z_intercept - self._Rr) * chainstay_slope - 2 * self._A
    c = self._A * self._A + (chainstay_z_intercept - self._Rr) *\
        (chainstay_z_intercept - self._Rr) - (self._Rr * self._Rr)

    descrim = b * b - 4 * a * c

    if descrim < 0 or (descrim > 0 and self._Cx < 0):
    '''
    self._t2x = (self._A + self._Cx) / 2
    self._t2z = ((self._Cz - self._Rr) / 2) + self._Rr
    self._t2l = 2 * math.sqrt((self._A + self._Cx) *\
                              (self._A + self._Cx) +\
                              (self._Cz - self._Rr) * (self._Cz - self._Rr))
  
  def _compute_control_sensitivity(self, control_sensitivity, top_speed):
    control_sensitivity.clear()
    for v in range(0, top_speed):
      control_sensitivity.append((self._k4 * v) /\
                                 (self._Rh + (self._k3 / self._Rh) *\
                                             (-self._k1 + self._k2 * v * v)))

  def _compute_control_spring(self, control_spring, top_speed):
    control_spring.clear()
    for v in range(0, top_speed):
      control_spring.append(self._k1 - self._k2 * (v * v))

  def _compute_crank(self):
    ## Crank
    crank_x = self._Cx + self._A
    crank_z = self._Cz

  def _compute_down_tube(self):
    if (self._Cx >= 0):
      self._t5x = (((self._A + self._Cx) - self._fork_top_x) / 2) + self._fork_top_x
    else:
      self._t5x = ((self._fork_top_x - (self._Cx + self._A)) / 2) +\
                  (self._Cx + self._A)

    if (self._Cz >= self._fork_top_z):
      self._t5z = (self._Cz - self._fork_top_z) / 2 + self._fork_top_z
    else:
      self._t5z = (self._fork_top_z - self._Cz) / 2 + self._Cz

    self._t5l = math.sqrt((self._fork_top_z - self._t5z) *\
                          (self._fork_top_z - self._t5z) +\
                          (self._fork_top_x - self._t5x) *\
                          (self._fork_top_x - self._t5x))

  def _compute_fork(self):
    ## Compute fork
    gamma = (math.pi / 2) + self._beta
    fork_slope = math.tan(gamma)
    self._fork_bottom_x = self._A + self._e * math.cos(math.pi + self._beta)
    self._fork_bottom_z = self._Rf + self._e * math.sin(math.pi + self._beta)
    fork_intercept = self._fork_bottom_z - fork_slope * self._fork_bottom_x

    a = fork_slope * fork_slope + 1
    b = 2 * (fork_intercept - self._Rf) * fork_slope - 2 * self._A
    c = self._A * self._A + (fork_intercept - self._Rf) *\
        (fork_intercept - self._Rf) - (self._Rf * self._Rf)

    descrim = b * b - 4 * a * c

    x_1 = 0
    z_1 = 0
    x_2 = 0
    z_2 = 0

    ## If the fork crosses the wheel
    if (descrim >= 0):
      descrim = math.sqrt(b * b - 4 * a * c)

      ## First position the fork crosses the front wheel (if assumed infinite
      ## length)
      x_1 = (-b + descrim) / (2 * a)
      z_1 = fork_slope * x_1 + fork_intercept

      ## Second position the fork crosses the front wheel (if assumed infinite
      ## length)
      x_2 = (-b - descrim) / (2 * a)
      z_2 = fork_slope * x_2 + fork_intercept
    else:
      #print('Fork does not cross the wheel (too much fork offset) error.')
      return False

    ## Points where the fork crosses the front wheel
    #self._ax.plot([x_1, x_2], [z_1, z_2], 'go')

    self._fork_top_x = 0
    self._fork_top_z = 0
    self._t3x = 0
    self._t3z = 0

    if (self._Hz > 2 * self._Rf):
      self._fork_top_x = (self._Hz - fork_intercept) / fork_slope
      self._fork_top_z = self._Hz
    else:
      if (z_1 > z_2):
        self._fork_top_x = x_1
        self._fork_top_z = z_1
      else:
        self._fork_top_x = x_2
        self._fork_top_z = z_2

    self._t3x = (self._fork_top_x - self._fork_bottom_x) / 2 + self._fork_bottom_x
    self._t3z = (self._fork_top_z - self._fork_bottom_z) / 2 + self._fork_bottom_z
    self._t3l = 2 * math.sqrt((self._fork_bottom_x - self._fork_top_x) *\
                              (self._fork_bottom_x - self._fork_top_x) +\
                              (self._fork_top_z - self._fork_bottom_z) *\
                              (self._fork_top_z - self._fork_bottom_z))
    
  def _compute_frame_components(self):
    self._compute_crank()
    self._compute_seat_stays()
    self._compute_chain_stays()
    self._compute_fork()
    self._compute_top_tube()
    self._compute_down_tube()
    self._compute_seat()

  def _compute_frame_cg(self):
    ## Compute the masses of each tube
    total_tube_length = self._t1l + self._t2l + self._t3l + self._t4l + self._t5l
    self._t1m = (self._t1l / total_tube_length) * self._m_frame
    self._t2m = (self._t2l / total_tube_length) * self._m_frame
    self._t3m = (self._t3l / total_tube_length) * self._m_frame
    self._t4m = (self._t4l / total_tube_length) * self._m_frame
    self._t5m = (self._t5l / total_tube_length) * self._m_frame

    ## Compute the CG of the frame in the x-dimension
    self._frame_cg_x = (self._t1m * self._t1x +\
                       self._t2m * self._t2x +\
                       self._t3m * self._t3x +\
                       self._t4m * self._t4x +\
                       self._t5m * self._t5x +\
                       self._A * self._m_front_wheel +\
                       (self._A + self._Cx) * self._m_crank) /\
     (self._m_frame + self._m_crank + self._m_front_wheel + self._m_rear_wheel)

    ## Compute the CG of the frame in the y-dimension
    self._frame_cg_z = (self._t1m * self._t1z +\
                       self._t2m * self._t2z +\
                       self._t3m * self._t3z +\
                       self._t4m * self._t4z +\
                       self._t5m * self._t5z +\
                       self._Rr * self._m_rear_wheel +\
                       self._Rf * self._m_front_wheel +\
                       self._Cz * self._m_crank) /\
      (self._m_frame + self._m_crank + self._m_front_wheel + self._m_rear_wheel)

  def _compute_head(self):
    x_prime = (self._torso_length + (self._head_diameter / 2)) *\
              math.cos(math.pi - self._alpha - self._theta) -\
              self._hip_center_delta_x

    z_prime = (self._torso_length + (self._head_diameter / 2)) *\
              math.sin(math.pi - self._alpha - self._theta) +\
              self._hip_center_delta_z

    self._head_cg_x = self._Hx - x_prime
    self._head_cg_z = self._Hz + z_prime

  def _compute_head_inertia_about_global_x_axis(self):
    ## Compute the head's inertia about its own CG. Note that we are idealizing
    ## the head as a sphere (which is where the below equation is coming from).
    head_local_Ixx = (2 / 5.0) * self._m_head * ((self._head_diameter / 2) ** 2)

    ## Use parallel axis theorum to shift the head's Ixx to be around the
    ## global x-axis.
    self._head_Ixx = head_local_Ixx + self._m_head * (self._head_cg_z ** 2)

    ## Radius of gyration about the wheel contact patch
    self._head_Kxx = math.sqrt(self._head_Ixx / self._m_head)

    ## Add the head's inertia to the overall rider's inertia.
    self._rider_Ixx += self._head_Ixx

  def _compute_legs(self):
    ## Leg
    self._leg_start_x = self._Hx + self._hip_center_delta_x
    self._leg_start_z = self._Hz + self._hip_center_delta_z
    self._leg_end_x = self._Hx + self._leg_length *\
                     math.cos(self._theta) + self._hip_center_delta_x

    ## Need this check to account for the rider being "pushed down" when their
    ## seat is angled downward.
    if self._hip_center_delta_z < 0:
      self._leg_end_z = self._Hz + self._leg_length *\
                       math.sin(self._theta)
    else:
      self._leg_end_z = self._Hz + self._leg_length *\
                       math.sin(self._theta) + self._hip_center_delta_z

    self._leg_cg_x = self._leg_start_x - (self._leg_start_x - self._leg_end_x) / 2
    self._leg_cg_z = self._leg_start_z - (self._leg_start_z - self._leg_end_z) / 2

  def _compute_leg_inertia_about_global_x_axis(self):
    ## Compute the local inertia values in the x,y,z directions. Note that we
    ## are idealizing the leg as a cylinder of constant diameter (which is where
    ## the below equations come from).
    leg_local_Ixx = (1 / 4.0) * self._m_leg *\
                    ((self._leg_diameter / 2) ** 2) + (1 / 12.0) * self._m_leg *\
                    (self._leg_length ** 2)
    leg_local_Iyy = (1 / 4.0) * self._m_leg *\
                    ((self._leg_diameter / 2) ** 2) + (1 / 12.0) * self._m_leg *\
                    (self._leg_length ** 2)
    leg_local_Izz = (1 / 2.0) * self._m_leg * ((self._leg_diameter / 2) ** 2)

    ## Compute local torso inertia tensor.
    leg_local_inertia_tensor =\
                    np.matrix([[leg_local_Ixx,        0,              0      ],
                               [      0,        leg_local_Iyy,        0      ],
                               [      0,              0,        leg_local_Izz]])

    ## Define the global coordinate system for reference.
    global_ref = np.matrix([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]])

    ## Create rotation matrix to dot with the global reference to create the
    ## final rotation matrix which will take our local inertia tensor and rotate
    ## it to align with the global coordinate system.
    local_leg_ref = np.matrix([[-math.sin(self._theta), 0,  math.cos(self._theta)],
                               [           0,          1,            0         ],
                               [-math.cos(self._theta), 0, -math.sin(self._theta)]])

    ## Compute final inertia rotation matrix to rotate the local inertia tensor
    ## to align with the global coordinate system.
    leg_rotation_matrix = global_ref * (local_leg_ref.transpose())

    ## Rotate local inertia tensor to align with the global coordinate system.
    leg_rotated_inertia_tensor = leg_rotation_matrix *\
                                 leg_local_inertia_tensor *\
                                 (leg_rotation_matrix.transpose())

    ## Use parallel axis theorum to shift the rotated inertia tensor to be about
    ## the global x-axis. Note that we are grabbing the 0th item in the tensor
    ## because we only care about Ixx.
    self._leg_Ixx = leg_rotated_inertia_tensor.item(0) +\
                   self._m_leg * ((((self._torso_width / 2) -\
                                   (self._leg_diameter / 2)) ** 2) +\
                                 (self._leg_cg_z ** 2))

    ## Radius of gyration about the wheel contact patch. Note that we don't
    ## have to multiple by 2 here because if we double the inertia we also
    ## double the mass (so it cancels out).
    self._leg_Kxx = math.sqrt(self._leg_Ixx / self._m_leg)

    ## Multiple by 2 because the rider usually has 2 legs.
    self._rider_Ixx += 2 * self._leg_Ixx

  def _compute_rider_cg(self):
    ## Compute the CG of the rider in the x-dimension
    self._rider_cg_x = ((self._head_cg_x * self._m_head) +\
                       (self._torso_cg_x * self._m_torso) +\
                       2 * (self._leg_cg_x * self._m_leg) +\
                       2 * (self._arm_cg_x * self._m_arm)) / self._m_rider

    ## Compute the CG of the rider in the y-dimension
    self._rider_cg_z = ((self._head_cg_z * self._m_head) +\
                       (self._torso_cg_z * self._m_torso) +\
                       2 * (self._leg_cg_z * self._m_leg) +\
                       2 * (self._arm_cg_z * self._m_arm)) / self._m_rider

  def _compute_rider_components(self):
    self._compute_head()
    self._compute_torso()
    self._compute_legs()
    self._compute_arms()
    self._compute_rider_cg()

  def _compute_rider_radius_of_gyration(self):
    self._rider_Ixx = 0.0
    self._compute_head_inertia_about_global_x_axis()
    self._compute_torso_inertia_about_global_x_axis()
    self._compute_leg_inertia_about_global_x_axis()
    self._compute_arm_inertia_about_global_x_axis()

    self._rider_Kxx =\
      math.sqrt(((self._head_Kxx ** 2) * (self._m_head / self._m_rider)) +\
                ((self._torso_Kxx ** 2) * (self._m_torso / self._m_rider)) +\
                2 * ((self._leg_Kxx ** 2) * (self._m_leg / self._m_rider)) +\
                2 * ((self._arm_Kxx ** 2) * (self._m_arm / self._m_rider)))

  def _compute_seat(self):
    ## Seat Back
    self._phi = math.pi - self._alpha - self._theta
    self._seat_back_start_x = self._Hx
    self._seat_back_start_z = self._Hz
    self._seat_back_end_x = self._Hx - self._torso_length * math.cos(self._phi)
    self._seat_back_end_z = self._Hz + self._torso_length * math.sin(self._phi)

    ## Lower Seat
    self._seat_bottom_start_x = self._Hx
    self._seat_bottom_start_z = self._Hz

    #torso_delta_x = self._torso_depth * math.cos(self._alpha - (math.pi / 2) + self._theta)
    #torso_delta_z = self._torso_depth * math.sin(self._alpha - (math.pi / 2) + self._theta) 
    #self._seat_bottom_end_x = self._Hx + torso_delta_x
    #self._seat_bottom_end_z = self._Hz + torso_delta_z
    self._seat_bottom_end_x = self._Hx + self._torso_depth * math.cos(self._theta)
    self._seat_bottom_end_z = self._Hz + self._torso_depth * math.sin(self._theta)

    #self._seat_bottom_end_x = self._Hx + (self._leg_length / 4) * math.cos(self._theta)
    #self._seat_bottom_end_z = self._Hz + (self._leg_length / 4) * math.sin(self._theta)

  def _compute_seat_stays(self):
    ## Seat Stay
    self._t1x = self._Hx / 2
    self._t1z = ((self._Hz - self._Rr) / 2) + self._Rr
    self._t1l = 2 * math.sqrt(\
    (self._Hz - self._Rr) * (self._Hz - self._Rr) + self._Hx * self._Hx)

  def _compute_top_tube(self):
    self._t4x = (self._fork_top_x - self._Hx) / 2 + self._Hx
    self._t4z = (self._fork_top_z - self._Hz) / 2 + self._Hz
    self._t4l = math.sqrt((self._fork_top_x - self._Hx) * (self._fork_top_x -
    self._Hx) + (self._fork_top_z - self._Hz) * (self._fork_top_z - self._Hz))

  def _compute_torso(self):
    self._phi = math.pi - self._alpha - self._theta
    self._torso_start_x = self._Hx + self._hip_center_delta_x
    self._torso_start_z = self._Hz + self._hip_center_delta_z
    self._torso_end_x = self._Hx + self._hip_center_delta_x -\
                       self._torso_length * math.cos(self._phi)
    self._torso_end_z = self._Hz + self._hip_center_delta_z +\
                       self._torso_length * math.sin(self._phi)
    self._torso_cg_x = self._Hx + self._hip_center_delta_x -\
                      (self._torso_length / 2) * math.cos(self._phi)
    self._torso_cg_z = self._Hz + self._hip_center_delta_z +\
                      (self._torso_length / 2) * math.sin(self._phi)

  def _compute_torso_inertia_about_global_x_axis(self):
    ## Compute the local inertia values in the x,y,z directions. Note that we
    ## are idealizing the torso as a cuboid (which is where the below equations
    ## come from).
    torso_local_Ixx = (1 / 12.0) * self._m_torso * ((self._torso_width ** 2) +\
                                                   (self._torso_length ** 2))
    torso_local_Iyy = (1 / 12.0) * self._m_torso * ((self._torso_depth ** 2) +\
                                                   (self._torso_length ** 2))
    torso_local_Izz = (1 / 12.0) * self._m_torso * ((self._torso_width ** 2) +\
                                                   (self._torso_depth ** 2))
    ## Compute local torso inertia tensor.
    torso_local_inertia_tensor =\
                np.matrix([[torso_local_Ixx,         0,              0        ],
                           [       0,         torso_local_Iyy,       0        ],
                           [       0,                0,        torso_local_Izz]])

    ## Define the global coordinate system for reference.
    global_ref = np.matrix([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]])

    ## Create rotation matrix to dot with the global reference to create the
    ## final rotation matrix which will take our local inertia tensor and rotate
    ## it to align with the global coordinate system.
    local_torso_ref = np.matrix([[math.sin(self._phi),  0, math.cos(self._phi)],
                                 [         0,          1,          0        ],
                                 [-math.cos(self._phi), 0, math.sin(self._phi)]])

    ## Compute final inertia rotation matrix to rotate the local inertia tensor
    ## to align with the global coordinate system.
    torso_rotation_matrix = global_ref * (local_torso_ref.transpose())

    ## Rotate local inertia tensor to align with the global coordinate system.
    torso_rotated_inertia_tensor = torso_rotation_matrix *\
                                   torso_local_inertia_tensor *\
                                   (torso_rotation_matrix.transpose())

    ## Use parallel axis theorum to shift the rotated inertia tensor to be about
    ## the global x-axis. Note that we are grabbing the 0th item in the tensor
    ## because we only care about Ixx.
    self._torso_Ixx = torso_rotated_inertia_tensor.item(0) +\
                     self._m_torso * (self._torso_cg_z ** 2)

    ## Radius of gyration about the wheel contact patch.
    self._torso_Kxx = math.sqrt(self._torso_Ixx / self._m_torso)

    ## Add the torso's inertia to the overall rider's inertia
    self._rider_Ixx += self._torso_Ixx

  def _fit_rider_to_bike(self):
    angle_value = ((self._Cz - self._Hz) / (self._leg_length - self._Cr))
    
    ## Check for invalid angle values which would signify that the rider cannot
    ## fit on the bike.
    if angle_value < -1.0 or angle_value > 1.0:
        return False
        
    ## Compute the angle of the seat bottom relative to the ground plane.
    theta_prime = math.asin(angle_value)

    ## Compute the angle of the seat bottom relative to the ground plane,
    ## adjusting for the thickness of the rider's legs.
    angle_value = (self._Cz - ((self._leg_diameter / 2) *\
                            math.cos(theta_prime)) - self._Hz) /\
                            (self._leg_length - self._Cr)
    
    ## Check for invalid angle values which would signify that the rider cannot
    ## fit on the bike.
    if angle_value < -1.0 or angle_value > 1.0:
        return False
    self._theta = math.asin(angle_value)

    ## Compute the distance between the seat pivot and the center of the rider's
    ## hip.
    self._hip_center_delta_x = (self._torso_depth / 2) *\
                              math.cos(self._alpha - (math.pi / 2) + self._theta)
    self._hip_center_delta_z = (self._torso_depth / 2) *\
                              math.sin(self._alpha - (math.pi / 2) + self._theta) +\
                              (math.cos(self._theta) * (self._leg_diameter / 2))

    ## Compute the seat offset in the x-direction.
    self._Hx = self._A + self._Cx - math.cos(self._theta) *\
               (self._leg_length - self._Cr) - self._hip_center_delta_x

    ## Compute the total mass of the bike with the rider.
    self._m_bike = self._m_frame + + self._m_rider + self._m_crank +\
                   self._m_front_wheel + self._m_rear_wheel

    ## Compute the locations of all the frame components.
    self._compute_frame_components()

    ## Compute all the locations of the rider's components and adjust the
    ## frame's seat location as well.
    self._compute_rider_components()

    ## Compute the bike's overall CG (frame + rider)
    self._compute_bike_cg()

    ## Compute the bike's overall inertias and radius of gyration about the
    ## ground plane (wheel contact patch).
    self._compute_bike_radius_of_gyration()

    return self._rider_fits_on_bike()

  def _plot_arms(self, color):
    ## Plot Arm Centerline
    self._ax.plot([self._arm_start_x, self._arm_end_x],\
             [self._arm_start_z, self._arm_end_z], color + '-')

    ## Plot Arm CG
    self._ax.plot([self._arm_cg_x], [self._arm_cg_z], color + 'x')

    return BoundingBox([self._arm_start_x, self._arm_start_z],
                       [self._arm_end_x, self._arm_end_z])

  def _plot_bike(self, ax, color):
    ## Get the figure and axis to plot on.
    self._fig = plt.gcf()
    self._ax = ax

    bounding_boxes = []

    ## Plot all the components
    bounding_boxes.append(self._plot_rider_components(color))
    bounding_boxes.append(self._plot_frame_components())
    self._plot_bike_cg()
    self._plot_bike_radius_of_gyration(color)

    merged_bb = BoundingBox([0, 0], [0, 0])
    for bounding_box in bounding_boxes:
      merged_bb.merge(bounding_box)

    '''
    print('merged_bb -- lower_left: [' + str(merged_bb._lower_left_x) + ', ' +\
          str(merged_bb._lower_left_y) + ']')
    print('merged_bb -- top_right : [' + str(merged_bb._top_right_x) + ', ' +\
          str(merged_bb._top_right_y) + ']')
    '''

    ## Common bounding box for a bike. Will need to update this later so it
    ## expands and contracts with actual bike size.
    self._ax.set_xlim([merged_bb._lower_left_x - 0.2, merged_bb._top_right_x + 0.2])
    self._ax.set_ylim([merged_bb._lower_left_y - 0.2, merged_bb._top_right_y + 0.2])
    self._ax.set_aspect('equal')
    ax.set_xlabel('[m]')
    ax.set_ylabel('[m]')
    ax.grid(True)

  def _plot_bike_cg(self):
    ## Plot the CG of the bike
    self._ax.plot([self._m_bike_x], [self._m_bike_z], 'ko')

  def _plot_bike_radius_of_gyration(self, color='y'):
    ## Plot bike Kxx as a line across the screen
    self._ax.plot([0, self._A], [self._bike_Kxx, self._bike_Kxx], color + '--')

  def _plot_chain_stays(self):
      self._ax.plot([0, (self._A + self._Cx)], [self._Rr, self._Cz], 'r-')
      self._ax.plot([self._t2x], [self._t2z], 'rx')

      return BoundingBox([0, self._Rr], [(self._A + self._Cx), self._Cz])

  def _plot_crank(self):
    crank_x = self._Cx + self._A
    crank_z = self._Cz
    crank = plt.Circle((crank_x, crank_z),\
                       self._Cr,\
                       fill = False,\
                       color='m')
    self._ax.plot([crank_x], [crank_z], 'm+')
    self._ax.add_artist(crank)

    return BoundingBox([crank_x - self._Cr, crank_z - self._Cr],
                       [crank_x + self._Cr, crank_z + self._Cr])

  def _plot_down_tube(self):
    self._ax.plot([self._fork_top_x, self._A + self._Cx],\
             [self._fork_top_z, self._Cz], 'r-')
    self._ax.plot([self._t5x], [self._t5z], 'rx')

    return BoundingBox([self._fork_top_x, self._fork_top_z],
                       [(self._A + self._Cx), self._Cz])

  def _plot_fork(self):
    ## Bottom of the fork
    #self._ax.plot([self._fork_bottom_x], [self._fork_bottom_z], 'yo')

    self._ax.plot([self._fork_bottom_x, self._fork_top_x],\
             [self._fork_bottom_z, self._fork_top_z], 'r-')
    self._ax.plot([self._t3x], [self._t3z], 'rx')

    return BoundingBox([self._fork_bottom_x, self._fork_bottom_z],
                       [self._fork_top_x, self._fork_top_z])

  def _plot_frame_cg(self):
    ## Plot the CG of the frame
    self._ax.plot([self._frame_cg_x], [self._frame_cg_z], 'ro')

  def _plot_frame_components(self):
    bounding_boxes = []
    bounding_boxes.append(self._plot_front_wheel())
    bounding_boxes.append(self._plot_rear_wheel())
    bounding_boxes.append(self._plot_crank())
    bounding_boxes.append(self._plot_seat_stays())
    bounding_boxes.append(self._plot_chain_stays())
    bounding_boxes.append(self._plot_fork())
    bounding_boxes.append(self._plot_top_tube())
    bounding_boxes.append(self._plot_down_tube())
    bounding_boxes.append(self._plot_seat())
    self._plot_frame_cg()

    merged_bb = BoundingBox([0, 0], [0, 0])
    for bounding_box in bounding_boxes:
      merged_bb.merge(bounding_box)

    return merged_bb

  def _plot_front_wheel(self):
    front_wheel_x = self._A
    front_wheel_z = self._Rf
    front_wheel = plt.Circle((front_wheel_x, front_wheel_z),\
                             self._Rf,\
                             fill = False,\
                             color='k')
    self._ax.plot([front_wheel_x], [front_wheel_z], 'k+')
    self._ax.add_artist(front_wheel)

    return BoundingBox([(front_wheel_x - self._Rf), 0],
                       [(front_wheel_x + self._Rf), (2 * self._Rf)])

  def _plot_head(self, color):
    head_radius = self._head_diameter / 2
    head = plt.Circle((self._head_cg_x, self._head_cg_z),\
                      head_radius,\
                      fill = False,\
                      color=color)

    ## Plot Head Outline
    self._ax.add_artist(head)

    ## Plot Head CG
    self._ax.plot([self._head_cg_x], [self._head_cg_z], color + 'x')
    
    return BoundingBox([(self._head_cg_x - head_radius), self._head_cg_z - head_radius],
                       [(self._head_cg_x + head_radius), self._head_cg_z + head_radius])

  def _plot_legs(self, color):
    ## Plot Leg Centerline
    self._ax.plot([self._leg_start_x, self._leg_end_x],\
             [self._leg_start_z, self._leg_end_z], color + '-')

    ## Plot Leg CG
    self._ax.plot([self._leg_cg_x], [self._leg_cg_z], color + 'x')

    return BoundingBox([self._leg_start_x, self._leg_start_z],
                       [self._leg_end_x, self._leg_end_z])

  def _plot_rear_wheel(self):
    rear_wheel_x = 0.0
    rear_wheel_z = self._Rr
    rear_wheel = plt.Circle((rear_wheel_x, rear_wheel_z),\
                            self._Rr,\
                            fill = False,\
                            color='k')
    self._ax.plot([rear_wheel_x], [rear_wheel_z], 'k+')
    self._ax.add_artist(rear_wheel)

    return BoundingBox([(rear_wheel_x - self._Rr), 0],
                       [(rear_wheel_x + self._Rr), (2 * self._Rr)])

  def _plot_rider_cg(self, color):
    ## Plot the CG of the rider 
    self._ax.plot([self._rider_cg_x], [self._rider_cg_z], color + 'o')

  def _plot_rider_radius_of_gyration(self):
    ## Plot rider Kxx as a line across the screen
    self._ax.plot([0, self._A], [self._rider_Kxx, self._rider_Kxx], 'k*-')

  def _plot_rider_components(self, color):
    bounding_boxes = []
    bounding_boxes.append(self._plot_head(color))
    bounding_boxes.append(self._plot_torso(color))
    bounding_boxes.append(self._plot_legs(color))
    bounding_boxes.append(self._plot_arms(color))
    self._plot_rider_cg(color)

    merged_bb = BoundingBox([0,0], [0,0])
    for bounding_box in bounding_boxes:
      merged_bb.merge(bounding_box)

    return merged_bb

  def _plot_seat(self):
    ## Upper Seat
    self._ax.plot([self._seat_back_start_x, self._seat_back_end_x],\
             [self._seat_back_start_z, self._seat_back_end_z], 'c-')

    ## Lower Seat
    self._ax.plot([self._seat_bottom_start_x, self._seat_bottom_end_x],\
             [self._seat_bottom_start_z, self._seat_bottom_end_z], 'c-')

    return BoundingBox([self._seat_back_start_x, self._seat_back_start_z],
                       [self._seat_back_end_x, self._seat_back_end_z])

  def _plot_seat_stays(self):
    self._ax.plot([0, self._Hx], [self._Rr, self._Hz], 'r-')
    self._ax.plot([self._t1x], [self._t1z], 'rx')

    return BoundingBox([0, self._Rr], [self._Hx, self._Hz])

  def _plot_top_tube(self):
    self._ax.plot([self._fork_top_x, self._Hx], [self._fork_top_z, self._Hz], 'r-')
    self._ax.plot([self._t4x], [self._t4z], 'rx')

    return BoundingBox([self._fork_top_x, self._fork_top_z], [self._Hx, self._Hz])

  def _plot_torso(self, color):
    ## Plot torso centerline
    self._ax.plot([self._torso_start_x, self._torso_end_x],\
             [self._torso_start_z, self._torso_end_z], color + '-')

    ## Plot Torso CG
    self._ax.plot([self._torso_cg_x], [self._torso_cg_z], color + 'x')

    return BoundingBox([self._torso_start_x, self._torso_start_z],
                       [self._torso_end_x, self._torso_end_z])

  def _front_wheel_clears_torso(self):
    ## First check if the seat-back intersects the rear wheel, if it does then
    ## we know the rider's back does as well.
    seat_slope = math.tan(self._alpha + self._theta)
    seat_z_intercept = self._seat_back_start_z - seat_slope * self._seat_back_start_x

    ## Ensure the front wheel doesn't go through the rider's back
    a = seat_slope * seat_slope + 1
    b = 2 * (seat_z_intercept - self._Rf) * seat_slope - 2 * self._A
    c = self._A * self._A + (seat_z_intercept - self._Rf) * (seat_z_intercept -\
     self._Rf) - (self._Rf * self._Rf)

    descrim = b * b - 4 * a * c

    if descrim >= 0:
      descrim = math.sqrt(descrim)

      ## Compute the position the seat-back intersects the front wheel
      ## (assuming an infinite length seat back)
      x_1 = (-b + descrim) / (2 * a)
      z_1 = seat_slope * x_1 + seat_z_intercept
      x_2 = (-b - descrim) / (2 * a)
      z_2 = seat_slope * x_2 + seat_z_intercept

      #print('x_1, z_1: ' + str(x_1) + ', ' + str(z_1))
      #print('x_2, z_2: ' + str(x_2) + ', ' + str(z_2))
      #print('seat_bottom_start_x: ' + str(self._seat_bottom_start_x))
      #print('seat_bottom_end_x: ' + str(self._seat_bottom_end_x))

      if x_1 <= self._seat_back_start_x and x_2 >= self._seat_back_end_x:
        return False

      if x_1 >= self._seat_back_start_x and x_2 <= self._seat_back_end_x:
        return False

      if x_2 <= self._seat_back_start_x and x_1 >= self._seat_back_end_x:
        return False

      if x_2 >= self._seat_back_start_x and x_1 <= self._seat_back_end_x:
        return False

    ## Next, we check that the seat bottom doesn't intersect the front wheel.
    seat_slope = math.tan(self._theta)
    seat_z_intercept = self._seat_bottom_start_z - seat_slope * self._seat_bottom_start_x

    a = seat_slope * seat_slope + 1
    b = 2 * (seat_z_intercept - self._Rf) * seat_slope - 2 * self._A
    c = self._A * self._A + (seat_z_intercept - self._Rf) * (seat_z_intercept -\
     self._Rf) - (self._Rf * self._Rf)

    descrim = b * b - 4 * a * c

    if descrim >= 0:
      descrim = math.sqrt(descrim)

      ## Compute the position the seat-bottom intersects the front wheel
      ## (assuming an infinite length seat back)
      x_1 = (-b + descrim) / (2 * a)
      z_1 = seat_slope * x_1 + seat_z_intercept
      x_2 = (-b - descrim) / (2 * a)
      z_2 = seat_slope * x_2 + seat_z_intercept

      #print('x_1, z_1: ' + str(x_1) + ', ' + str(z_1))
      #print('x_2, z_2: ' + str(x_2) + ', ' + str(z_2))
      #print('seat_bottom_start_x: ' + str(self._seat_bottom_start_x))
      #print('seat_bottom_end_x: ' + str(self._seat_bottom_end_x))

      if x_1 <= self._seat_bottom_start_x and x_2 >= self._seat_bottom_end_x:
        return False

      if x_1 >= self._seat_bottom_start_x and x_2 <= self._seat_bottom_end_x:
        return False

      if x_2 <= self._seat_bottom_start_x and x_1 >= self._seat_bottom_end_x:
        return False

      if x_2 >= self._seat_bottom_start_x and x_1 <= self._seat_bottom_end_x:
        return False

    ## Finally, check to see that the entire rider isn't inside the wheel.
    if self._Rf >= math.sqrt(math.pow(self._seat_bottom_start_x - self._A, 2) +\
                             math.pow(self._seat_bottom_start_z - self._Rf, 2)):
      return False

    return True

  def _rear_wheel_clears_torso(self):
    ## First check if the seat-back intersects the rear wheel, if it does then
    ## we know the rider's back does as well.
    seat_slope = math.tan(self._alpha + self._theta)
    seat_z_intercept = self._seat_back_start_z - seat_slope * self._seat_back_start_x

    a = seat_slope * seat_slope + 1
    b = 2 * (seat_z_intercept - self._Rr) * seat_slope
    c = (seat_z_intercept - self._Rr) * (seat_z_intercept - self._Rr) -\
     (self._Rr * self._Rr)

    descrim = b * b - 4 * a * c

    if descrim >= 0:
      descrim = math.sqrt(descrim)

      ## Compute the position the seat-back intersects the rear wheel
      ## (assuming an infinite length seat back)
      x_1 = (-b + descrim) / (2 * a)
      z_1 = seat_slope * x_1 + seat_z_intercept
      x_2 = (-b - descrim) / (2 * a)
      z_2 = seat_slope * x_2 + seat_z_intercept

      #print('x_1, z_1: ' + str(x_1) + ', ' + str(z_1))
      #print('x_2, z_2: ' + str(x_2) + ', ' + str(z_2))
      #print('seat_bottom_start_x: ' + str(self._seat_bottom_start_x))
      #print('seat_bottom_end_x: ' + str(self._seat_bottom_end_x))

      if x_1 <= self._seat_back_start_x and x_2 >= self._seat_back_end_x:
        return False

      if x_1 >= self._seat_back_start_x and x_2 <= self._seat_back_end_x:
        return False

      if x_2 <= self._seat_back_start_x and x_1 >= self._seat_back_end_x:
        return False

      if x_2 >= self._seat_back_start_x and x_1 <= self._seat_back_end_x:
        return False

    ## Next, we check that the seat- bottom doesn't intersect the rear wheel.
    seat_slope = math.tan(self._theta)
    seat_z_intercept = self._seat_bottom_start_z- seat_slope * self._seat_bottom_start_x

    a = seat_slope * seat_slope + 1
    b = 2 * (seat_z_intercept - self._Rr) * seat_slope
    c = (seat_z_intercept - self._Rr) * (seat_z_intercept - self._Rr) -\
     (self._Rr * self._Rr)

    descrim = b * b - 4 * a * c

    if descrim >= 0:
      descrim = math.sqrt(descrim)

      ## Compute the position the seat-bottom intersects the rear wheel
      ## (assuming an infinite length seat back)
      x_1 = (-b + descrim) / (2 * a)
      z_1 = seat_slope * x_1 + seat_z_intercept
      x_2 = (-b - descrim) / (2 * a)
      z_2 = seat_slope * x_2 + seat_z_intercept

      if x_1 <= self._seat_bottom_start_x and x_2 >= self._seat_bottom_end_x:
        return False

      if x_1 >= self._seat_bottom_start_x and x_2 <= self._seat_bottom_end_x:
        return False

      if x_2 <= self._seat_bottom_start_x and x_1 >= self._seat_bottom_end_x:
        return False

      if x_2 >= self._seat_bottom_start_x and x_1 <= self._seat_bottom_end_x:
        return False

    ## Finally, check to see that the entire rider isn't inside the wheel.
    if self._Rr >= math.sqrt(math.pow(self._seat_bottom_start_x, 2) +\
                             math.pow(self._seat_bottom_start_z - self._Rr, 2)):
      return False

    return True

  def _wheels_clear_riders_head(self):
    #(R0-R1)^2 <= (x0-x1)^2+(y0-y1)^2 <= (R0+R1)^2

    ## Check if the front wheel intersects the rider's head.
    sum_of_diffs = math.pow(self._A - self._head_cg_x, 2) + math.pow(self._Rf - self._head_cg_z, 2)
    if math.pow((self._Rf - (self._head_diameter / 2)), 2) <= sum_of_diffs and\
       math.pow((self._Rf + (self._head_diameter / 2)), 2) >= sum_of_diffs:
       return False

    ## Check if the rear wheel intersects the rider's head.
    sum_of_diffs = math.pow(self._head_cg_x, 2) + math.pow(self._Rr - self._head_cg_z, 2)
    if math.pow((self._Rr - (self._head_diameter / 2)), 2) <= sum_of_diffs and\
       math.pow((self._Rr + (self._head_diameter / 2)), 2) >= sum_of_diffs:
       return False

    return True

  ## Checks that the current bike and rider combination is valid (aka the rider
  ## can actually rach the crank pedals at their farthest throw while staying
  ## in their seat. Additionally checks other cases such as the wheel going
  ## through the rider's body, overlapping wheels, etc.
  ##
  ## Returns True if theh rider can fit on the bike.
  def _rider_fits_on_bike(self):
    if self._wheels_clear_riders_head() == False:
      #print('A wheel intersects the rider\'s head!')
      return False

    ## Check that the rider's torso does not intersect with the front wheel.
    if self._front_wheel_clears_torso() == False:
      #print('Front wheel intersects rider\'s torso!')
      return False

    ## Check that the rider's torso does not intersect with the rear wheel.
    if self._rear_wheel_clears_torso() == False:
      #print('Rear wheel intersects rider\'s torso!')
      return False

    ## Ensure the fork isn't inverted
    if self._fork_top_z < self._fork_bottom_z:
      #print('Fork is inverted!')
      return False

    ## Ensure the wheels don't overlap
    if self._Rf + self._Rr >= self._A:
      #print('Wheels overlap!')
      return False

    if self._leg_length <= (2 * self._Cr):
      #print('Leg length must be greater than crank diameter!')
      return False

    ## Ensure the crank isn't inside the front wheel
    if math.pow(self._Rf, 2) >=\
       math.pow(self._Cx, 2) + math.pow((self._Cz - self._Rf), 2):
      #print('Cranks inside front wheel!')
      return False

    ## Ensure the crank isn't inside the rear wheel
    if math.pow(self._Rr, 2) >=\
       math.pow((self._A + self._Cx), 2) + math.pow((self._Cz - self._Rr), 2):
      #print('Cranks inside rear wheel!')
      return False

    ## Ensure the seat is above the floor plane
    if self._Hz <= 0:
      #print('Rider\'s seat is beneath the floor plane!')
      return False

    ## Ensure the cranks don't hit the ground
    if self._Cz - self._Cr <= 0:
      #print('Cranks go beneath the floor plane!')
      return False

    return True

  ## Updates the internal symbols for each of the bike parameters in
  ## bike_params. Note that we are assuming that the input dictionary will be
  ## param_name -> value, and that all the names below will be present and all
  ## their values will be decimal values.
  def _update_bike_params(self, single_bike_params):
    ## First clear out all variables
    self._clear_bike_params()

    ## Store a copy of the parameters for later lookup.
    self._single_bike_params = copy.deepcopy(single_bike_params)

    ## Bike Parameters
    self._A              = single_bike_params['wheelbase']
    self._alpha          = math.radians(single_bike_params['hip_angle'])
    self._beta           = math.radians(single_bike_params['headtube_angle'])
    self._Cr            = single_bike_params['crank_radius']
    self._Cx            = single_bike_params['crank_x_offset']
    self._Cz            = single_bike_params['crank_z_offset']
    self._e              = single_bike_params['fork_offset']
    self._Hz            = single_bike_params['seat_height']
    self._Rh            = single_bike_params['handlebar_radius']
    self._Rf            = single_bike_params['front_wheel_radius']
    self._Rr            = single_bike_params['rear_wheel_radius']
    self._m_frame        = single_bike_params['frame_mass']
    self._m_crank        = single_bike_params['crank_mass']
    self._m_front_wheel  = single_bike_params['front_wheel_mass']
    self._m_rear_wheel   = single_bike_params['rear_wheel_mass']

  ## Updates the internal symbols for each of the rider parameters in
  ## rider_params, and computes the mass of each of the rider's body parts.
  ## Note that we are assuming that the input dictionary will be
  ## param_name -> value, and that all the names below will be present and all
  ## their values will be decimal values.
  def _update_rider_params(self, rider_params):
    ## Rider Parameters
    self._m_rider        = rider_params['rider_mass']
    self._head_diameter  = rider_params['head_diameter']
    self._torso_length   = rider_params['torso_length']
    self._torso_depth    = rider_params['torso_depth']
    self._torso_width    = rider_params['torso_width']
    self._arm_length     = rider_params['arm_length']
    self._arm_diameter   = rider_params['arm_diameter']
    self._leg_length     = rider_params['leg_length']
    self._leg_diameter   = rider_params['leg_diameter']

    ## Compute the mass of each of the rider's body segments.
    self._m_head   = self._m_rider * self._body_segment_to_mass_percentage['head']
    self._m_torso  = self._m_rider * self._body_segment_to_mass_percentage['torso']
    self._m_arm    = self._m_rider * self._body_segment_to_mass_percentage['arm']
    self._m_leg    = self._m_rider * self._body_segment_to_mass_percentage['leg']

  def plot_control_sensitivity(self, ax, control_sensitivity, formatting,
                               rider_name):
    ## Get the figure and axis to plot on.
    fig = plt.gcf()

    top_speed = len(control_sensitivity)
    '''
    control_spring = []
    control_sensitivity = []
    self.compute_patterson_curves(control_spring, control_sensitivity, top_speed) 
    error = self.compute_sum_of_diff_of_squares(target_control_sensitivity,
                                                control_sensitivity)
    '''

    x_axis_values = range(top_speed)
    ax.set_xlabel('Speed [m/s]')
    ax.set_ylabel('Control Sensitivity []')
    #ax.plot(x_axis_values, target_control_sensitivity, 'ko', label='target')
    ax.plot(x_axis_values, control_sensitivity, formatting, linewidth=2.0, 
            label=rider_name)
    ax.legend(bbox_to_anchor=(1, 1))
    ax.grid(True)

## A class to represent a bounding box, which is used to determine the overall
## plot size for the bicycle's and rider's components.
class BoundingBox:

  def __init__(self, point1, point2):
    self._lower_left_x = min(point1[0], point2[0])
    self._lower_left_y = min(point1[1], point2[1])
    self._top_right_x = max(point1[0], point2[0])
    self._top_right_y = max(point1[1], point2[1])

  ## Take the two points and make a bounding box about them.
  def merge(self, other):
    if other._lower_left_x < self._lower_left_x:
      self._lower_left_x = other._lower_left_x

    if other._lower_left_y < self._lower_left_y:
      self._lower_left_y = other._lower_left_y

    if other._top_right_x > self._top_right_x:
      self._top_right_x = other._top_right_x

    if other._top_right_y > self._top_right_y:
      self._top_right_y = other._top_right_y

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
