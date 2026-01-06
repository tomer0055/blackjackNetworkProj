import table,player
import socket
import UdpMan
from  network_module.TcpClient  import TcpClient
class gameManager:
    tcp_port = UdpMan.tcp_port

    if __name__ == "__main__":
        #send udp broadcast
        udp = UdpMan.UdpMan(tcp_port)
        udp.start_broadcast()

        #liss
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.bind(("",tcp_port))
        sc.listen()

        #create tcp client
        conn, addr = sc.accept()
        print(f"New TCP connection from {addr}")
        tcp_cl= TcpClient(conn, addr)
        p = player.player(tcp_cl,addr)
        tcp_cl.recv_request()
        tb = table.table(p)
        tb.start_round()


        #player
        #start game
        #manage game
        #end game
        print(gm.get_game("game1"))
        gm.delete_game("game1")
        print(gm.get_game("game1"))