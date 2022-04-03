from dataclasses import dataclass
from itertools import cycle

import numpy as np

from Bank import Bank
from cards import CHANCE, CHEST
from sentences import MENUS, SENTENCES
from tiles import SETS, TILES, get_state, states

# Use this to similate pattern of actions you want to get
# e.g. rollDice, buy, endTurn = [0, 1, 5]
# you can also set the next dices numbers
# dices = [[3, 2], [4, 5]]
debug = []


@dataclass
class Player:
    id: int
    name: str
    bank: Bank
    __money: int = 1500
    __location: int = 0
    count_turn: int = 0
    count_double: int = 0
    total_dices: int = 0
    free_jail_card_counter: int = 0
    last_debt: int = -1
    double: bool = False
    try_double: bool = False
    pay_fine: bool = False
    in_jail: bool = False
    forced_to_jail: bool = False
    is_moving_out_of_jail: bool = False
    forced_to_nearest: bool = False
    loop_while: bool = False
    turn: bool = True
    current: bool = False
    auctioning: bool = False
    bankruptcy: bool = False

    def __call__(self, players):
        self.current = True
        self.players: list["Player"] = players

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, x):
        self.__money = x

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, x):
        self.__location = x

    def get_index_by_id(self):
        return next(
            (i for i, player in enumerate(self.players) if player.id == self.id), -1,
        )

    def choose_action(self, possibility, action=False):
        if debug:
            return debug.pop(0)

        while True:
            try:
                print('player : ', self.id)
                print('location : ', self.location)
                print('ses choix : ', possibility)
                x = input("choose : ")
                if x == "q":
                    quit()
                if x == "c":
                    return None
                if x == "e" and action:
                    return x
                res = int(x)
                if res not in possibility:
                    continue
                return res
            except ValueError:
                pass

    def roll_dice(self):
        dices = np.random.randint(1, 7, size=2)
        self.total_dices = np.sum(dices)

        if dices[0] == dices[1]:
            self.count_double += 1
            self.double = True

            if self.count_double == 3:
                self.move_to_jail()

        else:
            self.double = False
            self.turn = False

    def pay_to(self, player: "Player", amount: int):
        self.last_debt = player.id
        self.money -= amount
        player.money += amount

    def transaction(self, amount: int):
        self.last_debt = -1
        self.money += amount

    def move_by_dice(self, nbr: int):
        temp = self.location + nbr
        if temp >= TILES.shape[0]:
            self.transaction(200)
            temp %= TILES.shape[0]
        self.location = temp

    def move_by_card(self, where, backward=False, move_backward=False):
        self.loop_while = True

        if self.location > where and not backward and not move_backward:
            self.transaction(200)

        self.location = where if not move_backward else self.location + where

    def move_to_nearest(self, property_type):
        last = TILES[TILES["type"] == property_type].iloc[-1]
        tiles = list(SETS[last["idFamily"]])
        tiles.append(self.location)
        tiles.sort()
        try:
            where = tiles[tiles.index(self.location) + 1]
        except IndexError:
            where = tiles[0]

        if self.location > last["id"]:
            self.transaction(200)

        self.loop_while = True
        self.forced_to_nearest = True
        self.location = where

    def move_to_jail(self):
        self.forced_to_jail = True
        self.in_jail = True
        self.turn = False
        self.location = 10

    def out_of_jail(self):
        self.in_jail = False
        self.location = 10

    def move_out_of_jail(self):
        self.is_moving_out_of_jail = True
        self.out_of_jail()

    def get_price(self, case, case_state, double):
        price = 0
        if case["type"] == "property":
            price = (
                case["house_0"] * 2
                if case_state["isFamily"] and not case_state["built"]
                else case[f"house_{case_state['built']}"]
            )
        elif case["type"] == "railroad":
            price = case["rent"] * np.count_nonzero(states[case["idFamily"], :, 0])
            if double:
                price *= 2
        else:
            price = (
                4 * self.total_dices
                if not case_state["isFamily"]
                else 10 * self.total_dices
            )
            if double:
                price *= 2

        return price

    def land_on_property(self):
        case = TILES.loc[self.location]

        if (
            case["type"] == "property"
            or case["type"] == "railroad"
            or case["type"] == "utility"
        ):
            case_state = get_state(case)
            if case_state["owned"] >= 0:
                if case_state["owned"] != self.id and not case_state["mortgaged"]:
                    owner: Player = self.players[case_state["owned"]]
                    amount = owner.get_price(case, case_state, self.forced_to_nearest)
                    self.pay_to(owner, amount)
            else:
                if not self.forced_to_nearest:
                    while (action := self.choose_action(list(dict(enumerate(MENUS["buy"])).keys()))) is None:
                        pass
                else:
                    action = 0
                    self.forced_to_nearest = False
                # Buy
                if action == 0:
                    self.buy(case)
                if action == 1:
                    self.put_for_auction(case)

        if case["type"] == "tax":
            self.transaction(-case["price"])

        if case["type"] == "gotojail":
            self.move_to_jail()

        if case["type"] == "chance" or case["type"] == "chest":
            active = CHANCE if case["type"] == "chance" else CHEST
            text = active[0](self)
            print(text)
            active.append(active.pop(0))

        if (
            case["type"] == "start"
            or case["type"] == "visiting"
            or case["type"] == "parking"
        ):
            pass

    def put_for_auction(self, case):
        bidamount = 1

        players_in = [player for player in self.players if not player.bankruptcy]
        for player in players_in:
            player.auctioning = True
        nb_bidder = len(players_in)

        bidder_cycled = cycle(players_in)

        while True:
            while bidder := next(bidder_cycled):
                if bidder.auctioning:
                    break

            if nb_bidder == 1:
                bidder.win_auction(case, bidamount)
                break

            while (action := bidder.choose_action(list(dict(enumerate(MENUS["auction"])).keys()))) is None:
                pass

            if action == 0:
                bidamount = 100
            if action == 1:
                bidder.auctioning = False
                nb_bidder -= 1

    def win_auction(self, case, bidAmount):
        self.auctioning = False
        self.buy_by_auction(case, bidAmount)

    def end_turn(self):
        self.count_double = 0
        self.turn = True
        self.forced_to_jail = False
        self.try_double = False
        self.current = False

    def buy(self, case):
        states[case["idFamily"], case["idInFamily"], 0] = self.id
        self.transaction(-case["price"])

    def buy_by_auction(self, case, bidamount):
        states[case["idFamily"], case["idInFamily"], 0] = self.id
        self.transaction(-bidamount)

    def action_on_property(self, action: str):
        ids = getattr(self, f"get_{action}_property")()
        print(ids)
        tile_id = int(input("tile_id: "))
        if tile_id == "c":
            return False

        getattr(self, action)(TILES.loc[tile_id])

    def mortgage(self, case):
        states[case["idFamily"], case["idInFamily"], 1] = 1
        self.transaction(case["mortgagePrice"])

    def unmortgage(self, case):
        states[case["idFamily"], case["idInFamily"], 1] = 0
        self.transaction(-(case["mortgagePrice"] + case["mortgagePrice"] // 10))

    def build(self, case):
        states[case["idFamily"], case["idInFamily"], 2] += 1
        if states[case["idFamily"], case["idInFamily"], 2] < 5:
            self.bank.remaining_houses -= 1
        else:
            self.bank.remaining_houses += 4
            self.bank.remaining_hotels -= 1

        self.transaction(-case["housePrice"])

    def sell(self, case):
        if states[case["idFamily"], case["idInFamily"], 2] == 5:
            self.bank.remaining_hotels += 1
            self.bank.remaining_houses -= 4
        else:
            self.bank.remaining_houses += 1

        states[case["idFamily"], case["idInFamily"], 2] -= 1

        self.transaction(case["housePrice"] // 2)

    def get_own_property(self):
        res = []
        for i, family in enumerate(SETS):
            indexes = np.where(states[i, : len(family), 0] == self.id)[0]
            for j in indexes:
                res.append(family[j])

        return res

    def get_mortgage_property(self):
        res = []
        for i, family in enumerate(SETS):
            indexes = np.where(
                (states[i, : len(family), 0] == self.id)
                & (states[i, : len(family), 1] == 0)
                & np.all(states[i, : len(family), 2] == 0)
            )[0]
            for j in indexes:
                res.append(SETS[i][j])

        return res

    def get_unmortgage_property(self):
        indexes = np.where((states[:, :, 0] == self.id) & (states[:, :, 1] == 1))
        return [SETS[i][j] for i, j in zip(*indexes)]

    def get_build_property(self):
        res = []
        for i, family in enumerate(SETS):
            if i <= 7:
                indexes = np.where(
                    np.all(states[i, : len(family), 0] == self.id)
                    & np.all(states[i, : len(family), 1] == 0)
                    & (
                        np.amin(states[i, : len(family), 2])
                        >= states[i, : len(family), 2]
                    )
                    & (states[i, : len(family), 2] != 5)
                    & (
                        self.bank.remaining_houses > 0
                        if np.any(states[i, : len(family), 2] < 4)
                        else self.bank.remaining_hotels > 0
                    )
                )[0]
                for j in indexes:
                    res.append(SETS[i][j])
        return res

    def get_sell_property(self):
        res = []
        for i, family in enumerate(SETS):
            if i <= 7:
                indexes = np.where(
                    (states[i, : len(family), 2] > 0)
                    & (
                        np.amax(states[i, : len(family), 2])
                        <= states[i, : len(family), 2]
                    )
                    & (
                        self.bank.remaining_houses >= 4
                        if np.any(states[i, : len(family), 2] == 5)
                        else True
                    )
                )[0]
                for j in indexes:
                    res.append(SETS[i][j])
        return res

    def give_properties(self, player_id, tiles: list[int]):
        for tile_id in tiles:
            tile = TILES.loc[tile_id]
            states[tile["idFamily"], tile["idInFamily"], 0] = player_id

    def get_free_jail_card(self):
        self.free_jail_card_counter += 1

    def use_free_jail_card(self):
        self.free_jail_card_counter -= 1

    def check_actions(self):
        actions = []

        # Roll dice
        if self.turn and not self.in_jail:
            actions.append(0)
        # Mortgage
        if bool(self.get_mortgage_property()) and not self.forced_to_jail:
            actions.append(1)
        # Unmortgage
        if bool(self.get_unmortgage_property()) and not self.forced_to_jail:
            actions.append(2)
        # Build
        if bool(self.get_build_property()) and not self.forced_to_jail:
            actions.append(3)
        # Sell
        if bool(self.get_sell_property()) and not self.forced_to_jail:
            actions.append(4)
        # End turn
        if (
            (
                self.money > 0
                and not self.turn
                and not (self.in_jail and not self.try_double)
            )
            or self.forced_to_jail
            or (0 < self.count_turn < 3 and self.pay_fine)
        ):
            actions.append(5)
        # Try Double
        if self.in_jail and not self.forced_to_jail and not self.try_double:
            actions.append(6)
        # Pay Fine
        if self.in_jail and not self.forced_to_jail and not self.try_double:
            actions.append(7)
        # Use Free Jail Card
        if self.in_jail and self.free_jail_card_counter and not self.forced_to_jail:
            actions.append(8)
        # Get out of the game
        if self.bankruptcy:
            actions = [9]
            
        return self.choose_action(actions, action=True)

    def trade(self):
        ids = [p.id for p in self.players if not p.bankruptcy and not self.id == p.id]
        print(ids)
        player_id = input("player_id: ")
        if player_id == "c":
            return False

        trader: Player = self.players[player_id]
        trade_dict = {
            "get": {"money": 0, "properties": []},
            "give": {"money": 0, "properties": []},
        }

        while True:

            action = self.choose_action(list(dict(enumerate(MENUS["trade"])).keys()))

            if action is None:
                break

            if action == 5:
                response = trader.choose_action(list(dict(enumerate(MENUS["response_trade"])).keys()))
                if response == 1:
                    self.accept_trade(trader, trade_dict)
                if response == 2:
                    self.refuse_trade(trader)
                break

            concerned = (self, "give") if action in [1, 2] else (trader, "get")

            if action == 1 or action == 3:

                ids = concerned[0].get_own_property()
                print(ids)
                tile_id = input("tile_id: ")

                if tile_id == "c":
                    continue
                if tile_id in trade_dict[concerned[1]]["properties"]:
                    trade_dict[concerned[1]]["properties"].remove(tile_id)
                else:
                    trade_dict[concerned[1]]["properties"].append(tile_id)

            if action == 2 or action == 4:

                amount = input("amount: ")
                if amount == "c":
                    continue
                trade_dict[concerned[1]]["money"] = amount

    def accept_trade(self, trader: "Player", trade_dict: dict):
        trader.money += trade_dict["give"]["money"]
        self.money += trade_dict["get"]["money"]
        trader.money -= trade_dict["get"]["money"]
        self.money -= trade_dict["give"]["money"]

        trader.give_properties(self.id, trade_dict["get"]["properties"])
        self.give_properties(trader.id, trade_dict["give"]["properties"])

    def refuse_trade(self, trader):
        pass

    def get_heritage(self):
        heritage = 0
        for i, family in enumerate(SETS):
            tile_id = np.where(
                (states[i, : len(family), 0] == self.id)  # Own
                & (states[i, : len(family), 1] == 0)  # Mortgageable
            )[0]
            for y in tile_id:
                case = TILES[family[y]]
                heritage += (
                    case["mortgagePrice"] + case["housePrice"] // 2 * case["built"]
                )

        return heritage

    def game_over(self):
        self.bankruptcy = True

    def win(self):
        return SENTENCES["congratulations"](self.players[0].name)

    def birthday(self):
        for player in self.players:
            if self.get_index_by_id() != player.id:
                player.payTo(self, 10)

    def elected(self):
        for player in self.players:
            if self.get_index_by_id() != player.id:
                self.pay_to(player, 50)

    def cost_from_repairs(self):
        return (
            states[states[:, :, 2] < 5][:, 2].sum() * 25
            + np.count_nonzero(states[:, :, 2] == 5) * 100
        )

    def cost_from_more_repairs(self):
        return (
            states[states[:, :, 2] < 5][:, 2].sum() * 40
            + np.count_nonzero(states[:, :, 2] == 5) * 115
        )
