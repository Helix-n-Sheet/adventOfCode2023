### QUESTION
"""
https://adventofcode.com/2023/day/7
"""

### PREAMBLE
import re

start_node_suffix = 'A'
end_node_suffix   = 'Z'

RL_map = {'L':0, 'R':1}

### FUNCTIONS

def determine_nSteps(navigation_string, start_node_suffix, end_node_suffix):
    """
    parse the navigation string and calculate how many steps to get from the 
    start_node to the end_node
    """
    # parse the input string
    nav_directions, nodes = parse_nav_string(navigation_string)
    starting_nodes = [key for key in nodes.keys() if key[-1] == start_node_suffix]
    possible_ending_nodes   = [key for key in nodes.keys() if key[-1] == end_node_suffix]
    print(len(starting_nodes),starting_nodes)
    print(len(possible_ending_nodes),possible_ending_nodes)
    # traverse the network to get to end_node
    nSteps = traverse_network(nav_directions, nodes, starting_nodes, possible_ending_nodes)
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


def traverse_network(nav_order, network, start_nodes, end_nodes):
    """
    using the network and navigation order, move through the network from start
    nodes to any of the end nodes. Count the steps.
    """
    # get number of steps in the navigation order
    nOrders = len(nav_order)
    # step number starts at zero, so need to add 1 before returning
    nSteps = 0
    # loop until we've traversed to the end node
    current_nodes = start_nodes
    while True:
        # determine what the next move instruction is, either R or L
        step_instruction = nav_order[nSteps % nOrders]
        # get the move instruction index, either 0 or 1
        step_index = RL_map.get(step_instruction)
        
        # loop over all current nodes
        next_nodes = []
        for node in current_nodes:
            # grab the next node
            next_nodes.append(network[node][step_index])
        
        # before we move on, gotta add to the step counter
        nSteps += 1
        # update current node
        current_nodes = next_nodes
        # test to see if all nodes finish at an end node, create a list of bools
        # and check if all of the bools are True
        exit_bool = all([node in end_nodes for node in current_nodes])
        if exit_bool:
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
    
    value = determine_nSteps(nav_instructions, start_node_suffix, end_node_suffix)
    print(value)
    assert value == 2

    nav_instructions = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    
    value = determine_nSteps(nav_instructions, start_node_suffix, end_node_suffix)
    print(value)
    assert value == 6

    nav_instructions = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    value = determine_nSteps(nav_instructions, start_node_suffix, end_node_suffix)
    print(value)
    assert value == 6

    with open('./navigation_instructions.txt','r') as infile:
        nav_instructions = infile.read()
    value = determine_nSteps(nav_instructions, start_node_suffix, end_node_suffix)
    print(value)


