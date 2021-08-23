# Hearthstone card lookup
# Copyright (C) 2021 Samuel Kacer
#GNU GENERAL PUBLIC LICENSE V2
# author: Samuel Kacer <samuel.kacer@gmail.com>
# <home page>

import api
import globalPluginHandler
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
		ui.browseableMessage(f"status: {response.status}")
	except HTTPError as e:
		ui.message(f"Couldn't get card info for {selection}: {e}")

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

