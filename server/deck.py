import random
from server.card import card
class deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()
    def build(self): #we need to use numbers for protocol, later in view we will use good UX names
        self.cards = [
            card(rank, suit)
            for suit in range(4)
            for rank in range(1, 14)
        ]
    def shuffle(self):
        random.shuffle(self.cards)
    def draw(self):
        if not self.cards:
            raise RuntimeError("Deck is empty")
        return self.cards.pop()