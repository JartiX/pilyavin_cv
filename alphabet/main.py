import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from collections import defaultdict
from pathlib import Path

# A B 8 0 1 W X * - / P D
# + + + + + + + + + + + +

def filling_factor(arr):
    return np.sum(arr)/arr.size

def count_holes(region):
    labeled = label(np.logical_not(region.image))
    regions = regionprops(labeled)
    holes = 0
    for region in regions:
        coords = np.where(labeled == region.label)
        bound = True
        for y, x in zip(*coords):
            if y == 0 or x == 0 or y == labeled.shape[0] - 1 or x == labeled.shape[1] - 1:
                bound = False
        holes += bound
    return holes

def has_vline(arr, width=1):
    return width <= np.sum(arr.mean(0) == 1)

def recognize(region):
    if filling_factor(region.image) == 1.0:
        return "-"
    else:
        holes = count_holes(region)
        if holes == 2: # 8 or B
            if has_vline(region.image, 3):
                return "B"
            else:
                return "8"
        elif holes == 1: # A, 0, D или P
            ny, nx = (region.centroid_local[0] / region.image.shape[0], 
            region.centroid_local[1] / region.image.shape[1])
            if np.isclose(ny, nx, 0.05): # P 0
                if has_vline(region.image) and (ny < 0.4 or nx < 0.4):
                    return "P"
                else:
                    return "0"
            elif has_vline(region.image): # P D
                if filling_factor(region.image) > 0.53: # D
                    return "D"
                return "P"  
            else: # A 0
                if ny < 0.5 or nx < 0.5:
                    if filling_factor(region.image) > 0.5:
                        return "0"
                return "A"
        else: # 1 W X * /
            if has_vline(region.image): # 1 *
                if filling_factor(region.image) > 0.5:
                    return "*"
                return "1"
            else: # W X * /
                eccentricity = (region.eccentricity)
                framed = region.image
                framed[0, :] = 1
                framed[-1, :] = 1
                framed[:, 0] = 1
                framed[:, -1] = 1
                holes = count_holes(region)
                if eccentricity < 0.4:
                    return "*"
                else:
                    match holes:
                        case 2: return '/'
                        case 4: return "X"
                    if eccentricity > 0.5:
                        return "W"
                    else:
                        return "*"

image = plt.imread("5/symbols.png").mean(2)
image[image > 0] = 1

regions = regionprops(label(image))
symbols = len(regions)

result = defaultdict(lambda: 0)

path = Path(".") / "5/result"
path.mkdir (exist_ok = True)

plt.figure()

for i, region in enumerate(regions):
    print(i)
    symbol = recognize(region)
    plt.clf()
    plt.title(f"{symbol = }")
    plt.imshow(region.image)
    plt.tight_layout()
    plt.savefig(path / f"{i}.png")
    result[symbol] += 1
print(result)
# {'D': 31, 'X': 23, '/': 35, '*': 41, '1': 40, 'A': 35, 'P': 37, '8': 33, '-': 31, 'B': 38, 'W': 26, '0': 30}