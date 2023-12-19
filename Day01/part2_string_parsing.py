### QUESTION: 
"""
https://adventofcode.com/2023/day/1
"""

### PREAMBLE 
import re
import timeit

number_strings = {'one':'1',
                  'two':'2',
                  'three':'3',
                  'four':'4',
                  'five':'5',
                  'six':'6',
                  'seven':'7',
                  'eight':'8',
                  'nine':'9'}
                 #'zero':0,

def search_string(string):
    dgt = ''
    for i in range(len(string)):
        substring = string[:i+1]
        for number in number_strings:
            if number in substring:
                dgt = number_strings[number]
                return dgt
    return dgt

def search_string_bkwrds(string):
    dgt = ''
    for i in range(len(string)):
        substring = string[-i-1:]
        for number in number_strings:
            if number in substring:
                dgt = number_strings[number]
                return dgt
    return dgt

def re_parse_string(calibration_string):
    lines = calibration_string.split('\n')
    sum = 0
    for line in lines:
        # split whole line into match groups of only strings and digits.
        string_splits = re.findall(r'[a-zA-Z]+|\d',line)
        # convert substrings to digits
        digit_splits = []
        # loop over all string splits to find digits or number strings in each 
        # split; finding the first digit only!
        for split in string_splits:
            found_digit = None
            # search for number characters
            try:
                found_digit = str(int(split))
            # split is a string
            except:
                # search for number string in split
                found_digit = search_string(split)
            # if a digit, whether number or string, was found, then append that
            # number to the list. BREAK OUT if one digit has been found.
            if found_digit:
                digit_splits.extend(found_digit)
                break
        
        # loop over all string splits to find digits or number strings in each 
        # split; finding the last digit only!
        for split in string_splits[::-1]:
            found_digit = None
            try:
                found_digit = str(int(split))
            except:
                found_digit = search_string_bkwrds(split)
            if found_digit:
                digit_splits.extend(found_digit)
                break
        sum += int(digit_splits[0]+digit_splits[-1])
    return sum

### TEST HANDLES
if __name__ == '__main__':
    original_calibration_string='1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet'
    new_calibration_string='two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen'
    
    value = re_parse_string(original_calibration_string)
    assert value == 142

    value = re_parse_string(new_calibration_string)
    assert value == 281

    t = timeit.Timer(lambda: re_parse_string(original_calibration_string))
    print('regex function:', t.timeit(100), '<usec>')

    with open('/workspaces/adventOfCode2023/Day01/calibration_document.txt','r') as infile:
        calibration_string = infile.read()
        print(re_parse_string(calibration_string))

