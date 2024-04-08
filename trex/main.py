import mss
import numpy as np
import cv2
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
import time
import keyboard

sct = mss.mss()
sct_mon = sct.monitors[0]

# Эти параметры нужно настроить как на скринах trex/Templates

# Корды бокса перед дино
top = 570
left = 390
width = 60
height = 55

# Корректировка для duck дино
dino = 32

# Корректировка высоты и ширины высоких кактусов
height_cactus = 47
width_cactus = 30
big_cactus_top = 10

# Параметры тройного высокого кактуса
big_cactus_left = 120

# Параметры 1-2 высокого кактуса
big_12cactus_left = 50

# Параметры мини кактуса
mini_cactus_top = 20
mini_cactus_left = 70
mini_cactus_width = 40
mini_cactus_height = 20



def get_screen_by_coords(coord):
    screen = sct.grab(sct_mon)
    screen = Image.frombytes("RGB", screen.size, screen.bgra, "raw", "BGRX")
    draw = ImageDraw.Draw(im=screen, mode=screen.mode)
    outline = ImageColor.getrgb('green')
    box_xy = (
        (coord['left'], coord['top'], ),
        ((coord['left'] + coord['width']), 
        (coord['top'] + coord['height'])),
    )
    draw.rectangle(xy=box_xy, outline=outline)

    screen.save(f'trex/screens/screen_{int(time.time())}.png')


def get_screen(m=sct_mon):
    screen = sct.grab(m)
    screen = np.array(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    return screen

def trex():
    while True:
        if keyboard.is_pressed('space'):
            break
    start_time = time.time()
    while True:
        current_time = time.time()
        score = (current_time - start_time) * 10
        if score < 1000:
            offset = int((score // 100) * 8)
        else:
            offset = int(min((score // 100) * 10, 130))
        coords = {'top': top, 'left': left+offset, 'width': width, 'height': height}
        scrn = get_screen(coords)
        jump = round(np.mean(cv2.Canny(scrn, threshold1=100, threshold2=200)), 4)
        if jump != 0:
            print(score, offset, jump)
            coords_dino = {'top': top+dino, 'left': left+offset, 'width': width, 'height': height-dino}
            scr = get_screen(coords_dino)
            if not np.mean(cv2.Canny(scr, threshold1=100, threshold2=200)):
                keyboard.press('down')
                continue

            coords_cactus = {'top': top-big_cactus_top, 'left': left+big_cactus_left+offset, 'width': width+width_cactus, 'height': height-height_cactus}
            check_big_cuctus = get_screen(coords_cactus) 
            if np.mean(cv2.Canny(check_big_cuctus, threshold1=100, threshold2=200)):
                print("TRIPPLE BIG CUCTUS DETECTED")
                keyboard.release('down')
                keyboard.press('space') 
                if score < 115:
                    time.sleep(0.33)
                elif score < 170:
                    time.sleep(0.31)
                elif score < 400:
                    time.sleep (0.28)
                elif score < 600:
                    time.sleep(0.22)
                elif score < 1850:
                    time.sleep(0.19)
                else:
                    time.sleep(0.19)
                keyboard.release('space')
                keyboard.press('down')
                continue

            coords_cactus = {'top': top-big_cactus_top, 'left': left+big_12cactus_left+offset, 'width': width+width_cactus, 'height': height-height_cactus}
            check_12big_cuctus = get_screen(coords_cactus) 
            if np.mean(cv2.Canny(check_12big_cuctus, threshold1=100, threshold2=200)):
                print("1-2BIG CUCTUS DETECTED")
                keyboard.release('down')
                keyboard.press('space') 
                if score < 115:
                    time.sleep(0.25)
                elif score < 170:
                    time.sleep(0.24)
                elif score < 400:
                    time.sleep (0.23)
                elif score < 900:
                    time.sleep(0.16)
                else:
                    time.sleep(0.15)
                keyboard.release('space')
                keyboard.press('down')
                continue

            
            coord_mini_cuctus = {'top': top+mini_cactus_top, 'left': left+mini_cactus_left+offset, 'width': width-mini_cactus_width, 'height': height-mini_cactus_height}
            check_mini_cuctus = get_screen(coord_mini_cuctus) 
            if not np.mean(cv2.Canny(check_mini_cuctus, threshold1=100, threshold2=200)):
                print("MINI CUCTUS DETECTED")
                keyboard.release('down')
                keyboard.press('space') 
                if score < 115:
                    time.sleep(0.18)
                elif score < 170:
                    time.sleep(0.17)
                elif score < 400:
                    time.sleep (0.16)
                elif score < 900:
                    time.sleep(0.15)
                else: 
                    time.sleep(0.14)
                keyboard.release('space')
                keyboard.press('down')
                continue

            keyboard.release('down')
            keyboard.press('space')
            if score < 115:
                time.sleep(0.234)
            elif score < 170:
                time.sleep(0.215)
            elif score < 400:
                time.sleep (0.196)
            elif score < 600:
                time.sleep(0.15)
            elif score < 1200:
                time.sleep(0.14)
            elif score < 1300:
                time.sleep(0.145)
            elif score < 1400:
                time.sleep(0.14)
            elif score < 1850:
                time.sleep(0.15)
            else:
                time.sleep(0.15)
            keyboard.release('space')
            keyboard.press('down')


if __name__ == "__main__":
    trex()

    # coords = {'top': top, 'left': left, 'width': width, 'height': height}
    # coords_dino = {'top': top+dino, 'left': left, 'width': width, 'height': height-dino}
    # coords_12big_cactus = {'top': top-big_cactus_top, 'left': left-big_12cactus_left, 'width': width+width_cactus, 'height': height-height_cactus}
    # coords_3big_cactus = {'top': top-big_cactus_top, 'left': left-big_cactus_left, 'width': width+width_cactus, 'height': height-height_cactus}
    # coord_mini_cuctus = {'top': top+mini_cactus_top, 'left': left+mini_cactus_left, 'width': width-mini_cactus_width, 'height': height-mini_cactus_height}
    # get_screen_by_coords(coord_mini_cuctus)