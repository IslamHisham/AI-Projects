from utils import *

values={"A1": "2468", "H2": "23568", "D8": "1235679", "F1": "123689", "D2":
"4", "D4": "23678", "I7": "9", "F4": "23468", "A9": "2346", "E3":
"25689", "I1": "123678", "B3": "3", "B8": "8", "C2": "68", "B5": "46",
"H4": "1", "I9": "1235678", "I5": "35678", "B7": "7", "A4": "5", "I2":
"123568", "E9": "12345678", "D6": "23568", "H3": "2456789", "C3":
"4678", "A8": "2346", "F9": "1234568", "C1": "4678", "B2": "2", "G7":
"1234568", "C9": "13456", "D3": "25689", "D7": "123568", "C8":
"13456", "E4": "234678", "I3": "25678", "E5": "13456789", "G6": "9",
"E8": "12345679", "G1": "1234678", "E1": "123689", "A7": "2346", "H1":
"2346789", "F3": "25689", "H8": "234567", "G4": "23678", "D5":
"1356789", "D9": "1235678", "D1": "123689", "C6": "368", "H9":
"2345678", "F8": "1234569", "C4": "9", "B6": "1", "G9": "12345678",
"G3": "245678", "G8": "1234567", "E6": "23568", "I6": "4", "I4":
"23678", "F6": "23568", "A3": "1", "A2": "9", "H5": "35678", "H6":
"23568", "F2": "7", "B1": "5", "E2": "123568", "G5": "35678", "F5":
"1345689", "A6": "7", "F7": "1234568", "I8": "123567", "C5": "2",
"B9": "9", "G2": "123568", "H7": "234568", "A5": "3468", "C7":
"13456", "B4": "46", "E7": "1234568"}

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
#constructing first and second diagonals
first_diagonal=[]
second_diagonal=[]
j=1
k=9
for i in rows:
    first_diagonal.append(i+str(j))
    second_diagonal.append(i+str(k))
    j+=1
    k-=1
# TODO: Update the unit list to add the new diagonal units 'added the diagonals in a list to th unitlist list of lists'
unitlist = unitlist+[first_diagonal,second_diagonal]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    for box in units.keys():
        print("box is:",box)
        if len(values[box])==2: #since we are talking about twins so we can only lock two digits
            print("found two digited box which is:",box, "its value is",values[box])
            for unit in units[box]:#loop to search for the twin
                twin_box=False
                print("the unit is:",unit)
                for box_peer in unit:
                    if values[box]== values[box_peer] and box != box_peer: #twin found as same value exist in another box
                        twin_box=box_peer #pointing to the twin
                        print("twin found and it's:",twin_box,"its value is:", values[twin_box]) 
                        break
                if twin_box:
                    print("starting the digits removal loop")
                    for box_peer in unit:#loop to remove the digits of the twins from all other peers
                        print("we ar at box:",box_peer, "in the loop")
                        if box_peer==twin_box or box_peer == box:#skip removing digits from the twin or the box itself
                            print("skipping box:",box_peer,"as its the twin")
                            continue
                        print("box is:",box_peer,"old box value is:",values[box_peer])
                        values[box_peer]=values[box_peer].replace(values[box][0],'').replace(values[box][1],'')
                        print("new box value is:",values[box_peer])      
    return values

values2=naked_twins(values)
display(values)
print("*******************************************************")
display(values2)
    
