#Card Classification
from pandas import DataFrame as df

class ClassificatonTools:

    points_dictionary = {"card"    :   ["a","2","3","4","5","6","7","8","9","10","j","q","k"],
                        "points"   :   [ 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 10, 10 ,10],
                        "row_val"  :   [ 1,1,1,1,1,1,1,1,1,1,1,1,1],
                        "col_val"  :   [ 1,1,1,1,1,1,1,1,1,1,1,1,1]
                         }    
    lookup_table = df(points_dictionary)


    def card_scoring(num_symbols):
        match num_symbols:
            case 1: 
                card_value = 1
            case 2:
                card_value = 2
            case 3:
                card_value = 3
            case 4:
                card_value = 4
            case 5:
                card_value = 5
            case 6:
                card_value = 6
            case 7:
                card_value = 7
            case 8:
                card_value = 8
            case 9:
                card_value = 9
            case _:
                card_value = 10
        
        return card_value

if __name__=="__main__":
    print(ClassificatonTools.lookup_table)

