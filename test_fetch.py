from difflib import ndiff
from addon.globalPlugins.hscl import fetch
import time

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

climacticNecroticExplosion = """Climactic Necrotic Explosion
10 mana
1 Blood, 1 Frost, 1 Unholy
Lifesteal. Deal 6 damage. Summon 3 2/2 Souls. <i>(Randomly improved by Corpses you've spent)</i>
Spell
Death Knight
Legendary
Festival of Legends
The less legible the band's logo, the more hardcore it is."""

def test_runeCard():
	checkCardText('Climactic Necrotic Explosion', climacticNecroticExplosion)

si7Agent = """SI:7 Agent
3 mana
3 3
Combo: Deal 3 damage.
Minion
Rogue
Rare
Legacy
The agents of SI:7 are responsible for Stormwind's covert activities.  Their duties include espionage, assassination, and throwing surprise birthday parties for the royal family."""

def test_si7():
	checkCardText('si:7 agent', si7Agent)

max_attempts = 10
max_backoff = 60
starting_backoff = 2

def checkCardText(cardName: str, expectedCardText: str, attempt=0) -> None:
	cardTextResult = fetch.getCardFieldsIterator(cardName)
	if isinstance(cardTextResult, str):
		if "HTTP Error 429" in cardTextResult and attempt < max_attempts:
			backoff = min(max_backoff, (starting_backoff * 2 ** attempt))
			print(f"Failed due to rate limiting. Sleeping {backoff}s and retrying")
			time.sleep(backoff)
			checkCardText(cardName, expectedCardText, attempt + 1)
		else: 
			raise Exception(f"Failed to fetch card text: {cardTextResult}")
	else:
		actualCardTextLines = list(cardTextResult)
		expectedCardTextLines = expectedCardText.split('\n')
		if actualCardTextLines != expectedCardTextLines:
			diff = '\n'.join(ndiff(expectedCardTextLines, actualCardTextLines))
			raise Exception(f"Card text for {cardName} did not match:\n{diff}")