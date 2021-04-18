# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

from .wanikani import wankani_kanji, wankani_vocab
from .models import WkSubject
from typing import List, Optional
from anki.notes import Note
from anki.utils import stripHTML
from aqt import mw
from enum import Enum, auto


class MnemonicType(Enum):
    reading = auto()
    meaning = auto()


def add_reading_mnemonic_to_note(
        note: Note,
        scr_field: str,
        mnemonic_field: str,
        individual: bool = False,
        triggered_field_index: Optional[int] = None) -> bool:
    return add_wk_mnemonic_to_note(note=note,
                                   scr_field=scr_field,
                                   mnemonic_field=mnemonic_field,
                                   individual=individual,
                                   mnemonic_type=MnemonicType.reading,
                                   triggered_field_index=triggered_field_index)


def add_meaning_mnemonic_to_note(
        note: Note,
        scr_field: str,
        mnemonic_field: str,
        individual: bool = False,
        triggered_field_index: Optional[int] = None) -> bool:
    return add_wk_mnemonic_to_note(note=note,
                                   scr_field=scr_field,
                                   mnemonic_field=mnemonic_field,
                                   individual=individual,
                                   mnemonic_type=MnemonicType.meaning,
                                   triggered_field_index=triggered_field_index)


def add_wk_mnemonic_to_note(
        note: Note,
        scr_field: str,
        mnemonic_field: str,
        individual: bool,
        mnemonic_type: MnemonicType,
        triggered_field_index: Optional[int] = None) -> bool:
    # field missing from note?
    if not valid_note_fields(note, [scr_field, mnemonic_field]):
        return False

    # field already filled?
    if note[mnemonic_field]:
        return False

    if triggered_field_index is not None:
        src_index = get_field_index(note, scr_field)
        if src_index != triggered_field_index:
            return False

    scr_text = stripHTML(note[scr_field])
    # showInfo(f'og text: {note[scr_field]}\nsearch text: {scr_text}')
    # source field is blank
    if not scr_text:
        return False

    mnemonic_string_list: List[str] = []

    vocab_subject: Optional[WkSubject] = wankani_vocab(scr_text)

    if vocab_subject:
        mnemonic_string_list.append(': '.join([
            f'<vocabulary>{scr_text}</vocabulary>',
            f'<b>{vocab_subject.meaning}</b>'
        ]))
        vocab_mnemonic = (vocab_subject.reading_mnemonic
                          if mnemonic_type is MnemonicType.reading else
                          vocab_subject.meaning_mnemonic)
        mnemonic_string_list.append(vocab_mnemonic)
    else:
        mnemonic_string_list.append(
            f'<vocabulary>{scr_text}</vocabulary>: <b>Unknown</b><br>'
            f"~😿 We couldn't find a mnemonic for {scr_text} on wanikani, "
            "But we encourage you to try writing your own! 😺~")

    if individual:
        kanji_only = strip_out_kanji(note[scr_field])
        for kanji in kanji_only:
            kanji_subject: Optional[WkSubject] = wankani_kanji(kanji)
            if kanji_subject:
                mnemonic_string_list.append(': '.join([
                    f'<kanji>{kanji}</kanji>',
                    f'<b>{kanji_subject.meaning}</b>'
                ]))
                kanji_mnemonic = (kanji_subject.reading_mnemonic
                                  if mnemonic_type is MnemonicType.reading else
                                  kanji_subject.meaning_mnemonic)
                mnemonic_string_list.append(kanji_mnemonic)
            else:
                mnemonic_string_list.append(
                    f'<kanji>{kanji}</kanji>: <b>Unknown</b><br>'
                    f"~😿 We couldn't find a mnemonic for {kanji} on wanikani, "
                    "But we encourage you to try writing your own! 😺~")

    if not mnemonic_string_list:
        return False

    note[mnemonic_field] = '<br>'.join(mnemonic_string_list)
    # note.flush()
    return True


def valid_note_fields(note: Note, fields: List[str]) -> bool:
    if mw is None or mw.col is None:
        raise AttributeError()
    note_fields = mw.col.models.fieldNames(note.model())
    for field in fields:
        if field not in note_fields:
            return False
    return True


def get_field_index(note: Note, field: str) -> int:
    if mw is None or mw.col is None:
        raise AttributeError()
    note_fields = mw.col.models.fieldNames(note.model())
    return note_fields.index(field)


def strip_out_kanji(src_text: str) -> str:
    """Remove all html and return only the kanji.
    """
    # stripped_text = stripHTML(src_text)
    return ''.join([char for char in src_text if is_kanji(char)])


def is_kanji(char: str):
    # taken from these references
    # https://en.wikipedia.org/wiki/CJK_Unified_Ideographs#CJK_Unified_Ideographs_blocks
    # https://stackoverflow.com/questions/30069846/how-to-find-out-chinese-or-japanese-character-in-a-string-in-python
    return ord(u"\u4e00") <= ord(char) <= ord(u"\u9fff")
