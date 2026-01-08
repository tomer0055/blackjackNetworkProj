import threading
from server.table import table
from server.player import player
import socket
from server.UdpMan import UdpMan
from  network_module.TcpClient  import TcpClient


class gameManager:
    def __init__(self):
        pass
    @staticmethod
    def start_game(conn,addr):
        tcp_cl = None

        try:
            print(f"Starting game with client at {addr}")
            tcp_cl = TcpClient(conn, addr)
            num_rounds,client_team_name = tcp_cl.recv_request()
            if num_rounds is None or client_team_name is None:
                print(f"Invalid initial request from client at {addr}. Ending game.")
                return
            
            p = player(client_team_name,tcp_cl)
            tb = table(p)
            
            while(num_rounds > 0):
                tb.game()
                num_rounds-=1
            
        except Exception as e:
            print(f"Error during game with client at {addr}: {e}")
        finally:
            print(f"Ending game with client at {addr}")
            if tcp_cl is not None:
                tcp_cl.close()
            else:
                conn.close()
        
    @staticmethod
    def game_loop(sc):
        while True:
            conn, addr = sc.accept()
            print(f"New TCP connection from {addr}")

            print(f"Starting game manager...{conn},{addr}")
            th=threading.Thread(target=gameManager.start_game, args=(conn,addr), daemon=True).start()
            
     

if __name__ == "__main__":
    print("Server started")
    #send udp broadcast
    tcp_port = UdpMan.def_tcp
    udp = UdpMan(tcp_port)
    udp.start_broadcast()

    print(f"Server listening on TCP port {tcp_port}")
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sc.bind(("", tcp_port))    
        sc.listen()
        gameManager.game_loop(sc)
    except Exception as e:
        print(f"Failed to start TCP server on port {tcp_port}: {e}")
        exit(1)
    
    
                



    #player
    #start game
    #manage game
    #end game
