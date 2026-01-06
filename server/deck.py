class deck:
    cards = []
    def __init__(self, cards):
        self.cards = cards
    def shuffle(self):
        import random
        random.shuffle(self.cards)
    def deal_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()