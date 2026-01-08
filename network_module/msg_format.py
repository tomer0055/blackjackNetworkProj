__all__ = ["MsgFormatHandler"]
class msgFormatHandler:
       
    __server_name= " EMT_BlackJackServer "
    __offer_msg_type = 0x2
    __request_msg_type = 0x3
    __payload_client_msg_type = 0x4
    __payload_server_msg_type = 0x5
    __magic_cookie = 0xabcddcba
    __magic_cookie_size = 4  #4 bytes
    __msg_type_size = 1  #1 byte
    @staticmethod
    def to_offer_format(tcp_port:int):
            magic_cookie = msgFormatHandler.__magic_cookie.to_bytes(msgFormatHandler.__magic_cookie_size, 'big')
            message_type = msgFormatHandler.__offer_msg_type.to_bytes(msgFormatHandler.__msg_type_size, 'big')
            port_bytes = tcp_port.to_bytes(2, 'big')
            server_name_bytes = msgFormatHandler.__server_name.encode('utf-8')[:32]
            server_name_bytes = server_name_bytes.ljust(32, b'\x00')  
            return magic_cookie + message_type + port_bytes + server_name_bytes
    @staticmethod    
    def to_request_format( num_rounds:int, client_team_name:str):
            magic_cookie = msgFormatHandler.__magic_cookie.to_bytes(msgFormatHandler.__magic_cookie_size, 'big')
            message_type = msgFormatHandler.__request_msg_type.to_bytes(msgFormatHandler.__msg_type_size, 'big')
            num_rounds_byte = num_rounds.to_bytes(1, 'big')
            client_team_name_bytes = client_team_name.encode('utf-8')[:32]
            client_team_name_bytes = client_team_name_bytes.ljust(32, b'\x00')
            return magic_cookie + message_type + num_rounds_byte + client_team_name_bytes
    
    @staticmethod    
    def to_payload_format_client(player_decision:str):
        magic_cookie = msgFormatHandler.__magic_cookie.to_bytes(msgFormatHandler.__magic_cookie_size, 'big')
        message_type = msgFormatHandler.__payload_client_msg_type.to_bytes(msgFormatHandler.__msg_type_size, 'big')
        decision_bytes = player_decision.encode('utf-8')[:5]
        decision_bytes = decision_bytes.ljust(5, b'\x00')
        return magic_cookie + message_type + decision_bytes
    
    # magic_cookie (4 bytes) + message_type (1 byte) + round_result (1 byte) + card_rank (2 bytes) + card_suit (1 byte)
    @staticmethod
    def to_payload_format_server(round_result:int, card_rank:int, card_suit:int):

        magic_cookie = msgFormatHandler.__magic_cookie.to_bytes(msgFormatHandler.__magic_cookie_size, 'big')
        message_type = msgFormatHandler.__payload_server_msg_type.to_bytes(msgFormatHandler.__msg_type_size, 'big')  
        round_result_byte = round_result.to_bytes(1, 'big')
        card_rank_bytes = card_rank.to_bytes(2, 'big')
        card_suit_byte = card_suit.to_bytes(1, 'big')
        return magic_cookie + message_type + round_result_byte + card_rank_bytes + card_suit_byte

    # magic_cookie (4 bytes) + message_type (1 byte) + round_result (1 byte) + card_rank (2 bytes) + card_suit (1 byte)
    @staticmethod
    def client_receive_payload_parse(data):
        if len(data) < 7:
            return None  
        magic_cookie = int.from_bytes(data[0:4], 'big')
        message_type = data[4]
        round_result = data[5]
        card_rank = int.from_bytes(data[6:8], 'big')
        card_suit = data[8]
        if magic_cookie != msgFormatHandler.__magic_cookie or message_type != msgFormatHandler.__payload_server_msg_type:
            return None  
        return (round_result, card_rank, card_suit)
    # magic_cookie (4 bytes) + message_type (1 byte) + decision (5 bytes)
    @staticmethod
    def client_receive_offer(data):
        if len(data) < 39:
            return None  
        magic_cookie = int.from_bytes(data[0:4], 'big')
        message_type = data[4]
        tcp_port = int.from_bytes(data[5:7], 'big')
        server_name_bytes = data[7:39]
        server_name = server_name_bytes.decode('utf-8').rstrip('\x00')
        if magic_cookie != msgFormatHandler.__magic_cookie or message_type != msgFormatHandler.__offer_msg_type:
            return None  
        return (tcp_port, server_name)

    @staticmethod
    def server_receive_payload_parse(data):
        if len(data) < 6:
            return None  
        magic_cookie = int.from_bytes(data[0:4], 'big')
        message_type = data[4]
        decision_bytes = data[5:10]
        player_decision = decision_bytes.decode('utf-8').rstrip('\x00')
        if magic_cookie != msgFormatHandler.__magic_cookie or message_type != msgFormatHandler.__payload_client_msg_type:
            return None  
        return player_decision
    # magic_cookie (4 bytes) + message_type (1 byte) + num_rounds (1 byte) + team_name (32 bytes)
    @staticmethod
    def server_receive_init_request( data):
        if len(data) < 38:
            return None  
        magic_cookie = int.from_bytes(data[0:4], 'big')
        message_type = data[4]
        num_rounds = data[5]
        team_name_bytes = data[6:38]
        client_team_name = team_name_bytes.decode('utf-8').rstrip('\x00')
        if magic_cookie != msgFormatHandler.__magic_cookie or message_type != msgFormatHandler.__request_msg_type:
            return None  
        return (num_rounds, client_team_name)
