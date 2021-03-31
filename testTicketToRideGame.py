import pytest
from collections import defaultdict

class test_Deck():
    from TicketToRideGame import Deck
    deck_input={'a':1,'b':2,'c':3}
    test_deck = Deck(deck_input)

    all_elements = len(test_deck.current_deck)
    elements =  test_deck.pop_n(all_elements)
    result_dict = defaultdict(int)
    for element in elements:
        result_dict[element]+=1
    assert dict(result_dict) == deck_input

    #make sure the restart mechanisem works
    elements = test_deck.pop_n(all_elements)
    result_dict = defaultdict(int)
    for element in elements:
        result_dict[element] += 1
    assert dict(result_dict) == deck_input