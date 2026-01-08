from enum import Enum

class Suit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3


class card:
    suit= None 
    rank = ""
    value = 0
    def __init__(self, rank ,suit:Suit):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit
    
    def get_suit_value(self):
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

