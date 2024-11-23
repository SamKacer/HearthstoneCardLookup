# Hearthstone card lookup
# Copyright (C) 2021 Samuel Kacer
#GNU GENERAL PUBLIC LICENSE V2
# author: Samuel Kacer <samuel.kacer@gmail.com>
# https://github.com/SamKacer/HearthstoneCardLookup

from typing import Optional, Union
import api
import globalPluginHandler
import gui
import re
from scriptHandler import script
from textInfos import POSITION_SELECTION
import ui
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen, Request
import wx

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self) -> None:
		super().__init__()
		self.dialogue = None
	@script("Lookup Hearthstone card info for card name from selection or clipboard.", gesture="kb:NVDA+H")
	def script_lookupFromSelectionOrClipboard(self, gesture):
		selection = getSelectedText().strip()
		if selection:
			lookupCardInfo(selection)


	@script("Lookup Hearthstone card info for card name from user input.", gesture="kb:NVDA+shift+H")
	def script_lookupFromInput(self, gesture):
		if self.dialogue:
			if self.dialogue.IsActive():
				ui.message("Dialogue already open")
				return
			else:
				self.dialogue.Close()
		self.dialogue = wx.TextEntryDialog(
			gui.mainFrame,
			"Please enter card name to lookup",
			"Lookup Hearthstone card",
			style=wx.OK|wx.CANCEL
		)
		def callback(result):
			if result == wx.ID_OK:
				text = self.dialogue.GetValue().strip()
				if text:
					lookupCardInfo(text)
			self.dialogue = None
		#end def
		gui.runScriptModalDialog(self.dialogue, callback)

def lookupCardInfo(cardName: str) -> None:
	ui.message("fetching card info")
	
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
	if isinstance(data, HTTPError):
		return ui.message(f"Couldn't get card info for {cardName}: {data}")
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

	match = re.search(r'(?sm)<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="text">.*?<center>(.*?)</center>', data)
	text = re.sub(r'(<b>)|(</b>)', "", match.group(1)) if match else None

	ui.browseableMessage('<p>' + '</p>\n<p>'.join(
		filter(
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
	) + '</p>', cardName, True)


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

