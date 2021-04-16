# Wanikani Mnemonics for Anki

An add on for Anki 2.1 that allows you add mnemonics to your flashcards from Wanikani.

### Configuration

Anki allows users to configure this add-on from the add-on manager.

The config is a simple config.json:

```json
{
  "wanikaniApiKey": "ENTER-YOUR-API-KEY",
  "source_field": "NAME-OF-CARD-FIELD",
  "meaning_mnemonic_field": "NAME-OF-CARD-FIELD",
  "reading_mnemonic_field": "NAME-OF-CARD-FIELD",
  "individual_kanji_mnemonics": true,
  "auto_mode": false
}
```

### Styling

Add this styling to your card

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
