import pandas as pd
from random import shuffle
from numpy import roll
from poker_server import constants
from poker_server.hand import Hand

"""
serwer multiplayer
+   karty
+   deck wspólny, rozdanie kart
+   zdefiniowanie wszystkich hand rating-ów
+   znalezienie najlepszej konfiguracji kart
+   opcje fold,check/call,bet/raise
+   bank
SERWEEEEEEER

sytuacje z all-in-ami
+wypłacenie zwycięzcy
side poty
+nazwy zmiennych zmienic

"""


class Table:
    def __init__(self, num_of_players, starting_money) -> None:
        self.num_of_players = num_of_players
        self.community_cards = constants.deck[
            2 * num_of_players : 2 * num_of_players + 5
        ]
        self.prev_action = "check"
        df_helper = {
            f"player {player}": Hand((2 * player, 2 * player + 2), self.community_cards)
            for player in range(self.num_of_players)
        }
        self.players = pd.DataFrame(
            {
                "index": df_helper.keys(),
                "pocket": df_helper.values(),
                "hand": list(map(lambda x: x.hand_descending, df_helper.values())),
                "hand rating": list(map(lambda x: x.hand_rating(), df_helper.values())),
                "money": starting_money,
                "bet": 0,
                "in game": True,
                "all in": False,
            }
        )
        self.players_in_game = self.players[
            self.players["in game"] == True
        ].reset_index(drop=True)

    def __repr__(self) -> pd.DataFrame:
        return self.players.to_string(index=False)

    # def in_game(self)->pd.DataFrame:
    #    return self.players[self.players['in game'] ==True].reset_index(drop=True)
    def bet(self, player: int, amount: int) -> None:
        # print(self.players.at[player,'bet']+amount,self.players_in_game.at[((self.players_in_game[self.players_in_game['index']==f'player {player}'].index[0]-1)%len(self.players_in_game.index)),'bet'])
        if (
            self.players.at[player, "bet"] + amount
            >= self.players_in_game.at[
                (
                    (
                        self.players_in_game[
                            self.players_in_game["index"] == f"player {player}"
                        ].index[0]
                        - 1
                    )
                    % len(self.players_in_game.index)
                ),
                "bet",
            ]
        ):
            if self.players.at[player, "money"] - amount >= 0:
                self.players.at[player, "money"] -= amount
                self.players.at[player, "bet"] += amount
                self.players.at[player, "all in"] = (
                    True if self.players.at[player, "money"] - amount == 0 else False
                )
                self.players_in_game = self.players[
                    self.players["in game"] == True
                ].reset_index(drop=True)
                self.prev_action = "bet"
            else:
                print("somethings wrong")
        else:
            print("call instead")
            # self.call(player)

    def call(self, player: int) -> None:
        prev = self.players_in_game.at[
            (
                (
                    self.players_in_game[
                        self.players_in_game["index"] == f"player {player}"
                    ].index[0]
                    - 1
                )
                % len(self.players_in_game.index)
            ),
            "bet",
        ]
        your_current = self.players.at[player, "bet"]
        self.prev_action = "call"
        if self.players.at[player, "money"] - (prev - your_current) > 0:
            self.players.at[player, "money"] -= prev - your_current
            self.players.at[player, "bet"] += prev - your_current
        else:
            money = self.players.at[player, "money"]
            self.players.at[player, "bet"] += money
            self.players.at[player, "money"] = 0
            self.players.at[player, "all in"] = True
        self.players_in_game = self.players[
            self.players["in game"] == True
        ].reset_index(drop=True)

    def fold(self, player: int) -> None:
        self.players.at[player, "in game"] = False
        self.players_in_game = self.players[
            self.players["in game"] == True
        ].reset_index(drop=True)

    def check(self, player: int) -> None:
        if (
            self.players.at[player, "bet"]
            == self.players_in_game.at[
                (
                    (
                        self.players_in_game[
                            self.players_in_game["index"] == f"player {player}"
                        ].index[0]
                        - 1
                    )
                    % len(self.players_in_game.index)
                ),
                "bet",
            ]
        ):
            self.prev_action = "check"
            print("checking")
        else:
            print("call instead")
            # self.call(player)

    def determine_winner(
        self,
    ) -> list:  # ustawia wygranych w kolejności od 1 miejsca na wypadek side pot
        hand_scores = self.players_in_game["hand rating"]
        score_sort = sorted(hand_scores, key=lambda x: x[0])
        grouped_scores = [[] for _ in range(10)]
        for hand in score_sort:
            grouped_scores[hand[0] - 1].append(hand)
        # removes empty lists
        grouped_scores = [i for i in grouped_scores if i != []]
        for scores in grouped_scores:
            if len(scores) == 1:
                continue
            else:
                grouped_scores[grouped_scores.index(scores)] = sorted(
                    scores,
                    key=lambda x: [
                        -constants.ranks.index(scores[0]) for scores in x[1]
                    ],
                )
        merge_groups = [j for i in grouped_scores for j in i]
        return [
            self.players_in_game["index"][
                self.players_in_game["hand rating"] == i
            ].values[0]
            for i in merge_groups
        ]

    def deal_new_cards(self) -> None:
        shuffle(constants.deck)
        self.community_cards = constants.deck[
            2 * self.num_of_players : 2 * self.num_of_players + 5
        ]
        df_helper = [
            Hand((2 * i, 2 * i + 2), self.community_cards)
            for i in range(self.num_of_players)
        ]
        money = self.players["money"]
        indexes = self.players["index"]
        self.players = pd.DataFrame(
            {
                "index": indexes,
                "pocket": df_helper,
                "hand": list(map(lambda x: x.hand_descending, df_helper)),
                "hand rating": list(map(lambda x: x.hand_rating(), df_helper)),
                "money": money,
                "bet": 0,
                "in game": True,
                "all in": False,
            }
        ).apply(roll, shift=-1)
        self.players_in_game = self.players[
            self.players["in game"] == True
        ].reset_index(drop=True)


