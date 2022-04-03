import random
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Card:

    func: Callable
    text: str = field(default_factory=lambda x: x.strip().split(";"))

    def __call__(self, player):
        self.func(player)
        return self.text


class Chance(Card):
    pass


class Chest(Card):
    pass


texts = open("cards.txt", "r").readlines()

CHEST = [
    Chest(lambda x: x.move_by_card(0), texts[0]),
    Chest(lambda x: x.transaction(200), texts[1]),
    Chest(lambda x: x.transaction(-50), texts[2]),
    Chest(lambda x: x.transaction(-50), texts[3]),
    Chest(lambda x: x.get_free_jail_card(), texts[4]),
    Chest(lambda x: x.move_to_jail(), texts[5]),
    Chest(lambda x: x.transaction(100), texts[6]),
    Chest(lambda x: x.transaction(20), texts[7]),
    Chest(lambda x: x.birthday(), texts[8]),
    Chest(lambda x: x.transaction(100), texts[9]),
    Chest(lambda x: x.transaction(-100), texts[10]),
    Chest(lambda x: x.transaction(-50), texts[11]),
    Chest(lambda x: x.transaction(25), texts[12]),
    Chest(lambda x: x.transaction(-x.cost_from_repairs_plus()), texts[13]),
    Chest(lambda x: x.transaction(10), texts[14]),
    Chest(lambda x: x.transaction(100), texts[15]),
]

CHANCE = [
    Chance(lambda x: x.move_by_card(0), texts[16]),
    Chance(lambda x: x.move_by_card(24), texts[17]),
    Chance(lambda x: x.move_by_card(39), texts[18]),
    Chance(lambda x: x.move_by_card(11), texts[19]),
    Chance(lambda x: x.move_to_nearest("railroad"), texts[20]),
    Chance(lambda x: x.move_to_nearest("railroad"), texts[21]),
    Chance(lambda x: x.move_to_nearest("utility"), texts[22]),
    Chance(lambda x: x.transaction(50), texts[23]),
    Chance(lambda x: x.get_free_jail_card(), texts[24]),
    Chance(lambda x: x.move_by_card(-3, moveBackward=True), texts[25]),
    Chance(lambda x: x.move_to_jail(), texts[26]),
    Chance(lambda x: x.transaction(-x.cost_from_repairs()), texts[27]),
    Chance(lambda x: x.transaction(-15), texts[28]),
    Chance(lambda x: x.move_by_card(5), texts[29]),
    Chance(lambda x: x.elected(), texts[30]),
    Chance(lambda x: x.transaction(150), texts[31]),
]

random.shuffle(CHEST)
random.shuffle(CHANCE)
