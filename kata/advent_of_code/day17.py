# Messy and unfinished attempt at advent of code day 17

BUFFER = 1

def pprint_matrix(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

coords = [('x=495', 'y=2..7'),
('y=7', 'x=495..501'),
('x=501', 'y=3..7'),
('x=498', 'y=2..4'),
('x=506', 'y=1..2'),
('x=498', 'y=10..13'),
('x=504', 'y=10..13'),
('y=13', 'x=498..504')]

min_x, min_y = (9999999999, 9999999999)
max_x, max_y = (0, 0)
sides = []
bottoms = []
for coord in coords:
    if 'x=' in coord[0]:
        x, y = coord
        x=int(x.replace('x=',''))
        start_y, end_y= y.replace('y=','').split("..")
        start_y = int(start_y)
        end_y = int(end_y)

        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x

        if end_y > max_y:
            max_y = end_y
        if start_y < min_y:
            min_y = start_y
        sides.insert(0, (x,(start_y, end_y)))

    else:
        y, x = coord
        y=int(y.replace('y=',''))
        start_x, end_x= x.replace('x=','').split("..")
        start_x = int(start_x)
        end_x = int(end_x)
        bottoms.insert(0, (y,(start_x, end_x)))

min_x -= BUFFER
max_y += BUFFER
n_columns = (max_x - min_x)
n_rows = (max_y - min_y + BUFFER)
spring_index = 500 - min_x

grid = [ [None] * n_columns for x in range(n_rows)]
grid[1][spring_index] = "+"

print("Min X", min_x)
print("Max X", max_x)
print("Min Y", min_y)
print("Max Y", max_y)
print("Sides", sides)
print("Bottoms", bottoms)

# Draw indicies
for i in range(n_columns):
    if i > 0:
        n_row = min_x+i
        grid[0][i] = n_row
    for j in range(n_rows):
            grid[j][0] = j
            if grid[j][i] == None:
                grid[j][i] = "."
pprint_matrix(grid)
print("\n")

# Draw Sides and Bottoms
while sides:
    x, y = sides.pop()
    for i in range(1, n_columns):
        for j in range(n_rows):
            if i == (x-min_x) and y[0] <= j <= y[1]:
                grid[j][i] = 'X'
            continue

while bottoms:
    y, x = bottoms.pop()
    for i in range(1, n_columns):
        for j in range(n_rows):
            if j == (y) and (x[0]-min_x) <= i <= (x[1]-min_x):
                grid[j][i] = 'X'
            continue

# Draw water
for i in range(1, n_columns):
    for j in range(n_rows):
        if i == spring_index and grid[j][i] == '.':
            grid[j][i] = "|"
        elif i == spring_index and grid[j][i] == 'X':
            # go as far left and right as possible
            col_jump = 1
            row_jump = 1
            no_clay = True
            while no_clay:
                if grid[j-row_jump][i-col_jump] != 'X':
                    grid[j-row_jump][i-col_jump] = "|"
                    col_jump += 1
                else:
                    no_clay = False

            print('hit some clay')
            break

pprint_matrix(grid)

