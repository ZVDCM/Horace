from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from mss import mss
from PIL import Image
from win32api import GetSystemMetrics
import pyautogui


def screenshot():
    img = pyautogui.screenshot()
    img = np.array(img)
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
    img = Image.frombytes("RGB", (width, height), img, "raw")
    img = img.resize((500, 500), Image.LANCZOS)
    return img


def convert_pil_image_to_QPixmap(img):
    data = img.tobytes("raw", "RGB")
    qImg = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

