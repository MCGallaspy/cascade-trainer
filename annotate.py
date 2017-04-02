# Project imports
import settings
import sys

def annotate():
    if settings.OPENCV_BIN_DIR:
        sys.path.insert(0, settings.OPENCV_BIN_DIR)
    
if __name__ == "__main__":
    annotate()