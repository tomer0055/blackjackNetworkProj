class view:
    def show_client_started(self):
        print("Client started, listening for offer requests...")

    def show_received_offer(self, server_name, server_ip):
        print(f"Received offer from {server_name} ({server_ip})")

    def show_game_start(self, rounds_num):
        print(f"\nStarting a new game with {rounds_num} rounds.")

    def show_round_start(self, round_number):
        print(f"\n--- Round {round_number} ---")

    def show_received_card(self, rank, suit):
        suit_names = ["Hearts", "Diamonds", "Clubs", "Spades"]
        rank_names = {
            1: "Ace",
            11: "Jack",
            12: "Queen",
            13: "King"
        }

        rank_str = rank_names.get(rank, str(rank))
        suit_str = suit_names[suit]

        print(f"Received card: {rank_str} of {suit_str}")

    def show_round_result(self, round_result):
        if round_result == 0x3:
            print("You won this round!")
        elif round_result == 0x2:
            print("You lost this round.")
        elif round_result == 0x1:
            print("This round ended in a tie.")
    def show_round_state(self, player_cards, dealer_card):
        print("\n--- Current Table ---")

        print("Player cards:")
        for rank, suit in player_cards:
            self.show_received_card(rank, suit)

        if dealer_card:
            print("\nDealer card:")
            self.show_received_card(dealer_card[0], dealer_card[1])
            
    def show_player_card(self, rank, suit):
         print("Player:", end=" ")
         self.show_received_card(rank, suit)

    def show_dealer_card(self, rank, suit):
        print("Dealer:", end=" ")
        self.show_received_card(rank, suit)    
        
    def end_game(self, wins, losses, ties):
        total = wins + losses + ties
        if total > 0:
            win_rate = wins / total
        else:
            win_rate = 0

        print(f"\nFinished playing {total} rounds, win rate: {win_rate:.2f}")

    def ask_player_decision(self):
        while True:
            choice = input("Hit or Stand? ").strip().lower()
            if choice == "hit":
                return "Hittt"
            elif choice == "stand":
                return "Stand"
            else:
                print("Invalid input. Please type 'Hit' or 'Stand'.")

    def show_message(self, message):
        print(message)
    def display_error(self, error):
        print(f"Error: {error}")