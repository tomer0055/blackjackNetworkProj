from network_module.msg_format import MsgFormatHandler

class Play:
    def __init__(self, clientNet, view):
        self.clientNet = clientNet
        self.view = view
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def start_game(self,roundsNum):
        self.view.show_game_start(roundsNum)
        for round_index in range(1, roundsNum + 1):
            self.view.show_round_start(round_index)
            self.play_single_round()
        self.view.end_game(self.wins, self.losses, self.ties)    
        
    def play_single_round(self):
        while True:
            # Receive payload from server
            data = self.clientNet.receive_tcp()

            # Parse payload using protocol handler
            parsed = MsgFormatHandler.client_receive_payload_parse(data)
            if parsed is None:
                self.view.show_error("Received invalid payload, ignoring")
                continue

            round_result, card_rank, card_suit = parsed

            # Show received card 
            if card_rank != 0:
                self.view.show_received_card(card_rank, card_suit)

            # 4. Check if round is over
            if round_result != 0x0:
                self.handle_round_result(round_result)
                break

            # 5. Ask player decision
            decision = self.view.ask_player_decision()

            # 6. Send decision to server
            packet = MsgFormatHandler.to_payload_format_client(decision)
            self.clientNet.send(packet)

                
                
    def handle_round_result(self, round_result):
        self.view.show_round_result(round_result)
        if round_result == 0x3:
            self.wins += 1
        elif round_result == 0x2:
            self.losses += 1
        elif round_result == 0x1:
            self.ties += 1               
    
