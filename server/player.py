from server.absPlayer import absPlayer
from network_module.TcpClient import TcpClient


class player(absPlayer):
    wins = 0
    total_games = 0
    TcpClient = None

    def __init__(self, name, TcpClient:TcpClient):
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
    def getTcpClient(self):
        return self.TcpClient
    def make_decision(self,result, dealer_visible_card, player_visible_card):
        # Send current hand and dealer's visible card to client
        self.TcpClient.send_round_update(result, dealer_visible_card.rank, dealer_visible_card.suit)
        res = self.TcpClient.recv_decision()
        return res

    

    
    
