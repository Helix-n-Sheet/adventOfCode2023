### QUESTION
"""
https://adventofcode.com/2023/day/7
"""

### PREAMBLE
import re

start_node = 'AAA'
end_node   = 'ZZZ'

RL_map = {'L':0, 'R':1}

### FUNCTIONS

def determine_nSteps(navigation_string, start_node, end_node):
    """
    parse the navigation string and calculate how many steps to get from the 
    start_node to the end_node
    """
    # parse the input string
    nav_directions, nodes = parse_nav_string(navigation_string)
    # traverse the network to get to end_node
    nSteps = traverse_network(nav_directions, nodes, start_node, end_node)
    return nSteps


def parse_nav_string(nav_string):
    """
    parse the input string into the navigation step order and network 
    definitions
    """
    # split up the lines
    lines = nav_string.split('\n')
    # gather the step instruction orders
    step_order = lines[0]
    # initiate the network dictionary
    network_dict = {}
    for line in lines[2:]:
        if not line: 
            continue
        node, left, right = re.findall(r'\w+',line)
        network_dict[node] = (left, right)
    return step_order, network_dict


def traverse_network(nav_order, network, start, end):
    """
    using the network and navigation order, move through the network from start
    node to end node. Count the steps.
    """
    # get number of steps in the navigation order
    nOrders = len(nav_order)
    # step number starts at zero, so need to add 1 before returning
    nSteps = 0
    # loop until we've traversed to the end node
    current_node = start
    while True:
        # determine what the next move instruction is, either R or L
        step_instruction = nav_order[nSteps % nOrders]
        # get the move instruction index, either 0 or 1
        step_index = RL_map.get(step_instruction)
        # grab the next node
        next_node = network[current_node][step_index]
        # before we move on, gotta add to the step counter
        nSteps += 1
        # update current node
        current_node = next_node
        if current_node == end:
            return nSteps

### TEST HANDLING
if __name__ == '__main__':
    nav_instructions = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    
    value = determine_nSteps(nav_instructions, start_node, end_node)
    print(value)
    assert value == 2

    nav_instructions = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    
    value = determine_nSteps(nav_instructions, start_node, end_node)
    print(value)
    assert value == 6

    with open('./navigation_instructions.txt','r') as infile:
        nav_instructions = infile.read()
    value = determine_nSteps(nav_instructions, start_node, end_node)
    print(value)

