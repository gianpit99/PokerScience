
import random

class Deck:
    def __init__(self):
        self.deck = ['Ah', 'As', 'Ad', 'Ac',
                     '2h', '2s', '2d', '2c',
                     '3h', '3s', '3d', '3c',
                     '4h', '4s', '4d', '4c',
                     '5h', '5s', '5d', '5c',
                     '6h', '6s', '6d', '6c',
                     '7h', '7s', '7d', '7c',
                     '8h', '8s', '8d', '8c',
                     '9h', '9s', '9d', '9c',
                     'Th', 'Ts', 'Td', 'Tc',
                     'Jh', 'Js', 'Jd', 'Jc',
                     'Qh', 'Qs', 'Qd', 'Qc',
                     'Kh', 'Ks', 'Kd', 'Kc']

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()
