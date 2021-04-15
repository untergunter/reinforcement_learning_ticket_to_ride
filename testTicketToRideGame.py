import pytest
import pandas as pd
from collections import defaultdict,Counter

from TicketToRideGame import Deck, Board ,TicketToRideGame


deck_input = {'a':1,'b':2,'c':3}

@pytest.fixture()
def deck():
    return Deck(deck_input)

def test_init(deck):
    assert deck.next_deck == []
    input_from_current_deck = dict(Counter(deck.current_deck))
    assert input_from_current_deck == deck_input

def test_deck(deck):
    assert deck.type_quantity == deck_input

def test_deck_pop_n(deck):
    all_elements = len(deck.current_deck)
    elements = deck.pop_n(all_elements)
    result_dict = defaultdict(int)
    for element in elements:
        result_dict[element]+=1
    assert dict(result_dict) == deck_input
    assert len(deck.current_deck) == 0
    deck.reset_deck()
    elements = deck.pop_n(all_elements+1)
    assert len(deck.current_deck) == all_elements-1

def test_reset_deck(deck):
    deck.current_deck = []
    deck.reset_deck()
    input_copy = deck_input.copy()
    for card in deck.current_deck:
        input_copy[card] -= 1
    for card,count in input_copy.items():
        assert count == 0

    # test add_cards_underneath
    assert 'new_card' not in deck.current_deck
    deck.add_cards_underneath(['new_card'])
    assert 'new_card' not in deck.current_deck
    deck.reset_deck()
    assert deck.current_deck == ['new_card']

@pytest.fixture
def board():
    return Board()

def test_bord_setup(board):
    assert len(board.road_owner) == len(board.road_data_by_id)
    for key in range(len(board.road_owner)):
        assert key in board.road_data_by_id

def test_calculate_all_valid_ways_to_get_grey_road(board):
    cards = {'green':5,'blue':3,'red':2}
    two_ways = board.calculate_all_valid_ways_to_get_grey_road(cards, 3)
    assert len(two_ways) == 2
    no_way = board.calculate_all_valid_ways_to_get_grey_road(cards, 6)
    assert no_way is None


def test_generate_valid_cards_count_for_path(board):

    got_result = board.generate_valid_cards_count_for_path(4 , 'yellow' , 5 , 0)
    assert got_result == ('yellow',4)

    not_enough_cards = board.generate_valid_cards_count_for_path(6 , 'yellow' , 5 , 0)
    assert not_enough_cards is None

    enough_with_jokers = board.generate_valid_cards_count_for_path(6 , 'yellow' , 5 , 1)
    assert enough_with_jokers == ('yellow',5,'joker',1)

    only_jokers = board.generate_valid_cards_count_for_path(6 , 'yellow' , 0 , 6)
    assert only_jokers == ('joker', 6)

def test_cards_can_purchase_road(board):
    cards = {'yellow':8}
    single_color_can = board.cards_can_purchase_road(cards,1)
    assert single_color_can == [('yellow',6)]
    gray_single_color = board.cards_can_purchase_road(cards,0)
    assert gray_single_color == [('yellow',4)]
    cards = {'yellow': 4,'red':5,'blue':3}
    gray_multi_color = board.cards_can_purchase_road(cards, 0)
    assert sorted(gray_multi_color) == [('red',4),('yellow',4)]

def test_occupy_path(board):
    assert board.road_owner[0] is None
    board.occupy_path(0,0)
    assert board.road_owner[0] == 0

def test_can_a_path_be_occupied(board):
    cards = {'green': 4}
    assert board.can_a_path_be_occupied(cards,0) is True
    cards = {'blue': 3,'joker':1}
    assert board.can_a_path_be_occupied(cards, 0) is True
    cards = {'green': 3}
    assert board.can_a_path_be_occupied(cards, 0) is False
    board.occupy_path(0,0)
    cards = {'green': 4}
    assert board.can_a_path_be_occupied(cards,0) is False

@pytest.fixture
def game():
    return TicketToRideGame()

def test_carriages_deck(game):
    cards_count = dict(Counter(game.carriages_deck.current_deck))
    for color in cards_count:
        if color != 'joker':
            assert cards_count[color] == 12
        elif color == 'joker':
            assert cards_count[color] == 14

def test_create_missions_deck(game):
    missions = game.missions_deck.current_deck
    raw_missions = pd.read_csv(r'data/destinations.csv')
    assert len(missions)==len(raw_missions)


if __name__ == '__main__':
    pytest.main()