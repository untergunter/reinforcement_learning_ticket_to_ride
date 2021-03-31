from random import shuffle

class TicketToRideGame:
    def __init__(self):
        pass

class Board:
    def __init__(self):
        pass

class Deck:
    """
    this is a deck of cards
    """
    def __init__(self,type_quantity:dict):
        self.type_quantity = type_quantity
        self.current_deck = self.reset_deck()

    def reset_deck(self):
        """
        restarts a deck based on the initial type_quantity dictionary
        creates a deck, shuffles it, returns it
        :return: None
        """


        dec = []
        for card,number_of in self.type_quantity.items():
            for _ in range(number_of):
                dec.append(card)

        shuffle(dec)

        return dec

    def pop_n(self,n:int):
        """
        removes n cards from the current deck and returns them

        :param n:
        :return:
        """

        result=[]
        for _ in range(n):
            if len(self.current_deck)==0:
                self.current_deck = self.reset_deck()
            result.append(self.current_deck.pop())
        return result

    def add_cards_underneath(self,cards_back_to_deck):
        for card in cards_back_to_deck:
            self.current_deck.insert(0,card)

class Player:
    def __init__(self):
        pass

if __name__ == '__main__':
    pass