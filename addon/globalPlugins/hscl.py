# Hearthstone card lookup
# Copyright (C) 2021 Samuel Kacer
#GNU GENERAL PUBLIC LICENSE V2
# author: Samuel Kacer <samuel.kacer@gmail.com>
# https://github.com/SamKacer/HearthstoneCardLookup

from typing import Optional
import api
import globalPluginHandler
import re
from scriptHandler import script
from threading import Thread
from textInfos import POSITION_SELECTION
import ui
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script("Lookup Hearthstone card info.", gesture="kb:NVDA+H")
	def script_lookup(self, gesture):
		selection = getSelectedText().strip()
		if selection:
			if   "’" in selection:
				selection = selection.replace("’", "'")
			Thread(target=lookupCardInfo, args=(selection, )).start()


def lookupCardInfo(cardName: str) -> None:
	url = 'https://hearthstone.fandom.com/wiki/' + quote(cardName)
	try:
		response = urlopen(url)
		data = response.read().decode('utf-8')
		set = matchImage("Set", data)
		multiClass = matchLink("Multiclass", data)
		class_ = matchImage("Class", data)
		type = matchLink("Type", data)
		school = matchLink("Spell school", data)
		minionType = matchLink("Minion type", data)
		rarity = matchImage("Rarity", data) or matchLink("Rarity", data)
		cost = matchNumberBeforeImg("Cost", data)
		attack = matchNumberBeforeImg("Attack", data)
		health = matchNumberBeforeImg("Health", data)
		durability = matchNumberBeforeImg("Durability", data)

		match = re.search(r'(?sm)Flavor text</div>.*?<p><i>(.*?)</i>', data)
		flavor = match.group(1) if match else None

		match = re.search(r'(?sm)</table></div>(.*?)<div', data)
		text = re.sub(r'(<b>)|(</b>)', "", match.group(1)) if match else None

		ui.browseableMessage('<p>' + '</p>\n<p>'.join(
			filter(
				lambda f: f is not None,
				(
					cardName,
					f"{cost} mana" if cost else None,
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
		) + '</p>', cardName, True)
	except HTTPError as e:
		if e.code == 404:
			# in some webpages, namely top decks, all letters are capital, which is 404 in wiki
			# Capitalize all words except for exceptions, but always capitalize the first
			capitalized = " ".join(word.capitalize() if i == 0 or word.lower() not in LITTLE_WORDS else word.lower() for i, word in enumerate(cardName.split()))
			if capitalized != cardName:
				return lookupCardInfo(capitalized)
		ui.message(f"Couldn't get card info for {cardName}: {e}")

LITTLE_WORDS = {'the', 'a', 'to', 'for', 'of', 'in'}

def th_re(label: str) -> str:
	return r'<th>' + label + ':' + '</th>'

def matchImage(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	m = re.search(th_re(label) + r'.*?<td>.*?alt="(.*?)".*?</td>', row) if row else None
	return m.group(1).strip() if m else None

def matchLink(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	m = re.search(th_re(label) + r'.*?<td>.*?<a.*?>(.*?)</a>', row) if row else None
	return m.group(1).strip() if m else None

def matchNumberBeforeImg(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	m = re.search(th_re(label) + r'.*?<td>(.*?)<img', row) if row else None
	return m.group(1).strip() if m else None

def matchRow(label:str, string: str) -> Optional[str]:
	match = re.search(th_re(label) + r'.*?</tr>', string)
	return match.group() if match else None

# adapted from Quick Dictionary by Oleksandr Gryshchenko <grisov.nvaccess@mailnull.com>
def getSelectedText() -> str:
	"""Retrieve the selected text.
	If the selected text is missing - extract the text from the clipboard.
	If the clipboard is empty or contains no text data - announce a warning.
	@return: selected text, text from the clipboard, or an empty string
	@rtype: str
	"""
	obj = api.getFocusObject()
	treeInterceptor = obj.treeInterceptor
	if hasattr(treeInterceptor, 'TextInfo') and not treeInterceptor.passThrough:
		obj = treeInterceptor
	try:
		info = obj.makeTextInfo(POSITION_SELECTION)
	except (RuntimeError, NotImplementedError):
		info = None
	if not info or info.isCollapsed:
		try:
			text = api.getClipData()
		except Exception:
			text = ''
		if not text or not isinstance(text, str):
			# Translators: User has pressed the shortcut key for translating selected text,
			# but no text was actually selected and clipboard is clear
			ui.message(_("There is no selected text, the clipboard is also empty, or its content is not text!"))
			return ''
		return text
	return info.text

