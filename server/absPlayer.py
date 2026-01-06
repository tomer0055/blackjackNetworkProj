class absPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.standing = False
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_hand(self):
        return self.hand
    def hand_value(self) -> int:
        return sum(card.get_value() for card in self.hand)
    def reset_hand(self):
        self.hand = []
        self.standing = False
    def hit(self, card):
        if self.standing:
            raise RuntimeError("Cannot hit after standing")
        self.hand.append(card)
    def stand(self):
        self.standing = True
    
    