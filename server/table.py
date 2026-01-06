class table :
    players = []
    dealer = None

    def __init__(self):
        self.players = []
        self.dealer = None

    def add_player(self, player):
        self.players.append(player)

    def set_dealer(self, dealer):
        self.dealer = dealer

    def start_round(self):
        # Logic to start a round
        pass

    def end_round(self):
        # Logic to end a round
        pass