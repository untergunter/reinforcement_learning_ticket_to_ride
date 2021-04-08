from random import shuffle
import pandas as pd
from collections import namedtuple

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
        missions = pd.read_csv('destinations.csv')
        tuple_per_mission = missions.to_records(index=False)
        tuple_dict_count_for_Deck = {mission:1 for mission in tuple_per_mission}
        missions_deck = Deck(tuple_dict_count_for_Deck)
        return missions_deck


class Board:
    def __init__(self):
        self.roads = self.setup_roads()


    def setup_roads(self):
        roads = pd.read_csv('Railroads.csv')
        for _, row in roads.iterrows()
            route_name = (min(row[0],row[1]),max(row[0],row[1]))


class Deck:
    """
    this is a deck of cards
    """
    def __init__(self,type_quantity:dict):
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

        if len(self.next_deck)!=0:
            self.current_deck = self.next_deck.copy()
            self.next_deck = []

        else:
            current_deck = []
            for card,number_of in self.type_quantity.items():
                for _ in range(number_of):
                    current_deck.append(card)

            shuffle(current_deck)
            self.current_deck = current_deck

    def pop_n(self,n:int):
        """
        removes n cards from the current deck and returns them

        :param n:
        :return:
        """

        result=[]
        for _ in range(n):
            if len(self.current_deck)==0:
                self.reset_deck()
            result.append(self.current_deck.pop())
        return result

    def add_cards_underneath(self,cards_back_to_deck):
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