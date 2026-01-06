class view:
    def display_Win(self, message):
        print(f"Message: {message}")
    def display_Hand(self, player_name, hand):
        hand_representation = ', '.join([f"{card.get_rank()} of {card.get_suit().name}" for card in hand])
        print(f"{player_name}'s hand: {hand_representation}")
    def display_Score(self, player_name, score):
        print(f"{player_name}'s score: {score}")
    def display_Message(self, message):
        print(f"Message: {message}")

    def display_error(self, error):
        print(f"Error: {error}")