

from game import *
from deck import *
from hand_evaluator import *
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import os


def suited(cards):
    '''
    method that returns true if the hand is suited and false otherwise
    '''
    
    return cards[0][1] == cards[1][1]

def getWinners(playersHands, table):
    '''
    method that takes players hands and tables and returns a binary array
    of 1 indicating that a player won/tied or 0 indicating that a player
    lost

    parameters
    ----------
    playersHands : list of list of players cards

    table : list of table cards

    returns
    -------
    binary array indicating if the player won/tied (1) or lost (0)
    '''

    # Create an array to hold the players hand rank
    hand_ranks = []

    # Calculate the hand rank for each player
    for hand in playersHands:
        hand_ranks.append(eval7(hand + table))

    # Find the best rank of the hands
    min_rank = min(hand_ranks)

    # return 1 if the players hand rank is the same as the best (tie or win)
    return [min_rank == hand_rank for hand_rank in hand_ranks]

def getHandClass(hand):
    '''
    method that takes a players hand, and formats a string in one of the three
    caategories
    - pocket pair (e.g. (Ah, As) -> 'AA')
    - Suited cards (e.g. (Ah, Th) -> 'ATs')
    - Off Sutied cards (e.g. (Ah, Ts) -> 'ATo')

    parameters
    ----------
    hand : array of length 2 containing a players two cards


    return
    ------
    formated string of players hand class (pockets, suited, non-suited)
    '''

    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    card1_face = hand[0][0]
    card1_suit = hand[0][1]
    card2_face = hand[1][0]
    card2_suit = hand[1][1]

    # If the cards are pockets
    if card1_face == card2_face:
        return card1_face + card2_face

    # If the cards are suited
    if card1_suit == card2_suit:
        suited_marker = 's'
    else:
        suited_marker = 'o'

    # Return the higher card first
    if cards.index(card1_face) > cards.index(card2_face):
        return card1_face + card2_face + suited_marker
    else:
        return card2_face + card1_face + suited_marker


