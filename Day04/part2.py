### QUESTION
"""
... you win copies of the scratchcards below the winning card equal to the 
number of matches. So, if card 10 were to have 5 matching numbers, you would 
win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same 
card number as the card they copied. So, if you win a copy of card 10 and it 
has 5 matching numbers, it would then win a copy of the same cards that the 
original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until 
none of the copies cause you to win any more cards. (Cards will never make you 
copy a card past the end of the table.)

This time, the above example goes differently:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

- Card 1 has four matching numbers, so you win one copy each of the next four 
  cards: cards 2, 3, 4, and 5.
- Your original card 2 has two matching numbers, so you win one copy each of 
  cards 3 and 4.
- Your copy of card 2 also wins one copy each of cards 3 and 4.
- Your four instances of card 3 (one original and three copies) have two 
  matching numbers, so you win four copies each of cards 4 and 5.
- Your eight instances of card 4 (one original and seven copies) have one 
  matching number, so you win eight copies of card 5.
- Your fourteen instances of card 5 (one original and thirteen copies) have no 
  matching numbers and win no more cards.
- Your one instance of card 6 (one original) has no matching numbers and wins no 
  more cards.

Once all of the originals and copies have been processed, you end up with 1 
instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of 
card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example 
pile of scratchcards causes you to ultimately have 30 scratchcards!

Process all of the original and copied scratchcards until no more scratchcards 
are won. Including the original set of scratchcards, how many total scratchcards 
do you end up with?
"""

### PREAMBLE
import re

### FUNCTIONS

def parse_card(card_string):
    """
    parse the standard formatted strings associated with scratch cards
    """
    # grab card_id
    card_id = int(re.search(r'\d+',card_string)[0])
    # grab strings associated with winning and card numbers
    winning_numbers, card_numbers = card_string.split(':')[1].split('|')
    # parse the strings to get the individual numbers, formatted as str
    winning_numbers = winning_numbers.split()
    card_numbers = card_numbers.split()
    # return a list of lists where 0th list is the winning numbers and 1st list
    # is the card numbers
    card_results = [winning_numbers, card_numbers]
    return card_id, card_results
    
    ## create the card_dict where card_id is the key and the value is a tuple of
    ## the winning_numbers and card_numbers
    ## grab card_id to use as key for dictionary
    #card_dict = {card_id: (winning_numbers, card_numbers)}
    #return card_dict


def determine_nCards(scratch_cards):
    """
    """
    # split each card up
    card_strings = scratch_cards.split('\n')
    # initiate the card_counts dict 
    card_counts = {}
    # loop over all cards, starting from card 1 that has only one instance
    for card_string in card_strings:
        try:
            card_id, card_results = parse_card(card_string)
            # grab value of card_counts for card_id if already present in dict
            # otherwise set card_counts[card_id] value to 1
            card_counts[card_id] = card_counts.get(card_id,1)
        except Exception as e:
            continue
        
        # determine inner join between winning and card numbers
        # quick implementation using sets... 
        # works because the set removes redundant instances of an element. so
        # difference in length between the combined list and the set is the 
        # count of duplicate elements (the inner join) between the two lists  
        # NOTE: might cause bugs if the game allows for duplicate numbers in 
        # card_numbers but expects these instances to count only once
        join = len(card_results[0] + card_results[1]) - len(set(card_results[0]+card_results[1]))
  
        # if the join between winning and card numbers is greater than 0, we get
        # `card_counts[card_id]` more instances of scratch cards that are at 
        # most `join` cards after `card_id`. 
        if join > 0:
            # loop over card_ids that are, at most, `join` distance after 
            # `card_id`
            for copy in range(card_id+1, card_id+1+join):
                card_counts[copy] = card_counts.get(copy,1) + card_counts[card_id] 
        else:
            continue

    # sum up all counts
    _sum = sum([val for val in card_counts.values()])
    return _sum

### TEST HANDLES
if __name__ == '__main__':
    scratch_cards = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    value = determine_nCards(scratch_cards)
    print(value)
    assert value == 30

    with open('./scratch_cards.txt','r') as infile:
        scratch_cards = infile.read()
    value = determine_nCards(scratch_cards)
    print(value)

