# pyright: reportUnknownMemberType=false

from typing import Optional
from aqt import mw
from PyQt5.QtWidgets import QAction, QMenu
from aqt import gui_hooks
from anki.notes import Note
from aqt.editor import EditorWebView
from aqt.utils import showInfo, qconnect

from .src import config

meaning_mnemonic_field_name = config['meaning_mnemonic_field']
reading_mnemonic_field_name = config['reading_mnemonic_field']

if config['auto_mode']:

    def unfocus_callback(changed: bool, note: Note,
                         current_field_idx: int) -> bool:
        showInfo(
            f'Updating fields: {meaning_mnemonic_field_name} and {reading_mnemonic_field_name}'
        )
        return changed

    gui_hooks.editor_did_unfocus_field.append(unfocus_callback)


def context_menu_callback(editor_webview: EditorWebView, menu: QMenu) -> None:
    note: Optional[Note] = editor_webview.editor.note
    if not note:
        raise ValueError

    def add_meaning_mnemonic():
        note
        showInfo(f'Updating field: {meaning_mnemonic_field_name}')

    def add_reading_mnemonic():
        note
        showInfo(f'Updating field: {reading_mnemonic_field_name}')

    add_meaning_mnemonic_action = QAction('Add meaning mnemonic from Wanikani',
                                          mw)
    add_reading_mnemonic_action = QAction('Add reading mnemonic from Wanikani',
                                          mw)
    qconnect(add_meaning_mnemonic_action.triggered, add_meaning_mnemonic)
    qconnect(add_reading_mnemonic_action.triggered, add_reading_mnemonic)

    menu.addActions([add_meaning_mnemonic_action, add_reading_mnemonic_action])


gui_hooks.editor_will_show_context_menu.append(context_menu_callback)