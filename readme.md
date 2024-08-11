# Hearthstone Card Lookup

This is an NVDA addon that lets users quickly lookup info for a specific Hearthstone card by its name.

- [download stable version](https://github.com/SamKacer/HearthstoneCardLookup/releases/download/v0.10/HearthstoneCardLookup-0.10.nvda-addon)

## Usage

Either select the text of a card name or have it copied to your clipboard, then press NVDA + H, which will try to find the card info and display it in a pop-up browseable window.

Alternatively, you can press NVDA + shift + H, which will bring up a dialogue where you can type in the name of a card to look up.

### Example output

```
Tirion Fordring
8 mana
6 6
Divine Shield. Taunt. Deathrattle: Equip a 5/3 Ashbringer.
Minion
Paladin
Legendary
Legacy
If you haven't heard the Tirion Fordring theme song, it's because it doesn't exist.
``` 	

## Changelog

### v0.10
- fix addon not working since hearthstone wiki moved to new website

### v0.9
- show all runes for cards with more than one rune, like Climactic Necrotic Explosion

### v0.8
- updated to work with NVDA 2023
- fixed addon not working anymore after Hearthstone fandom wiki changed its layout
- fixed minion types and multi class not showing

### v0.7
- opening a card lookup dialog will only allow one such dialog to exist
- compatible with NVDA version 2022.1

### v0.6
- fix some cards not being fetched like Whack-A-Gnoll Hammer and Flurry (Rank 1)

### v0.5
- fetching card info is faster in some cases
- added new command for looking up card info from user input (NVDA + shift + H)

### v0.4
- display multiclass if available for card

### v0.3

-     Fix stats sometimes not displaying for weapons
-     Dont display mana cost for costless cards
-     Make possible to lookup cards as listed on top decks

###v0.2

- display minion type
- fix strange symbols rendering for some cards

### v0.1

- initial release

## [Homepage](https://github.com/SamKacer/HearthstoneCardLookup)

Use this github to post issues with the addon.
