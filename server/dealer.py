from server.absPlayer import absPlayer
from server.card import card


class dealer(absPlayer):
    tb = None
    def __init__(self,table):
        super().__init__("Dealer")
        self.current_score = 0
        self.tb = table

    def shuffle_deck(self, deck):
        self.deck = deck

    def deal_card(self):
        if len(self.deck) == 0:
            return None
        return self.deck.pop()
    

    def check_if_higher_than_17(self):
        return self.current_score > 17


    def hit_once(self, card:card):
        self.hand.append(card)
        self.current_score += card.get_value()
       


