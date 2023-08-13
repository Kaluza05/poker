import pandas as pd
from random import shuffle
from numpy import roll
'''
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

'''
RANKS = '23456789TJQKA'
SUITS = 'HDCS' #hearts, diamonds,clubs,spades
DECK = [rank+suit for suit in SUITS for rank in RANKS]

N=5
SB= 10 #small blind
BB = 2*SB #big blind
STARTING_MONEY = 1000


def get_rank(hand:list)->list: return [RANKS.index(card[0])+2 for card in hand]
def get_suit(hand:list)->list: return [card[1] for card in hand]

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
    four = [i for i in hand if len(i)==4]
    if four:
        for j in hand:
            if len(j) !=4: return [four[0][0][0],j[0][0]]
    return False
def full_house(hand:list):#4
    for i in hand:
        for j in hand:
            if len(i)==2 and len(j)==3: return [j[0][0][0],i[0][0][0]]
    return False
def flush(hand:list):#5
    for suit in SUITS:
        if get_suit(hand).count(suit)>=5: return [card[0] for card in hand if card[1]==suit][:5]
    return False
def straight(hand:list,helper:list):#6
    ranks =get_rank(hand)
    if len(set(ranks))>=5:
        for i in set(ranks):
            st = [i+k for k in range(5)]
            if set.intersection(set(st),set(ranks))==set(st):
                return helper[ranks.index(st[4])][0][0]
    return False
def three_of_a_kind(hand:list):#7
    three = [i for i in hand if len(i)==3]
    if three:
        for j in hand:
            if j !=three[0]: return [three[0][0][0],j[0][0]]
    return False
def two_pair(hand:list):#8
    two = [i for i in hand if len(i)==2 ][:2]
    if len(two) ==2:
        for j in hand:
            if len(j)==1:return [two[0][0][0],two[1][0][0],j[0][0]]
    return False
def one_pair(hand:list):#9
    one = [i for i in hand if len(i)==2]
    if one:
        for j in hand:
            if j !=one[0]:return [one[0][0][0],j[0][0]]
    return False
def high_card(hand:list):#10
    return list(map(lambda x:x[0],hand))[:5]
def best_config(hand:list):
    def help(hand:list):
        holder = []
        for val in get_rank(hand):
            h_many =get_rank(hand).count(val)
            help = [hand[get_rank(hand).index(val)+i] for i in range(h_many)]
            if help not in holder:
                holder.append(help)
        return holder
    helper = help(hand)
    if royal_flush(hand): return 1,royal_flush(hand)
    elif straight_flush(hand): return 2,straight_flush(hand)
    elif four_of_a_kind(helper): return 3,four_of_a_kind(helper)
    elif full_house(helper): return 4,full_house(helper)
    elif flush(hand): return 5,flush(hand)
    elif straight(hand,helper): return 6,straight(hand,helper)
    elif three_of_a_kind(helper): return 7,three_of_a_kind(helper)
    elif two_pair(helper): return 8,two_pair(helper)
    elif one_pair(helper): return 9,one_pair(helper)
    else: return 10,high_card(hand)


class Hand():
    def __init__(self,deck_range,community_cards) -> None:
        self.hand = [DECK[i] for i in range(*deck_range)]
        self.whole_hand = self.hand + community_cards
        self.hand_descending = sorted(self.whole_hand,key= lambda x:-RANKS.index(x[0]))
    def __str__(self) -> str:
        return repr(self.hand)
    def __repr__(self) -> str:
        return repr(self.hand)
    def __add__(self,other)->list:
        return self.hand+other
    def hand_rating(self):
        return best_config(self.hand_descending)
