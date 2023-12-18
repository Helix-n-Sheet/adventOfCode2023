### QUESTION
"""
... it looks like each card has two lists of numbers separated by a vertical bar 
(|): a list of winning numbers and then a list of numbers you have. You organize 
the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of 
the numbers you have appear in the list of winning numbers. The first match 
makes the card worth one point and each match after the first doubles the point 
value of that card.

For example:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) 
and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers 
you have, four of them (48, 83, 17, and 86) are winning numbers! That means 
card 1 is worth 8 points (1 for the first match, then doubled three times for 
each of the three matches after the first).

Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
Card 4 has one winning number (84), so it is worth 1 point.
Card 5 has no winning numbers, so it is worth no points.
Card 6 has no winning numbers, so it is worth no points.
So, in this example, the Elf's pile of scratchcards is worth 13 points.

Take a seat in the large pile of colorful cards. How many points are they worth 
in total?
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

