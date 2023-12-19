### QUESTION
"""
https://adventofcode.com/2023/day/4
"""

### PREAMBLE
import re

### FUNCTIONS

def parse_card(card_string):
    """
    parse the standard formatted strings associated with scratch cards
    """
    # grab strings associated with winning and card numbers
    winning_numbers, card_numbers = card_string.split(':')[1].split('|')
    # parse the strings to get the individual numbers, formatted as str
    winning_numbers = winning_numbers.split()
    card_numbers = card_numbers.split()
    # return a list of lists where 0th list is the winning numbers and 1st list
    # is the card numbers
    card_results = [winning_numbers, card_numbers]
    return card_results
    
    ## create the card_dict where card_id is the key and the value is a tuple of
    ## the winning_numbers and card_numbers
    ## grab card_id to use as key for dictionary
    #card_id = re.search(r'\d+',card_string)[0]
    #card_dict = {card_id: (winning_numbers, card_numbers)}
    #return card_dict


def determine_winnings(scratch_cards):
    """
    """
    _sum = 0
    # split each card up
    card_strings = scratch_cards.split('\n')
    print(len(card_strings))
    # loop over all cards
    for i, card_string in enumerate(card_strings):
        # parse the string 
        #print(card_string)
        try:
            card_results = parse_card(card_string)
        except:
            continue
        # determine inner join between winning and card numbers
        # quick implementation using sets... 
        # works because the set removes redundant instances of an element. so
        # difference in length between the combined list and the set is the 
        # count of duplicate elements (the inner join) between the two lists  
        # NOTE: might cause bugs if the game allows for duplicate numbers in 
        # card_numbers but expects these instances to count only once
        count = len(card_results[0] + card_results[1]) - len(set(card_results[0]+card_results[1]))
        print(i, count, _sum)
        # determine points
        if count > 0:
            points = 2**(count-1)
            # add to sum
            _sum += points
    return _sum

### TEST HANDLES
if __name__ == '__main__':
    scratch_cards = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    value = determine_winnings(scratch_cards)
    print(value)
    assert value == 13

    with open('./scratch_cards.txt','r') as infile:
        scratch_cards = infile.read()
    value = determine_winnings(scratch_cards)
    print(value)

