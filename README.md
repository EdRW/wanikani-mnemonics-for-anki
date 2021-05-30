# Wanikani Mnemonics for Anki

An add on for Anki 2.1 that helps you add mnemonics to your flashcards from Wanikani.

### How to install

- Find the Anki add-ons folder by going to the Tools>Add-ons menu item in the main Anki window.
- Click on the View Files button, and a folder will pop up.
- Download this project and place it inside of the folder that opened.
- Now restart Anki.

### Configuration

Anki allows users to configure this add-on from the add-on manager.

The config is a simple config.json:

```json
{
  "auto_mode": false,
  "get_kanji_mnemonics": true,
  "get_radical_mnemonics": true,
  "get_vocab_mnemonics": true,
  "meaning_mnemonic_field": "NAME-OF-CARD-FIELD",
  "reading_mnemonic_field": "NAME-OF-CARD-FIELD",
  "source_field": "NAME-OF-CARD-FIELD",
  "wanikaniApiKey": "ENTER-YOUR-API-KEY"
}
```

### Styling

Add this styling to your card in order to get Wanikani style color highlighting.

Note: The colors will not be displayed while editing the card but they will be displayed when viewing them during reviews.

```css
vocabulary {
  color: rgb(255, 255, 255);
  background-color: rgb(161, 0, 241);
}

kanji {
  background-color: #f100a1;
  color: #fff;
}

reading {
  background-color: #474747;
  color: #fff;
}

radical {
  background-color: #00a1f1;
  color: #fff;
}
```

## Development

### Todo List

- [ ] Option to include links to wanikani page to the mnemonic or replace mnemonic entirely with just the link
