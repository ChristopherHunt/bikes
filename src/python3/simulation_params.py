import copy

class SimulationParams:
  'Defines a container for all the input parameters for bicycle simulations.'

  def __init__(self):
    self._bike_params = {}
    self._ga_config = {}
    self._partitioning_attributes = []
    self._partitioning_radius = 0
    self._riders = []
    self._sample_count = 0
    self._target_control_sensitivity = []
    self._top_speed = 0

  @property
  def bike_params(self):
    return self._bike_params; 

  @property
  def ga_config(self):
    return self._ga_config; 

  @property
  def partitioning_attributes(self):
    return self._partitioning_attributes; 

  @property
  def partitioning_radius(self):
    return self._partitioning_radius; 

  @property
  def riders(self):
    return self._riders; 

  @property
  def sample_count(self):
    return self._sample_count; 

  @property
  def target_control_sensitivity(self):
    return self._target_control_sensitivity; 

  @property
  def top_speed(self):
    return self._top_speed; 

  @bike_params.setter
  def bike_params(self, value):
      self._bike_params = copy.deepcopy(value)

  @ga_config.setter
  def ga_config(self, value):
      self._ga_config = copy.deepcopy(value)

  @partitioning_attributes.setter
  def partitioning_attributes(self, value):
      self._partitioning_attributes = copy.deepcopy(value)

  @partitioning_radius.setter
  def partitioning_radius(self, value):
      self._partitioning_radius = copy.deepcopy(value)

  @riders.setter
  def riders(self, value):
      self._riders = copy.deepcopy(value)

  @sample_count.setter
  def sample_count(self, value):
      self._sample_count = copy.deepcopy(value)

  @target_control_sensitivity.setter
  def target_control_sensitivity(self, value):
      self._target_control_sensitivity = copy.deepcopy(value)

  @top_speed.setter
  def top_speed(self, value):
      self._top_speed = value

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
