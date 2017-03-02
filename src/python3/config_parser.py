# parser.py
#!/usr/bin/python3

import copy
import re
import sys

class Parser:
  'Class to parse input strings for the bike plotter. See the description of\
  the parse function for more details.'

  def __init__(self):
    ## Returns a match on strings that lead with a '#' ('  # stuff  ')
    self.comment_line = re.compile('#.*$|\s*$', re.IGNORECASE)

    ## Returns a match on strings with a single param (' param = decimal_value ')
    ## and also allows for trailing comments (' decimal_value  # stuff ')
    self.single_curve_value = re.compile('\s*(-?\d+\.\d*|-?\d+)\s*|\s*#.*$', re.IGNORECASE)

    ## Returns a match on strings with a single param (' param = decimal_value ')
    ## and also allows for trailing comments (' param = decimal_value # stuff ')
    self.single_decimal_param = re.compile('\s*(\w+)\s*=\s*(-?\d+\.\d*|-?\d+)\s*|\s*#.*$', re.IGNORECASE)

    ## Returns a match on strings with a single param (' param = string_value ')
    ## and also allows for trailing comments (' param = string_value # stuff ')
    self.single_string_param = re.compile('\s*(\w+)\s*=\s*(\w+)\s*|\s*#.*$', re.IGNORECASE)

    ## Returns a match on strings with a range of params (' param = x to y by z ')
    ## and also allows for trailing comments (' param = x to y by z # stuff ' )
    self.range_param = re.compile('\s*(\w+)\s*=\s*(-?\d+\.\d*|-?\d+)\s*to\s*(-?\d+\.\d*|-?\d+)\s*by\s*(-?\d+.\d*|-?\d+)\s*|#.*$', re.IGNORECASE)

    ## Returns a match on strings with a set of params (' param = [x, y ,  z] ')
    ## where x, y and z are decimal values. Also allows for trailing comments
    ## (' param = [x, y ,  z] # stuff ' )
    self.set_decimal_param = re.compile('\s*(\w+)\s*=\s*\[\s*(-?\d+\.\d*|-?\d+)(\s*,\s*(-?\d+\.\d*|-?\d+)\s*)*\s*\](\s*$|\s*#.*$)', re.IGNORECASE)
  
    ## Returns a match on strings with a set of params (' param = [x, y ,  z] ')
    ## where x, y and z are string values. Also allows for trailing comments
    ## (' param = [x, y ,  z] # stuff ' )
    self.set_string_param = re.compile('\s*(\w+)\s*=\s*\[\s*(\w+)(\s*,\s*(\w+)\s*)*\s*\](\s*$|\s*#.*$)', re.IGNORECASE)
  
  ## Opens the input_file and creates a mapping of the contents to their values
  ## in the input dictionary. The expected inputs of this dictionary are as
  ## follows:
  ##
  ##    measurement = # 
  ##    measurement = x to y by z
  ##    measurement = [x, y, z]
  ##
  ## The first case defines a single value for the given measurement. The value
  ## in the dictionary for this measurement will be:
  ##
  ##    measurement = [#]
  ##
  ## Where the value is inside a list (with length 1).
  ##
  ## The second case defines a range for the given measurement, as well as a
  ## step size to iterate through that range. The values in the dictionary will
  ## be a list of all possible measurements that fit within that range.
  ##
  ##    measurement = [x, x + z, x + 2z, ... , y]
  ##
  ## Note that if the range is invalid an error will be printed and False will
  ## be returned.
  ##
  ## The third case defines a set of values the user wants to specify for a
  ## given measurement. The values in the dictionary will be this list.
  ##
  ##    measurement = [x, y, z]
  ##
  ## If this function is called on an improperly formated input_file it will
  ## return False to signify that the parse was unsuccessful.
  def parse_bike(self, dictionary, input_file):
    with open(input_file, 'r') as params_file:
      for param_line in params_file:
        ## First check to see if this is purely a comment line or a line with
        ## just whitespace, if so, skip it.
        if self.comment_line.match(param_line):
          continue

        ## Next check if this is a line for a ranged param value.
        match = self.range_param.match(param_line)
        if match:
          if not self._parse_range_param_line(dictionary, match):
            print('Unable to parse improperly formated line in input file <'
                  + input_file + '> -- Improper range on line:')
            print('\'' + param_line.strip() + '\'')
            return False
          continue

        ## Next check if this is a line for a set param value.
        match = self.set_decimal_param.match(param_line)
        if match:
          self._parse_set_decimal_param_line(dictionary, match)
          continue

        ## Next check if this is a line for a single param value.
        match = self.single_decimal_param.match(param_line)
        if match:
          self._parse_single_decimal_param_line_as_list(dictionary, match)
          continue

        ## If none of the lines matched then it was an improperly formated line
        ## so skip it.
        print('Unable to parse improperly formatted line in input file <'
              + input_file + '>:')
        print('\'' + param_line.strip() + '\'')
        return False

      return True

  ## Parses the contents of the input_file as if it contained only decimal
  ## values, appending each to the output_list. Also clears the output_list
  ## prior to starting this to ensure the contents are proper.
  def parse_curve_file(self, output_list, input_file):
    with open(input_file, 'r') as curve_file:
      output_list.clear()
      for line in curve_file:
        ## First check to see if this is purely a comment line or a line with
        ## just whitespace, if so, skip it.
        if self.comment_line.match(line):
          continue

        ## Otherwise, treat this as a float value.
        match = self.single_curve_value.match(line)
        if match:
          self._parse_curve_value_line(output_list, match)

        else:
          ## If none of the lines matched then it was an improperly formated line
          ## so skip it.
          print('Unable to parse improperly formatted line in input file <'
                + input_file + '>:')
          print('\'' + line.strip() + '\'')
          return False
    return True

  ## Opens the input_file and creates a mapping of the contents to their values
  ## in the input dictionary. The expected inputs of this dictionary are as
  ## follows:
  ##
  ##    parameter = # 
  ##    parameter = x to y by z
  ##    parameter = [x, y, z]
  ##
  ## The first case defines a single value for the given parameter. The value
  ## in the dictionary for this measurement will be:
  ##
  ##    parameter = [#]
  ##
  ## Where the value is inside a list (with length 1).
  ##
  ## The second case defines a range for the given parameter, as well as a
  ## step size to iterate through that range. The values in the dictionary will
  ## be a list of all possible parameters that fit within that range.
  ##
  ##    parameter = [x, x + z, x + 2z, ... , y]
  ##
  ## Note that if the range is invalid an error will be printed and False will
  ## be returned.
  ##
  ## The third case defines a set of values the user wants to specify for a
  ## given parameter. The values in the dictionary will be this list.
  ##
  ##    parameter = [x, y, z]
  ##
  ## If this function is called on an improperly formated input_file it will
  ## return False to signify that the parse was unsuccessful.
  def parse_genetic_algorithm_config_file(self, dictionary, input_file):
    with open(input_file, 'r') as params_file:
      for param_line in params_file:
        ## First check to see if this is purely a comment line or a line with
        ## just whitespace, if so, skip it.
        if self.comment_line.match(param_line):
          continue

        ## Next check if this is a line for a ranged param value.
        match = self.range_param.match(param_line)
        if match:
          if not self._parse_range_param_line(dictionary, match):
            print('Unable to parse improperly formated line in input file <'
                  + input_file + '> -- Improper range on line:')
            print('\'' + param_line.strip() + '\'')
            return False
          continue

        ## Next check if this is a line for a set param value.
        match = self.set_decimal_param.match(param_line)
        if match:
          self._parse_set_decimal_param_line(dictionary, match)
          continue

        ## Next check if this is a line for a single param value.
        match = self.single_decimal_param.match(param_line)
        if match:
          self._parse_single_decimal_param_line_as_list(dictionary, match)
          continue

        ## If none of the lines matched then it was an improperly formated line
        ## so skip it.
        print('Unable to parse improperly formatted line in input file <'
              + input_file + '>:')
        print('\'' + param_line.strip() + '\'')
        return False

      return True

  ## Opens the input_file and creates a mapping of the contents to their values
  ## in the input dictionary. The expected inputs of this dictionary are as
  ## follows:
  ##
  ##    parameter = # 
  ##    parameter = [x, y, z]
  ##
  ## The first case defines a single value for the given parameter. The value
  ## in the dictionary for this measurement will be:
  ##
  ##    parameter = [#]
  ##
  ## Where the value is inside a list (with length 1).
  ##
  ## The second case defines a set of values the user wants to specify for a
  ## given parameter. The values in the dictionary will be this list.
  ##
  ##    parameter = [x, y, z]
  ##
  ## If this function is called on an improperly formated input_file it will
  ## return False to signify that the parse was unsuccessful.
  def parse_partitioning_config_file(self, dictionary, input_file):
    with open(input_file, 'r') as params_file:
      for param_line in params_file:
        ## First check to see if this is purely a comment line or a line with
        ## just whitespace, if so, skip it.
        if self.comment_line.match(param_line):
          continue

        ## Next check if this is a line for a set param value.
        match = self.set_string_param.match(param_line)
        if match:
          self._parse_set_string_param_line(dictionary, match)
          continue

        ## Next check if this is a line for a single param value.
        match = self.single_decimal_param.match(param_line)
        if match:
          self._parse_single_decimal_param_line_as_list(dictionary, match)
          continue

        ## If none of the lines matched then it was an improperly formated line
        ## so skip it.
        print('Unable to parse improperly formatted line in input file <'
              + input_file + '>:')
        print('\'' + param_line.strip() + '\'')
        return False

      return True

  ## Opens the input_file and creates a mapping of the contents to their values
  ## in the input dictionary. The expected inputs of this dictionary are as
  ## follows:
  ##
  ##    measurement = value
  ##
  ## This case defines a single value for the given measurement. The value in
  ## the dictionary for this measurement will be:
  ##
  ##    'measurement' --> value
  ##
  ## The resulting dictionary will be appended to the riders_list. If this
  ## function is called on an improperly formated input_file it will return
  ## False to signify that the parse was unsuccessful.
  def parse_riders(self, riders_list, input_file):
    with open(input_file, 'r') as params_file:
      rider_params = {}
      for param_line in params_file:
        ## First check to see if this is purely a comment line or a line with
        ## just whitespace, if so, skip it.
        if self.comment_line.match(param_line):
          continue

        ## Next check if this is a line for a ranged param value.
        match = self.range_param.match(param_line)
        if match:
          ## Return False here because the rider cannot have ranges.
          return False

        ## Next check if this is a line for a set param value.
        match = self.set_decimal_param.match(param_line)
        if match:
          ## Return False here because the rider cannot have sets of values.
          return False

        ## Next check if this is a line for a single decimal param value.
        match = self.single_decimal_param.match(param_line)
        if match:
          self._parse_single_decimal_param_line(rider_params, match)
          continue

        ## Next check if this is a line for a single string param value.
        match = self.single_string_param.match(param_line)
        if match:
          ## If this is the beginning of a new rider config block (specified by
          ## having the param line 'rider_name = name', and there was a previous
          ## rider_config block, then append the previous rider_params to the
          ## riders_list.
          if self._is_new_rider_config(match) and rider_params:
            riders_list.append(copy.deepcopy(rider_params))
            rider_params.clear()

          ## Parse the param_line
          self._parse_single_string_param_line(rider_params, match)
          continue

        ## If none of the lines matched then it was an improperly formated line
        ## so skip it.
        print('Unable to parse improperly formatted line in input file <'
              + input_file + '>:')
        print('\'' + param_line.strip() + '\'')
        return False

      riders_list.append(copy.deepcopy(rider_params))
      return True

  def print_params_to_file(self, params, output_file):
    with open(output_file, 'w') as output:
      for key, value in params.items():
        pass

  ## Populates the list with the single decimal value supplied by match.
  def _parse_curve_value_line(self, output_list, match):
    output_list.append(float(match.group(1)))
      

  ## Populates the dictionary with the single param matching supplied by match.
  def _parse_single_decimal_param_line(self, dictionary, match):
    dictionary[match.group(1)] = float(match.group(2))
      
  ## Populates the dictionary with the single param matching supplied by 'match'
  ## as a list of values.
  def _parse_single_decimal_param_line_as_list(self, dictionary, match):
    value_list = []
    value_list.append(float(match.group(2)))
    dictionary[match.group(1)] = copy.deepcopy(value_list)

  ## Populates the dictionary with the single param matching supplied by 'match'.
  def _is_new_rider_config(self, match):
    if match.group(1) == 'rider_name':
      return True
    return False

  ## Populates the dictionary with the single param matching supplied by 'match'.
  def _parse_single_string_param_line(self, dictionary, match):
    dictionary[match.group(1)] = match.group(2)

  ## Populates the dictionaty with the range of inputs supplied by match.
  def _parse_range_param_line(self, dictionary, match):
    param = match.group(1)
    start = float(match.group(2))
    end = float(match.group(3))
    step = float(match.group(4))

    if step == 0:
      print('Cannot have a step with value: 0')
      return False

    if abs(end - (start + step)) >= abs(end - start):
      return False

    param_range = []

    param_range.append(start)

    value = start + step
    old_difference = abs(end - start)
    new_difference = abs(end - value)

    while old_difference > new_difference:
      ## Don't overshoot the end of the range.
      if value >= end and step > 0 or value <= end and step < 0:
        param_range.append(end)
        break

      param_range.append(value)

      value = value + step
      old_difference = new_difference
      new_difference = abs(end - value)

    dictionary[param] = copy.deepcopy(param_range)
    return True

  ## Populates the dictionaty with the set of inputs defined in match.
  def _parse_set_decimal_param_line(self, dictionary, match):
    param_set = []

    ## Split into the param and the set of values. We have to do this because
    ## match doesn't do any string splitting for us.
    param_split = match.group().split('=')
    param = param_split[0].replace(' ', '')
    values = param_split[1].split(',')

    ## Parse out each value in the set.
    for value in values:
      cleaned_value = value.replace('[', '').replace(']', '').replace(' ', '')
      param_set.append(float(cleaned_value.split('#')[0]))

    dictionary[param] = copy.deepcopy(param_set)

  ## Populates the dictionaty with the set of inputs defined in match.
  def _parse_set_string_param_line(self, dictionary, match):
    param_set = []

    ## Split into the param and the set of values. We have to do this because
    ## match doesn't do any string splitting for us.
    param_split = match.group().split('=')
    param = param_split[0].replace(' ', '')
    values = param_split[1].split(',')

    ## Parse out each value in the set.
    for value in values:
      cleaned_value = value.replace('[', '').replace(']', '').replace(' ', '')
      param_set.append(cleaned_value.split('#')[0])

    dictionary[param] = copy.deepcopy(param_set)

## Needed so we can import this module into Jupyter notebooks.
def load_ipython_extension(ipython):
  pass

## Needed so we can import this module into Jupyter notebooks.
def unload_ipython_extension(ipython):
  pass
