### QUESTION: 
"""
The newly-improved calibration document consists of lines of text; each line 
originally contained a specific calibration value that the Elves now need to 
recover. On each line, the calibration value can be found by combining the 
first digit and the last digit (in that order) to form a single two-digit 
number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. 
Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the 
calibration values?"""

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
