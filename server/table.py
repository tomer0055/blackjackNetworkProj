from server.deck import deck
from server.dealer import dealer
#THis is my LOCAL VERSION --------------------------------
#Round result codes (for network payload)
ROUND_NOT_OVER = 0x0
TIE = 0x1
PLAYER_LOSE = 0x2
PLAYER_WIN = 0x3 

class table :

    def __init__(self, player):
        self.player = player
        self.dealer = dealer()
        self.deck = None
        self.round_over = False

    def start_round(self):
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.round_over = False
        self.deck = deck()
        for _ in range(2):
            self.player.hit(self.deck.draw())
            self.dealer.hit(self.deck.draw())

        #Return dealer's visible card
        return self.dealer.get_hand()[0]

    def player_hit(self):
        card = self.deck.draw()
        self.player.hit(card)

        if self.player.hand_value() > 21:
            self.round_over = True
        return card

    def player_stand(self):
        self.player.stand()
        self._dealer_turn()
        self.round_over = True

    def _dealer_turn(self):
        while self.dealer.should_hit():
            self.dealer.hit(self.deck.draw())
        self.dealer.stand()
    
    def get_round_result(self) -> int:
        if not self.round_over:
            return ROUND_NOT_OVER

        p = self.player.hand_value()
        d = self.dealer.hand_value()

        if p > 21:
            return PLAYER_LOSE
        if d > 21:
            return PLAYER_WIN
        if p > d:
            return PLAYER_WIN
        if d > p:
            return PLAYER_LOSE
        return TIE