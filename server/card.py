class card:
    suit= None 
    rank = ""
    value = 0
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
    def get_suit(self):
        return self.suit
    def get_rank(self):
        return self.rank
    def get_value(self):
        return self.value

from enum import Enum, auto
class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()