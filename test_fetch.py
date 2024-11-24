from difflib import ndiff
from addon.globalPlugins.hscl import fetch

angryChickenText = """Angry Chicken
1 mana
1 1
Has +5 Attack while damaged.
Beast
Minion
Neutral
Rare
Legacy
There is no beast more frightening (or ridiculous) than a fully enraged chicken."""

def test_fetchMinion():
	checkCardText('angry chicken' , angryChickenText)

def test_minion_all_caps():
	checkCardText('ANGRY CHICKEN', angryChickenText)

fireballText = """Fireball
4 mana
Deal 6 damage.
Fire
Spell
Mage
Free
Legacy
This spell is useful for burning things.  If you're looking for spells that toast things, or just warm them a little, you're in the wrong place."""

def test_fireball():
	checkCardText('fireball', fireballText)

fieryWarAxeText = """Fiery War Axe
2 mana
3 2
Weapon
Warrior
Free
Legacy
During times of tranquility and harmony, this weapon was called by its less popular name, Chilly Peace Axe."""

def test_weapon():
	checkCardText('fiery war axe', fieryWarAxeText)

lightningBloomText = """Lightning Bloom
0 mana
Refresh 2 Mana Crystals. Overload: (2)
Nature
Spell
Druid/Shaman
Common
Scholomance Academy
Curiously, this plant never blooms in the same place twice."""

def test_multiclass():
	checkCardText('lightning bloom', lightningBloomText)

def checkCardText(cardName: str, expectedCardText: str) -> None:
	cardTextResult = fetch.getCardFieldsIterator(cardName)
	if isinstance(cardTextResult, str):
		raise Exception(f"Failed to fetch card text: {cardTextResult}")
	else:
		actualCardTextLines = list(cardTextResult)
		expectedCardTextLines = expectedCardText.split('\n')
		if actualCardTextLines != expectedCardTextLines:
			diff = '\n'.join(ndiff(expectedCardTextLines, actualCardTextLines))
			raise Exception(f"Card text for {cardName} did not match:\n{diff}")