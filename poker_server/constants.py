ranks = "23456789TJQKA"
suits = "HDCS"  # hearts, diamonds,clubs,spades
deck = [rank + suit for suit in suits for rank in ranks]

N = 5
small_blind = 10  # small blind
big_blind = 2 * small_blind  # big blind
starting_money = 1000
