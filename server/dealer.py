from server import absPlayer


class dealer(absPlayer):
    deck = []
    table= None
    def __init__(self,table):
        super().__init__("Dealer")
        self.corrent_score = 0
        self.table = table
    def shuffle_deck(self, deck):
        self.deck = deck
    def deal_card(self):
        if len(self.deck) == 0:
            return None
        return self.deck.pop()
    def check_if_higher_than_17(self):
        return self.current_score > 17
    def hit(self, card):
        while(self.check_if_higher_than_17==False):
            self.hand.append(card)
            self.current_score += card.get_value()
        self.table.end_round()


