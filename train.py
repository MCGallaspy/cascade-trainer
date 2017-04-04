"""train.py

Calls opencv_traincascade with the default values from create_samples.py.
You can optionally specify the values.
The number of stages in the classifier can be specified as the argument.
If the number of stages is omitted, it defaults to 5.

Usage:
    train.py [--dry-run] [options]
    train.py <stages> [--dry-run] [options]

Options:
    --help, -h                        Print this help message.
    --dry-run, -d                     Prints what it would do instead of executing.
    
    --output-path=<path>, -o <path>   [Default: classifier] The path where the classifier output files will go. It will be created if it doesn't exist
    --vector=<file>, -V <file>        [Default: vec.bin] The binary output of opencv_createsamples
    --positives=<file>, -p <file>     [Default: annotations.txt] The annotations file for positive images.
    --negatives=<file>, -n <file>     [Default: negatives.txt] The annotations file for negative images.
    --width=<px>, -w <px>             [Default: 24] Width in pixels of the output samples from create_samples.py.
    --height=<px>, -H <px>            [Default: 24] Height in pixels of the output samples from create_samples.py.
"""
import docopt
import os
import subprocess

import settings

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    dry = args["--dry-run"]
    
    pos = 0
    with open(args["--positives"], "r") as f:
        pos = len(list(f))
    neg = 0
    with open(args["--negatives"], "r") as f:
        neg = len(list(f))
    
    if args["<stages>"] is None:
        args["<stages>"] = "5"
    
    cmd = [
        os.path.join(settings.OPENCV_BIN_DIR, "opencv_traincascade"),
        "-data " + os.path.abspath(args["--output-path"]),
        "-vec " + os.path.abspath(args["--vector"]),
        "-bg " + os.path.abspath(args["--negatives"]),
        "-numPos " + str(pos),
        "-numNeg " + str(neg),
        "-w " + args["--width"],
        "-h " + args["--height"],
        "-numStages "+ args["<stages>"],
    ]
    if dry:
        print("Would run {}".format(" ".join(cmd)))
    else:
        try:
            os.makedirs(os.path.abspath(args["--output-path"]))
        except os.error:
            pass
        subprocess.call(" ".join(cmd), shell=True)