from server import absPlayer


class player(absPlayer):
    wins = 0
    total_games = 0
    TcpClient = None

    def __init__(self, name, TcpClient):
        super().__init__(name)
        self.corrent_score = 0
        self.hand = []
        self.TcpClient = TcpClient

    def add_win(self):
        self.wins += 1
        self.total_games += 1

    def add_loss(self):
        self.total_games += 1
    def get_win_rate(self):
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games
    

    
    
