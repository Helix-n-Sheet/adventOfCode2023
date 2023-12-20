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
    d = a*t_hold*(t_max - t_hold)
"""

### PREAMBLE


### FUNCTIONS
def calc_win_product(race_history_string, init_speed, accel):
    """
    """
    # parse the race history string
    race_history = parse_history(race_history_string)
    # prep the product variable
    product = 1
    # loop over races in the history file
    for max_time, distance in race_history:
        # prep the wins counts
        race_wins = 0
        # loop over t_hold values
        for t_hold in range(1,max_time):
            # calculate the expected distance
            dist = calc_distance(max_time, t_hold, accel)
            # if expected distance is greater than the previous distance, 
            # add to counts
            if dist > distance:
                race_wins += 1
        # multiply by race_wins
        product *= race_wins
    return product


def calc_distance(max_time, t_hold, acceleration):
    """
    calculate the distance traveled during the max_time of the race after
    holding the button for t_hold. 
    """
    return acceleration*t_hold*(max_time-t_hold)


def parse_history(race_history_string):
    """
    """
    max_times = [int(time) for time in race_history_string.split('\n')[0].split(':')[1].split()]
    distance  = [int(dist) for dist in race_history_string.split('\n')[1].split(':')[1].split()]

    race_history = list(zip(max_times,distance))
    return race_history


### TEST HANDLING
if __name__ == '__main__':
    boat_race_history = """Time:      7  15   30
Distance:  9  40  200"""
    
    init_speed  = 0     # units: mm ms^-1
    accel       = 1     # units: mm ms^-2, multiply by seconds held to get race 
                        # velocity
    
    value = calc_win_product(boat_race_history, init_speed, accel)
    print(value)
    assert value == 288

    with open('boat_racing.txt','r') as infile:
        boat_race_history = infile.read()
    value = calc_win_product(boat_race_history, init_speed, accel)
    print(value)


