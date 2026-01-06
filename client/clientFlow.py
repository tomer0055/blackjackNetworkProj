from client.clientNetwork import clientNetwork
from network_module.msg_format import msgFormatHandler
from client.play import Play
from client.view import view


def main():
    ui = view()
    ui.show_client_started()
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
            ui.show_error("Invalid offer received")
            continue
        
        tcp_port, server_name = offer
        ui.show_received_offer(server_name, server_ip)
        # Establish TCP connection to the server
        try:
            net.connect((server_ip, tcp_port))
        except Exception as e:
            ui.show_error(f"Failed to connect to server: {e}")
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
        ui.show_message("Waiting for new offers...\n")


if __name__ == "__main__":
    main()