

from game import *
from hand_evaluator import eval7
import numpy as np

def main():
    best_hand = []
    best_score = np.inf

    for i in range(1):
        print("{:.2f}".format(i / 1 * 100))
        game = Game()

        hand = []
        for _ in range(7):
            hand.append(game.deck.deal())

        score = eval7(hand)
        if best_score > score:
            best_score = score
            best_hand = hand

    print()
    print("HAND: {}, SCORE: {}".format(best_hand, best_score))


if __name__ == "__main__":
    main()
