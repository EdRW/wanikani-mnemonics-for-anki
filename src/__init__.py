# pyright: reportUnknownMemberType=false
import json
from typing import TypedDict

from aqt import mw


class Config(TypedDict):
    wanikaniApiKey: str
    meaning_mnemonic_field: str
    reading_mnemonic_field: str
    auto_mode: bool


config: Config

if mw is None:
    with open('config.dev.json') as file:
        config = json.load(file)
else:
    config = mw.addonManager.getConfig(__name__)
