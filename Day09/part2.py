### QUESTION
"""
https://adventofcode.com/2023/day/9
"""

### PREAMBLE
import numpy as np

### FUNCTIONS

def sum_forward_extrapolations(sensor_reading_string):
    """
    loop over all sensor reading histories, extrapolate the next value for each
    history. sum the extrapolations. 
    """
    # parse the input string
    all_sensor_readings = parse_sensor_readings(sensor_reading_string)
    # prep sum variable
    _sum = 0
    # loop over all sensor data histories
    for sensor_reading in all_sensor_readings:
        # perform the extrapolation and add to the sum
        _sum += extrapolate_forward(sensor_reading)
    return _sum


def sum_backward_extrapolations(sensor_reading_string):
    """
    loop over all sensor reading histories, extrapolate the next value for each
    history. sum the extrapolations. 
    """
    # parse the input string
    all_sensor_readings = parse_sensor_readings(sensor_reading_string)
    # prep sum variable
    _sum = 0
    # loop over all sensor data histories
    for sensor_reading in all_sensor_readings:
        # perform the extrapolation and add to the sum
        _sum += extrapolate_backward(sensor_reading)
    return _sum


def parse_sensor_readings(sensor_reading_string):
    """
    create a list of numpy arrays from the input sensor reading histories
    """
    sensor_readings = [np.array([int(x) for x in line.split()]) for line in sensor_reading_string.split('\n') if line != '']
    return sensor_readings


def extrapolate_forward(sensor_history):
    """
    do the forward extrapolation series for a single sensor's history
    """
    # initiate list of last value in each history level
    last_datas  = []
    # set current level to the input sensor_history 
    current = sensor_history
    # continuously loop until the boolean test is complete
    while set(current) != set([0]):
        # add the current level's last value to the last_datas list
        last_datas.append(current[-1])
        # get the new level
        new = differences(current)
        # update current to be the new level of sensor readings
        current = new
    return sum(last_datas)


def extrapolate_backward(sensor_history):
    """
    do the backward extrapolation series for a single sensor's history
    """
    # initiate list of last value in each history level
    first_datas  = []
    # set current level to the input sensor_history 
    current = sensor_history
    # continuously loop until the boolean test is complete
    while set(current) != set([0]):
        # add the current level's last value to the last_datas list
        first_datas.append(current[0])
        # get the new level
        new = differences(current)
        # update current to be the new level of sensor readings
        current = new
    
    extrapolation = 0
    for i, elem in enumerate(first_datas):
        pos_neg = 1 if not i % 2 else -1
        extrapolation += elem*pos_neg

    return extrapolation


def differences(sensor_readings):
    """
    calculate the next level in sensor readings
    """
    return sensor_readings[1:] - sensor_readings[:-1]


### TEST HANDLING
if __name__ == '__main__':
    sensor_reading_string = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    value = sum_forward_extrapolations(sensor_reading_string)
    print(value)
    assert value == 114

    value = sum_backward_extrapolations(sensor_reading_string)
    print(value)
    assert value == 2

    with open('./sensor_readings.txt','r') as infile:
        sensor_reading_string = infile.read()
    value = sum_forward_extrapolations(sensor_reading_string)
    print(value)

    value = sum_backward_extrapolations(sensor_reading_string)
    print(value)

