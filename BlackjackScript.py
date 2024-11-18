import random
from ScriptHandler import DeckOperations as DeckOP
from ScriptHandler import PointsOperations as Points

game = True
deck = DeckOP.Deck
cards_available = DeckOP.Options
score = 0


while game is True:
    answer = input("Hit or Pass?:")
    
    if answer == "Hit":
        card = random.choice(cards_available)
        print(card)
        DeckOP.RemoveCard(deck,card)
        if deck[card] == 0:
            cards_available.remove(card)
            
        new_score = Points.CalculatePoints(score, card)
        score = new_score
        game = Points.Endgame(game)
        
    elif answer == "Pass":
        print("Thanks for playing")
        game = False
        
    else:
        print("Bad input, try again with 'Hit' or 'Pass'")
