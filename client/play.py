from network_module.msg_format import msgFormatHandler

class Play:
    def __init__(self, clientNet, view):
        self.clientNet = clientNet
        self.view = view
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def start_game(self,roundsNum):
        self.view.show_game_start(roundsNum)
        for _ in range(roundsNum):
            self.view.show_round_start(roundsNum)
            self.play_single_round()
        self.view.end_game(self.wins, self.losses, self.ties)    
        
    def play_single_round(self):
        while True:
            # 1. Receive payload from server (blocking)
            data = self.clientNet.receive_tcp()

            # 2. Parse payload using protocol handler
            parsed = msgFormatHandler.client_receive_payload_parse(data)
            if parsed is None:
                self.view.show_error("Received invalid payload, ignoring")
                continue

            round_result, card_rank, card_suit = parsed

            # 3. Show received card (if exists)
            if card_rank != 0:
                self.view.show_received_card(card_rank, card_suit)

            # 4. Check if round is over
            if round_result != 0x0:
                self.handle_round_result(round_result)
                break

            # 5. Ask player decision
            decision = self.view.ask_player_decision()

            # 6. Send decision to server
            packet = msgFormatHandler.to_payload_format_client(decision)
            self.clientNet.send(packet)

                
                
    def handle_round_result(self, round_result):
        self.view.show_round_result(round_result)
        if round_result == 0x3:
            self.wins += 1
        elif round_result == 0x2:
            self.losses += 1
        elif round_result == 0x1:
            self.ties += 1               
    
