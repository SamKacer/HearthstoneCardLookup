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
<i>There is no beast more frightening (or ridiculous) than a fully enraged chicken.</i>"""

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
<i>This spell is useful for burning things.  If you're looking for spells that toast things, or just warm them a little, you're in the wrong place.</i>"""

def test_fireball():
	checkCardText('fireball', fireballText)

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