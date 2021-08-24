# Hearthstone card lookup
# Copyright (C) 2021 Samuel Kacer
#GNU GENERAL PUBLIC LICENSE V2
# author: Samuel Kacer <samuel.kacer@gmail.com>
# <home page>

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
			Thread(target=lookupCardInfo, args=(selection, )).start()


def lookupCardInfo(cardName: str) -> None:
	url = 'https://hearthstone.fandom.com/wiki/' + quote(cardName)
	try:
		response = urlopen(url)
		bs = response.read().decode('utf-8')
		# bs = re.sub(r'(?sm)<script.*>.*</script>', "", bs)
		set = matchImage("Set", bs)
		class_ = matchImage("Class", bs)
		type = matchLink("Type", bs)
		school = matchLink("Spell school", bs)
		rarity = matchImage("Rarity", bs) or matchLink("Rarity", bs)
		cost = matchNumberBeforeImg("Cost", bs)
		attack = matchNumberBeforeImg("Attack", bs)
		health = matchNumberBeforeImg("Health", bs)

		match = re.search(r'(?sm)Flavor text</div>.*?<p><i>(.*?)</i>', bs)
		flavor = match.group(1) if match else None

		match = re.search(r'(?sm)</table></div>(.*?)<div', bs)
		text = re.sub(r'(<b>)|(</b>)', "", match.group(1)) if match else None

		ui.browseableMessage('\n'.join(
			filter(
				lambda f: f is not None,
				(
					cardName,
					f"{cost} mana",
					f"{attack} {health}" if attack and health else None,
					text,
					school,
					type,
					class_,
					rarity,
					set,
					flavor,
				)
			)
		))
	except HTTPError as e:
		ui.message(f"Couldn't get card info for {cardName}: {e}")

def th_re(label: str) -> str:
	return r'<th>' + label + ':' + '</th>'

def matchImage(label: str, string: str) -> Optional[str]:
	row = matchRow(label, string)
	m = re.search(th_re(label) + r'.*?<td>.*?alt="(.*?)".*?</td>', row)
	return m.group(1).strip() if m else None

def matchLink(label: str, string: str) -> Optional[str]:
	m = re.search(th_re(label) + r'.*?<td>.*?<a.*?>(.*?)</a>', string)
	return m.group(1).strip() if m else None

def matchNumberBeforeImg(label: str, string: str) -> Optional[str]:
	m = re.search(th_re(label) + r'.*?<td>(.*?)<img', string)
	return m.group(1).strip() if m else None

def matchRow(label:str, string: str) -> Optional[str]:
	match = re.search(th_re(label) + r'.*?</tr>', string)
	return match.group() if match else None

# from quick dictionary addon by 
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

