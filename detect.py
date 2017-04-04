"""detect.py

Given a set of images, attempts to detect objects with a cascade file in the default output path of train.py.
Optionally, you can specify the path to another cascade file.

Usage:
    detect.py  [--cascade=<file>] [--recursive] <images>...

Options:
    --help, -h                   Print this help message.
    --cascade=<file>, -c <file>  [Default: classifier/cascade.xml] The path to a classifier's cascade.xml file
                                 trained using opencv_traincascade.
    --recursive, -r              Interprets <images> as paths, attempts to detect objects for each file in them.
"""
import cv2
import docopt
import os

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    
    cascade = cv2.CascadeClassifier(os.path.abspath(args["--cascade"]))
    filenames = args["<images>"]
    if args["--recursive"]:
        filenames = []
        for path in args["<images>"]:
            filenames += list(os.path.join(path, f) for f  in os.listdir(path))
    
    for filename in filenames:
        img = cv2.imread(filename)
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            print("Error with {}".format(filename))
        else:
            objects = cascade.detectMultiScale(gray)
            for (x,y,w,h) in objects:
                cv2.rectangle(img,
                              (x, y),
                              (x + w, y + h),
                              (255, 0, 0),
                              2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
            cv2.imshow('img', img)
            cv2.waitKey(0)
            cv2.destroyWindow('img')