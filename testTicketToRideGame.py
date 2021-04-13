import pytest
from collections import defaultdict,Counter
from TicketToRideGame import Deck, Board


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

if __name__ == '__main__':
    pytest.main()