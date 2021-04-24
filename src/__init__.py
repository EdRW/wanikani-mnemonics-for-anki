# pyright: reportUnknownMemberType=false
import json
from typing import Optional, TypedDict

from aqt import mw


class Config(TypedDict):
    wanikaniApiKey: str
    source_field: str
    meaning_mnemonic_field: str
    reading_mnemonic_field: str
    get_vocab_mnemonics: bool
    get_kanji_mnemonics: bool
    get_radical_mnemonics: bool
    auto_mode: bool


def get_config() -> Config:
    if mw is None:
        with open('config.dev.json') as file:
            return json.load(file)
    else:
        config: Optional[Config] = mw.addonManager.getConfig(__name__)
        if not config:
            raise ValueError()
        return config