def can_bet(previous_action) -> bool:
    if previous_action in ["bet", "check", "call"]:
        return True
    return False


def can_check(previous_action) -> bool:
    if previous_action in ["call", "check"]:
        return True
    return False


def can_call(previous_action) -> bool:
    if previous_action in ["bet", "call", "check"]:
        return True
    return False


def game():
    shuffle(constants.deck)
    table = Table(num_of_players=constants.N, starting_money=starting_money)
    while True:
        table.bet(0, constants.small_blind)
        table.bet(1, constants.big_blind)
        for stage in [0, 3, 4, 5]:
            table.prev_action = "check"
            first_action = True
            while (
                not (
                    table.players_in_game["bet"] == table.players_in_game["bet"][0]
                ).all()
            ) or first_action:
                first_action = False
                for player in range(constants.N):
                    player = (player + 2) % table.num_of_players
                    if table.players.iat[
                        player, table.players.columns.get_loc("in game")
                    ]:
                        print(table)
                        print(
                            table.players.iat[
                                player, table.players.columns.get_loc("pocket")
                            ]
                        )
                        print(
                            table.players.iat[
                                player, table.players.columns.get_loc("pocket")
                            ]
                            + table.community_cards[:stage]
                        )

                        ask = True
                        while ask:
                            ask = False
                            print(
                                f'{table.players.at[player,"index"]} what do you want to do'
                            )
                            what = input()
                            if what == "bet" and can_bet(table.prev_action):
                                amount = int(input("how much do you want to bet?: "))
                                table.bet(player, amount)
                            elif what == "call" and can_call(table.prev_action):
                                table.call(player)
                            elif what == "check" and can_check(table.prev_action):
                                table.check(player)
                            elif what == "fold":
                                table.fold(player)
                            else:
                                ask = True
        winners = table.determine_winner()
        print(winners)
        # table.players.at[table.players[table.players['index']==winners[0]].index[0],'money'] += sum(table.players['bet'])
        print(table.players)
        pot = sum(table.players["bet"])
        for player in winners:
            if (
                table.players.at[
                    table.players[table.players["index"] == player].index[0], "all in"
                ]
                == False
            ):
                table.players.at[
                    table.players[table.players["index"] == player].index[0], "money"
                ] += pot
                break
            else:
                players_bet = table.players.at[
                    table.players[table.players["index"] == player].index[0], "bet"
                ]

        table.deal_new_cards()
        print(table.players)


if __name__ == "__main__":
    game()
