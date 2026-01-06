class absPlayer:
    hand = []
    current_score = 0
    name = ""
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def update_score(self, points):
        raise NotImplementedError("Subclasses must implement this method")
    def get_score(self):
        raise NotImplementedError("Subclasses must implement this method")
    def set_score(self, score):
        raise NotImplementedError("Subclasses must implement this method")
    def hit(self, card):
        raise NotImplementedError("Subclasses must implement this method")
    def stand(self):
        raise NotImplementedError("Subclasses must implement this method")
    def get_hand(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    