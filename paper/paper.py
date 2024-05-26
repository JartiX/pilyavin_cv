import cv2
import zmq
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

port = 5055
ip = "192.168.0.113"

socket.connect(f"tcp://{ip}:{port}")


camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_EXPOSURE, -6)

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

# lower = 13
# upper = 6
lower = 94
upper = 46


def lower_update(value):
    global lower
    lower = value

def upper_update(value):
    global upper
    upper = value

cv2.createTrackbar("Lower", "Mask", lower, 255, lower_update)
cv2.createTrackbar("Upper", "Mask", upper, 255, upper_update)

while camera.isOpened():
    # ret, image = camera.read()

    bts = socket.recv()
    arr = np.frombuffer(bts, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    key = cv2.waitKey(10)

    if key == ord("p"):
        cv2.imwrite("out.png", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    mask = cv2.Canny(gray, lower, upper)

    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, cnts, -1, (0,0,0), 1)
    if len(cnts) == 0:
        continue

    rect = cv2.minAreaRect(cnts[0])
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    cv2.drawContours(image, [box], 0, (255, 255, 0), 2)

    eps = 0.006 * cv2.arcLength(cnts[0], True)
    approx =  cv2.approxPolyDP(cnts[0], eps, True)
    for p in range(len(approx)):
        cv2.circle(image, tuple(*approx[p]), 4, (0, 255, 0), 2*p)
    approx = approx.astype(np.float32)

    pts_fg = np.float32( [ [image.shape[1], 0], [0,0], [0, image.shape[0]],[image.shape[1], image.shape[0]]] )

    M = cv2.getPerspectiveTransform(approx, pts_fg)
    aff_fg = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))

    pos = np.where(aff_fg > 0)
    temp = np.zeros_like(image)
    temp[pos] = aff_fg[pos]

    cv2.putText(temp, "HUTAO", (60, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 3)
    cv2.putText(temp, "THE BEST", (60, 120), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 3)

    M = cv2.getPerspectiveTransform(pts_fg, approx)
    aff_fg = cv2.warpPerspective(temp, M, (image.shape[1], image.shape[0]))

    pos = np.where(aff_fg > 0)
    image[pos] = aff_fg[pos]

    if key == ord('q'):
        break

    cv2.imshow("Image", image)
    cv2.imshow("Mask", mask)


camera.release()
cv2.destroyAllWindows()