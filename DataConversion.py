# -*- coding: utf-8 -*-

import random
import math
import json
import matplotlib
from PIL import Image 
import subprocess, os
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


try:
    camera_installation_cost = int(input('Enter cost C [142]: ') or 142)
except ValueError:
    camera_installation_cost = 142

try:
    coverage_ratio = float(input('Enter coverage CR [0.9]: ') or 0.9)
except ValueError:
    coverage_ratio = 0.9


try:
    d = int(input('Enter distance [20]: ') or 20)
except ValueError:
    d = 20

try:
    FovDegree  = int(input('Enter AOV [120]: ') or 120)
except ValueError:
    FovDegree  = 120



def get_coords_from_pictre(filename: str):
    image = Image.open(filename).convert('RGB')
    pixels = np.asarray(image)
    indigo = [63, 72, 204]
    red = [237, 28, 36]
    orange = [255, 127, 39]
    yellow = [255, 242, 0]
    black = [0, 0, 0]
    # white = [255, 255, 255]
    # Find coordinates of all pixels below threshold
    blocks = np.column_stack(np.where(np.all(pixels==black,axis=2))).tolist()
    p3 = np.column_stack(np.where(np.all(pixels==yellow,axis=2))).tolist()
    p2 = np.column_stack(np.where(np.all(pixels==orange,axis=2))).tolist()
    p1 = np.column_stack(np.where(np.all(pixels==red,axis=2))).tolist()
    cam = np.column_stack(np.where(np.all(pixels==indigo,axis=2))).tolist()
    size = pixels.shape
    return [blocks, p3, p2, p1, cam, size]

phase = int(input('Please enter number of phases [defaut= 4]: ') or 4)


try:
    picpath_1 = input(f'Phase 1\tPicture name [1.png]: ')
except ValueError:
    picpath_1 = '1.png'
if picpath_1 == '':
    picpath_1 = '1.png'
if not picpath_1.endswith('.png'):
    picpath_1 += '.png'

# m = int(input('Please enter height m [defaut= 80]: ') or 80)
# n = int(input('Please enter width n [defaut= 40]: ') or 40)


cells = get_coords_from_pictre(picpath_1)
m, n, _ = cells[5]


data_for_opl = [[[0 for _ in range(m*n)] for __ in range(phase)] for ___ in range(m*n)]
# print(len(data_for_opl), len(data_for_opl[0]), len(data_for_opl[0][0]))


# Initialize Wjt with empty lists for each phase
Wjt = [[] for _ in range(phase)]

