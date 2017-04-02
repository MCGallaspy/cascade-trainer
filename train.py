import os
import re
import requests

from os.path import join
from pprint import pprint
from googleapiclient.discovery import build

# Project imports
import secrets

def main():    
    whitespace_expr = re.compile(r"[^\w\d]")
    imgdir = join(".", "images")
    try:
        os.makedirs(imgdir)
    except os.error:
        pass

    service = build("customsearch", "v1", developerKey=secrets.apikey)

    res = service.cse().list(
      q='lemon trees',
      cx=secrets.searchid,
      searchType='image',
    ).execute()

    for item in res['items']:
        cleaned_title = whitespace_expr.sub("_", item['title']).replace(".", "") + '.jpg'
        resp = requests.get(item['link'])
        if resp.status_code == requests.codes.ok:
            with open(join(imgdir, cleaned_title), 'wb') as f:
                f.write(resp.content)

if __name__ == "__main__":
    main()