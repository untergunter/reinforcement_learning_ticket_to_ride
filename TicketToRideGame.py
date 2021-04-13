from random import shuffle

import numpy as np
import pandas as pd
from collections import defaultdict, namedtuple


class TicketToRideGame:

    def __init__(self):
        self.carriages_deck = self.create_carriages_deck()
        self.missions_deck = self.create_missions_deck()

    def create_carriages_deck(self):
        carriages = {color: 12 for color in ('pink', 'white', 'blue', 'yellow'
                                             , 'orenge', 'black', 'red', 'green')}
        carriages['joker'] = 14
        carriages_deck = Deck(carriages)
        return carriages_deck

    def create_missions_deck(self):
        missions = pd.read_csv(r'data/destinations.csv')
        tuple_per_mission = missions.to_records(index=False)
        tuple_dict_count_for_Deck = {mission: 1 for mission in tuple_per_mission}
        missions_deck = Deck(tuple_dict_count_for_Deck)
        return missions_deck


class Board:
    def __init__(self):
        self.road_data_by_id, self.road_owner, self.road_id_by_name \
            = self.setup_roads()

    def setup_roads(self):
        roads = pd.read_csv(r'data/Railroads.csv')
        Road = namedtuple('Road', ['length', 'color'])
        road_data_by_id = dict()
        road_id_by_name = defaultdict(list)
        path_occupied_id = [None for player_id in range(len(roads))]
        for route_id, row in roads.iterrows():
            route_name = (row[0], row[1])
            road_data = Road(length=row[2], color=row[3])
            road_data_by_id[route_id]= road_data
            road_id_by_name[route_name].append(route_id)
        return road_data_by_id, path_occupied_id, road_id_by_name

    def generate_valid_cards_count_for_path(self
                                            , length_needed: int
                                            , color_name: str
                                            , color_amount: int
                                            , joker_amount: int):
        """
        we prefer to use color and not jokers if possible.
        :param length_needed:
        :param color_name:
        :param color_amount:
        :param joker_amount:
        :return:
        """
        if color_amount >= length_needed:
            return (color_name , length_needed)
        elif color_amount < length_needed:
            enough_jokers = length_needed - color_amount
            if enough_jokers <= joker_amount:
                if color_amount>0:
                    return (color_name,color_amount
                        , 'joker',enough_jokers)
                elif color_amount == 0:
                    return ('joker', enough_jokers)
            else:
                return None

    def calculate_all_valid_ways_to_get_grey_road(self, cards, length):
        all_valid_combinations = {self.cards_specific_color(color, length, cards)
                                  for color, amount in cards.items()}
        all_valid_combinations.discard(None)
        if len(all_valid_combinations) == 0:
            return None
        elif len(all_valid_combinations) > 0:
            return all_valid_combinations

    def cards_can_purchase_road(self, cards: dict, road_id: int):
        length, route_color = self.road_data_by_id[road_id]
        if route_color == 'gray':
            all_options = self.calculate_all_valid_ways_to_get_grey_road\
                (self, cards, length)
            return all_options

        elif route_color != 'gray':
            cards_for_route = \
                self.cards_specific_color(route_color, length, cards)
            if cards_for_route is not None:
                all_options = [cards_for_route]
                return all_options

    def cards_specific_color(self, route_color: str, length: int, cards: dict):
        jokers_available = 0 if not 'joker' in cards else cards['joker']
        color_cards_count = 0 if not route_color in cards else cards[route_color]

        cars_combination = self.generate_valid_cards_count_for_path(
            length, route_color, color_cards_count, jokers_available)

        return cars_combination

    def can_a_path_be_occupied(self, cards: dict, road_id: int):
        road_is_not_occupied = self.road_owner[road_id] is None


class Deck:
    """
    this is a deck of cards
    """

    def __init__(self, type_quantity: dict):
        self.type_quantity = type_quantity
        self.next_deck = []
        self.current_deck = []
        self.reset_deck()

    def reset_deck(self):
        """
        restarts a deck based on the initial type_quantity dictionary
        or what remains from returned cards
        creates a deck, shuffles it, returns it
        :return: None
        """

        if len(self.next_deck) != 0:
            self.current_deck = self.next_deck.copy()
            self.next_deck = []

        else:
            current_deck = []
            for card, number_of in self.type_quantity.items():
                for _ in range(number_of):
                    current_deck.append(card)

            shuffle(current_deck)
            self.current_deck = current_deck

    def pop_n(self, n: int):
        """
        removes n cards from the current deck and returns them

        :param n:
        :return:
        """

        result = []
        for _ in range(n):
            if len(self.current_deck) == 0:
                self.reset_deck()
            result.append(self.current_deck.pop())
        return result

    def add_cards_underneath(self, cards_back_to_deck):
        """
        returns the cards to the next deck
        :param cards_back_to_deck:
        :return:
        """

        for card in cards_back_to_deck:
            self.next_deck.append(card)


class Player:
    def __init__(self):
        pass


if __name__ == '__main__':
    pass
