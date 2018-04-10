from utils import *

def choose_one(values):
    "choosing one of the squares with the fewest possibilities"
    for i in range(2,10):
        for box in values.keys():
            if len(values[box])==i:
                return box
possibilities=[]
def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values=reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    #check if the sudoko is completed or not and return the sudoko if completed
    completed=True
    for box in values.keys():
        if len(values[box])>1:
                completed=False
                break
    if completed==True:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    box=choose_one(values)
    for i in values[box]:#loop over all possible values of the box
        new_values=values.copy()
        new_values[box]=i
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        new_values=search(new_values)
        if new_values:
            return new_values
    # If you're stuck, see the solution.py tab!
