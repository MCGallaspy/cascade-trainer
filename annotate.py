"""annotate.py

Interactively sort and then annotate the images in the directory specified by the setting UNSORTED_IMG_DIR.
Images will be rescaled to a width of 400px (specifiable with the --width option).
Then each image will be displayed from the UNSORTED_IMG_DIR. Press "y" or "n" to sort it.
Pressing "y" sends it the the directory specified by the setting POSITIVE_IMG_DIR.
Pressing "n" sends it the the directory specified by the setting NEGATIVE_IMG_DIR.

After sorting, this script will call opencv_annotation on the POSITIVE_IMG_DIR.

An alternate usage creates an annotation for the NEGATIVE_IMG_DIR.

Usage:
    annotate.py [--output=<file>] [--width=<px>] [--dry-run] [--quiet]
    annotate.py --negative [--neg-output=<file>] [--dry-run]

Options:
    --help, -h                      Print this help message.
    --width=<px>, -w <px>           [Default: 400] Specify the width in pixels to rescale each image to.
    --output=<file>, -o <file>      [Default: annotations.txt] The output file to send the opencv annotations to.
    --dry-run, -d                   Prints what it would do instead of executing.
    --quiet, -q                     If specified, suppresses output.
    --negative, -N                  Create negative annotation file.                    
    --neg-output=<file>, -n <file>  [Default: negatives.txt] Creates a negative annotation file, overwriting <file>.
"""
import docopt
import cv2
import os
import shutil
import subprocess

# Project imports
import settings
import sys

def normalize(dir, width, dry=False):
    if dry:
        print("Would normalize images in {} to {}px width".format(dir, width))
        return
    for filename in os.listdir(dir):
        src = os.path.abspath(os.path.join(dir, filename))
        img = cv2.imread(src, cv2.IMREAD_COLOR)
        if img is None:
            continue
        imgheight, imgwidth, channels = img.shape
        scale = float(width) / imgwidth
        size = (int(scale * imgheight), width)
        newimg = cv2.resize(img, size)
        cv2.imwrite(src, newimg)

def sort_images(dir, pos_dest, neg_dest, dry=False):
    if dry:
        print("Would sort images in {} to pos. dir {} and neg. dir {}".format(dir, pos_dest, neg_dest))
        return
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

def annotate(dir, output_file, dry=False):
    cmd = [
        os.path.join(settings.OPENCV_BIN_DIR, 'opencv_annotation'),
        '--annotations=' + os.path.abspath(output_file),
        '--images=' + dir,
    ]
    if dry:
        print("Would call subprocess '{}'".format(" ".join(cmd)))
    else:
        subprocess.call(cmd, shell=True)

def negative_annotate(dir, output_file, dry=False):
    if dry:
        print("Would create negative annotation at {} for {}".format(output_file, dir))
        return
    filenames = [os.path.abspath(os.path.join(dir, filename)) for filename in os.listdir(dir)]
    with open(output_file, "w") as f:
        f.write("\n".join(filenames))

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    
    if args["--negative"]:
        negative_annotate(settings.NEGATIVE_IMG_DIR, args["--neg-output"], args["--dry-run"])
        sys.exit(0)
    
    output_file = args["--output"]
    dry = args["--dry-run"]
    quiet = args["--quiet"]
    width = int(args["--width"])
    if not quiet:
        print ("Normalizing to {}px.".format(width))
    normalize(settings.UNSORTED_IMG_DIR, width, dry)
    if not quiet:
        print("Sorting images.")
    sort_images(settings.UNSORTED_IMG_DIR, settings.POSITIVE_IMG_DIR, settings.NEGATIVE_IMG_DIR, dry)
    if not quiet:
        print("Calling opencv_annotation.")
    annotate(settings.POSITIVE_IMG_DIR, output_file, dry)
