from abc import ABC
from typing import Any, Dict, List, Literal, TypedDict
from dataclasses import dataclass


@dataclass
class WkCollection(TypedDict):
    id: int
    object: str
    total_count: int
    data: List[Dict[str, Any]]


@dataclass
class WkSubject(ABC):
    id: int
    object: Literal['kanji', 'vocabulary']
    characters: str
    meaning_mnemonic: str
    reading_mnemonic: str

    def __init__(self, source: Dict[str, Any]):
        self.id = source['id']
        self.object = source['object']
        self.characters = source['data']['characters']
        self.meaning_mnemonic = source['data']['meaning_mnemonic']
        self.reading_mnemonic = source['data']['reading_mnemonic']


@dataclass
class WkKanji(WkSubject):
    meaning_hint: str
    reading_hint: str

    def __init__(self, source: Dict[str, Any]):
        super().__init__(source)
        self.meaning_hint = source['data']['meaning_hint']
        self.reading_hint = source['data']['reading_hint']


class ContextSentence(TypedDict):
    en: str
    ja: str


class AudioMetadata(TypedDict):
    voice_actor_id: str
    gender: str
    voice_description: str


class PronunciationAudio(TypedDict):
    url: str
    content_type: str
    metadata: AudioMetadata


@dataclass
class WkVocab(WkSubject):
    context_sentences: List[ContextSentence]
    pronunciation_audios: PronunciationAudio

    def __init__(self, source: Dict[str, Any]):
        super().__init__(source)
        self.context_sentences = source['data']['context_sentences']
        self.pronunciation_audios = source['data']['pronunciation_audios']


def wk_subject_factory(source: Dict[str, Any]) -> WkSubject:
    if source['object'] == 'kanji':
        return WkKanji(source)
    elif source['object'] == 'vocabulary':
        return WkVocab(source)
    raise ValueError('Dict is not a valid wk_subject')
