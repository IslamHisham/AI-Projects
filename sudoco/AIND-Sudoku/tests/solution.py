
from utils import *


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
        #print("box is:",box)
        if len(values[box])==2: #since we are talking about twins so we can only lock two digits
            #print("found two digited box which is:",box, "its value is",values[box])
            for unit in units[box]:#loop to search for the twin
                twin_box=False
                #print("the unit is:",unit)
                for box_peer in unit:
                    if values[box]== values[box_peer] and box != box_peer: #twin found as same value exist in another box
                        twin_box=box_peer #pointing to the twin
                        #print("twin found and it's:",twin_box,"its value is:", values[twin_box]) 
                        break
                if twin_box:
                    #print("starting the digits removal loop")
                    for box_peer in unit:#loop to remove the digits of the twins from all other peers
                        #print("we ar at box:",box_peer, "in the loop")
                        if box_peer==twin_box or box_peer == box:#skip removing digits from the twin or the box itself
                            #print("skipping box:",box_peer,"as its the twin")
                            continue
                        #print("box is:",box_peer,"old box value is:",values[box_peer])
                        values[box_peer]=values[box_peer].replace(values[box],'')
                        #print("new box value is:",values[box_peer])      
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function 'using the eliminate function in the class solution to finish the project faster'
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function 'using the only_choise function in the class solution to finish the project faster'
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function 'using the reduce_puzzle function in the class solution to finish the project faster'
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def choose_one(values):
    "choosing one of the squares with the fewest possibilities, this will be used in the search function"
    for i in range(2,10):
        for box in values.keys():
            if len(values[box])==i:
                return box
            
def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function ' I implemented this function my own way as this might be the basis of a decision tree
    # First, reduce the puzzle using the previous function
    values=reduce_puzzle(values)
    if values is False:
        return False ## Failure
    #check if the sudoko is completed or not and return the sudoko if completed
    completed=True
    for box in values.keys():
        if len(values[box])>1:
                completed=False
                break
    if completed==True:
        return values
    values=naked_twins(values)
    # Choose one of the unfilled squares with the fewest possibilities
    box=choose_one(values)
    for i in values[box]:#loop over all possible values of the box
        new_values=values.copy()
        new_values[box]=i
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        new_values=search(new_values)
        if new_values:
            return new_values


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
