### QUESTION
"""
https://adventofcode.com/2023/day/5

NOTE: the smallest location is much smaller than the smallest seed number. So, 
sort location numbers and then back calculate seed numbers, checking to see if
each seed number is represented in the original list of seed ranges. Break once
a seed ID is found. 
This strategy has the potential to be slower since there are more location 
numbers (4.1 billion) than seed numbers (1.7 billion) but the objective is find 
the smallest location value so we should design the code with that in mind.

Timing-wise, the forward process is slightly faster per iteration but will only
exit once all seed numbers have been tested. The backward process will calculate
fictional seeds but should exit as soon as a match with reality is found. 

The backward implementation took a bit longer than I expected, but only took 

real	1m48.883s
user	1m48.875s
sys	0m0.008s

in the end! Meanwhile, the forward approach is still running and has been for
hours.
"""

### PREAMBLE
import timeit


### FUNCTIONS

def parse_almanac(almanac_string):
    """
    parse the full almanac file, creating a dict of dicts for the attribute map
    as well as starting seed numbers. 
    returns almanac_dict that is a dict of lists, where each sublist is filled
    with tuples associated with the mapping. These tuples are formatted as:
    (source_start, destination_start, range_length) all formatted as ints.
    """
    # break the file into the individual blocks
    mapping_blocks = almanac_string.split('\n\n')
    # prep the dictionary
    almanac_dict = {}
    # loop over blocks
    for block in mapping_blocks:
        # break the block into lines
        lines = block.split('\n')
        # lines[0] holds the dict key
        dict_key = lines[0].split(':')[0].split()[0]
        # the seeds block has a separate format
        if dict_key == 'seeds':
            # get the seed numbers, accounting for the new formatting
            seed_ranges = parse_seed_block(lines[0])
            # add the seeds dict to the almanac dict
            almanac_dict[dict_key] = seed_ranges
            # move on to the next block
            continue

        # parse other blocks
        almanac_dict[dict_key] = []
        # lines[0] for these just holds the key info
        for line in lines[1:]:
            if not line:
                continue
            dest_start, source_start, range_len = line.split()
            almanac_dict[dict_key].append((int(source_start),int(dest_start),int(range_len)))
    
    #### INSPECTING SEEDS
    #nSeeds = sum([seed_range[1] for seed_range in seed_ranges])
    #print(nSeeds) --> 1,679,109,896
    #print('Smallest seed value:', min([seed_range[0] for seed_range in seed_ranges]))
    # --> Smallest seed value: 40,283,135
    #print('Largest seed value:', max([seed_range[0]+seed_range[1] for seed_range in seed_ranges]))
    # --> Largest seed value: 4,068,452,766

    #### INSPECTING LOCATIONS 
    #nLocations = sum([mapping_range[2] for mapping_range in almanac_dict['humidity-to-location']])
    #nLocation_ranges = len([mapping_range[2] for mapping_range in almanac_dict['humidity-to-location']])
    #print(nLocations) --> 4,122,156,611
    #print(nLocation_ranges) --> 43
    #print('Smallest location value:', min([mapping_range[1] for mapping_range in almanac_dict['humidity-to-location']]))
    # --> Smallest location value: 0
    #print('Largest location value:', max([mapping_range[1]+mapping_range[2] for mapping_range in almanac_dict['humidity-to-location']]))
    # --> Largest location value: 4,294,967,296

    return almanac_dict

def parse_seed_block(seed_line):
    """
    parse the line of seeds, where each pair of numbers is a starting value and
    the range length for the seeds to be planted.
    return the list of ranges for seed numbers
    """
    numbers = [int(number) for number in seed_line.split(':')[1].split()]
    number_pairs = list(zip(numbers[::2],numbers[1::2]))
    #print('Number of seed ranges:', len(number_pairs))
    return number_pairs


# ------------------------------------------------------------------------------
# BRUTE FORCE - FORWARD APPROACH
# ------------------------------------------------------------------------------
def determine_next_attribute(source_index,ranges_list):
    """
    check the mapping_dict to see if index is within source ranges explicitly 
    defined. If it does sit in a defined range, return the associated 
    destination value. Else, the mapping is 1:1 for source and destination. 
    """
    # loop over ranges defined in ranges_list
    for _range in ranges_list:
        # boolean test to see the index is in the source range defined by 
        # _range[0] <= index < _range[0]+_range[2]
        if source_index >= _range[0] and source_index < _range[0]+_range[2]:
            # if true, then the destination index is equal to the 
            # destination_start value plus the difference between index and
            # source_start values. 
            return _range[1]+source_index-_range[0]
    
    # if the source_index value is not within any of the explicitly defined
    # ranges, then return the same index.
    return source_index


