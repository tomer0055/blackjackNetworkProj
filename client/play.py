from network_module.msg_format import msgFormatHandler
from client.view import view

class Play:
    def __init__(self, clientNet, view:view):
        self.clientNet = clientNet
        self.ui = view
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.player_cards = []
        self.dealer_card = None
        self.initial_cards_received = 0

    def start_game(self,roundsNum):
        self.ui.show_game_start(roundsNum)
        for round_index in range(1, roundsNum + 1):
            self.ui.show_round_start(round_index)
            self.play_single_round()
        self.ui.end_game(self.wins, self.losses, self.ties)    
        
    def play_single_round(self):
        self.player_cards = []
        self.dealer_card = None
        self.initial_cards_received = 0
        
        while True:
            # Receive payload from server
            data = self.clientNet.receive_tcp()

            # Parse payload using protocol handler
            parsed = msgFormatHandler.client_receive_payload_parse(data)
            if parsed is None:
                self.ui.display_error("Received invalid payload, ignoring")
                continue

            round_result, card_rank, card_suit = parsed

            # Show received card 
            if card_rank != 0:
                self.ui.show_received_card(card_rank, card_suit)

            # 4. Check if round is over
            if round_result != 0x0:
                self.handle_round_result(round_result)
                break

            # 5. Ask player decision
            decision = self.ui.ask_player_decision()

            # 6. Send decision to server
            packet = msgFormatHandler.to_payload_format_client(decision)
            self.clientNet.send(packet)

                
                
    def handle_round_result(self, round_result):
        self.ui.show_round_result(round_result)
        if round_result == 0x3:
            self.wins += 1
        elif round_result == 0x2:
            self.losses += 1
        elif round_result == 0x1:
            self.ties += 1               
    
