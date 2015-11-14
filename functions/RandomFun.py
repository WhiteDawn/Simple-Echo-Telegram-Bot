import random

class Straws:
    def __init__(self, header, middle, footer):
        self.header = header
        self.middle = middle
        self.footer = footer
        random.seed()

    def get(self):
        segments = random.randint(1, 10)

        straw = self.header
        for i in range(segments):
            straw = straw + self.middle

        return straw + self.footer