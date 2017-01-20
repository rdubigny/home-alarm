class Counter:
    def __init__(self):
        self.count = 0
        self.max = 3

    def incr(self):
        self.count = (self.count + 1) % self.max
        return self.count == 0
