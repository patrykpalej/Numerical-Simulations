class Character:
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.velocity = kwargs["velocity"]
        self.power = kwargs["power"]

    def move(self, delta_x, delta_y):
        self.x = max(min(self.x + delta_x, 98), 1)
        self.y = max(min(self.y + delta_y, 98), 1)
