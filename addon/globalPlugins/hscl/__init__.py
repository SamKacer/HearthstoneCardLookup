# Hearthstone card lookup
# Copyright (C) 2021 Samuel Kacer
#GNU GENERAL PUBLIC LICENSE V2
# author: Samuel Kacer <samuel.kacer@gmail.com>
# https://github.com/SamKacer/HearthstoneCardLookup

# ignore import error in case running tests and nvda imports are unavailable
try:
	from . import hscl

	GlobalPlugin = hscl.GlobalPlugin
except: pass
