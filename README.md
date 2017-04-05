## What is this?

A set of Python scripts for easily creating a Haar cascade object detector using OpenCV.
OpenCV has some tool for this already, which these scripts complement.
For example, there is a script for automatically downloading images from Google's custom search engine API.
You can specify many options using these scripts, however for advanced use most of the scripts support the
`--dry-run` option so you can see how the related OpenCV tool would be used as a starting point.

The emphasis of this set of scripts is on getting something that just works without having to think about a lot of
different options. However the scripts do support specifying many options. Check out the `--help` messages
for more info.

## Setup

I have tested this with the following versions, however I suspect that other versions of Python or OpenCV
are readily supported. If you get these to work with other versions, be sure to open a PR!

Requirements:

    * Python 2.7
    * OpenCV 3.2.0
    * A Google Custom Search Engine API key and engine id for `get_images.py`.

Detailed instructions:

Get the above software. OpenCV's recommended installation method is to add it's `.pyc` file directly to your
Python site packages directory (something like `python\Lib\site-packages`).

To use `get_images.py` you'll also need a [Google CSE](https://developers.google.com/custom-search/) engine id and
API key. Add your secrets to a new file in this directory called `secrets.py`:

```python
# secrets.py
apikey='Your API key here'
searchid='Your custom search engine id here'
```

Next adjust `settings.py` to your preference. At a minimum you should set `OPENCV_BIN_DIR` so that it points to
the directory where the opencv applications are (e.g. `opencv_annotation`, `opencv_traincascade`). On my installation
these are found in `opencv\build\x64\vc14\bin`. The other default values will create directories in the current
working directory.

Run `pip install -r requirements.txt` to get the required Python packages.
I recommend using a [virtual environment](https://pypi.python.org/pypi/virtualenv).

## Usage

All commands support a `--help` option and most have a `--dry-run` option as well.
Below I outline the basic usage, but see the help messages for more details.

## `get_images.py`

Get candidate images for your positive training set and optionally the negative training set from Google CSE.
If you already have images, you can put them in the NEGATIVE_IMG_DIR or POSITIVE_IMG_DIR and skip this step.

```bash
>> python get_images.py faces --negative-term=cats --negative-term=lemons
```

## `annotate.py`

Use this next to create positive and negative annotation files. The negative annotations are created automatically:

```bash
>> python annotate.py --negative
```

Positive annotation is interactive.
First you'll identify whether the images contain any of the target object.
Follow the prompts on the shell as the images are displayed to you 1-by-1.
Press "y" or "n" to indicate that an image either contains any of the object of interest or not and move it to the
appropriate directory.

Then `opencv_annotation` will be called on the POSITIVE_IMG_DIR.
Click on the images to create a bounding box for the objects to train on. Then press "c" to confirm it, and "n" to
move on to the next image. Pressing "d" clears selections. The escape key exits this stage, but you can start it
again by calling `annotate.py`.

```bash
>> python annotate.py
```

## `create_samples.py`

This step prepares the binary data from the positive samples needed for `opencv_traincascade`.

```bash
>> python create_samples.py
```

## `train.py`

This step trains the classifier. It can take a long time, depending on the number of samples and stages!
The default value is 5 stages. If you wish to add more, then it will pick back up from the latest stage you stopped
at, so you can always add more stages later if needed.

```bash
>> python train.py
```

If the number of images is too low or some images are too similar, then the classifier may fail early. In that case,
run `train.py` with the `--dry-run` option, copy the command that would have been run, and specify that a fewer
number of positive images are used in training by changing the `-numPos` option.

```bash
>> python train.py -d

Would run Z:\foo\bar\opencv_traincascade -data classifier -vec vec.bin -bg negatives.txt -numPos 68 -numNeg 140 -w 24 -h 24 -numStages 5

>> Z:\foo\bar\opencv_traincascade -data classifier -vec vec.bin -bg negatives.txt -numPos 40 -numNeg 140 -w 24 -h 24 -numStages 5
```

## `detect.py`

Use the trained classifer to detect objects of interest in a file or directory. For a file:

```bash
>> python detect.py test_set/10_Best_ideas_about_Baby_Faces_on_Pinterest_Beautiful_babies_.jpg
```

Or for a directory:

```bash
>> python detect.py -r test_set
```

Example trained cascade and a test set are included, however the cascade is not very good probably due to a low number
of example images used and the small number of stages.
