class Node:
    def __init__(self, spot_price):
        self.up = None
        self.down = None
        self.spot_price = spot_price
        self.option_value = 0
