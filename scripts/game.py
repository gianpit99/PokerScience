from hand_evaluator import eval7
from deck import Deck

class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck()


        self.bb = 0
        self.sb = 0
        self.anti = 0

        self.pot = 0
        self.table = []

    def dealFlop(self):
        for _ in range(3):
            self.table.append(self.deck.deal())

    def dealTurn(self):
        self.table.append(self.deck.deal())

    def dealRiver(self):
        self.table.append(self.deck.deal())

    def newHand(self):
        self.deck = Deck()
        self.table = []
        self.pot = 0

    def addPlayer(self, player):
        self.players.append(player)

    def handScore(self, hand, table):
        return eval7(hand + table)
