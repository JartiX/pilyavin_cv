import cv2

# cv2.namedWindow("Frame", cv2.WINDOW_GUI_NORMAL)
capt = cv2.VideoCapture('pictures/pictures.avi')

if not capt.isOpened():
    print("ERRROR")

cnt = 0
while capt.isOpened():
    ret, image = capt.read()
    if not ret:
        break
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 12:
        continue
    if (cv2.arcLength(contours[7], True) - cv2.arcLength(contours[7], False) == 1):
        cnt += 1
        # cv2.putText(image, f"Изображение по счёту {i}, найдено {cnt} раз", (10, 30), cv2.FONT_HERSHEY_COMPLEX,1, (0,0,255), 2)
        # cv2.imshow("Frame", image)
        # cv2.waitKey(0)
        
print(cnt)
# Ответ 69
