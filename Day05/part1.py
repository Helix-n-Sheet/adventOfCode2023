### QUESTION
"""
https://adventofcode.com/2023/day/5
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
            # grab the seed numbers from the same line
            seed_nums = lines[0].split(':')[1].split()
            # add the seeds dict to the almanac dict
            almanac_dict[dict_key] = [int(seed) for seed in seed_nums]
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
            
    return almanac_dict

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


def slower_determine_next_attribute(source_index,ranges_list):
    """
    check the mapping_dict to see if index is within source ranges explicitly 
    defined. If it does sit in a defined range, return the associated 
    destination value. Else, the mapping is 1:1 for source and destination. 
    """
    # loop over ranges defined in ranges_list
    for _range in ranges_list:
        # boolean test to see the index is in the source range defined by 
        # _range[0] <= index < _range[0]+_range[2]
        if source_index in range(_range[0],_range[0]+_range[2]):
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


def get_smallest_location(almanac_string):
    """
    run the analysis
    """
    almanac_dict = parse_almanac(almanac_string)
    locations = []
    for seed in almanac_dict['seeds']:
        loc = get_seed_location(seed, almanac_dict)
        locations.append(int(loc))
    #print(locations)
    return min(locations)

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

    value = get_smallest_location(almanac_string)
    assert value == 35
    
    t = timeit.Timer(lambda: get_smallest_location(almanac_string))
    print('Current implementation:', t.timeit(100), '<usec>')
    
    print('\n\n')

    with open('./almanac.txt','r') as infile:
        almanac_string = infile.read()
    value = get_smallest_location(almanac_string)
    print(value)
    
    t = timeit.Timer(lambda: get_smallest_location(almanac_string))
    print('Current implementation:', t.timeit(100), '<usec>')


