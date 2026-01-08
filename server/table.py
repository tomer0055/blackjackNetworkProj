from server.deck import deck
from server.dealer import dealer
from server.player import player
#THis is my LOCAL VERSION --------------------------------
#Round result codes (for network payload)
ROUND_NOT_OVER = 0x0
TIE = 0x1
PLAYER_LOSE = 0x2
PLAYER_WIN = 0x3 

class table :

    def __init__(self, player:player):
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

        self.get_round_result()  # Check if round is over after hit
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
        
        p = self.player.hand_value()
        d = self.dealer.hand_value()

        if p > 21:
            player.add_loss()
            return PLAYER_LOSE
        if d > 21:
            player.add_win()
            return PLAYER_WIN
        if p > d:
            player.add_win()
            return PLAYER_WIN
        if d > p:
            player.add_loss()
            return PLAYER_LOSE
        
        player.add_tie()
        return TIE





    def game(self):
        self.start_round()
        d_hand = self.dealer.get_hand()[0]
        p_hand = self.player.get_hand()[0]
        player.init_game(d_hand[0])
        while not self.round_over:
            decision = self.player.make_decision(self.get_round_result,d_hand,p_hand)
            if decision == 1:
                self.player_hit()
            elif decision == 0:
                self.player_stand()
            else:
                raise ValueError("Invalid decision")
        


        