from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from PIL import Image
import ctypes
import pyautogui


def screenshot():
    img = pyautogui.screenshot()
    img = np.array(img)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    img = Image.frombytes("RGB", (w, h), img, "raw")
    img = img.resize((400, 225), Image.LANCZOS)
    return img

def rdc_screenshot():
    img = pyautogui.screenshot()
    img = np.array(img)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    img = Image.frombytes("RGB", (w, h), img, "raw")
    img = img.resize((1280, 720), Image.LANCZOS)
    return img

def convert_pil_image_to_QPixmap(img):
    data = img.tobytes("raw", "RGB")
    qImg = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

