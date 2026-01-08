from server.absPlayer import absPlayer
from  network_module.TcpClient  import TcpClient


class player(absPlayer):
    wins = 0
    total_games = 0
    tie=0
    tcp = None


    def __init__(self, name, tcp:TcpClient):
        super().__init__(name)
        self.corrent_score = 0
        self.hand = []
        self.tcp = TcpClient

    def add_tie(self):
        self.total_games += 1
    
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
        return self.tcp
    def make_decision(self,result, dealer_visible_card, player_visible_card):
        # Send current hand and dealer's visible card to client
        self.tcp.send_round_update(result, dealer_visible_card.rank, dealer_visible_card.suit)
        res = self.tcp.recv_decision()
        return res
    def init_game(self, dealer_visible_card):
        self.tcp.send_round_update(0, self.get_hand[0].rank, self.get_hand[0].suit)
        self.tcp.send_round_update(0, self.get_hand[1].rank, self.get_hand[1].suit)
        self.tcp.send_round_update(0, dealer_visible_card.rank, dealer_visible_card.suit)


    

    
    
