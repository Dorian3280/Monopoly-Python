from Displayer import Displayer


displayer = Displayer()


class Bank:
    def __init__(self) -> None:
        self.id = -1
        self.remainingHouses = 32
        self.remainingHotels = 12

    def __call__(self):
        displayer.bank(self)
