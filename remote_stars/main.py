import numpy as np
import matplotlib.pyplot as plt
import socket


host = "84.237.21.36"
port = 5152


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data


def check(B, y, x):
    if not 0 <= x < B.shape[0]:
        return False
    if not 0 <= y < B.shape[1]:
        return False
    if B[y, x] != 0:
        return True
    return False


def neighbors4(B, y, x):
    left = y, x-1
    right = y, x+1
    top = y-1, x
    bottom = y+1, x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top = None
    if not check(B, *right):
        right = None
    if not check(B, *bottom):
        bottom = None
    return left, right, top, bottom


def find_xtr(array):
    xtr_list = []
    for y in range(array.shape[0]):
        for x in range(array.shape[1]):
            nbs = neighbors4(array, y, x)
            cnt = 0
            for n in nbs:
                if n is not None:
                    if array[y, x] > array[n]:
                        cnt += 1
            if cnt == len(nbs):
                xtr_list.append((y, x))

    return xtr_list


def find_dist(dot1: tuple, dot2: tuple) -> int:
    return np.sqrt((dot2[0]-dot1[0])**2 + (dot1[1]-dot2[1])**2)


if __name__ == "__main__":
    images = []
    dist = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        for i in range(10):
            sock.send(b"get")
            bts = recvall(sock, 40002)
            im = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0],
                                                                    bts[1])
            dots = find_xtr(im)
            if len(dots) == 2:
                dist = find_dist(dots[0], dots[1])
                images.append((im, dist))
            else:
                images.append((im, None))

            sock.send(f"{dist:.1f}".encode())
            print(sock.recv(20))

    with open("data.txt", "w") as f:
        for k, img in enumerate(images):
            plt.subplot(2, 5, k+1)

            if img[1] is not None:
                plt.title(f"Dist: {img[1]:.1f}")
                f.write(f"Изображение: {k+1}, расстояние: {img[1]:.1f}\n")
                print(f"Изображение: {k+1}, расстояние: {img[1]:.1f} ")
            else:
                plt.title(f"Dist: None")
                f.write(f"Изображение: {k+1}, расстояние: None\n")
                print(f"Изображение: {k+1}, расстояние: None ")

            plt.imshow(img[0])
    plt.show()
