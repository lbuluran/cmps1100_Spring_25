import copy

#Game of Life
# * = dead | 0 = alive
num_columns = 10
num_rows = 10
num_timesteps = 10

#D.R.Y. - Don't Repeat Yourself

initial_grid = []
for row in range(num_rows):
    current_row = []
    for col in range(num_columns): 
        current_row.append('*')
    initial_grid.append(current_row)

initial_grid[1][3] = '0'
initial_grid[1][4] = '0'
initial_grid[1][5] = '0'


current_grid = copy.deepcopy(initial_grid)
initial_grid[0][0] = '0'

found_positions = [] #Iterations Storage

for timestep in range(num_timesteps):
    #We need to ipdate the current grid into a new grid
    #Using the 4 rules for the game of life
    #Then we need rto set the current grid to the new grid
    #Then repea.
    new_grid = copy.deepcopy(current_grid)

    for row in range(num_rows):
        for col in range(num_columns):
            neighbors = []
            for index_i in [-1, 0, 1]:
                for index_j in [-1, 0, 1]:
                    if row+index_i >= 0 and row+index_i<num_rows and col+index_j >= 0 and col+index_j < num_columns:
                        neighbors.append([index_i, index_j])
            number_of_live_neighbors = len(neighbors)
            if number_of_live_neighbors < 2:
                new_grid[row][col] = '*'
            elif number_of_live_neighbors ==2:
                new_grid[row][col] = current_grid[row][col]
            elif number_of_live_neighbors > 3:
                new_grid[row][col] = '*'
            else:
                new_grid[row][col] = '0'
for row in current_grid:
    print(row)
print("--Next Generation")
for grid in found_positions:
    if new_grid == grid:
        print("Repeated after", timestep, "timesteps")
found_positions.append(copy.deepcopy(new_grid))
current_grid = copy.deepcopy(new_grid)

#How long till the game repates