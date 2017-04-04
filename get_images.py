"""get_images.py

Searches for images using google custom search engine api.
To search for terms with whitespace, surround the term "with quotes".
Results from terms specified with the --negative-term option will be
added to the negative images directory.

Usage:
    get_images.py <terms>... [--negative-term=<term>]... [--count=<count>] [--dry-run]

Options:
    --help, -h                         Print this help message.
    --negative-term=<term>, -n <term>  Results of searches for this term will be added to the negative sample directory.
    --count=<count>, -c <count>        [default: 100] For each term, get <count> number of images.
    --dry-run, -d                      Prints what it would do instead of executing.
"""
import docopt
import os
import re
import requests
import sys

from os.path import join
from pprint import pprint
from googleapiclient.discovery import build

# Project imports
import secrets
import settings

def get_images(term, dest, num=100):
    total = 0
    nonalnum_expr = re.compile(r"[^\w\d]+")
    try:
        os.makedirs(dest)
    except os.error:
        pass

    service = build("customsearch", "v1", developerKey=secrets.apikey)

    while total < num:
        res = service.cse().list(
          q=term,
          cx=secrets.searchid,
          searchType='image',
          num=10,
          start=total+1,
        ).execute()

        total += len(res['items'])
        
        for item in res['items']:
            resp = requests.get(item['link'])
            if resp.status_code == requests.codes.ok:
                cleaned_title = nonalnum_expr.sub("_", item['title']) + '.jpg'
                filename = join(dest, cleaned_title)
                with open(filename, 'wb') as f:
                    f.write(resp.content)

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    count = int(args["--count"])
    dry_run = args["--dry-run"]
    for term in args["<terms>"]:
        if dry_run:
            print("Would search google for {} images with positive term {}".format(count, term))
        else:
            get_images(term, settings.UNSORTED_IMG_DIR, num=count)
    for term in args["--negative-term"]:
        if dry_run:
            print("Would search google for {} images with negative term {}".format(count, term))
        else:
            get_images(term, settings.NEGATIVE_IMG_DIR, num=count)
