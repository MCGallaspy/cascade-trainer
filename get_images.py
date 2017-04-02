import os
import re
import requests

from os.path import join
from pprint import pprint
from googleapiclient.discovery import build

# Project imports
import secrets

def get_images(term, dest, num=40):
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
          start=total,
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
    get_images('lemon tree', 'unsorted_images')
    for term in ['motorcycles', 'faces', 'owls', 'city']:
        get_images(term, 'neg_images')
