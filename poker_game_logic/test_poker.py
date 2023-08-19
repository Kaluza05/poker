from hand_logic import *

def test_three_of_a_kind():
    three_hand = ["2H", "2D", "2S", "3C", "4D"]
    assert three_of_a_kind(three_hand) == True

    non_three_hand = ["2H", "3D", "2S", "3C", "4D"]
    assert three_of_a_kind(non_three_hand) == False


def test_straight():
    straight_hand = ["2H", "3D", "4S", "5C", "6D"]
    helper = helper(straight_hand)
    assert straight(straight_hand) == True


