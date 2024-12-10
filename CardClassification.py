#Card Classification
from pandas import DataFrame as df

class ClassificatonTools:

    points_dictionary = {"card"    :   ["a","2","3","4","5","6","7","8","9","10","j","q","k"],
                        "points"   :   [ 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 10, 10 ,10],
                        "row_val"  :   [ 1,1,1,1,1,1,1,1,1,1,1,1,1],
                        "col_val"  :   [ 1,1,1,1,1,1,1,1,1,1,1,1,1]
                         }    
    lookup_table = df(points_dictionary)

if __name__=="__main__":
    print(ClassificatonTools.lookup_table)