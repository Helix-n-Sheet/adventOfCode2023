### QUESTION: 
"""
https://adventofcode.com/2023/day/1
"""

### PREAMBLE 
import re
import timeit

def basic_parse_string(calibration_string):
    lines = calibration_string.split('\n')
    sum = 0
    for line in lines:
        line_values = []
        for char in line:
            try: 
                value = int(char)
                line_values.append(str(value))
            except:
                continue
        #print(line,int(line_values[0]+line_values[-1]))
        sum += int(line_values[0] + line_values[-1])
    return sum

def re_parse_string(calibration_string):
    lines = calibration_string.split('\n')
    sum = 0
    for line in lines: 
        line_values = re.findall(r'\d',line)
        sum += int(str(line_values[0])+str(line_values[-1]))
    return sum

### TEST HANDLES
if __name__ == '__main__':
    calibration_string='1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet'
    
    value = basic_parse_string(calibration_string)
    assert value == 142

    t = timeit.Timer(lambda: basic_parse_string(calibration_string))
    print('basic function:', t.timeit(100), '<usec>')

    value = re_parse_string(calibration_string)
    assert value == 142

    t = timeit.Timer(lambda: re_parse_string(calibration_string))
    print('regex function:', t.timeit(100), '<usec>')

    with open('/workspaces/adventOfCode2023/Day01/calibration_document.txt','r') as infile:
        calibration_string = infile.read()
        print(re_parse_string(calibration_string))
