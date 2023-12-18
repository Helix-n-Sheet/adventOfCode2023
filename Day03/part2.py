### QUESTION
"""
... A gear is any * symbol that is adjacent to exactly two part numbers. Its 
gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so 
that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has 
part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the 
lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear 
because it is only adjacent to one part number.) Adding up all of the gear 
ratios produces 467835.
"""

### PREAMBLE
import re
import numpy as np


### FUNCTIONS
def parse_schematics(schematics_string):
    """
    parse the schematics file into lines. sum up all numbers adjacent to at 
    least one symbol. 
    1) iterating over each line, find * symbols on the line.
        a) check for numbers adjacent to each * symbol on the same line. 
        b) check for numbers adjacent to each * symbol on the previous line. 
        c) check for numbers adjacent to each * symbol on the next line. 
        d) if the * symbol is adjacent to exactly two numbers, multiply those
        numbers together. 
        e) add the product to the sum. 
    2) return the sum.
    """
    _sum = 0
    schema_lines = schematics_string.split('\n')
    nlines = len(schema_lines)
    # loop over all lines in the schematics
    for j, line in enumerate(schema_lines):
        # create the symbol regex iterator
        symbol_iterator = re.finditer(r'\*',line)
        # create list of gear indices on line j
        gears = [_match.start(0) for _match in symbol_iterator]
        
        if not gears:
            continue

        # create the number regex iterator
        number_iterator = re.finditer(r'\d+',line)
        # get list of tuples, where each tuple is filled with the number value 
        # and a tuple of len = 2 with the indices associated with the number
        j_numbers = [(int(line[_match.start(0):_match.end(0)]),_match.span()) for _match in number_iterator]

        # get list of tuples associated with numbers on the previous line, j-1
        if j-1 >= 0:
            number_iterator = re.finditer(r'\d+',schema_lines[j-1])
            i_numbers = [(int(schema_lines[j-1][_match.start(0):_match.end(0)]),_match.span()) for _match in number_iterator]
        else:
            i_numbers = []

        # get list of tuples associated with numbers on the next line, j+1
        if j+1 >= 0:
            number_iterator = re.finditer(r'\d+',schema_lines[j+1])
            k_numbers = [(int(schema_lines[j+1][_match.start(0):_match.end(0)]),_match.span()) for _match in number_iterator]
        else:
            k_numbers = []

        # loop over all gears on the j line; look for adjacent numbers
        for gear in gears:
            # collect adjacent numbers
            adjacent_numbers = []
            # look for gear-adjacent numbers on the j line
            j_adjacency = adjacency(gear, j_numbers)
            # add adjacent numbers to the holding list
            adjacent_numbers.extend(j_adjacency)

            # check to see if i_numbers is empty
            if i_numbers:
                # look for gear-adjacent numbers on the i line 
                i_adjacency = adjacency(gear,i_numbers)
                # add adjacent numbers to the holding list
                adjacent_numbers.extend(i_adjacency)

            # check to see if k_numbers is empty
            if k_numbers:
                # look for gear-adjacent numbers on the k line 
                k_adjacency = adjacency(gear,k_numbers)
                # add adjacent numbers to the holding list
                adjacent_numbers.extend(k_adjacency)

            if len(adjacent_numbers) == 2:
                _sum += np.prod(adjacent_numbers)

    return _sum


def adjacency(gear_index,number_indices_list):
    """
    check whether number indices are within the indices associated with gears
    return the list of numbers if at least one number is found in the indices 
    or an empty list otherwise
    """
    # loop over numbers to check if they are positioned with the gear
    number_list = []
    for number in number_indices_list:
        num = number[0]
        num_indices = range(number[1][0]-1,number[1][1]+1)
        # check if symbol index in number indices
        if gear_index in num_indices:
            number_list.append(num)
    # if no symbol is within the number indices, return False
    return number_list


### TEST HANDLES
if __name__ == '__main__':
    schematics = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    value = parse_schematics(schematics)
    print(value)
    assert value == 467835

    with open('./engine_schematics.txt','r') as infile:
        schematics = infile.read()
    value = parse_schematics(schematics)
    print(value)

