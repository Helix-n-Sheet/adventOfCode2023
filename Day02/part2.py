### QUESTION: 
# oh this is dumb... grumble grumble grumble
"""
... in each game you played, what is the fewest number of cubes of each color 
that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

- In game 1, the game could have been played with as few as 4 red, 2 green, and 
  6 blue cubes. If any color had even one fewer cube, the game would have been 
  impossible.
- Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue 
  cubes.
- Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
- Game 4 required at least 14 red, 3 green, and 15 blue cubes.
- Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

The power of a set of cubes is equal to the numbers of red, green, and blue 
cubes multiplied together. The power of the minimum set of cubes in game 1 is 
48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these 
five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What 
is the sum of the power of these sets?
"""

### PREAMBLE
import re
import numpy as np

def parse_game_string(game_string):
    """ 
    parse each line to get Game ID and pull results
    """
    game_dict = {}
    game_lines = game_string.split('\n')
    for line in game_lines:
        # gather Game ID
        game_id = int(re.search(r'\d+',line)[0])
        pull_strings = line.split(':')[1].split(';')
        # gather the pull strings describing the game
        game_dict[game_id] = pull_strings
    return game_dict


def parse_pull_string(pull_string):
    """
    parse a single pull's set of results
    right now, the formatting is clean. always number color comma
    """
    pull_dict = {}
    color_strings = pull_string.split(',')
    for color_string in color_strings:
        count, color = color_string.split()
        pull_dict[color] = int(count)
    return pull_dict


def min_cubes(pull_results,cube_counts):
    """
    determine the minimum number of cubes for each color necessary for the game
    results. Compare to the values in cube_counts. 
    return the product of these minumum cube numbers
    """
    for color, count in pull_results.items():
        assumed_count = cube_counts.get(color,0)
        if count > assumed_count:
            cube_counts[color] = count
        else:
            continue
    return cube_counts


def game_powers(game_string):
    """
    Read in a game string. Check for minimum cube count necessary to have all 
    pulls be possible. Sum power of minimum cube counts for all games. Return 
    sum.
    """
    # create dict objct w/ keys being Game IDs and values being the pull 
    # strings
    games = parse_game_string(game_string)
    _sum = 0 
    for gameID, pull_strings in games.items():
        minimum_cubes = {}
        #minimum_cubes = {'red':0,'blue':0,'green':0}
        for pull_string in pull_strings:
            pull_dict = parse_pull_string(pull_string)
            minimum_cubes = min_cubes(pull_dict,minimum_cubes)
        game_power = np.prod([val for val in minimum_cubes.values()])
        _sum += game_power
    return _sum


### TEST HANDLES
if __name__ == '__main__':
    games = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    
    value = game_powers(games)
    assert value == 2286

    with open('game_results.txt','r') as infile:
        games = infile.read()
    value = game_powers(games)
    print(value)
