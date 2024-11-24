from difflib import ndiff
from addon.globalPlugins.hscl import fetch

angryChickenTextLines = """angry chicken
1 mana
1 1
Has +5 Attack while damaged.
Beast
Minion
Neutral
Rare
Legacy
<i>There is no beast more frightening (or ridiculous) than a fully enraged chicken.</i>""".split('\n')

def test_fetchMinion():
	cardTextResult = fetch.getCardFieldsIterator('angry chicken')
	if isinstance(cardTextResult, str):
		raise Exception(f"Failed to fetch card text: {cardTextResult}")
	else:
		cardTextLines = list(cardTextResult)
		if cardTextLines != angryChickenTextLines:
			diff = '\n'.join(ndiff(angryChickenTextLines, cardTextLines))
			raise Exception(f"Card text did not match:\n{diff}")