def range_win_prob(num_players, num_hands, verbose=True):
    '''
    function that takes a given number of players and a given number of hands
    and returns the win rate and hand played rate for each hand class

    parameters
    ----------

    num_players : int for the number of players

    num_hands : int for the number of hands to run

    verbose : weather or not to plot the results

    returns
    -------
    win_count : dictionary for each hand class that show an int of the number of hands won

    play_count : dictionary for each hand class that show an int of the number of hands played
    '''



    SUIT_TO_INDEX = {'':''}

    play_count = {'AA':0, 'AKs':0, 'AQs':0, 'AJs':0, 'ATs':0, 'A9s':0, 'A8s':0, 'A7s':0, 'A6s':0, 'A5s':0, 'A4s':0, 'A3s':0, 'A2s':0,
                  'AKo':0, 'KK':0, 'KQs':0, 'KJs':0, 'KTs':0, 'K9s':0, 'K8s':0, 'K7s':0, 'K6s':0, 'K5s':0, 'K4s':0, 'K3s':0, 'K2s':0,
                  'AQo':0, 'KQo':0, 'QQ':0, 'QJs':0, 'QTs':0, 'Q9s':0, 'Q8s':0, 'Q7s':0, 'Q6s':0, 'Q5s':0, 'Q4s':0, 'Q3s':0, 'Q2s':0,
                  'AJo':0, 'KJo':0, 'QJo':0, 'JJ':0, 'JTs':0, 'J9s':0, 'J8s':0, 'J7s':0, 'J6s':0, 'J5s':0, 'J4s':0, 'J3s':0, 'J2s':0,
                  'ATo':0, 'KTo':0, 'QTo':0, 'JTo':0, 'TT':0, 'T9s':0, 'T8s':0, 'T7s':0, 'T6s':0, 'T5s':0, 'T4s':0, 'T3s':0, 'T2s':0,
                  'A9o':0, 'K9o':0, 'Q9o':0, 'J9o':0, 'T9o':0, '99':0, '98s':0, '97s':0, '96s':0, '95s':0, '94s':0, '93s':0, '92s':0,
                  'A8o':0, 'K8o':0, 'Q8o':0, 'J8o':0, 'T8o':0, '98o':0, '88':0, '87s':0, '86s':0, '85s':0, '84s':0, '83s':0, '82s':0,
                  'A7o':0, 'K7o':0, 'Q7o':0, 'J7o':0, 'T7o':0, '97o':0, '87o':0, '77':0, '76s':0, '75s':0, '74s':0, '73s':0, '72s':0,
                  'A6o':0, 'K6o':0, 'Q6o':0, 'J6o':0, 'T6o':0, '96o':0, '86o':0, '76o':0, '66':0, '65s':0, '64s':0, '63s':0, '62s':0,
                  'A5o':0, 'K5o':0, 'Q5o':0, 'J5o':0, 'T5o':0, '95o':0, '85o':0, '75o':0, '65o':0, '55':0, '54s':0, '53s':0, '52s':0,
                  'A4o':0, 'K4o':0, 'Q4o':0, 'J4o':0, 'T4o':0, '94o':0, '84o':0, '74o':0, '64o':0, '54o':0, '44':0, '43s':0, '42s':0,
                  'A3o':0, 'K3o':0, 'Q3o':0, 'J3o':0, 'T3o':0, '93o':0, '83o':0, '73o':0, '63o':0, '53o':0, '43o':0, '33':0, '32s':0,
                  'A2o':0, 'K2o':0, 'Q2o':0, 'J2o':0, 'T2o':0, '92o':0, '82o':0, '72o':0, '62o':0, '52o':0, '42o':0, '32o':0, '22':0}

    win_count = {'AA':0, 'AKs':0, 'AQs':0, 'AJs':0, 'ATs':0, 'A9s':0, 'A8s':0, 'A7s':0, 'A6s':0, 'A5s':0, 'A4s':0, 'A3s':0, 'A2s':0,
                 'AKo':0, 'KK':0, 'KQs':0, 'KJs':0, 'KTs':0, 'K9s':0, 'K8s':0, 'K7s':0, 'K6s':0, 'K5s':0, 'K4s':0, 'K3s':0, 'K2s':0,
                 'AQo':0, 'KQo':0, 'QQ':0, 'QJs':0, 'QTs':0, 'Q9s':0, 'Q8s':0, 'Q7s':0, 'Q6s':0, 'Q5s':0, 'Q4s':0, 'Q3s':0, 'Q2s':0,
                 'AJo':0, 'KJo':0, 'QJo':0, 'JJ':0, 'JTs':0, 'J9s':0, 'J8s':0, 'J7s':0, 'J6s':0, 'J5s':0, 'J4s':0, 'J3s':0, 'J2s':0,
                 'ATo':0, 'KTo':0, 'QTo':0, 'JTo':0, 'TT':0, 'T9s':0, 'T8s':0, 'T7s':0, 'T6s':0, 'T5s':0, 'T4s':0, 'T3s':0, 'T2s':0,
                 'A9o':0, 'K9o':0, 'Q9o':0, 'J9o':0, 'T9o':0, '99':0, '98s':0, '97s':0, '96s':0, '95s':0, '94s':0, '93s':0, '92s':0,
                 'A8o':0, 'K8o':0, 'Q8o':0, 'J8o':0, 'T8o':0, '98o':0, '88':0, '87s':0, '86s':0, '85s':0, '84s':0, '83s':0, '82s':0,
                 'A7o':0, 'K7o':0, 'Q7o':0, 'J7o':0, 'T7o':0, '97o':0, '87o':0, '77':0, '76s':0, '75s':0, '74s':0, '73s':0, '72s':0,
                 'A6o':0, 'K6o':0, 'Q6o':0, 'J6o':0, 'T6o':0, '96o':0, '86o':0, '76o':0, '66':0, '65s':0, '64s':0, '63s':0, '62s':0,
                 'A5o':0, 'K5o':0, 'Q5o':0, 'J5o':0, 'T5o':0, '95o':0, '85o':0, '75o':0, '65o':0, '55':0, '54s':0, '53s':0, '52s':0,
                 'A4o':0, 'K4o':0, 'Q4o':0, 'J4o':0, 'T4o':0, '94o':0, '84o':0, '74o':0, '64o':0, '54o':0, '44':0, '43s':0, '42s':0,
                 'A3o':0, 'K3o':0, 'Q3o':0, 'J3o':0, 'T3o':0, '93o':0, '83o':0, '73o':0, '63o':0, '53o':0, '43o':0, '33':0, '32s':0,
                 'A2o':0, 'K2o':0, 'Q2o':0, 'J2o':0, 'T2o':0, '92o':0, '82o':0, '72o':0, '62o':0, '52o':0, '42o':0, '32o':0, '22':0}

    for hand_number in range(num_hands):
        if verbose: print("Completion: {:.2f}".format(hand_number /num_hands * 100))

        deck = Deck()
        playersHands =[]

        # Deal two cards for each player
        for _ in range(num_players):
            playersHands.append([deck.deal(), deck.deal()])

        # Deal the table
        table = [deck.deal(), deck.deal(), deck.deal(), deck.deal(), deck.deal()]

        # Check which players won
        winners = getWinners(playersHands, table)

        # Iterate over the winners and losers
        for i, winner in enumerate(winners):
            # Increment the play count if the hand was played
            play_count[getHandClass(playersHands[i])] += 1

            if winner == 1: # If the hand was a winner
                win_count[getHandClass(playersHands[i])] += 1

        del deck
        del table
        del winners
        del playersHands

    # Normalize the win counts to get the win percentages
    win_percentage = {}
    for handType, playCount in play_count.items():
        win_percentage[handType] = win_count[handType] / play_count[handType]

    #Get the card combinations and counts for each combination
    if verbose:
        handClass = list(win_percentage.keys())
        winPercent = list(win_percentage.values())

        for i, name in enumerate(handClass):
            handClass[i] += '\n' + '{:.{}f}'.format(winPercent[i], 4)

        #Format the labels as a numpy array for seaborn
        labels = []
        data = []
        for i in range(13):
            labels.append(handClass[i*13:i*13+13])
            data.append(winPercent[i*13:i*13+13])

        # Create a numpy array for the data and labels for ploting
        labels = np.array(labels)
        data = np.array(data)

        # Create the plot
        fig, ax = plt.subplots(figsize=(14, 12))

        # Populate the plot
        ax = sns.heatmap(data, annot = labels, linewidths=.5, fmt = '')

        # Set the labels on the plots
        ax.set(xticklabels=[])
        ax.set(yticklabels=[])
        ax.set(title='Winning Probabilities for {} Person Poker'.format(num_players))

        # Show the plot
        plt.show()

    # Return the win_count and play_count dictionaries
    return win_count, play_count



