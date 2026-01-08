from server.deck import deck
from server.dealer import dealer
from server.player import player
from server.absPlayer import absPlayer
#Round result codes (for network payload)
ROUND_NOT_OVER = 0x0
TIE = 0x1
PLAYER_LOSE = 0x2
PLAYER_WIN = 0x3 

class table :
    
    
    round_over=False
    def __init__(self, player:player):
        self.p = player
        self.dealer = dealer(self)
        self.deck = None
        self.round_result=ROUND_NOT_OVER

    def start_round(self):
        print("____________Starting new round...")
        self.p.reset_hand()
        self.dealer.reset_hand()
        self.round_over = False
        self.round_result = ROUND_NOT_OVER
        self.deck = deck()
        for _ in range(2):
            self.p.hit(self.deck.draw())
            self.dealer.hit_once(self.deck.draw())
        print("INIT--Player's hand:", [f"{card.rank} of {card.suit}" for card in self.p.get_hand()])
        print("INIT--Dealer's hand:", [f"{card.rank} of {card.suit}" for card in self.dealer.get_hand()])
        #Return dealer's visible card
        return self.dealer.get_hand()[0]

    def player_hit(self):
        card = self.deck.draw()
        self.p.hit(card)
        self.send_card_to_player(self.p, self.p.get_hand()[-1])
        return card

    def player_stand(self):
        self.p.stand()
        self.dealer_turn_over()


    # def _dealer_turn(self):
    #     # show hidden card
    #     self.round_result = self.get_round_result()
    #     self.p.tcp.send_round_update(self.round_result, self.dealer.get_hand()[-1].get_value(), self.dealer.get_hand()[-1].suit)# second card

    #     while self.dealer.hand_value() < 17 and not self.round_over:
    #         print(f" D hand value = {self.dealer.hand_value()}") 
    #         self.dealer.hit_once(self.deck.draw())
    #         print("Dealer hits:", [f"{card.rank} of {card.suit}" for card in self.dealer.get_hand()])
    #         if(self.dealer.hand_value() > 21):
    #             self.round_over = True
    #         if(self.round_over or self.dealer.hand_value() >=17):
    #             self.round_result = self.get_round_result()    
    #         self.p.tcp.send_round_update(self.round_result, self.dealer.get_hand()[-1].get_value(), self.dealer.get_hand()[-1].suit)
    #     self.round_over = True
       
    def dealer_turn_over(self):
        #show hidden card.
        self.send_card_to_player(self.p, self.dealer.get_hand()[-1]) # second card
        while self.get_round_result() == ROUND_NOT_OVER:
            self.dealer.hit_once(self.deck.draw())
            self.send_card_to_player(self.p, self.dealer.get_hand()[-1])
        self.round_over = True




         # Final result after dealer's turn
    def send_card_to_player(self,user, card):
        res = self.get_round_result()
        user.tcp.send_round_update(res, card.rank, card.suit)
        

    
    def get_round_result(self) -> int:
        if(self.round_over):
            
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
            
            if p == d:
                self.p.add_tie()
                return TIE
            
        if(self.dealer.hand_value() >=17 and self.p.is_standing()):
            self.round_over = True
            return self.get_round_result()
        
        if self.p.hand_value() > 21:
            self.round_over = True
            return self.get_round_result()
            
        return ROUND_NOT_OVER

  

    def game(self):
        self.start_round()
        print(f"Game started. with player {self.p.get_name()}")

        self.send_card_to_player(self.p, self.p.get_hand()[0]) # first card
        self.send_card_to_player(self.p, self.p.get_hand()[1]) # second card

        d_card = self.dealer.get_hand()[0]
        print("Dealer's visible card:", d_card.get_value(), d_card.suit)
        self.send_card_to_player(self.p, d_card)
        while not self.round_over:
            print("Player's current hand:", [f"{card.rank} of {card.suit}" for card in self.p.get_hand()])
            decision = self.p.wait_for_round_result()
            if decision == 1:
                self.player_hit()
            elif decision == 0:
                self.player_stand()
            else:
                raise ValueError("Invalid decision")
        print("Round over. Result code:", self.round_result)
        


        