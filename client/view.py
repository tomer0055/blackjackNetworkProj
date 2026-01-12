class view:
    def __init__(self):
        self.hide_dealer_second_card = True
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
    def show_round_state(self, player_cards, dealer_cards):
        print("\n--- Current Table ---")

        if player_cards:
            print("\nYour hand:")
            self._print_cards_row(player_cards)

        if self.hide_dealer_second_card:
            visible = [dealer_cards[0], ("HIDDEN", None)]
            print("\nDealer hand:")
            self._print_cards_row(visible)
        else:    
            print("\nDealer hand:")
            self._print_cards_row(dealer_cards)
            
    def show_player_card(self, rank, suit):
        print("\nYou received:")
        self._print_cards_row([(rank, suit)])

    def show_dealer_cards(self, rank, suit):
        print("\nDealer received:")
        self._print_cards_row([(rank, suit)])   
        
    def end_game(self, wins, losses, ties):
        total = wins + losses + ties
        win_rate = (wins / total * 100) if total > 0 else 0

        print("\n===== Game Statistics =====")
        print(f"Total rounds: {total}")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Ties: {ties}")
        print(f"Win rate: {win_rate:.2f}%")
        print("===========================")
        print(f"\nFinished playing {total} rounds, win rate: {win_rate:.2f}")
    
    def _render_card(self, rank, suit):
        if rank == "HIDDEN":
            return [
            "┌───────┐",
            "│ HIDDEN│",
            "│       │",
            "│HIDDEN │",
            "└───────┘"
            ]
        suit_symbols = {
            0: "♥",  # Hearts
            1: "♦",  # Diamonds
            2: "♣",  # Clubs
            3: "♠"   # Spades
        }

        rank_names = {
            1: "A",
            11: "J",
            12: "Q",
            13: "K"
        }

        r = rank_names.get(rank, str(rank))
        s = suit_symbols.get(suit, "?")

        return [
            "┌───────┐",
            f"│ {r:<2}    │",
            f"│   {s}   │",
            f"│    {r:>2} │",
            "└───────┘"
        ]

    def _print_cards_row(self, cards):
        rendered = [self._render_card(rank, suit) for rank, suit in cards]
        for i in range(5):
            print(" ".join(card[i] for card in rendered))
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