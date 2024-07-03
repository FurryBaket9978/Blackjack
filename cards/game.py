import random
import pygame

class Game:
    def __init__(self) -> None:
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.hand = []
        self.dealer_hand = []

    def create_deck(self) -> list:
        deck = []
        for i in range(1,5):
            if i == 1:
                suit = "S"
            elif i == 2:
                suit = "C"
            elif i == 3:
                suit = "D"
            else:
                suit = "H"
            for j in range(2,15):
                if j == 11:
                    value = "J"
                elif j == 12:
                    value = "Q"
                elif j == 13:
                    value = "K"
                elif j == 14:
                    value = "A"
                else:
                    value = j
                deck.append((suit, value))
        
        return deck

    def shuffle_deck(self) -> list:
        random.shuffle(self.deck)
        return self.deck
    
    def deal_cards(self) -> list:
        hand = [self.deck[0], self.deck[1]]
        self.deck = self.deck[2::]
        return hand
    
    def hit(self, hand:list) -> list:
        hand.append(self.deck[0])
        self.deck.remove(self.deck[0])
        return hand
    
    def eval(self, hand:list) -> int:
        total = 0
        for i in hand:
            if i[1] in ["J", "Q", "K"]:
                total += 10
            elif i[1] == "A":
                total += 11
            else:
                total += i[1]
        if total > 21:
            for i in hand:
                if i[1] == "A":
                    total -= 10
        return total
    
    def load_image(self, path:str, surface:pygame.surface.Surface, x:int, y:int, size:tuple = (100,100)) -> None:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, size)
        surface.blit(img, (x,y))
    
    def get_path(self, card:tuple) -> str:
        if type(card[1]) == int and card[1] < 10:
            val = "0" + str(card[1])
        else:
            val = str(card[1])
        if card[0] == 'C':
            suit = 'clubs'
        elif card[0] == 'H':
            suit = 'hearts'
        elif card[0] == 'S':
            suit = 'spades'
        else:
            suit = 'diamonds'
        return f"/Users/philipgill/Developer/cards/kenney_playing-cards-pack/PNG/Cards (large)/card_{suit}_{val}.png"


    def update_card_display(self, surface:pygame.surface.Surface, stage:str) -> None:
        length = 100 * len(self.hand)
        for count, i in enumerate(self.hand):
            self.load_image(self.get_path(i), surface, (300+(75*count)),550)

        for count, i in enumerate(self.dealer_hand):
            if count == 0 or stage not in ["betting", "player"]:
                self.load_image(self.get_path(i), surface, (300+(75*count)), 100)
            else:
                self.load_image("/Users/philipgill/Developer/cards/kenney_playing-cards-pack/PNG/Cards (large)/card_back.png", surface, (300+(75*count)), 100)
    
    def reset(self):
        self.__init__()