class Table():
    def __init__(self,num_of_players,starting_money) -> None:
        self.num_of_players = num_of_players
        self.community_cards = DECK[2*num_of_players:2*num_of_players+5]
        self.prev_action = 'check'
        df_helper = {f'player {player}':Hand((2*player,2*player+2),self.community_cards) for player in range(self.num_of_players)}
        self.players = pd.DataFrame({'index':df_helper.keys(),
                                     'pocket':df_helper.values(),
                                     'hand':list(map(lambda x:x.hand_descending,df_helper.values())),
                                     'hand rating': list(map(lambda x:x.hand_rating(),df_helper.values())),
                                     'money':starting_money,
                                     'bet':0,
                                     'in game':True,
                                     'all in': False})
        self.players_in_game = self.players[self.players['in game'] ==True].reset_index(drop=True)
    def __repr__(self)->pd.DataFrame:
        return self.players.to_string(index= False)
    #def in_game(self)->pd.DataFrame:
    #    return self.players[self.players['in game'] ==True].reset_index(drop=True)
    def bet(self,player:int,amount:int)->None:
        #print(self.players.at[player,'bet']+amount,self.players_in_game.at[((self.players_in_game[self.players_in_game['index']==f'player {player}'].index[0]-1)%len(self.players_in_game.index)),'bet'])
        if self.players.at[player,'bet']+amount >= self.players_in_game.at[((self.players_in_game[self.players_in_game['index']==f'player {player}'].index[0]-1)%len(self.players_in_game.index)),'bet']:
            if self.players.at[player,'money'] - amount >= 0:
                self.players.at[player,'money'] -= amount
                self.players.at[player,'bet'] += amount
                self.players.at[player,'all in'] = True if self.players.at[player,'money'] - amount == 0 else False
                self.players_in_game = self.players[self.players['in game'] ==True].reset_index(drop=True)
                self.prev_action = 'bet'
            else:print('somethings wrong')
        else: 
            print('call instead')
            #self.call(player)
    def call(self,player:int)->None:
        prev = self.players_in_game.at[((self.players_in_game[self.players_in_game['index']==f'player {player}'].index[0]-1)%len(self.players_in_game.index)),'bet']
        your_current = self.players.at[player,'bet']
        self.prev_action = 'call'
        if self.players.at[player,'money'] - (prev-your_current) >0:
            self.players.at[player,'money'] -= prev-your_current
            self.players.at[player,'bet'] += prev-your_current
        else:
            money = self.players.at[player,'money']
            self.players.at[player,'bet'] += money
            self.players.at[player,'money'] = 0
            self.players.at[player,'all in'] = True
        self.players_in_game = self.players[self.players['in game'] ==True].reset_index(drop=True)
    def fold(self,player:int)->None:
        self.players.at[player,'in game']= False
        self.players_in_game = self.players[self.players['in game'] ==True].reset_index(drop=True)
    def check(self,player:int)->None:
        if self.players.at[player,'bet'] == self.players_in_game.at[((self.players_in_game[self.players_in_game['index']==f'player {player}'].index[0]-1)%len(self.players_in_game.index)),'bet']:
            self.prev_action = 'check'
            print('checking')
        else:
            print('call instead')
            #self.call(player)
    def determine_winner(self)->list: # ustawia wygranych w kolejności od 1 miejsca na wypadek side pot
        hand_scores = self.players_in_game['hand rating']
        score_sort = sorted(hand_scores,key=lambda x:x[0])
        grouped_scores = [[] for _ in range(10)]
        for hand in score_sort:
            grouped_scores[hand[0]-1].append(hand)
        grouped_scores= [i for i in grouped_scores if i!=[]] #removes empty lists
        for scores in grouped_scores:
            if len(scores)==1:
                continue
            else:
                grouped_scores[grouped_scores.index(scores)]=sorted(scores,key=lambda x: [-RANKS.index(scores[0]) for scores in x[1]])
        merge_groups =[j for i in grouped_scores for j in i]
        return [self.players_in_game['index'][self.players_in_game['hand rating']== i].values[0] for i in merge_groups]
    def deal_new_cards(self)->None:
        shuffle(DECK)
        self.community_cards = DECK[2*self.num_of_players:2*self.num_of_players+5]
        df_helper = [Hand((2*i,2*i+2),self.community_cards) for i in range(self.num_of_players)]
        money = self.players['money']
        indexes = self.players['index']
        self.players = pd.DataFrame({'index':indexes,
                                     'pocket':df_helper,
                                     'hand':list(map(lambda x:x.hand_descending,df_helper)),
                                     'hand rating': list(map(lambda x:x.hand_rating(),df_helper)),
                                     'money':money,
                                     'bet':0,
                                     'in game':True,
                                     'all in': False}).apply(roll,shift=-1)
        self.players_in_game = self.players[self.players['in game'] ==True].reset_index(drop=True)



def can_bet(previous_action)->bool:
    if previous_action in ['bet','check','call']: return True
    return False
def can_check(previous_action)->bool:
    if previous_action in ['call','check']: return True
    return False
def can_call(previous_action)->bool:
    if previous_action in ['bet','call','check']: return True
    return False


def game():
    shuffle(DECK)
    table = Table(num_of_players=N,starting_money=STARTING_MONEY)
    while True:
        table.bet(0,SB)
        table.bet(1,BB)
        for stage in [0,3,4,5]:
            table.prev_action = 'check'
            first_action = True
            while (not (table.players_in_game['bet'] == table.players_in_game['bet'][0]).all()) or first_action:
                first_action = False
                for player in range(N):
                    player = (player+2)%table.num_of_players
                    if table.players.iat[player,table.players.columns.get_loc('in game')]:
                        print(table)
                        print(table.players.iat[player,table.players.columns.get_loc('pocket')] )
                        print(table.players.iat[player,table.players.columns.get_loc('pocket')] + table.community_cards[:stage])

                        ask = True
                        while ask:
                            ask = False
                            print(f'{table.players.at[player,"index"]} what do you want to do')
                            what = input()
                            if what == 'bet' and can_bet(table.prev_action):
                                amount = int(input('how much do you want to bet?: '))
                                table.bet(player,amount)
                            elif what =='call' and can_call(table.prev_action):
                                table.call(player)
                            elif what == 'check' and can_check(table.prev_action):
                                table.check(player)
                            elif what == 'fold':
                                table.fold(player)
                            else: ask = True
        winners = table.determine_winner()
        print(winners)
        #table.players.at[table.players[table.players['index']==winners[0]].index[0],'money'] += sum(table.players['bet'])
        print(table.players)
        pot = sum(table.players['bet'])
        for player in winners:
            if table.players.at[table.players[table.players['index']==player].index[0],'all in'] == False:
                table.players.at[table.players[table.players['index']==player].index[0],'money'] += pot
                break
            else:
                players_bet = table.players.at[table.players[table.players['index']==player].index[0],'bet']
                
        table.deal_new_cards()
        print(table.players)



game()

