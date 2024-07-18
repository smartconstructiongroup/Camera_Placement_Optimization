import json
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import os

from Categorized_Value_1 import Categorized_Value


from findDic import findDic


N = 3
vals = np.ones((N, 4))

# black
vals[0, 0] = 0 # red
vals[0, 1] = 0 # green
vals[0, 2] = 0 # blue
vals[0, 3] = 1 # Alpha

# red
vals[1, 0] = 1
vals[1, 1] = 0
vals[1, 2] = 0
vals[1, 3] = 1

# white
vals[2, 0] = 1 
vals[2, 1] = 1 
vals[2, 2] = 1 
vals[2, 3] = 1 

# #gray
# vals[3, 0] = 0.5  
# vals[3, 1] = 0.5  
# vals[3, 2] = 0.5
# vals[3, 3] = 1

phase_number = int(input('Please enter phase number [1]: ') or 1)


indices_of_camera_candids = Categorized_Value()


total_phases = len(indices_of_camera_candids)
if total_phases < phase_number:
    print(f'There is not enough phases ({total_phases}) in inputs compared to your phase number ({phase_number})')

answers = findDic([i[0] for i in indices_of_camera_candids[phase_number-1]])

mat_filename = f'Phase {phase_number} mat.json'
if not mat_filename.endswith('.json'):
    mat_filename += '.json'
with open(mat_filename, 'r') as rfile:
    mat = json.loads(rfile.read())
m = mat['dimensions'][0]
n = mat['dimensions'][1]
id2index = mat['id2index']



# creating a {(i, j): 2} dictionary
# each (i, j) represents a cell in matrix
# value of each cell (e.i. 2) represents color-index of the cell
# color-index 0: black
#             1: red
#             2: white
#             3 and more: grays/shadows
cell_color_list = {}
for i in range(m):
    for j in range(n):
        cell_color_list[i, j] = 2


# reading block list data from file
block_list_filename = f'Phase {phase_number} block_list.json'
if not block_list_filename.endswith('.json'):
    block_list_filename += '.json'
with open(block_list_filename, 'r') as rfile:
    json_block_list = json.loads(rfile.read())


# assigning color-index of black (0) to blocks
    
for item in json_block_list:
    cell_color_list[item['x'] - 1, item['y'] - 1] = 0


# read coverage data file, containing list of covered cells by each candid-camera-id
coverage_filename = f'Phase {phase_number} coverage.json'
if not coverage_filename.endswith('.json'):
    coverage_filename += '.json'
with open(coverage_filename, 'r') as rfile:
    json_coverage = json.loads(rfile.read())


# assign coverage data file to coverage dictionary
coverage = json_coverage['coverage']


# reading pulp library's results
# with open('optimization_solution.json', 'r') as rfile:
#     results = json.loads(rfile.read())
# 
# answers = []
# for item in results.items():
#     if item[1]['solution_value'] == 1.0:
#         answers.append(item[1]['index'])
# 
#     elif item[1]['solution_value'] != 0.0:
#         print(item[1]['index'], item[1]['solution_value'])
# print(answers)


# reading answers (e.i. x[15] = 1) from results.yml file
# answers = [int(i) for i in input('Please enter id of selected cameras separated with commas like 2,43,23,etc. : ').split(',')]


print('List of id_number of selected {} cameras:\n{}'.format(len(answers), answers))
answers = [i[1] for i in answers]
# PLease insert answers manually in next line and un-comment it
# answers = []

# create and evaluate real_coverage and co_coverage dictionaries
real_coverage = {}
co_coverage = {}


for i in range(m):
    for j in range(n):
        # assign black color to all co_coverage cells
        co_coverage[i, j] = 0

        # if it's not a block make it white [2]
        # assign 0 to blocks in real_coverage
        if not cell_color_list[i, j] == 0:
            co_coverage[i, j] = 2
            real_coverage[i, j] = 0


z_plotdata = {}
k = 0
# for each camera in list of selected cameras
for ans in answers:

    # recolor all cells except for blocks to white [2]
    for item in cell_color_list:
        if cell_color_list[item] != 0:
            cell_color_list[item] = 2

    # assign gray color to cells covered by one of selected cameras [ans]
    cover = coverage[str(ans)]
    for item in cover:
        x = id2index[str(item)][0]
        y = id2index[str(item)][1]
        cell_color_list[x, y] = 3
        
        # adding this cell to grayed cells for real coverage computations
        real_coverage[x, y] = 1

    # assiging red color to current camera cell [x0, y0]
    x0 = id2index[str(ans)][0]
    y0 = id2index[str(ans)][1]
    cell_color_list[x0, y0] = 1

    z = []
    for i in range(m):
        z.append([])

        for j in range(n):
            if cell_color_list[i, j] == 1:
                co_coverage[i, j] = 1
            elif cell_color_list[i, j] == 3 and co_coverage[i, j] != 1:
                co_coverage[i, j] += 1
            z[i].append(cell_color_list[i, j])

    z_plotdata[k] = z
    k += 1


# max_color is maximum color-index of static plot's cells
max_color = 0

# z2 is second matrix of color-indices (vals2) of each cell
# to be used in static plot
z2 = []

# assiging color-index of each cell to relevant cell of z2
for i in range(m):
    z2.append([])
    for j in range(n):
        if co_coverage[i, j] > max_color:
            max_color = co_coverage[i, j]
        z2[i].append(co_coverage[i, j])

# num_grays is maximum number of coverage overlaps
# equal to maximum index minus index of red/white/black cells
num_grays = max_color - 2
print('Maximum number of coverage overlaps: {}'.format(num_grays))

# get a cpoy of basic list of colors vals and save it in vals2
# in order to use it in static plot
vals2 = vals

# adding gray color with gradual transparency for each overlapping occurance
for i in range(num_grays):
    color = [0.4, 0.1, 0.4, (i + 1) / num_grays * 0.9]
    vals2 = np.append(vals2, [color], axis=0)


# counting number of covered cells
grays = 0
for item in real_coverage:
    if real_coverage[item] == 1:
        grays += 1

print("Real coverage is %{}".format(int(grays/len(real_coverage) * 100)))
# print("Real coverage is {} counting blocks.".format(round(grays/(m * n), 2)))


# we had ommited gray from vals matris at first (line 31-35)
# now we have to add it for animated plot as we need it
vals = np.append(vals, [[0.5, 0.5, 0.5, 1]], axis=0)

# animated plot representing different cameras each time
cmp4 = ListedColormap(vals)
fig, ax = plt.subplots()
ax.pcolormesh(z_plotdata[0], cmap=cmp4)

import matplotlib.animation as animation

def animate(i):
    ax.pcolormesh(z_plotdata[i], cmap=cmp4)  # update the data.
    return ax,

ani = animation.FuncAnimation(
    fig, animate, frames=range(k), interval=300, save_count=k-1, blit=True)


# Static plot representing overlaps
cmp4_2 = ListedColormap(vals2)
fig1, ax1 = plt.subplots()
ax1.pcolormesh(z2, cmap=cmp4_2)


# showing both/all of the plots
plt.show()