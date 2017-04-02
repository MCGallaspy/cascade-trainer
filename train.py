from pprint import pprint
import secrets

from googleapiclient.discovery import build

def main():
    service = build("customsearch", "v1", developerKey=secrets.apikey)
    
    res = service.cse().list(
      q='lemon trees',
      cx=secrets.searchid,
      searchType='image',
    ).execute()
    
    for item in res['items']:
        pprint(item)

if __name__ == "__main__":
    main()