for t in range(1, phase+1):

    try:
        picpath = input(f'Phase {t}\tPicture name [{t}.png]: ') if t > 1 else picpath_1
    except ValueError:
        picpath = f'{t}.png'



    if picpath == '':
        picpath = f'{t}.png'
    if not picpath.endswith('.png'):
        picpath += '.png'


    # paintImage = os.path.join(os.getcwd(), picpath)
    #get the path of paint:
    # paintPath = os.path.splitdrive(os.path.expanduser("~"))[0]+r"\WINDOWS\system32\mspaint.exe"

    #open the file with paint
    # subprocess.Popen([paintPath, paintImage])

    # input(f"Phase {t}\tPress Enter after saving your photo to continue ...")

    cells = get_coords_from_pictre(picpath)
    blocks = cells[0]
    priority_3 = cells[1]
    priority_2 = cells[2]
    priority_1 = cells[3]
    cam_candid_list_1 = cells[4]
    m_picture, n_picture, _ = cells[5]

    print(f'Phase {t}\tCreating coverage')



    fov = FovDegree * (math.pi / 180)

    N = 7
    vals = np.ones((N, 4))

    # black
    vals[0, 0] = 0 #red
    vals[0, 1] = 0 #green
    vals[0, 2] = 0 #blue

    # gray
    vals[1, 0] = 0.5 
    vals[1, 1] = 0.5 
    vals[1, 2] = 0.5

    # red
    vals[2, 0] = 1 
    vals[2, 1] = 0 
    vals[2, 2] = 0 

    # white
    vals[3, 0] = 1 
    vals[3, 1] = 1 
    vals[3, 2] = 1 

    # orange
    vals[4, 0] = 1 
    vals[4, 1] = 127/255 
    vals[4, 2] = 39/255

    # yellow
    vals[5, 0] = 1 
    vals[5, 1] = 242/255 
    vals[5, 2] = 39/255

    # indigo
    vals[6, 0] = 63/255 
    vals[6, 1] = 72/255 
    vals[6, 2] = 204/255

    cmp4 = ListedColormap(vals)

    block_list = []
    # block_list2 = []
    defmat = []
    id_number = 0
    cam_candid_list = []
    cam_candid = {}
    coverage_candid_list = []
    coverage_candid = {}
    id2index = {}
    index2id={}
    # for i in range(int(percent*m*n/100)):
    #     randnum = random.randint(1, m*n)
    #     if randnum not in block_list2: 
    #         block_list2.append(randnum)
    for i in range(m):
        row = []
        for j in range(n):
            id_number += 1
            id2index[id_number] = (i, j)
            index2id[(i, j)]=id_number
            # num = input('enter element (%d,%d):' % (i,j))
            num = 0
            x = i + 1
            y = j + 1
            # weight = random.randint(1, 5)
            
            ncolor = 3
            weight = 0
            is_block = False
            candid = False
            f_cost = 0

            if [i, j] in blocks:
                is_block = True
                block_list.append({'x': x, 'y': y, 'x*': x, 'y*': y, 'r': math.sqrt(x**2 + y**2)})
                ncolor = 0

                # for [i,j] in blocks:
                #     if i+1 <= m-1 and  [i+1,j] not in blocks:
                #         cam_candid_list.append((i+1)*(n-1)+j)
                #     if i-1 >= 0 and [i-1,j] not in blocks:
                #         cam_candid_list.append((i-1)*(n-1)+j)
                #     if j+1 <= n-1 and[i,j+1] not in blocks:
                #         cam_candid_list.append(i*(n-1)+j+1)
                #     if j-1 >= 0 and[i,j-1] not in blocks:
                #         cam_candid_list.append(i*(n-1)+j-1)

            

            if [i, j] in priority_1:
                weight = 3
                ncolor = 2

            elif [i, j] in priority_2:
                weight = 2
                ncolor = 4

            elif [i, j] in priority_3:
                weight = 1
                ncolor = 5

            elif [i, j] in cam_candid_list_1:
                weight = 1
                candid = True
                ncolor = 3
            # if id_number == 65:
            #     print('test')
            if not is_block and weight > 0:
                coverage_candid_list.append(id_number)
                coverage_candid[id_number] = {'num': num, 'weight': weight, #weight,
                        'f': 1, # f_cost,
                    'color': ncolor, 'candid': candid, 'id': id_number,
                    'block': is_block, 'x': x, 'y': y, 'x*': x, 'y*': y,
                    'r': math.sqrt(x**2 + y**2), 'tetha': math.atan(y/x), 'lambda': False}

            side = -1
            if candid:
                if i==0 or (i-1>=0 and [i-1,j] in blocks):
                    side = 0
                elif j==n-1 or (j+1<=n-1 and [i,j+1] in blocks):
                    side = 1
                elif i==m-1 or (i+1<=m-1 and [i+1,j] in blocks):
                    side = 2
                elif j==0 or (j-1>=0 and [i,j-1] in blocks):
                    side = 3
                else:
                    pass

                cam_candid_list.append(id_number)
                cam_candid[id_number] = {'num': num, 'weight': weight, #weight,
                        'f': 1, # f_cost,
                    'color': ncolor, 'candid': candid, 'id': id_number,
                    'block': is_block, 'x': x, 'y': y, 'x*': x, 'y*': y,
                    'r': math.sqrt(x**2 + y**2), 'tetha': math.atan(y/x), 
                    'lambda': False, "side": side}

            # ncolor = 0 
            # tarife tak take selulha
            row.append({'num': num, 'weight': weight, #weight,
                        'f': 1, # f_cost,
                        'color': ncolor, 'candid': candid, 'id': id_number,
                        'block': is_block, 'x': x, 'y': y, 'x*': x, 'y*': y,
                        'r': math.sqrt(x**2 + y**2), 'tetha': math.atan(y/x), 'lambda': False, "side": side})

        defmat.append(row)

    current_phase_weights = []
    for i in range(m):
        for j in range(n):
            current_phase_weights.append(defmat[i][j]['weight'])
    Wjt[t-1] = current_phase_weights

    z_plotdata = {}
    k = -1
    coverage = {}
    coverage['dimensions'] = (m, n)
    coverage['count'] = (0, 0)
    coverage['coverage'] = {}


    for i in range(m):
        for j in range(n):
            if not defmat[i][j]['candid']:
                continue


            # data_for_opl_of_camera_in_phase = [0 for _ in range(m*n)]

            k += 1
            mat = deepcopy(defmat)
            x0 = mat[i][j]['x']
            y0 = mat[i][j]['y']

            grayed = []

            if mat[i][j]['side'] == 0:
                for row in mat:
                    for cell in row:
                        cell['x*'] = -(cell['y'] - y0)
                        cell['y*'] = cell['x'] - x0

                for block in block_list:
                    block['x*'] = -(block['y'] - y0)
                    block['y*'] = block['x'] - x0


            elif mat[i][j]['side'] == 2:
                for row in mat:
                    for cell in row:
                        cell['x*'] = cell['y'] - y0
                        cell['y*'] = -(cell['x'] - x0)

                for block in block_list:
                    block['x*'] = block['y'] - y0
                    block['y*'] = -(block['x'] - x0)
            

            if mat[i][j]['side'] == 3:
                for row in mat:
                    for cell in row:
                        cell['x*'] = cell['x'] - x0
                        cell['y*'] = cell['y'] - y0

                for block in block_list:
                    block['x*'] = block['x'] - x0
                    block['y*'] = block['y'] - y0


            elif mat[i][j]['side'] == 1:
                for row in mat:
                    for cell in row:
                        cell['x*'] = -(cell['x'] - x0)
                        cell['y*'] = -(cell['y'] - y0)

                for block in block_list:
                    block['x*'] = -(block['x'] - x0)
                    block['y*'] = -(block['y'] - y0)


            for row in mat:
                for cell in row:
                    cell['r'] = math.sqrt(cell['x*']**2 + cell['y*']**2)

                    if cell['x*'] != 0:
                        cell['tetha'] = math.atan(cell['y*']/cell['x*'])
                    else:
                        cell['tetha'] = math.pi/2

                    if cell['tetha'] < 0: cell['tetha'] = math.pi + cell['tetha']

            for block in block_list:
                block['r'] = math.sqrt(block['x*']**2 + block['y*']**2)

                if block['x*'] != 0:
                    block['tetha'] = math.atan(block['y*']/block['x*']) 
                else:
                    block['tetha'] = math.pi/2 
                
                if block['tetha'] < 0: block['tetha'] = math.pi + block['tetha']
                tetha2 = math.pi - (135 - block['tetha'])
                diameter = max(math.cos(tetha2), math.sin(tetha2)) * math.sqrt(2)
                block['tetha-max'] = block['tetha'] + (diameter / block['r']) * 0.5
                block['tetha-min'] = block['tetha'] - (diameter / block['r']) * 0.5
                # print('x: {}, y: {}, tetha: {}'.format(block['x'], block['y'], block['tetha']))

            for r, row in enumerate(mat):
                for c, cell in enumerate(row):
                    # cell['color'] = 3
                    clr = cell['color']
                    cell['lambda'] = False
                    if cell['y*'] < 0: continue
                    if not cell['block']:
                        if cell['r'] <= d and (cell['tetha'] >= (math.pi/2 - fov/2)) and (cell['tetha'] <= (math.pi/2 + fov/2)):
                            cell['color'] = 1
                            cell['lambda'] = True
                            
                            for block in block_list:
                                if (block['r'] <= cell['r']) and (block['tetha-max'] >= cell['tetha'] and block['tetha-min'] <= cell['tetha'] and block['y*'] > 0):
                                    cell['color'] = clr
                                    cell['lambda'] = False
                            
                            if cell['lambda']:
                                # print(t-1, (i*n)+(j+1)-1, (r*n)*(c+1)-1)
                                grayed.append(cell['id'])
                                
                                # print(t-1, (i*n)+(j+1)-1, (r*n)+(c+1)-1)
                                # data_for_opl[(i*n)+(j+1)-1][t-1][(r*n)+(c+1)-1] = 1
                                
                                #data_for_opl[t-1][(i*n)+(j+1)][(r*n)*(c+1)] = 1
                    else:
                        cell['color'] = 0
                        cell['lambda'] = False

                    # data_for_opl_of_camera_in_phase[(r*n)+(c+1)-1] = 1 if cell['lambda'] else 0
                    data_for_opl[(i*n)+(j+1)-1][t-1][(r*n)+(c+1)-1] = 1 if cell['lambda'] else 0

            # if (i*n)+(j+1)-1 not in data_for_opl.keys():
            #     data_for_opl[(i*n)+(j+1)-1] = {}

            # data_for_opl[(i*n)+(j+1)-1][t] = data_for_opl_of_camera_in_phase

            mat[i][j]['color'] = 6
            coverage['coverage'][mat[i][j]['id']] = grayed

            z = []
            for ii in range(m):
                z.append([])
                for jj in range(n):
                    z[ii].append(mat[ii][jj]['color'])
            z_plotdata[k] = z



    dmat = {'dimensions': (m, n)}
    dmat['d'] = d
    dmat['fov'] = fov
    # dmat['percent'] = percent
    dmat['cam_candids_ls'] = cam_candid_list
    dmat['cov_candids_ls'] = coverage_candid_list
    dmat['cam_candids'] = cam_candid
    dmat['cov_candids'] = coverage_candid
    dmat['id2index'] = id2index
    dmat['matrix'] = mat


    output = json.dumps(dmat, indent=4)
    with open(f'Phase {t} mat.json', 'w') as wfile:
        wfile.write(output)

    coverage['count'] = len(coverage['coverage'])

    output = json.dumps(coverage, indent=4)
    with open(f'Phase {t} coverage.json', 'w') as wfile:
        wfile.write(output)

    output = json.dumps(block_list, indent=4)
    with open(f'Phase {t} block_list.json', 'w') as wfile:
        wfile.write(output)

    fig, ax = plt.subplots()
    ax.pcolormesh(z_plotdata[0], cmap=cmp4)

    import matplotlib.animation as animation

    def animate(i):
        ax.pcolormesh(z_plotdata[i], cmap=cmp4)  # update the data.
        return ax,


    ani = animation.FuncAnimation(
        fig, animate, frames=range(k+1), interval=300, save_count=k-1, blit=True)

    # from matplotlib.widgets import Slider
    # axcolor = 'lightgoldenrodyellow'
    # ax.margins(x=0)
    # 
    # # adjust the main plot to make room for the sliders
    # plt.subplots_adjust(left=0.25, bottom=0.25)
    # 
    # # Make a horizontal slider to control the frequency.
    # axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    # freq_slider = Slider(
    #     ax = axfreq,
    #     label = 'Candid',
    #     valmin = 1,
    #     valmax = k,
    #     valinit = 1
    # )
    # 
    # # The function to be called anytime a slider's value changes
    # def update(val):
    #     ax.pcolormesh(z_plotdata[int(freq_slider.val)], cmap=cmp4)
    #     fig.canvas.draw_idle()
    # 
    # # register the update function with each slider
    # freq_slider.on_changed(update)
    # Set up formatting for the movie files

    # Writer = animation.writers['ffmpeg']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    # 
    # ani.save('im.mp4', writer=writer)

    # plt.pause(0.001)

    # plt.ion()

    plt.show()

    # import save_params

    # import os


