import random
def initialize_game(grid_size, probability):
    starting_point_for_life = [['*' if random.random()>probability else '0' for _ in range(grid_size)] for _ in range(grid_size)]
    return starting_point_for_life

def count_neighbors(cell, grid):
    #inputs: cell is a tuple (i,j), where i and j are nonnegative integers and grid is a list of list of '*' & '0'
    #output: a interger, the number of live neighbors ('0') of cells
    #side effects: none
    def is_valid_index(i,j):
        #Inpus: i,j are indices (integers)
        #Outpu: True/False depending on whether i,j are valid index on the board 
        if 0<=i<len(grid) and 0<=j<len(grid):
            return
        else: return False
    neighbors = [(cell[0]+index_i, cell[1]+index_j) for index_i in [-1,0,1] for index_j in [-1,0,1] if cell[0]+index_i>=0 and cell[1]+index_j >=0 and not index_i==index_j==0]
    print(neighbors)
    return len(neighbors)
count_neighbors([1,1], [['*','*'],['*','*']])

def update_cell(cell, grid):
    #To update cel, we call count_neighbors to get the number of live neighbors of cell
    #Then we apply rules of Game of Life
    new_grid = grid
    num_live_neighbors = count_neighbors(cell,grid)
    for row in range():
        for col in range():
            if num_live_neighbors<2:
                new_grid[row][col] = '*'
            elif num_live_neighbors==2:
                new_grid[row][col] = grid[row][col]
            elif num_live_neighbors>3:
                new_grid[row][col] = '*'
            else:
                new_grid[row][col] = '0'

def update_game(current_grid):
    new_grid = current_grid
    for row in range(len(new_grid)):
        for col in range(len(new_grid[0])):
            new_grid[row][col] = update_cell([row,col],current_grid)

def game_loop(initial_grid):
    


initialize_game = initialize_game(10,0.2)
for row in initialize_game:
     print(row)