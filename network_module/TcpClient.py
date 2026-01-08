import socket
import network_module.msg_format as msg_format


REQUEST_LEN = 38          # 4 + 1 + 1 + 32
CLIENT_PAYLOAD_LEN = 10   # 4 + 1 + 5
SERVER_PAYLOAD_LEN = 9    # 4 + 1 + 1 + 2 + 1

class TcpClient:
    def __init__(self, conn: socket.socket, addr=None):
        self.socket = conn
        self.addr = addr

    def close(self):
        if self.socket:
            try:
                self.socket.close()
            finally:
                self.socket = None

    def is_active(self) -> bool:
        return self.socket is not None

    # Read exactly n bytes from the socket
    def _recv_exact(self, n: int) -> bytes | None:
        if not self.is_active():
            raise RuntimeError("TCP connection is not active")

        chunks = []
        got = 0
        while got < n:
            part = self.socket.recv(n - got)
            if not part:  
                return None
            chunks.append(part)
            got += len(part)
        return b"".join(chunks)

    

    def recv_request(self):
        """
        Reads and parses the Request message from the client.
        Returns: (num_rounds, team_name) or None if disconnected/invalid.
        """
        data = self._recv_exact(REQUEST_LEN)
        if data is None:
            return None
        return msg_format.msgFormatHandler.server_receive_init_request(data)

    def recv_decision(self) -> str | None:
        """
        Reads and parses the client payload decision ("Hittt"/"Stand").
        """
        data = self._recv_exact(CLIENT_PAYLOAD_LEN)
        if data is None:
            return None
        str1 = msg_format.msgFormatHandler.server_receive_payload_parse(data)
        if str1 is "Hittt":
            return 1
        elif str1 is "Stand":
            return 0
        else :
            raise RuntimeError("Invalid decision received from client")

    def send_round_update(self, round_result: int, card_rank: int, card_suit: int):
        """
        Sends server payload (round result + card) to the client.
        """
        if not self.is_active():
            raise RuntimeError("TCP connection is not active")

        payload = msg_format.msgFormatHandler.to_payload_format_server(
            round_result, card_rank, card_suit
        )
        self.socket.sendall(payload)