def get_seed_location(seed_number, almanac_dict):
    """
    jump from 
    seed->soil->fertilizer->water->light->temperature->humidity->location to 
    get the seed's location number
    """
    soil_number = determine_next_attribute(seed_number,almanac_dict['seed-to-soil'])
    fertilizer_number = determine_next_attribute(soil_number,almanac_dict['soil-to-fertilizer'])
    water_number = determine_next_attribute(fertilizer_number,almanac_dict['fertilizer-to-water'])
    light_number = determine_next_attribute(water_number,almanac_dict['water-to-light'])
    temperature_number = determine_next_attribute(light_number,almanac_dict['light-to-temperature'])
    humidity_number = determine_next_attribute(temperature_number,almanac_dict['temperature-to-humidity'])
    location_number = determine_next_attribute(humidity_number,almanac_dict['humidity-to-location'])
    #print(seed_number, soil_number, fertilizer_number, water_number, light_number, temperature_number, humidity_number, location_number)
    return location_number


def forward_get_smallest_location(almanac_string):
    """
    run the analysis
    """
    # gather the mapping and seed ranges
    almanac_dict = parse_almanac(almanac_string)
    #
    min_location = float('inf')
    for seed_range in almanac_dict['seeds']:
        _range = range(seed_range[0],seed_range[0]+seed_range[1])
        for seed in _range:
            loc = get_seed_location(seed, almanac_dict)
            if loc < min_location:
                min_location = loc
    return min_location


# ------------------------------------------------------------------------------
# BACKWARD APPROACH
# ------------------------------------------------------------------------------
def determine_previous_attribute(destination_index, ranges_list):
    """
    check the mapping_dict to see if index is within destination ranges 
    explicitly  defined. If it does sit in a defined range, return the 
    associated source value. Else, the mapping is 1:1 for source and 
    destination. 
    """
    # loop over ranges defined in ranges_list
    for _range in ranges_list:
        # boolean test to see the index is in the destination range defined by 
        # _range[1] <= index < _range[1]+_range[2]
        if destination_index >= _range[1] and destination_index < _range[1]+_range[2]:
            # if true, then the source index is equal to the source_start value 
            # plus the difference between index and destination_start values. 
            return _range[0]+destination_index-_range[1]
    
    # if the destination_index value is not within any of the explicitly defined
    # ranges, then return the same index.
    return destination_index


def get_location_seed(loc_number, almanac_dict):
    """
    jump from 
    location->humidity->temperature->light->water->fertilizer->soil->seed to 
    get the location's seed number
    """
    humidity_number = determine_previous_attribute(loc_number,almanac_dict['humidity-to-location'])
    temperature_number = determine_previous_attribute(humidity_number,almanac_dict['temperature-to-humidity'])
    light_number = determine_previous_attribute(temperature_number,almanac_dict['light-to-temperature'])
    water_number = determine_previous_attribute(light_number,almanac_dict['water-to-light'])
    fertilizer_number = determine_previous_attribute(water_number,almanac_dict['fertilizer-to-water'])
    soil_number = determine_previous_attribute(fertilizer_number,almanac_dict['soil-to-fertilizer'])
    seed_number = determine_previous_attribute(soil_number,almanac_dict['seed-to-soil'])
    #print(seed_number, soil_number, fertilizer_number, water_number, light_number, temperature_number, humidity_number, loc_number)
    return seed_number


def backward_get_smallest_location(almanac_string):
    """
    run the analysis
    """
    # gather the mapping and seed ranges
    almanac_dict = parse_almanac(almanac_string)
    # determine the seed ranges before hand
    seed_ranges = [(start,start+range_len) for start, range_len in almanac_dict['seeds']]
    
    # loop over possible location numbers until one matches with a seed number
    loc = 0
    while True:
        seed = get_location_seed(loc, almanac_dict)
        #print(seed,loc)
        if any([start <= seed < end for start, end in seed_ranges]):
            return loc
        loc += 1


### TEST HANDLING
if __name__ == '__main__':
    almanac_string = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    value = forward_get_smallest_location(almanac_string)
    assert value == 46
    t = timeit.Timer(lambda: forward_get_smallest_location(almanac_string))
    print('Forward implementation:', t.timeit(100), '<usec>')
    print('\n\n')

    value = backward_get_smallest_location(almanac_string)
    assert value == 46
    t = timeit.Timer(lambda: backward_get_smallest_location(almanac_string))
    print('Backward implementation:', t.timeit(100), '<usec>')
    print('\n\n')

    with open('./almanac.txt','r') as infile:
        almanac_string = infile.read()
    value = backward_get_smallest_location(almanac_string)
    print(value)


