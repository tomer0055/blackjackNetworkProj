from server.deck import deck
from server.dealer import dealer
from server.player import player
#Round result codes (for network payload)
ROUND_NOT_OVER = 0x0
TIE = 0x1
PLAYER_LOSE = 0x2
PLAYER_WIN = 0x3 

class table :
    round_result = 0x0
    

    def __init__(self, player:player):
        self.p = player
        self.dealer = dealer(self)
        self.deck = None
        self.round_over = False

    def start_round(self):
        self.p.reset_hand()
        self.dealer.reset_hand()
        self.round_over = False
        self.deck = deck()
        for _ in range(2):
            self.p.hit(self.deck.draw())
            self.dealer.hit_once(self.deck.draw())

        #Return dealer's visible card
        return self.dealer.get_hand()[0]

    def player_hit(self):
        card = self.deck.draw()
        self.p.hit(card)
        if(self.p.hand_value() > 21):
            self.round_over = True
            self.round_result = self.get_round_result()  # Check if round is over after hit
        return card

    def player_stand(self):
        self.p.stand()
        self._dealer_turn()
        self.round_over = True

    def _dealer_turn(self):
        while self.dealer.hand_value() < 17:
            self.dealer.hit_once(self.deck.draw())
        round_result=self.get_round_result()  # Final result after dealer's turn
        
    
    def get_round_result(self) -> int:
        
        p = self.p.hand_value()
        d = self.dealer.hand_value()

        if p > 21:
            self.p.add_loss()
            return PLAYER_LOSE
        if d > 21:
            self.p.add_win()
            return PLAYER_WIN
        if p > d:
            self.p.add_win()
            return PLAYER_WIN
        if d > p:
           self.p.add_loss()
           return PLAYER_LOSE
        
        self.p.add_tie()
        return TIE





    def game(self):
        self.start_round()
        d_card = self.dealer.get_hand()[0]
        p_hand = self.p.get_hand()[0]
        self.p.init_game()
        while not self.round_over:
            decision = self.p.make_decision(self.round_result,d_card)
            if decision == 1:
                self.player_hit()
                self.p.tcp.send_round_update(self.round_result, self.p.get_hand()[-1].rank, self.p.get_hand()[-1].suit)
            elif decision == 0:
                self.player_stand()
                self.p.tcp.send_round_update(self.round_result, self.p.get_hand()[-1].rank, self.p.get_hand()[-1].suit)

            else:
                raise ValueError("Invalid decision")
        


        