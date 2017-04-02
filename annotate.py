import cv2
import os
import shutil
import subprocess

# Project imports
import settings
import sys

def normalize(dir, width):
    for filename in os.listdir(dir):
        src = os.path.abspath(os.path.join(dir, filename))
        img = cv2.imread(src, cv2.IMREAD_COLOR)
        if img is None:
            continue
        imgheight, imgwidth, channels = img.shape
        scale = float(width) / imgwidth
        size = (width,  int(scale * imgheight))
        newimg = cv2.resize(img, size)
        cv2.imwrite(src, newimg)

def sort_images(dir, pos_dest, neg_dest):
    try:
        os.makedirs(os.path.abspath(pos_dest))
    except os.error:
        pass
    try:
        os.makedirs(os.path.abspath(neg_dest))
    except os.error:
        pass
    
    for filename in os.listdir(dir):
        src = os.path.abspath(os.path.join(dir, filename))
        img = cv2.imread(src, cv2.IMREAD_COLOR)
        if img is None:
            print("Error with " + filename)
            continue
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.imshow('img', img)
        while True:
            c = cv2.waitKey(0)
            c = chr(c).lower()
            if c == 'n' or not c:
                shutil.move(src, os.path.join(neg_dest, filename))
                break
            elif c == 'y':
                shutil.move(src, os.path.join(pos_dest, filename))
                break
            else:
                print("Invalid option {}, choose y or n.".format(c))
        cv2.destroyWindow('img')

def annotate(dir):
    cmd = [
        os.path.join(settings.OPENCV_BIN_DIR, 'opencv_annotation'),
        '--annotations=' + os.path.abspath('annotations.txt'),
        '--images=' + os.path.abspath(dir),
    ]
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    normalize(settings.UNSORTED_IMG_DIR, 400)
    sort_images(settings.UNSORTED_IMG_DIR, settings.POSITIVE_IMG_DIR, settings.NEGATIVE_IMG_DIR)
    annotate(settings.POSITIVE_IMG_DIR)
