import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

def mini_obj(object):
    indices = np.argwhere(object)
    min_indices = indices.min(axis=0)
    max_indices = indices.max(axis=0)
    trimmed_obj = object[min_indices[0]:max_indices[0]+1, min_indices[1]:max_indices[1]+1]

    return trimmed_obj

img = np.load("figures/ps.npy.txt")
labeled_img = label(img)
number_of_objs = labeled_img.max()

unique_structures = []

for i in range(1, number_of_objs+1):
    curr_obj = mini_obj(labeled_img == i)
    k = False
    for index, j in enumerate(unique_structures):
        if curr_obj.shape[0] != j[0].shape[0] or curr_obj.shape[1] != j[0].shape[1]:
            continue 
        if np.all(j[0] == curr_obj):
            k = True
            unique_structures[index][1] += 1
            break
    if not k:
        unique_structures.append([curr_obj, 1])

print(f'Number of objects: {number_of_objs}')
print(f'Types of objects: {len(unique_structures)}')
print(*[f'Object {index+1}: {x[1]} times' for index,x in enumerate(unique_structures)], sep='\n')

plt.imshow(labeled_img)
plt.show()
