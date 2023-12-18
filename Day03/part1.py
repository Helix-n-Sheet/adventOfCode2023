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

digit_list = ['1','2','3','4','5','6','7','8','9','0']

def parse_schematics(schematics_string):
    """
    parse the schematics file into lines. sum up all numbers adjacent to at 
    least one symbol. 
    1) iterating over each line, find symbols on the line.
        a) check for numbers adjacent to each symbol on the same line. 
        b) check for numbers adjacent to each symbol on the next line. 

    """
    _sum = 0
    schema_lines = schematics_string.split('\n')
    nlines = len(schema_lines)
    # loop over all lines in the schematics
    for j, line in enumerate(schema_lines):
        # create the regex iterator
        symbol_iterator = re.finditer(r'[@$+-/=#%*&]',line)
        # get list of symbol indices
        symbol_indices = [_match.start(0) for _match in re.finditer(r'[@$+=#%*&\/\-]',line)]
        print(j, [_match for _match in re.finditer(r'[@$+=#%*&\/\-]',line)])

        # move to next line if no symbol is found on the current line
        if not symbol_indices:
            print('\n')
            continue
        
        # loop over all symbols on this line
        j_numbers = [(int(line[_match.start(0):_match.end(0)]),range(*_match.span())) for _match in re.finditer(r'\d+',line)]
        
        # get adjacent line indices 
        i = j - 1
        k = j + 1

        if i == -1:
            print(schema_lines[i])
            i_numbers = [(int(schema_lines[i][_match.start(0):_match.end(0)]),range(*_match.span())) for _match in re.finditer(r'\d+',schema_lines[i])]
        else:
            i_numbers = []

        print(line)

        if k <= nlines:
            print(schema_lines[k])
            k_numbers = [(int(schema_lines[k][_match.start(0):_match.end(0)]),range(*_match.span())) for _match in re.finditer(r'\d+',schema_lines[k])]
        else:
            k_numbers = []

        for symbol_index in symbol_indices:
            # find adjacent numbers to symbol on the same line
            line_numbers = get_numbers(j_numbers,symbol_index)
            _sum += sum(line_numbers)
            print('Same line:', sum(line_numbers))
         
            # find adjacent numbers to symbol on the previous line
            line_numbers = get_numbers(i_numbers,symbol_index)
            _sum += sum(line_numbers)
            print('Previous line:', sum(line_numbers))
            
            # find adjacent numbers to symbol on the next line
            line_numbers = get_numbers(k_numbers,symbol_index)
            _sum += sum(line_numbers)
            print('Next line:', sum(line_numbers))
        
        print('\n')
    
    return _sum

def get_numbers(number_list,symbol_index):
    """
    get number(s) on line line_index that are adjacent to a symbol at symbol_index
    """
    # determine indices of potentially adjacent digits
    before = symbol_index - 1
    after  = symbol_index + 1
  
    # gather numbers that are adjacent
    numbers = []
    for number in number_list:
        # check to see if a number is in the before index
        if before in number[1] or symbol_index in number[1] or after in number[1]:
            numbers.append(number[0])
        
    return numbers


### TEST HANDLES
if __name__ == '__main__':
    schematics = """
467..114..
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



