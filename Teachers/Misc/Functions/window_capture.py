from PyQt5.QtGui import QImage, QPixmap
import win32gui
import win32ui
import numpy as np
from mss import mss
from PIL import Image, ImageFilter
from win32api import GetSystemMetrics


def set_pixel(img, w, x, y, rgb=(0, 0, 0)):
    pos = (x*w + y)*3
    if pos >= len(img):
        return img
    img[pos:pos+3] = rgb
    return img


def add_mouse(img, w):
    cursor, (cx, cy) = get_cursor()
    cursor_mean = cursor.mean(-1)
    where = np.where(cursor_mean > 0)
    for x, y in zip(where[0], where[1]):
        rgb = [x for x in cursor[x, y]]
        img = set_pixel(img, w, x+cy-9, y+cx-9, rgb=rgb)
    return img


def get_cursor():
    _, hcursor, (cx, cy) = win32gui.GetCursorInfo()
    hwin = win32gui.GetDesktopWindow()
    hwindc = win32gui.GetWindowDC(hwin)
    hdc = win32ui.CreateDCFromHandle(hwindc)
    
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 36, 36)

    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), hcursor)

    bmpinfo = hbmp.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)

    im = np.array(Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1))

    win32gui.DestroyIcon(hcursor)
    win32gui.DeleteObject(hbmp.GetHandle())
    hdc.DeleteDC()
    
    return im, (cx, cy)

def window_capture():
    with mss() as sct:
        monitor = sct.monitors[1]
        img = bytearray(sct.grab(monitor).rgb)
        img = add_mouse(img, monitor['width'])
        return img

def convert_bytearray_to_QPixmap(img):
    w, h = GetSystemMetrics(0), GetSystemMetrics(1)
    qimg = QImage(img, w, h, QImage.Format_RGB888)
    return QPixmap(qimg)

def convert_bytearray_to_pil_image(img):
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
    img = np.array(img)
    img = Image.frombytes("RGB", (width, height), img, "raw")
    return img

def convert_pil_image_to_QPixmap(img):
    data = img.tobytes("raw", "RGB")
    qImg = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)
