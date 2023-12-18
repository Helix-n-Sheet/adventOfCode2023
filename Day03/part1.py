### QUESTION
"""
If you can add up all the part numbers in the engine schematic, it should be 
easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of 
the engine. There are lots of numbers and symbols you don't really understand, 
but apparently any number adjacent to a symbol, even diagonally, is a "part 
number" and should be included in your sum. (Periods (.) do not count as a 
symbol.)

Here is an example engine schematic:

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

In this schematic, two numbers are not part numbers because they are not 
adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number 
is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all 
of the part numbers in the engine schematic?
"""

### PREAMBLE
import re


### FUNCTIONS
def parse_schematics(schematics_string):
    """
    parse the schematics file into lines. sum up all numbers adjacent to at 
    least one symbol. 
    1) iterating over each line, find numbers on the line.
        a) check for symbols adjacent to each symbol on the same line. 
        b) check for symbols adjacent to each symbol on the previous line. 
        c) check for symbols adjacent to each symbol on the next line. 
        d) if any adjacent symbols, add number to a sum.
    2) return the sum.
    """
    _sum = 0
    schema_lines = schematics_string.split('\n')
    nlines = len(schema_lines)
    # loop over all lines in the schematics
    for j, line in enumerate(schema_lines):
        # create the number regex iterator
        number_iterator = re.finditer(r'\d+',line)
        # get list of tuples, where each tuple is filled with the number value 
        # and a tuple of len = 2 with the indices associated with the number
        numbers = [(int(line[_match.start(0):_match.end(0)]),_match.span()) for _match in number_iterator]

        # skip the line if no numbers are present
        if not numbers:
            continue

        # create the symbol regex iterator
        symbol_iterator = re.finditer(r'[\@\$\+\=\#\%\*\&\/\-]',line)
        # get list of symbol indices for this line
        j_symbols = [_match.start(0) for _match in symbol_iterator]

        # get list of symbol indices for the previous line, j-1
        if j-1 >= 0:
            symbol_iterator = re.finditer(r'[\@\$\+\=\#\%\*\&\/\-]',schema_lines[j-1])
            i_symbols = [_match.start(0) for _match in symbol_iterator]
        else:
            i_symbols = []

        # get list of symbol indices for the next line
        if j+1 < nlines:
            symbol_iterator = re.finditer(r'[\@\$\+\=\#\%\*\&\/\-]',schema_lines[j+1])
            k_symbols = [_match.start(0) for _match in symbol_iterator]
        else:
            k_symbols = []


        adjacent_bool = False
        # loop over all numbers on the j line; look for adjacent symbols
        for number in numbers:
            num = number[0]
            # get the the indices where symbols might be adjacent
            adjacent_indices = range(number[1][0]-1,number[1][1]+1)
            # determine if the number is adjacent to a symbol on the j line
            adjacent_bool = adjacency(adjacent_indices, j_symbols)
            # if True
            if adjacent_bool:
                # add the number to the sum
                _sum += num
                # move on to the next number
                continue
            
            # check to see if i_symbols is empty
            if i_symbols:
                # determine if the number is adjacent to a symbol on the i line
                adjacent_bool = adjacency(adjacent_indices, i_symbols)
                # if True
                if adjacent_bool:
                    # add the number to the sum
                    _sum += num
                    # move on to the next number
                    continue
    
            # check to see if k_symbols is empty
            if k_symbols:
                # determine if the number is adjacent to a symbol on the k line
                adjacent_bool = adjacency(adjacent_indices, k_symbols)
                # if True
                if adjacent_bool:
                    # add the number to the sum
                    _sum += num
                    # move on to the next number
                    continue
        
    
    return _sum


def adjacency(indices,symbol_indices_list):
    """
    check whether symbol indices are within the indices associated with numbers
    return True if at least one symbol is found in the indices or False 
    otherwise
    """
    # loop over symbol indices to check if they are in the indices
    for symbol_index in symbol_indices_list:
        # check if symbol index in number indices
        if symbol_index in indices:
            return True
    # if no symbol is within the number indices, return False
    return False


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
    assert value == 4361

    with open('./engine_schematics.txt','r') as infile:
        schematics = infile.read()
    value = parse_schematics(schematics)
    print(value)

