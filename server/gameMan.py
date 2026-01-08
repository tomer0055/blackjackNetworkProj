from server.table import table
from server import player
import socket
from server.UdpMan import UdpMan
from  network_module.TcpClient  import TcpClient


class gameManager:
    def __init__(self):
        pass
    @staticmethod
    def start_game(conn,addr):
        tcp_cl = TcpClient(conn, addr)
        num_rounds,client_team_name = tcp_cl.recv_request()
        p = player.player(client_team_name,tcp_cl)
        tb = table(p)
        
        while(num_rounds>0):
            tb.game()
            num_rounds-=1
        

    

if __name__ == "__main__":
    print("Server started")
    #send udp broadcast
    tcp_port = UdpMan.def_tcp
    udp = UdpMan(tcp_port)
    udp.start_broadcast()

    print(f"Server listening on TCP port {tcp_port}")
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.bind(("", tcp_port))    
        sc.listen()
    except Exception as e:
        print(f"Failed to start TCP server on port {tcp_port}: {e}")
        exit(1)

    while True:
        conn, addr = sc.accept()
        print(f"New TCP connection from {addr}")
        print(f"Starting game manager...{conn},{addr}")
        gameManager.start_game(conn,addr)
                



    #player
    #start game
    #manage game
    #end game
