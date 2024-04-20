import cv2
import matplotlib.pyplot as plt
from collections import defaultdict

image = cv2.imread("figures_and_colors/balls_and_rects.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

colors_rect = defaultdict(lambda: 0)
colors_circle = defaultdict(lambda: 0)

(num_of_labels, _, stats, _) = cv2.connectedComponentsWithStats(gray, 4, cv2.CV_32S)

for i in range(1, num_of_labels):
        x, y, w, h = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        mini = hsv_image[y:y+h, x:x+w]  
        key = mini[h//2, w//2, 0]

        if(area == w*h):
            colors_rect[key] += 1     
        else:
            colors_circle [key] += 1

print(f"Circles: {colors_circle}")
print(f"Rectangles: {colors_rect}")   
print(f"Number of circles: {sum(colors_circle.values())}") 
print(f"Number of rectangles: {sum(colors_rect.values())}") 

plt.imshow(hsv_image)
plt.show()