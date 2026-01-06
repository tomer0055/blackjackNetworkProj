class card:
    suit= None 
    rank = ""
    value = 0
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def get_suit(self):
        return self.suit
    def get_rank(self):
        return self.rank
    def get_value(self):
        # Ace
        if self.rank == 1:
            return 11
        # J, Q, K
        if self.rank >= 11:
            return 10
        # 2–10
        return self.rank

from enum import Enum, auto
class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()