offset = 0
camera_mapping_for_opl = {}
camera_counter = 0
no_candids = []

for cam in range(m * n):
    if sum([sum(data_for_opl[cam][t]) for t in range(phase)]) == 0:
        no_candids.append(cam)
        continue
    camera_mapping_for_opl[camera_counter] = cam + 1  # Adding 1 to the extracted number before assigning
    camera_counter += 1


for no_camera in no_candids[::-1]:
    data_for_opl.pop(no_camera)

filename = f'Wjt.json'
with open(filename, 'w+') as file:
    output = json.dumps(Wjt)
    file.write(output)
print(f'Data saved in {filename}')
    # The rest of your loop continues here

# After the loop, you can use Wjt as needed

filename = f'DataForOPL- camera({len(camera_mapping_for_opl.keys())})-phase({phase})-cell({n*m}).json'
with open(filename, 'w+') as file:
    output = json.dumps(data_for_opl)
    file.write(output)
print(f'Data saved in {filename}')


filename = f'DataForOPL- camera mapping.json'
with open(filename, 'w+') as file:
    output = json.dumps(camera_mapping_for_opl)
    file.write(output)
print(f'Data saved in {filename}')
#import representation

# import opl
    # At the end of each phase, after filling the cam_candid_list or cam_candid dictionary

    # If using the list (assuming cam_candid_list contains unique camera candidate IDs)
