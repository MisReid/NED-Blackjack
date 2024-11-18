

#Place Classes Here#
class DeckOperations:
    
    def __init__(self,) -> None:
        
        pass
    
    Deck = {"A" : 4,
            "2" : 4,
            "3" : 4,
            "4" : 4,
            "5" : 4,
            "6" : 4,
            "7" : 4,
            "8" : 4,
            "9" : 4,
            "10": 4,
            "J" : 4,
            "Q" : 4,
            "K" : 4}
    
    Options = ["A" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def RemoveCard(deck,card):
        deck[card] = deck[card] - 1
        
        return 
    
    def DrawCard(self, card):
        
        return
    
class PointsOperations:

    def __init__(self) -> None:
        pass
    
    point_values={
                "A" : 1,
                "2" : 2,
                "3" : 3,
                "4" : 4,
                "5" : 5,
                "6" : 6,
                "7" : 7,
                "8" : 8,
                "9" : 9,
                "10": 10,
                "J" : 10,
                "Q" : 10,
                "K" : 10
                }
    
    def CalculatePoints(score, card):
        points = PointsOperations.point_values[card]
        score = score + points
        
        return points
        
    def Endgame(score,game = True):
        
        if score > 21:
            
            print("Better Luck Next Time")
            game is False
            
            return game
        
        else:
            
            return