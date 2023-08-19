from hand_logic import *

def test_three_of_a_kind():
    three_hand = ["4C", "3D","2H", "2D", "2S"]
    assert three_of_a_kind(three_hand) == ["2","4","3"]

    non_three_hand = ["4D","3H", "3D", "2S", "2C"]
    assert three_of_a_kind(non_three_hand) == False


def test_straight():
    straight_hand = ['6D', '5C', '4S', '3D', '2H']
    assert straight(straight_hand) == ['6']

    non_straight_hand = ['7D', '6C', '4S', '3D', '2H']
    assert straight(non_straight_hand) == False

def test_royal_flush():
    royal_hand = ["AH",'KH','QH','JH','TH','6H','4S']
    assert royal_flush(royal_hand) == ["A"]

    non_royal_hand = ["AH",'KS','QH','JH','TH','6H','4S']
    assert royal_flush(non_royal_hand) == False

def test_full_house():
    full_hand = ["AS",'AH','AD','KS','KC','9H','9D']
    assert full_house(full_hand) == ['A','K']

    non_full_hand = ["AS",'AH','KD','KS','TC','9H','9D']
    assert full_house(non_full_hand) == False

def test_two_pair():
    two_hand = ['JH','JS','TD','TC','8S','8C','5D']
    assert two_pair(two_hand) == ['J','T','8']

    non_two_hand = ['QH','TS','TD','TC','8S','8C','5D']
    assert two_pair(non_two_hand) == False