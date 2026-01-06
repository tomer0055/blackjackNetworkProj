import socket
class clientNetwork:
    UDP_PORT=13122
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind(('', self.UDP_PORT))
        self.tcp_socket = None
    
    def receive_udp(self):# udp recv
        data, addr = self.udp_socket.recvfrom(1024)
        return data, addr[0]
    def connect(self, address):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #set timeout in case server is not responding
        self.tcp_socket.settimeout(10)
        self.tcp_socket.connect(address)

    def send(self, data):
        if not self.tcp_socket:
            raise RuntimeError("Not connected to server")
        self.tcp_socket.sendall(data)


    def receive_tcp(self):
        if not self.tcp_socket:
            raise RuntimeError("Not connected to server")
        return self.tcp_socket.recv(1024)
    
    def disconnect(self):
        if self.tcp_socket:
            self.tcp_socket.close()
            self.tcp_socket = None