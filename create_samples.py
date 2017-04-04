"""create_samples.py

Calls opencv_createsamples with defaults from the output of annotations.txt.
You can optionally specify the values.

Usage:
    create_samples.py [--dry-run] [options]

Options:
    --help, -h                      Print this help message.
    --dry-run, -d                   Prints what it would do instead of executing.

    --positives=<file>, -p <file>   [Default: annotations.txt] The annotations file for positive images.
    --negatives=<file>, -n <file>   [Default: negatives.txt] The annotations file for negative images.
    --output-file=<file, -o <file>  [Default: vec.bin] The samples binary output file.
    --num=<num>, -N <num>           Specify the number of positive bounding boxes to use from the --positives file.
                                    If unspecified, the total number will be automatically determined and used
                                    as a default value.
    --width=<px>, -w <px>           [Default: 24] Width in pixels of the output samples. Used in training step.
    --height=<px>, -H <px>          [Default: 24] Height in pixels of the output samples. Used in training step.
    --show, -s                      Shows each image processed.
"""
import docopt
import os
import subprocess

import settings

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    dry = args["--dry-run"]
    
    if args["--num"] is None:
        args["--num"] = 0
        with open(args["--positives"], "r") as f:
            for line in f:
                args["--num"] += int(line.split(" ")[1])
    
    cmd = [
        os.path.join(settings.OPENCV_BIN_DIR, "opencv_createsamples"),
        "-vec " + os.path.abspath(args["--output-file"]),
        "-info " + os.path.abspath(args["--positives"]),
        "-bg " + os.path.abspath(args["--negatives"]),
        "-num " + str(args["--num"]),
        "-w " + args["--width"],
        "-h " + args["--height"],
        "-show" if args["--show"] else "",
    ]
    if dry:
        print("Would run {}".format(" ".join(cmd)))
    else:
        subprocess.call(" ".join(cmd), shell=True)