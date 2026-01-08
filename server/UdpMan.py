import socket
import time
from network_module.msg_format import msgFormatHandler


BROADCAST_IP = "<broadcast>"
BROADCAST_PORT = 13122    #from assignment
BROADCAST_INTERVAL = 1.0  #in seconds
tcp_port = 0


class UdpMan:
    def_tcp=54321

    def __init__(self, tcp_port: int):
        self.tcp_port = tcp_port
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def add_udp_socket(self):
        self.start_broadcast()

    def start_broadcast(self):
        self.running = True
        offer_packet = msgFormatHandler.to_offer_format(self.tcp_port)

        while self.running:
            try:
                self.sock.sendto(offer_packet, (BROADCAST_IP, BROADCAST_PORT))
                time.sleep(BROADCAST_INTERVAL)
            except Exception:
                break
    def get_tcp_port(self):
        return self.tcp_port
    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except Exception:
            pass