def parrallelizeRange(num_players, num_hands_per_process, number_of_process, verbose=True):
    '''
    function to compute the range_win_prob function in parrallel for better
    performance
    '''
    parameters = [(num_players, num_hands_per_process, False) for _ in range(number_of_process)]

    with Pool(os.cpu_count()) as p:
        results = p.starmap(range_win_prob, parameters)

    for i, result in enumerate(results):
        if i == 0:
            win_count, play_count = result
            continue

        for key, _ in win_count.items():
            win, play = result

            win_count[key] += win[key]
            play_count[key] += play[key]

    win_prob = {}
    for key, value in win_count.items():
        win_prob[key] = win_count[key] / play_count[key]

    #Get the card combinations and counts for each combination
    if verbose:
        handClass = list(win_prob.keys())
        winPercent = list(win_prob.values())


        for i, name in enumerate(handClass):
            handClass[i] += '\n' + '{:.{}f}'.format(winPercent[i], 4)

        #Format the labels as a numpy array for seaborn
        labels = []
        data = []
        for i in range(13):
            labels.append(handClass[i*13:i*13+13])
            data.append(winPercent[i*13:i*13+13])

        labels = np.array(labels)
        data = np.array(data)

        fig, ax = plt.subplots(figsize=(14, 12))

        ax = sns.heatmap(data, annot = labels, linewidths=.5, fmt = '')

        ax.set(xticklabels=[])
        ax.set(yticklabels=[])
        ax.set(title='Winning Probabilities for {} Person Poker'.format(num_players))

        plt.show()

    return win_prob

if __name__ == "__main__":
    parrallelizeRange(2, 10000, 10)
