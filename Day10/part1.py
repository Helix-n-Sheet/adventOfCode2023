### QUESTION
"""
https://adventofcode.com/2023/day/10
"""

### PREAMBLE
import re
import sys
import numpy as np

# creating a dictionary that defines the connections made by the various pipes
# assuming a 2d indexing strategy will be used to define the pipe grid. 
# keys will be the characters on said grid, with values being arrays of 
# positions of connections on the grid, relative to the current grid position
pipe_connections = {"|" : np.array([[-1,0],[1,0]]), # N,S
                    "-" : np.array([[0,-1],[0,1]]), # E,W
                    "L" : np.array([[-1,0],[0,1]]), # N,E
                    "J" : np.array([[-1,0],[0,-1]]),# N,W
                    "7" : np.array([[1,0],[0,-1]]), # S,W
                    "F" : np.array([[1,0],[0,1]])}  # S,E


### FUNCTIONS

def get_furthest_distance(pipes_string,start_string):
    """
    """
    # parse the pipes_string input to list of strings
    pipes_list = pipes_string.split('\n')
    maxChar_range = range(len(pipes_list[0]))
    # get the starting point
    starting_point = get_starting_pos(pipes_list,start_string)
    # get positions of connecting pipes for the starting point position
    # need to judge all four directions for the starting point since we do not
    # have context clues about what type of pipe is at the starting point
    connections = find_starting_connections(starting_point,pipes_list)
    # have a collection of previous positions associated with each connection
    prev_pos = [starting_point for i in connections]
    # all current connections are one distance away from starting point
    counter = 1
    
    # traverse the pipes in all directions until all pipes have meet up with 
    # another... I am likely making this more complex than it needs to be
    # looking at the input data, I know there are only two connections to the S
    # point...
    while True:
        next_connections = []
        for i, connection in enumerate(connections):
            new = find_next_connection(connection, prev_pos[i], pipes_list)
            # if a pipeline is a dead end, remove from the connections list
            if not new:
                continue
            # if a pipeline's connect sends us off the grid space, remove from
            # the connections list
            elif sum([elem in maxChar_range for elem in new]) != 2:
                continue
            # if two pipelines meet, their ``new`` values will be the same, at 
            # which point we should break out of the while loop
            elif new in next_connections:
                return counter + 1
            # otherwise, append to the connections list
            else:
                next_connections.append(new)
                
        # add to the distance counter
        counter += 1
        prev_pos = connections
        connections = next_connections


def get_starting_pos(pipes_list, start_string):
    """
    get the indices of the start_string character within the pipes_list, 
    assuming the format of the pipes_list is a list of strings
    return tuple of (i,j) where i is the line index and j is the char index in
    the line's string
    """
    
    for i, line in enumerate(pipes_list):
        _match = re.search(r'%s'%(start_string),line)
        if _match:
            j = _match.start(0)
            return [i,j]
    print('Error... no starting point found')
    sys.exit(0)

def find_starting_connections(position_indices, grid_list):
    """
    using the starting point's position indices to get adjacent characters (up, 
    down, left, right). Then judge which of those four symbols connect with the
    starting point.
    returns list of numpy arrays of len 2, associated with indices
    """
    
    # to be a connection, take direction's adjacent string and check if it 
    # matches one of the direction's acceptable pipe connections
    connections = [] 

    # for up direction, check for character with "south" direction
    up   = [position_indices[0]-1,position_indices[1]]
    char = grid_list[up[0]][up[1]]
    if char in ['|','7','F']:
        connections.append(up)

    # for down direction, check for char with "north" direction
    down = [position_indices[0]+1,position_indices[1]]
    char = grid_list[down[0]][down[1]]
    if char in ['|','L','J']:
        connections.append(down)

    # for left direction, check for char with "east" direction
    left = [position_indices[0],position_indices[1]-1]
    char = grid_list[left[0]][left[1]]
    if char in ['-','L','F']:
        connections.append(left)

    # for right direction, check for char with "west" direction
    right = [position_indices[0],position_indices[1]+1]
    char = grid_list[right[0]][right[1]]
    if char in ['-','J','7']:
        connections.append(right)
    
    # none or one connections found? can't have a connected pipe...
    if len(connections) < 2:
        print('Error, number of connections with the starting point does not allow for a complete pipe')
        sys.exit(0)
    # otherwise, search across any number of connections to the starting point
    return connections


def find_next_connection(pos,prev,grid_list):
    """
    """
    # get the character at the current position
    char = grid_list[pos[0]][pos[1]]
    # if the char key is not in the pipe_connections dictionary, then get an 
    # empty string. otherwise, get the relative connection values
    relative_connections = pipe_connections.get(char,'')
    # check for acceptable connection; if empty string, pass connection on to be
    # disposed of as a dead end
    if type(relative_connections) == str:
        return ''

    # take the relative connections indices and map them to the global position
    # of pos
    global_connections = [list(pos + elem) for elem in relative_connections] 
    # based on the prev position, determine which is actually the untraveled pos
    new_pos = global_connections[0] if global_connections[0] != prev else global_connections[1]

    # check to make sure the new_pos is associated with an accepting pipe type
    new_char = grid_list[new_pos[0]][new_pos[1]]
    new_relative_connections = pipe_connections.get(new_char,'')
    # N/S connection, E/W connection differ by multiple of -1 
    if -1*relative_connections in new_relative_connections:
        # we've got a good connection, accept the move. 
        return new_pos
    # the new_char doesn't have a mirroring connection, so we hit a dead end
    else:
        return ''


### TEST HANDLING
if __name__ == '__main__':

    start_string = 'S'

    pipes_grid = """.....
.S-7.
.|.|.
.L-J.
....."""

    value = get_furthest_distance(pipes_grid, start_string)
    print(value)
    assert value == 4

    pipes_grid = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

    value = get_furthest_distance(pipes_grid, start_string)
    print(value)
    assert value == 8

    with open('./pipes.txt','r') as infile:
        pipes_grid = infile.read()
    value = get_furthest_distance(pipes_grid, start_string)
    print(value)

