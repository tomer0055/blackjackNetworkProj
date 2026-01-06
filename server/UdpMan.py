class UdpMan:
    def __init__(self, server):
        self.server = server
        self.udp_sockets = {}

    def add_udp_socket(self, address, socket):
        self.udp_sockets[address] = socket

    def remove_udp_socket(self, address):
        if address in self.udp_sockets:
            del self.udp_sockets[address]

    def get_udp_socket(self, address):
        return self.udp_sockets.get(address)

    def broadcast(self, message):
        for socket in self.udp_sockets.values():
            socket.sendto(message.encode(), socket.getpeername())