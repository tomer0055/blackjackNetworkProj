from network_module.msg_format import msgFormatHandler

class Play:
    def __init__(self, clientNet, view):
        self.clientNet = clientNet
        self.view = view
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.player_cards = []
        self.dealer_card = None
        self.initial_cards_received = 0
        self.initial_deal_done = False
        self.waiting_for_decision = False

    def start_game(self,roundsNum):
        self.view.show_game_start(roundsNum)
        for round_index in range(1, roundsNum + 1):
            self.view.show_round_start(round_index)
            self.play_single_round()
        self.view.end_game(self.wins, self.losses, self.ties)    

    def reset_stats(self):
        self.player_cards = []
        self.dealer_card = None
        self.initial_cards_received = 0
        self.initial_deal_done = False
        self.waiting_for_decision = False

    def get_card(self):
        data = self.clientNet.receive_tcp()
        parsed = msgFormatHandler.client_receive_payload_parse(data)
        if parsed is None:
            raise RuntimeError("Received invalid initial game payload")
        round_result, card_rank, card_suit = parsed
        return round_result, card_rank, card_suit 

    def init_game(self):
        print("Dealing initial cards...")

        round_result, card_rank, card_suit  =self.get_card()  # First card
        self.player_cards.append((card_rank, card_suit))

        round_result, card_rank, card_suit  =self.get_card()  # Second card
        self.player_cards.append((card_rank, card_suit))

        # Check if round is over after initial deal and add 
        if(round_result != 0x0):
            self.handle_round_result(round_result)
            return

        round_result, card_rank, card_suit  =self.get_card()  # Dealer's visible card
        self.dealer_card = (card_rank, card_suit)

        self.view.show_round_state(self.player_cards, self.dealer_card)

    def ask_player_decision(self):
        
        while True:
            decision = self.view.ask_player_decision()
            self.clientNet.send(msgFormatHandler.to_payload_format_client(decision))
            if(decision == "Stand"):
                self.stand_decision()
                return

            if(decision == "Hittt"):
                res=self.hit_decision() 
                if(res == -1):
                    return


    def stand_decision(self):
        round_result, card_rank, card_suit  =self.get_card()
        self.view.show_dealer_card(card_rank, card_suit)
        while round_result == 0x0:
            round_result, card_rank, card_suit  =self.get_card()
            self.view.show_dealer_card(card_rank, card_suit)
        self.handle_round_result(round_result)
    
    def hit_decision(self):
        round_result, card_rank, card_suit  =self.get_card()
        print(f"Received card after hit. result{round_result}")
        self.player_cards.append((card_rank, card_suit))
        self.view.show_player_card(card_rank, card_suit)
        if round_result != 0x0:
            print(f"Received round result after hit. Result: {round_result}, Card: {card_rank} of {card_suit}")
            self.handle_round_result(round_result)
            return -1
        return 0

        



    def play_single_round(self):
        print("Starting a new round...")
        self.reset_stats()
        self.init_game()
        self.ask_player_decision()
    

                
                
    def handle_round_result(self, round_result):
        self.view.show_round_result(round_result)
        if round_result == 0x3:
            self.wins += 1
        elif round_result == 0x2:
            self.losses += 1
        elif round_result == 0x1:
            self.ties += 1               
        

    
