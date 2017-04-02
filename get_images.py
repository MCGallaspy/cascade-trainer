import os
import re
import requests

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
    get_images('lemon tree', settings.UNSORTED_IMG_DIR)
    for term in ['motorcycles', 'faces', 'owls', 'city']:
        get_images(term, settings.NEGATIVE_IMG_DIR)
