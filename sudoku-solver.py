'''
Representation of a traditional 9x9 sudoku board
 
 A1 A2 A3| A4 A5 A6| A7 A8 A9
 B1 B2 B3| B4 B5 B6| B7 B8 B9
 C1 C2 C3| C4 C5 C6| C7 C8 C9
---------+---------+---------
 D1 D2 D3| D4 D5 D6| D7 D8 D9
 E1 E2 E3| E4 E5 E6| E7 E8 E9
 F1 F2 F3| F4 F5 F6| F7 F8 F9
---------+---------+---------
 G1 G2 G3| G4 G5 G6| G7 G8 G9
 H1 H2 H3| H4 H5 H6| H7 H8 H9
 I1 I2 I3| I4 I5 I6| I7 I8 I9

'''

digits = "123456789" #the possible digits that can go in every square
rows = "ABCDEFGHI" #the rows of the grid
colmns = digits #the columns of the grid

def cross_product(A,B):
    '''
    Returns the coordinate of a square
    '''
    return [a + b for a in A for b in B]
'''
Equivlalent to:
list = []
for a in rows:
    for b in clmns:
        list.append(a + b)
'''

squares = cross_product(rows, colmns) #generates all the squares from A1 to I9

list_of_units = ([cross_product(rows, c) for c in colmns] +
                 [cross_product(r, colmns) for r in rows] +
                 [cross_product(rws, cols) for rws in ("ABC", "DEF", "HGI") for cols in ("123", "456", "789")])
#shows all the units of a given square (rows, columns, and same box)


units = dict((s, [u for u in list_of_units if s in u]) for s in squares) #lists the units in a dictionary pairing with the square

peers = dict((s, set(sum(units[s],[])) - set([s])) for s in squares) #lists the peers of a square in a dictionary

def eliminate(values, sqr, dgt):
    '''
    Eliminates a digit(dgt) from the values of sqr (values[s]). When the values are <=2 this change is propagated.
    '''
    if dgt not in values[sqr]:
        return values #other have already been eliminated
    
    values[sqr] = values[sqr].replace(dgt, " ")
    
    if len(values[sqr]) == 0:
        return False #no values left - CONTRADICTION
    elif len(values[sqr]) == 1:
        d2 = values[sqr]
        if not all(elimate(values, sqr2, dgt2) for sqr2 in peers[sqr]):
            return False
        
    for u in units[sqr]:
        dplaces = [sqr for sqr in u if dgt in values[sqr]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign_values(values, dplaces[0], dgt):
                return False
            
    return values

def assign_values(values, sqr, dgts):
    '''
    sqr is the square we are assigning a digit (dgts) to. Dgts is the digit that will be assigned to square sqr.
    All other values are eliminated from the dictionary holding the values for sqr, and this change is propagated.
    '''
    remaining_values = values[sqr].replace(dgts, " ")
    if all(eliminate(values, sqr, dgts2) for dgts2 in remaining_values):
        return values
    else:
        return False

def values(grid):
    '''
    Converts the grid to a dictionary of {Square: Char} with empty squares containing a value of 0.
    '''
    chars = [c for c in grid if c in digits or c in "0"]
    
    assert len(chars) == 81 #raises assertion error if not 9x9 grid
    
    return dict(zip(squares,chars))

def parse_grid(grid):
    '''
    Converts the grid to a dictionary mapping each square to a list of its possible values. 
    '''
    square_values = dict((s, digits) for s in squares)
    
    for s, d in values(grid).items():
        if d in digits and not assign_values(square_values, s, d):
            return False #if the digit d cannot be assigned to square s
        
    return square_values

def display(values):
    '''
    Displays the sudoku grid with the given values
    '''
    width = max(len(values[s]) for s in squares) + 1
    line = "+".join(["-" * (width * 3)] * 3)
    
    for r in rows:
        print("".join(values[r + c].center(width) + ("|" if c in "36" else "") for c in colmns))
        if(r in "CF"):
            print(line)
   
    print()
    
def search(values):
    '''
    Using Depth-First Search (DFS) attempt to solve for every unit by starting with the 
    squares with the lowest possible values.
    '''
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares):
        return values #puzzle is solved
    
    n, s = min((len(values[s]), s) for s in squares is len(values[s]) > 1)
    
    return some(search(assign_values(values.copy()), s, d) for d in values[s])

def some(seq):
    '''
    Cheks if attempt solves puzzle
    '''
    for element in seq:
        if element:
            return element
    return False
    
def solve_sudoku(grid):
    '''
    Solves the inputted sudoku puzzle.
    '''
    return search(parse_grid(grid))
