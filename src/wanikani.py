from typing import Dict, List, Optional
import urllib3
import json
from . import config
from .models import WkCollection, WkObjectType, WkSubject, wk_subject_factory

API_TOKEN = config['wanikaniApiKey']
BASE_URL = 'https://api.wanikani.com/v2'
endpoint = 'subjects'
headers = {'Authorization': 'Bearer ' + API_TOKEN}
search_url = 'https://www.wanikani.com/search'

InternalWkCache = Dict[str, WkSubject]


class WkCache:
    def __init__(self) -> None:
        self.caches: Dict[WkObjectType, InternalWkCache] = {
            WkObjectType.kanji: {},
            WkObjectType.vocabulary: {}
        }

    def get_kanji(self, slug: str):
        return self.caches[WkObjectType.kanji].get(slug)

    def get_vocab(self, slug: str):
        return self.caches[WkObjectType.vocabulary].get(slug)

    def set(self, slug: str, wk_subject: WkSubject):
        if wk_subject.object is WkObjectType.kanji:
            self.caches[WkObjectType.kanji][slug] = wk_subject
        elif wk_subject.object is WkObjectType.vocabulary:
            self.caches[WkObjectType.vocabulary][slug] = wk_subject


cache = WkCache()
http = urllib3.PoolManager()

counter = 0


def search_wk(slug: str):
    url = '/'.join([BASE_URL, endpoint]) + f'?slugs={slug}'
    response = http.request('GET', url, headers=headers)

    wk_collection: WkCollection = json.loads(response.data.decode('utf-8'))
    # global counter
    # counter += 1
    # with open('resp.json', mode='w', encoding='utf8') as file:
    #     file.write(f'{slug}: {str(counter)}\n' +
    #                json.dumps(wk_collection, indent=2))
    try:
        wk_subjects = [
            wk_subject_factory(data) for data in wk_collection['data']
        ]
    except KeyError:
        empty_list: List[WkSubject] = []
        return empty_list
    for wk_subject in wk_subjects:
        cache.set(slug, wk_subject)
    return wk_subjects


def wankani_vocab(slug: str) -> Optional[WkSubject]:
    if (vocab_subject := cache.get_vocab(slug)):
        return vocab_subject
    wk_subjects = search_wk(slug)
    for wk_subject in wk_subjects:
        if wk_subject.object is WkObjectType.vocabulary:
            return wk_subject
    return None


def wankani_kanji(slug: str) -> Optional[WkSubject]:
    if (kanji_subject := cache.get_kanji(slug)):
        return kanji_subject
    wk_subjects = search_wk(slug)
    for wk_subject in wk_subjects:
        if wk_subject.object is WkObjectType.kanji:
            return wk_subject
    return None
