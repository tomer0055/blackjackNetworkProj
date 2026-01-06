from clientNetwork import clientNetwork
from msgFormatHandler import msgFormatHandler
from play import Play
from view import view


def main():
    view = view()
    view.show_client_started()
    # Create the network layer (handles UDP and TCP sockets)
    net = clientNetwork()

    while True:
        try:
            num_rounds = int(input("Enter number of rounds to play: "))
            if num_rounds <= 0:
                continue
        except ValueError:
            continue

        # Listen for UDP OFFER message
        data, server_ip = net.receive_udp()

        # Parse the OFFER message using the protocol handler
        offer = msgFormatHandler.client_receive_offer(data)
        if offer is None:
            view.show_error("Invalid offer received")
            continue
        
        tcp_port, server_name = offer
        view.show_received_offer(server_name, server_ip)
        # Establish TCP connection to the server
        try:
            net.connect((server_ip, tcp_port))
        except Exception as e:
            view.show_error(f"Failed to connect to server: {e}")
            continue
        # Send initial REQUEST message
        request_packet = msgFormatHandler.to_request_format(
            num_rounds,
            "TEAM_CLIENT"
        )
        net.send(request_packet)
        play = Play(net)
        play.run(num_rounds)
        net.disconnect()
        view.show_message("Waiting for new offers...\n")


if __name__ == "__main__":
    main()