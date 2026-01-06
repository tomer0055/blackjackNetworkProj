import socket
import threading
from server.UdpMan import UdpMan

TCP_PORT = 5000  # arbitrary, clients will learn it via UDP

def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", TCP_PORT))
    s.listen()
    print(f"Server listening on TCP port {TCP_PORT}")

    while True:
        conn, addr = s.accept()
        print(f"New TCP connection from {addr}")
        conn.close()

if __name__ == "__main__":
    print("Server started")

    udp = UdpMan(TCP_PORT)
    threading.Thread(target=udp.start_broadcast, daemon=True).start()

    tcp_server()