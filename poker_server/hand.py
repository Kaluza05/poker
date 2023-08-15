from poker_server import constants


def get_rank(hand: list) -> list:
    return [constants.ranks.index(card[0]) + 2 for card in hand]


def get_suit(hand: list) -> list:
    return [card[1] for card in hand]


def royal_flush(hand: list):  # 1
    for suit in constants.suits:
        candidate = [card for card in hand if card[1] == suit][:5]
        if get_rank(candidate) == get_rank(["A", "K", "Q", "J", "T"]):
            return ["A"]
    return False


def straight_flush(hand: list):  # 2
    for suit in constants.suits:
        candidate = [card for card in hand if card[1] == suit]
        ranks = get_rank(candidate)
        if len(ranks) >= 5:
            for pos, rank in enumerate(ranks):
                st = [rank - k for k in range(5)]
                if set.intersection(set(st), set(ranks)) == set(st):
                    return candidate[pos][:5]
    return False


def four_of_a_kind(hand: list):  # 3
    four = [i for i in hand if len(i) == 4]
    if four:
        for j in hand:
            if len(j) != 4:
                return [four[0][0][0], j[0][0]]
    return False


def full_house(hand: list):  # 4
    for i in hand:
        for j in hand:
            if len(i) == 2 and len(j) == 3:
                return [j[0][0][0], i[0][0][0]]
    return False


def flush(hand: list):  # 5
    for suit in constants.suits:
        if get_suit(hand).count(suit) >= 5:
            return [card[0] for card in hand if card[1] == suit][:5]
    return False


def straight(hand: list, helper: list):  # 6
    ranks = get_rank(hand)
    if len(set(ranks)) >= 5:
        for i in set(ranks):
            st = [i + k for k in range(5)]
            if set.intersection(set(st), set(ranks)) == set(st):
                return helper[ranks.index(st[4])][0][0]
    return False


def three_of_a_kind(hand: list):  # 7
    three = [i for i in hand if len(i) == 3]
    if three:
        for j in hand:
            if j != three[0]:
                return [three[0][0][0], j[0][0]]
    return False


def two_pair(hand: list):  # 8
    two = [i for i in hand if len(i) == 2][:2]
    if len(two) == 2:
        for j in hand:
            if len(j) == 1:
                return [two[0][0][0], two[1][0][0], j[0][0]]
    return False


def one_pair(hand: list):  # 9
    one = [i for i in hand if len(i) == 2]
    if one:
        for j in hand:
            if j != one[0]:
                return [one[0][0][0], j[0][0]]
    return False


def high_card(hand: list):  # 10
    return list(map(lambda x: x[0], hand))[:5]


def get_helper(hand: list):
    holder = []
    for val in get_rank(hand):
        h_many = get_rank(hand).count(val)
        help = [hand[get_rank(hand).index(val) + i] for i in range(h_many)]
        if help not in holder:
            holder.append(help)
    return holder


def best_config(hand: list):
    helper = get_helper(hand)
    if royal_flush(hand):
        return 1, royal_flush(hand)
    elif straight_flush(hand):
        return 2, straight_flush(hand)
    elif four_of_a_kind(helper):
        return 3, four_of_a_kind(helper)
    elif full_house(helper):
        return 4, full_house(helper)
    elif flush(hand):
        return 5, flush(hand)
    elif straight(hand, helper):
        return 6, straight(hand, helper)
    elif three_of_a_kind(helper):
        return 7, three_of_a_kind(helper)
    elif two_pair(helper):
        return 8, two_pair(helper)
    elif one_pair(helper):
        return 9, one_pair(helper)
    else:
        return 10, high_card(hand)


class Hand:
    def __init__(self, deck_range, community_cards) -> None:
        self.hand = [constants.deck[i] for i in range(*deck_range)]
        self.whole_hand = self.hand + community_cards
        self.hand_descending = sorted(
            self.whole_hand, key=lambda x: -constants.ranks.index(x[0])
        )

    def __str__(self) -> str:
        return repr(self.hand)

    def __repr__(self) -> str:
        return repr(self.hand)

    def __add__(self, other) -> list:
        return self.hand + other

    def hand_rating(self):
        return best_config(self.hand_descending)
