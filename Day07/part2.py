### QUESTION
"""
https://adventofcode.com/2023/day/7
"""

### PREAMBLE

#cards = '23456789TJQKA' # ordered so that index in string is ranking as well
cards = 'J23456789TQKA' # ordered so that index in string is ranking as well
# use cards.find(substring) to get index of the substring

### FUNCTIONS

def determine_winnings(game_string):
    """
    """
    # parse the input string
    hands_bids = parse_games(game_string)
    nHands = len(hands_bids)
    # determine hand types
    hands_dict = judge_hands(hands_bids)
    # rank hands
    hands_ranked = rank_hands(hands_dict)
    #print(list(zip(range(nHands,0,-1),hands_ranked)))
    # calculate the sum of hand_bid*rank
    winnings = sum([rank*hand[1] for rank, hand in zip(range(nHands,0,-1),hands_ranked)])
    return winnings


def parse_games(game_string):
    """
    parse the hands_bids string that defines all hands to be analyzed
    """
    return [line.split() for line in game_string.split('\n') if line]


def judge_hands(hands_list):
    """
    loop over all hands and determine their type and card ranks
    """
    # prep the hand_type dict
    hand_types = {'5': [], 
                  '4': [], 
                  'fullhouse':[], 
                  '3': [],
                  'twopair':[],
                  '2': [],
                  '1': []}
    # loop over all hands
    for hand in hands_list:
        # get card ranking list, will be a list of indices for each card in hand
        card_ranks = [cards.find(card) for card in hand[0]]
        # determine number of jokers
        nJokers = card_ranks.count(0)
        # determine the set of card types in hand, using card rank numbers
        card_types = set(card_ranks)
        # loop over card types and count how many are observed, ignoring jokers
        counts = [card_ranks.count(card) for card in card_types if card != 0]
        # if there are only jokers in the hand: 
        if nJokers == 5:
            counts = [5]
        # if jokers are present alongside other cards, add their count to the 
        # maximum count value for those other cards
        elif nJokers:
            max_index = counts.index(max(counts))
            counts[max_index] += nJokers

        # boolean tests to determine type of hand, append 
        # (card_ranks, bid, hand_string) to respective hand types
        # fullhouse and two pair are the most difficult to determine so check 
        # those first
        if counts in [[3,2],[2,3]]:
            hand_types['fullhouse'].append((card_ranks,
                                            int(hand[1]),
                                            hand[0]))
        elif counts in [[2,2,1],[2,1,2],[1,2,2]]:
            hand_types['twopair'].append((card_ranks,
                                          int(hand[1]),
                                          hand[0]))
        # other hand types are directly determined by the maximum value in the
        # card_ranks so get those and append (card_ranks, bid) to the 
        # appropriate dictionary key's list
        else:
            # grab the maximum counts value, which will be the key in the 
            # hand_types dictionary 
            max_count = str(max(counts))
            hand_types[max_count].append((card_ranks,
                                          int(hand[1]),
                                          hand[0]))

    return hand_types


def rank_hands(hand_dict):
    """
    take dictionary of hand types, where keys are the hand type and values are
    lists of hands of that type
    """
    ranked_hands = []
    for key in ['5','4','fullhouse','3','twopair','2','1']:
        hands_list = hand_dict[key]
        # each element in hands_list is a tuple of (card_ranks, bid), sort the
        # hands_list by card ranking, decending priority from first card to 
        # last card.
        hands_list.sort(key = lambda x: (x[0][0],x[0][1],x[0][2],x[0][3],x[0][4]), reverse=True)
        # extend the ranked_hands list with the now sorted hands_list
        ranked_hands.extend(hands_list)
        #print(key,'\n',hands_list)
    return ranked_hands


### TEST HANDLING
if __name__ == '__main__':
    hands_bids_string = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    value = determine_winnings(hands_bids_string)
    print(value)
    assert value == 5905

    with open('./camel_card_hands.txt','r') as infile:
        hands_bids_string = infile.read()
    value = determine_winnings(hands_bids_string)
    print(value)


