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
        self.tcp = tcp

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
    def make_decision(self,result, card):
        # Send current hand and dealer's visible card to client
        print("card rank:", card.rank, "card suit:", card.suit)
        self.tcp.send_round_update(result, card.rank, card.suit)
        res = self.tcp.recv_decision()
        return res
    def init_game(self):
        print("card rank:", self.hand[0].rank, "card suit:", self.hand[0].suit)
        self.tcp.send_round_update(0, self.hand[0].rank, self.hand[0].get_suit_value())
        self.tcp.send_round_update(0, self.hand[1].rank, self.hand[1].get_suit_value())
        return



    

    
    
