from CONSTANTS import RANKS,SUITS,DECK

def get_rank(hand:list)->list: 
    return [RANKS.index(card[0])+2 for card in hand]
def get_suit(hand:list)->list: 
    return [card[1] for card in hand]

def royal_flush(hand:list):#1
    for suit in SUITS:
        candidate = [card for card in hand if card[1]==suit][:5]
        if get_rank(candidate)==get_rank(['A','K','Q','J','T']):
           return ['A']
    return False


def straight_flush(hand:list):#2
    for suit in SUITS:
        candidate = [card for card in hand if card[1]==suit]
        ranks = get_rank(candidate)
        if len(ranks)>=5:
            for pos, rank in enumerate(ranks):
                st = [rank-k for k in range(5)]
                if set.intersection(set(st),set(ranks))==set(st):
                    return candidate[pos][:5]
    return False


def four_of_a_kind(hand:list):#3
    four = [i for i in cups_form(hand) if len(i)==4]
    if four:
        hand_without_four = [i[0] for i in hand if i not in four[0]]
        return [four[0][0][0] , hand_without_four[0]]
    return False


def full_house(hand:list):#4
    helper = cups_form(hand)
    for i in helper:
        for j in helper:
            if len(i)==2 and len(j)==3: return [j[0][0][0],i[0][0][0]]
    return False


def flush(hand:list):#5
    for suit in SUITS:
        if get_suit(hand).count(suit)>=5: return [card[0] for card in hand if card[1]==suit][:5]
    return False


def straight(hand:list):#6
    ranks =get_rank(hand)
    if len(set(ranks))>=5:
        for i in set(ranks):
            st = [i+k for k in range(5)]
            if set(st).issubset(set(ranks)):return cups_form(hand)[ranks.index(st[4])][0][0]
            #if set.intersection(set(st),set(ranks))==set(st):
            #    return cups_form(hand)[ranks.index(st[4])][0][0]
    return False

#one more card
def three_of_a_kind(hand:list):#7
    three = [i for i in cups_form(hand) if len(i)==3]
    if three:
        hand_without_three = [i[0] for i in hand if i not in three[0]]
        return [three[0][0][0], *hand_without_three[:3]]
    return False


def two_pair(hand:list):#8
    two = [i for i in cups_form(hand) if len(i)==2 ][:2]
    if len(two) ==2:
        hand_without_two = [i[0] for i in hand if i not in two[0]+two[1]]
        return [two[0][0][0],two[1][0][0] , hand_without_two[0]]
    return False

#2 more cards 
def one_pair(hand:list):#9
    one = [i for i in cups_form(hand) if len(i)==2]
    if one:
        hand_without_pair = [i[0] for i in hand if i not in one[0]]
        return [one[0][0][0], *hand_without_pair[:3]]
    return False


def high_card(hand:list):#10
    return list(map(lambda x:x[0],hand))[:5]


def cups_form(hand:list)->list[list]:
    """
    sorts cards in a hand into "cups" in descending card strength, each containing one rank and possibly multiple cards:

    ['KH', 'QH', '9D', '9S', '9H', '6S', '4C'] ==> [['KH'], ['QH'], ['9D', '9S', '9H'], ['6S'], ['4C']]
    """
    holder = []
    for rank in get_rank(hand):
        h_many =get_rank(hand).count(rank)
        cup = [hand[get_rank(hand).index(rank)+i] for i in range(h_many)]
        if cup not in holder:
            holder.append(cup)
    return holder


def best_config(hand:list)->tuple:
    if royal_flush(hand): return 1,royal_flush(hand)
    elif straight_flush(hand): return 2,straight_flush(hand)
    elif four_of_a_kind(hand): return 3,four_of_a_kind(hand)
    elif full_house(hand): return 4,full_house(hand)
    elif flush(hand): return 5,flush(hand)
    elif straight(hand): return 6,straight(hand)
    elif three_of_a_kind(hand): return 7,three_of_a_kind(hand)
    elif two_pair(hand): return 8,two_pair(hand)
    elif one_pair(hand): return 9,one_pair(hand)
    else: return 10,high_card(hand)


class Hand():
    def __init__(self,deck_range,community_cards) -> None:
        self.pocket = [DECK[i] for i in range(*deck_range)]
        self.whole_hand = self.pocket + community_cards
        self.hand_descending = sorted(self.whole_hand,key= lambda x:-RANKS.index(x[0]))
    def __str__(self) -> str:
        return repr(self.pocket)
    def __repr__(self) -> str:
        return repr(self.pocket)
    def __add__(self,other)->list:
        return self.pocket+other
    def hand_rating(self):
        return best_config(self.hand_descending)