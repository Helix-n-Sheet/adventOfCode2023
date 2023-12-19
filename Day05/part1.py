### QUESTION
"""
The almanac (your puzzle input) lists all of the seeds that need to be planted. 
It also lists what type of soil to use with each kind of seed, what type of 
fertilizer to use with each kind of soil, what type of water to use with each 
kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is 
identified with a number, but numbers are reused by each category - that is, 
soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

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
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, 
and 13.

The rest of the almanac contains a list of maps which describe how to convert 
numbers from a source category into numbers in a destination category. That is, 
the section that starts with seed-to-soil map: describes how to convert a seed 
number (the source) to a soil number (the destination). This lets the gardener 
and his team know which soil to use with which seeds, which water to use with 
which fertilizer, and so on.

Rather than list every source number and its corresponding destination number 
one by one, the maps describe entire ranges of numbers that can be converted. 
Each line within a map contains three numbers: the destination range start, the 
source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, 
and a range length of 2. This line means that the source range starts at 98 and 
contains two values: 98 and 99. The destination range is the same length, but it 
starts at 50, so its two values are 50 and 51. With this information, you know 
that seed number 98 corresponds to soil number 50 and that seed number 99 
corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 
50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and 
also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds 
to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. 
So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks 
like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed 
number:

- Seed number 79 corresponds to soil number 81.
- Seed number 14 corresponds to soil number 14.
- Seed number 55 corresponds to soil number 57.
- Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd 
like to know the closest location that needs a seed. Using these maps, find the 
lowest location number that corresponds to any of the initial seeds. To do this, 
you'll need to convert each seed number through other categories until you can 
find its corresponding location number. In this example, the corresponding types 
are:

- Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 
  78, location 82.
- Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 
  43, location 43.
- Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 
  82, location 86.
- Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 
  35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed 
numbers?
"""

### PREAMBLE


### FUNCTIONS
def parse_almanac(almanac_string):
    """
    parse the full almanac file, creating a dict of dicts for the attribute map
    as well as starting seed numbers. 
    returns almanac_dict
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
            almanac_dict[dict_key] = seed_nums
            # move on to the next block
            continue

        # parse other blocks
        almanac_dict[dict_key] = {}
        # lines[0] for these just holds the key info
        for line in lines[1:]:
            # format of lines: destination range start, source range start, 
            # range length
            dest_start, source_start, range_len = line.split()
            # for the destination/source mapping, explicitly determine mapping
            source_dest_mapping = [[str(int(source_start)+i),str(int(dest_start)+i)] for i in range(int(range_len))]
            for _map in source_dest_mapping:
                # add source key with destination value
                almanac_dict[dict_key][_map[0]] = _map[1]

    #for key in almanac_dict.keys():
    #    print(key)
    #    print(almanac_dict[key],'\n')

    return almanac_dict

def determine_next_attribute(index,mapping_dict):
    """
    check the mapping_dict to see if index is explicitly defined as a key. If it
    is defined, return the associated value. Else, the mapping is 1:1 for key 
    values. 
    """
    return mapping_dict.get(index,index)
    

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
    print(seed_number, soil_number, fertilizer_number, water_number, light_number, temperature_number, humidity_number, location_number)
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
    print('\n\n')

    with open('./almanac.txt','r') as infile:
        almanac_string = infile.read()
    value = get_smallest_location(almanac_string)
    print(value)


