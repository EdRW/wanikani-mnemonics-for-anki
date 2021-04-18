# pyright: reportUnknownMemberType=false

from typing import Optional
from aqt import mw
from PyQt5.QtWidgets import QAction, QMenu
from aqt import gui_hooks
from anki.notes import Note
from aqt.editor import EditorWebView
from aqt.utils import qconnect

from .src import config
from .src.mnemonics import add_meaning_mnemonic_to_note, add_reading_mnemonic_to_note

source_field_name = config['source_field']
meaning_mnemonic_field_name = config['meaning_mnemonic_field']
reading_mnemonic_field_name = config['reading_mnemonic_field']
individual_kanji_mnemonics = config['individual_kanji_mnemonics']

if config['auto_mode']:

    def unfocus_callback(changed: bool, note: Note,
                         current_field_idx: int) -> bool:
        """Handles the updating of the note after a field has been unfocused

        Args:
            changed (bool): where or not a previous filter has changed the note in this call
            note (Note): the note to be updated
            current_field_idx (int): the index of the field that was just unfocused

        Returns:
            bool: If no changes made to note then returns the changed flag the same as it received it; if it makes a change it returns True.
        """
        meaning_success = add_meaning_mnemonic_to_note(
            note=note,
            scr_field=source_field_name,
            mnemonic_field=meaning_mnemonic_field_name,
            individual=individual_kanji_mnemonics,
            triggered_field_index=current_field_idx)
        reading_success = add_reading_mnemonic_to_note(
            note=note,
            scr_field=source_field_name,
            mnemonic_field=reading_mnemonic_field_name,
            individual=individual_kanji_mnemonics,
            triggered_field_index=current_field_idx)
        if note.id:
            note.flush()
        return meaning_success or reading_success

    gui_hooks.editor_did_unfocus_field.append(unfocus_callback)


def context_menu_callback(editor_webview: EditorWebView, menu: QMenu) -> None:
    note: Optional[Note] = editor_webview.editor.note

    def add_meaning_mnemonic():
        if not note:
            raise ValueError
        success = add_meaning_mnemonic_to_note(
            note=note,
            scr_field=source_field_name,
            mnemonic_field=meaning_mnemonic_field_name,
            individual=individual_kanji_mnemonics)
        if success:
            if note.id:
                # note is being created
                editor_webview.editor.loadNote()
            else:
                # note already exists
                note.flush()

    def add_reading_mnemonic():
        if not note:
            raise ValueError
        success = add_reading_mnemonic_to_note(
            note=note,
            scr_field=source_field_name,
            mnemonic_field=reading_mnemonic_field_name,
            individual=individual_kanji_mnemonics)
        if success:
            if note.id:
                # note is being created
                editor_webview.editor.loadNote()
            else:
                # note already exists
                note.flush()

    add_meaning_mnemonic_action = QAction('Add meaning mnemonic from Wanikani',
                                          mw)
    add_reading_mnemonic_action = QAction('Add reading mnemonic from Wanikani',
                                          mw)
    qconnect(add_meaning_mnemonic_action.triggered, add_meaning_mnemonic)
    qconnect(add_reading_mnemonic_action.triggered, add_reading_mnemonic)

    menu.addActions([add_meaning_mnemonic_action, add_reading_mnemonic_action])


gui_hooks.editor_will_show_context_menu.append(context_menu_callback)