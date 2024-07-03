import pygame
from constants import *
from game import *

#initilization and variable setting
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("/Users/philipgill/Developer/cards/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
money = 100
stage = "betting" # either: betting, dealing, player, house, or payout
pygame.display.set_caption('Blackjack')
game = Game()
running = True
#setting up input box for betting
base_font = pygame.font.Font(None, 32) 
user_text = '' 
input_rect = pygame.Rect(150, 600, 140, 32) 
color_active = pygame.Color('lightskyblue3') 
color_passive = pygame.Color('chartreuse4') 
color = color_passive 
active = False
text = base_font.render("Place bet here:", True, (0,0,0))
text_rect = text.get_rect()
text_rect.center = (225,580)
display = False
bet = 0

while running:
    if stage == "betting":
        game.reset()
        if money == 0:
            running = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and active:
                display = False 
                if event.key == pygame.K_BACKSPACE: 
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if money < int(user_text):
                        error = base_font.render("Invalid bet", True, (255,0,0))
                        error_rect = error.get_rect()
                        error_rect.center = (650,650)
                        display = True
                    else:
                        money -= int(user_text)
                        bet = int(user_text)
                        user_text = ""
                        stage = "dealing"
                else: 
                    user_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                display = False
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
    
    elif stage == "dealing":
        game.hand = game.deal_cards()
        game.dealer_hand = game.deal_cards()
        stage = "player"
    elif stage == "player":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP and not active:
                if event.key == pygame.K_h:
                    game.hit(game.hand)
                    if game.eval(game.hand) > 21:
                        stage = "payout"
                elif event.key == pygame.K_s:
                    stage = "house"
                elif event.key == pygame.K_t:
                    print(game.eval(game.hand))
                elif event.key == pygame.K_a:
                    print(money)
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
    elif stage == "house":
        game.update_card_display(surface, stage)
        total = game.eval(game.dealer_hand)
        if total < 16:
            game.hit(game.dealer_hand)
        else:
            stage = "payout"
    elif stage == "payout":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    stage = "betting"
        if game.eval(game.hand) == 21:
            outcome_text = "You won this round"
            money += bet * 2.5
            bet = 0
        elif game.eval(game.hand) > 21 or game.eval(game.hand) < game.eval(game.dealer_hand):
            outcome_text = "You lost this round"
        elif game.eval(game.hand) > game.eval(game.dealer_hand):
            outcome_text = "You won this round"
            money += bet * 2
            bet = 0
        elif game.eval(game.hand) == game.eval(game.dealer_hand):
            outcome_text = "You and the dealer tied"
            money += bet
            bet = 0
        outcome = base_font.render(outcome_text, True, (0,0,0))
        outcome_rect = outcome.get_rect()
        outcome_rect.center = (450,350)
        help_text = base_font.render("Press return to start a new round", True, (0,0,0))
        help_rect = help_text.get_rect()
        help_rect.center = (450, 370)
        surface.blit(help_text, help_rect)
        surface.blit(outcome, outcome_rect)
    
    if active: 
        color = color_active 
    else: 
        color = color_passive

    pygame.draw.rect(surface, color, input_rect) 
    text_surface = base_font.render(user_text, True, (255, 255, 255)) 
    surface.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    input_rect.w = max(140, text_surface.get_width()+10) 
    background = pygame.image.load("/Users/philipgill/Developer/cards/background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    money_text = base_font.render(f"Money: ${money}", True, (0,0,0))
    money_rect = money_text.get_rect()
    money_rect.center = (700,50)
    surface.blit(text, text_rect)
    surface.blit(money_text, money_rect)
    if display:
        surface.blit(error, error_rect)
    game.update_card_display(surface, stage)
    pygame.display.update()
    surface.blit(background, (0,0))