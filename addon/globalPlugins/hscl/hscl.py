# Hearthstone card lookup
# Copyright (C) 2021 Samuel Kacer
#GNU GENERAL PUBLIC LICENSE V2
# author: Samuel Kacer <samuel.kacer@gmail.com>
# https://github.com/SamKacer/HearthstoneCardLookup

import api
from .fetch import getCardFieldsIterator
import globalPluginHandler
import gui
from scriptHandler import script
from textInfos import POSITION_SELECTION
import ui
import wx

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self) -> None:
		super().__init__()
		self.dialogue = None

	# Translators: Name of command for lookingh up card info from selection or clipboard
	@script(_("Lookup Hearthstone card info for card name from selection or clipboard."), gesture="kb:NVDA+H")
	def script_lookupFromSelectionOrClipboard(self, gesture):
		selection = getSelectedText().strip()
		if selection:
			lookupCardInfo(selection)


	# Translators: Name of command for opening dialogue for looking up card info from user input
	@script(_("Lookup Hearthstone card info for card name from user input."), gesture="kb:NVDA+shift+H")
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
	# Translators: the message output when the addon starts fetching the card info
	ui.message(_("fetching card info"))
	cardFieldsResult = getCardFieldsIterator(cardName)
	if isinstance(cardFieldsResult, str):
		# an error occured in fetching card fields
		ui.browseableMessage(cardFieldsResult)
	else:
		ui.browseableMessage('<p>' + '</p>\n<p>'.join(cardFieldsResult) + '</p>', cardName, True)


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
			# Translators: User has pressed the shortcut key for looking up a card from selected text,
			# but no text was actually selected and clipboard is clear
			ui.message(_("There is no selected text, the clipboard is also empty, or its content is not text!"))
			return ''
		return text
	return info.text

