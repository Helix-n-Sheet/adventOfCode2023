### QUESTION: 
# oh this is dumb... grumble grumble grumble
"""
https://adventofcode.com/2023/day/2
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

def judge_pull(pull_results,ball_count):
    """
    compare the pull results with the assumed ball count to judge whether the
    result is possible or not
    return True if possible, False otherwise
    """
    # loop through color,count pairs in the pull results dict
    for color, count in pull_results.items():
        # check that the assumed ball count has that specific color, get 
        # associated value if so. Otherwise return 0. 
        assumed_count = ball_count.get(color,0)
        if count <= assumed_count:
            continue
        else:
            return 0
    return 1

def check_games(game_string, assumed_ball_count):
    """
    Read in a game string. Check plausability of each game. Sum Game IDs for 
    plausable games. Return Sum.
    """
    # create dict objct w/ keys being Game IDs and values being the pull 
    # strings
    games = parse_game_string(game_string)
    _sum = 0
    for gameID, pull_strings in games.items():
        pull_bools = []
        for pull_string in pull_strings:
            pull_dict = parse_pull_string(pull_string)
            pull_bool = judge_pull(pull_dict, assumed_ball_count)
            pull_bools.append(pull_bool)
        if np.prod(pull_bools) != 0:
            _sum += gameID
    return _sum

### TEST HANDLES
if __name__ == '__main__':
    games = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    
    assumed_ball_count = {'red': 12, 'green': 13, 'blue': 14}

    value = check_games(games,assumed_ball_count)
    assert value == 8

    with open('/workspaces/adventOfCode2023/Day02/game_results.txt','r') as infile:
        games = infile.read()
    value = check_games(games,assumed_ball_count)
    print(value) 
