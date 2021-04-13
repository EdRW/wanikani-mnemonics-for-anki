from src.models import WkCollection, wk_subject_factory
import urllib3
import json
from . import config

# ! DO NOT COMMIT THIS!
API_TOKEN = config['wanikaniApiKey']

http = urllib3.PoolManager()

BASE_URL = 'https://api.wanikani.com/v2'
endpoint = 'subjects'
headers = {'Authorization': 'Bearer ' + API_TOKEN}
search_url = 'https://www.wanikani.com/search'


def search_wk(slug: str):
    url = '/'.join([BASE_URL, endpoint]) + f'?slugs={slug}'
    response = http.request('GET', url, headers=headers)

    wk_collection: WkCollection = json.loads(response.data.decode('utf-8'))

    with open('resp.json', mode='w') as file:
        file.write(json.dumps(wk_collection, indent=2))

    return [wk_subject_factory(data) for data in wk_collection['data']]
