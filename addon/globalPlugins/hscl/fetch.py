# Hearthstone card lookup
# Copyright (C) 2021 Samuel Kacer
#GNU GENERAL PUBLIC LICENSE V2
# author: Samuel Kacer <samuel.kacer@gmail.com>
# https://github.com/SamKacer/HearthstoneCardLookup

from typing import Optional, Union, Iterable
import re
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen, Request


def getCardFieldsIterator(cardName: str) -> Union[Iterable[str], str]:
	if   "’" in cardName:
		cardName = cardName.replace("’", "'")

	# in some webpages, namely top decks, all letters are capital, which is 404 in wiki
	# Capitalize all words except for exceptions, but always capitalize the first
	capitalized = " ".join(word.capitalize() if i == 0 or word.lower() not in LITTLE_WORDS else word.lower() for i, word in enumerate(cardName.split()))

	# kind of a hack, might want to make this more robust so it would automatically take care of other cases
	bad_rank_spelling = '(rank'
	if bad_rank_spelling in capitalized:
		capitalized = capitalized.replace(bad_rank_spelling, '(Rank')
	bad_si7_spelling = 'Si:7'
	if bad_si7_spelling in capitalized:
		capitalized = capitalized.replace(bad_si7_spelling, 'SI:7')
	
	data = fetchCardHtmlFromWiki(capitalized)
	if isinstance(data, HTTPError) and capitalized != cardName:
		data = fetchCardHtmlFromWiki(cardName)
	else:
		cardName = capitalized
	if isinstance(data, HTTPError):
		return f"Couldn't get card info for {cardName}: {data}"
	set = matchLink("Card set", data)
	multiClass = matchPlainText("Multi-class", data)
	class_ = matchLink("Class", data)
	type = matchLink("Card type", data)
	school = matchLink("Spell school", data)
	minionType = (
		matchLink("Minion type", data)
		or matchLink("Minion types", data)
		)
	rarity = matchLink("Rarity", data)
	if(rarity == "Rarity"):
		rarity = "Free"
	runeHtml = matchRow("Runes", data)
	runes = ', '.join(
		str(matchNumberBeforeLinkDirectly(runeData) or '') + ' ' + str(matchLinkDirectly(runeData) or '')
		for runeData in runeHtml.split('<br />')
	) if runeHtml else None
	cost = matchNumberBeforeImg("Cost", data)
	attack = matchNumberBeforeImg("Attack", data)
	health = matchNumberBeforeImg("Health", data)
	durability = matchNumberBeforeImg("Durability", data)

	match = re.search(r'(?sm)<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="flavor">.*?<center>(.*?)</center>', data)
	flavor = match.group(1) if match else None
	if flavor.startswith('<i>'):
		flavor = flavor[3:]
	if flavor.endswith('</i>'):
		flavor = flavor[:-4]

	match = re.search(r'(?sm)<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="text">.*?<center>(.*?)</center>', data)
	text = re.sub(r'(<b>)|(</b>)', "", match.group(1)) if match else None

	return filter(
		lambda f: f is not None,
		(
			cardName,
			f"{cost} mana" if cost else None,
			runes,
			f"{attack} {health or durability}" if attack and (health or durability) else None,
			text,
			minionType,
			school,
			type,
			multiClass or class_,
			rarity,
			set,
			flavor,
		)
	)


def fetchCardHtmlFromWiki(cardName: str) -> Union[str, HTTPError]:
	request = Request(
		url='https://hearthstone.wiki.gg/wiki/' + quote(cardName),
		    headers={'User-Agent': 'Mozilla/5.0'}
	)
	try:
		return urlopen(request).read().decode('utf-8')	
	except HTTPError as e:
		return e

LITTLE_WORDS = {'the', 'a', 'to', 'for', 'of', 'in'}

def h3_re(label: str) -> str:
	return r'<h3 class="pi-data-label pi-secondary-font">' + label + ':</h3>'

def matchLink(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	text = matchLinkDirectly(row)
	if(text):
		text2 = matchSecondLink(label, row) if row else None
		if(text2):
			text = text + ' ' + text2
	return text if text else None

def matchLinkDirectly(row: Optional[str]) -> Optional[str]:
	m = re.search(r'(?sm)<a.*? title="(.*?)">', row) if row else None
	return m.group(1).strip() if m else None

def matchSecondLink(label: str, row: str) -> Optional[str]:
	m = re.search(r'(?sm)<a .*?</a><br><a .*?title="(.*?)">', row) if row else None
	return m.group(1).strip() if m else None

def matchNumberBeforeImg(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	m = re.search(r'(?sm)(.*?)<img', row) if row else None
	return m.group(1).strip() if m else None

def matchNumberBeforeLink(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	return matchNumberBeforeLinkDirectly(row) if row else None

def matchNumberBeforeLinkDirectly(row: Optional[str]) -> Optional[str]:
	m = re.search(r'(?sm)(.*?)<a', row) if row else None
	return m.group(1).strip() if m else None

def matchPlainText(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	return row.strip() if row else None

def matchRow(label:str, string: str) -> Optional[str]:
	match = re.search(r'(?sm)' + h3_re(label) + r'.*?<div .*?>(.*?)</div>', string)
	return match.group(1) if match else None

