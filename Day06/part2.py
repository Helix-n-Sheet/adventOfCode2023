### QUESTION
"""
https://adventofcode.com/2023/day/6

for this question: 
    d = v*t, where d is distance traveled, v is velocity, and t is time 
             post-holding the button. 
    we need to calculate d and then compare to previous results to determine if
    the run would beat that distance or not. 
    both v and t are dependent on t_hold, where t_hold is the time spent holding 
    the button. 
    v = a*t_hold, acceleration times t_hold to get velocity at the start of t.
    t = t_max - t_hold, t_max is the maximum amount of time for the race. 
    so, 
    d = a*t_hold*(t_max - t_hold) = a*t_max*t_hold - a*t_hold**2 (equation of a
    parabola)
    since this function is a parabola with bounding conditions of 
    0<= t_hold <= t_max, where at these bounds, d(t_hold=0,t_max) = 0, the 
    problem becomes rather simple. The max distance will be at t_hold = t_max/2. 
    Count the number of instances between 0 <= t_hold < t_max/2 then multiply by 
    2 and add 1.
    NOTE: implementing this strategy does not provide much of a timing 
    improvement...
"""

### PREAMBLE
import timeit
import numpy as np

### FUNCTIONS

def parse_history(race_history_string):
    """
    """
    max_times = [int(time) for time in race_history_string.split('\n')[0].split(':')[1].split()]
    distance  = [int(dist) for dist in race_history_string.split('\n')[1].split(':')[1].split()]

    race_history = list(zip(max_times,distance))
    return race_history


def calc_win_product(race_history_string, init_speed, accel): 
    """
    """
    # parse the race history string
    race_history = parse_history(race_history_string)
    # prep the product variable
    product = 1
    # loop over races in the history file
    for max_time, distance in race_history:
        # calc whole parabola
        t_hold_values = np.arange(0,max_time+1,1)
        y_values = accel*t_hold_values*t_hold_values[::-1]
        nWinning_races = sum(np.greater(y_values,distance))
        
        # only calc half parabola
        #t_hold_values = np.arange(0,max_time/2,1)
        #y_values = accel*t_hold_values*(max_time - t_hold_values)
        #nWinning_races = sum(np.greater(y_values,distance))*2 + 1
        #if len(t_hold_values) % 2 == 0:
        #    nWinning_races = sum(np.greater(y_values,distance))*2
        #else: 
        #    nWinning_races = sum(np.greater(y_values,distance))*2 + 1
        
        product *= nWinning_races
    return product

### TEST HANDLING
if __name__ == '__main__':
    # set basic variables
    init_speed  = 0     # units: mm ms^-1
    accel       = 1     # units: mm ms^-2, multiply by seconds held to get race 
                        # velocity
    
    # small but multiple races
    boat_race_history = """Time:      7  15   30
Distance:  9  40  200"""
    
    value = calc_win_product(boat_race_history, init_speed, accel)
    assert value == 288

    t = timeit.Timer(lambda: calc_win_product(boat_race_history, init_speed, accel))
    print('Fit implementation:', t.timeit(100), '<usec>')

    # larger values
    boat_race_history = """Time:      71530
Distance:  940200"""
    
    value = calc_win_product(boat_race_history, init_speed, accel)
    assert value == 71503

    t = timeit.Timer(lambda: calc_win_product(boat_race_history, init_speed, accel))
    print('Fit implementation:', t.timeit(100), '<usec>')

    with open('real_boat_racing.txt','r') as infile:
        boat_race_history = infile.read()
    value = calc_win_product(boat_race_history, init_speed, accel)
    print(value)
    