num_cam_candid_list = len(cam_candid_list)
print(f"Number of camera candidates in Phase {t} using list: {num_cam_candid_list}")

    # If using the dictionary (assuming cam_candid dictionary keys are unique camera candidate IDs)
num_cam_candid_dict = len(cam_candid)
print(f"Number of camera candidates in Phase {t} using dictionary: {num_cam_candid_dict}")

    # Continue with the rest of your loop or code


# Initialize a set to hold all unique cam_candid IDs from all phases
all_cam_candid_ids_set = set()

for t in range(1, phase+1):
    # Your existing loop code...

    # Option 1: Using the list, update the set with IDs from this phase's list
    all_cam_candid_ids_set.update(cam_candid_list)  # Adds elements, avoiding duplicates

    # Option 2: Using the dictionary, update the set with dictionary keys
    all_cam_candid_ids_set.update(cam_candid.keys())  # Adds keys, avoiding duplicates

    # Continue with the rest of your loop or code...

# Convert the set back to a list to finalize or for further processing (if necessary)
all_cam_candid_ids_list = list(all_cam_candid_ids_set)

# Now, all_cam_candid_ids_list contains all unique camera candidate IDs from all phases
# You can now use this list as needed. For example, to save it to a file:

filename = 'UniqueAllCamCandidIDs.json'
with open(filename, 'w+') as file:
    output = json.dumps(all_cam_candid_ids_list)
    file.write(output)
print(f'All unique camera candidate IDs saved in {filename}')


def list_to_string(lst):
    # Base case: if the item is not a list, return its string representation
    if not isinstance(lst, list):
        return str(lst)
    
    # Recursive case: process each item in the list
    inner_results = [list_to_string(item) for item in lst]
    # Combine the items with spaces, wrap in brackets
    return '[' + ' '.join(inner_results) + ']'

# Example usage


opl_input_dat_file = \
f"""/*********************************************
 * OPL 12.10.0.0 Data
 * Author: Mohadese
 * Creation Date: 28 فروردین 1403 ه‍.ش. at 6:44:13
 *********************************************/



NI = {camera_counter};
NJ = {m*n};
NT = {phase};
C = {camera_installation_cost};

f = [{" ".join(['15' for _ in range(camera_counter)])}];

f_bar = [{" ".join(['10' for _ in range(camera_counter)])}];


CR = [{" ".join([str(coverage_ratio) for _ in range(t)])}];
w = {list_to_string(Wjt)};
y = {list_to_string(data_for_opl)};

"""

with open("opl.dat", "w+", encoding="utf-8") as file:
    file.write(opl_input_dat_file)