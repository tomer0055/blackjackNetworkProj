class play:
    clientNet=None
    def __init__(self, clientNet):
        self.clientNet = clientNet

    def start_game(self, game_id):
        return self.client.send_request("play/start_game", {"game_id": game_id})

    def end_game(self, game_id):
        return self.client.send_request("play/end_game", {"game_id": game_id})

    def get_game_status(self, game_id):
        return self.client.send_request("play/get_game_status", {"game_id": game_id})
    

    # UDP before game start
    #Condition to start game time limit 100 ms if after --> start game
    #Condition to start game time limit 1000 ms if after --> wait for next game StandBY