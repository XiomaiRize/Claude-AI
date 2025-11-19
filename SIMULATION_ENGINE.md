# Simulation Engine Documentation

## Overview

The Dynamic RPG features a **realistic simulation engine** that tracks hundreds of variables to make the game world feel alive and reactive. **Claude (the AI Game Master) actively manages these variables** as you play, creating a living, breathing world where your actions have meaningful consequences.

## What Makes This Special?

Instead of a simple quest tracker, the game simulates:
- **NPC emotions** towards you (on a 0-10 scale)
- **Player conditions** (bleeding, poisoned, cursed, exhausted, etc.)
- **World states** (time, weather, village safety, economic conditions)
- **Reputation and fame** (or infamy!)
- **Realistic action gating** (can't cast magic if you have no mana!)

## How It Works

As you play, **Claude tracks and updates simulation variables** based on your actions. These variables then affect:
- What actions are possible
- How NPCs react to you
- What events can occur
- The difficulty of challenges

### Example Flow

```
YOU: "I refuse to help the blacksmith for the third time"

CLAUDE: The blacksmith's face darkens with frustration. "Fine! See if I
ever help YOU when you need it!" she snaps.

[Behind the scenes: blacksmith.annoyance increases from 6 to 9]

YOU: "I try to buy a weapon from the blacksmith"

CLAUDE: She crosses her arms and glares at you. "Not selling to the
likes of you. Get out of my shop!"

[Action blocked because blacksmith.annoyance is too high!]
```

## Simulation Systems

### 1. NPC Relationships (0-10 scale)

Every NPC tracks these emotions toward the player:

#### **Affection**
How much they like you emotionally
- 0-2: Despises you
- 3-4: Dislikes you
- 5: Neutral
- 6-7: Likes you
- 8-9: Really likes you
- 10: Loves/adores you

#### **Trust**
How much they trust you with important matters
- 0-2: Doesn't trust you at all
- 3-4: Suspicious of you
- 5: Neutral
- 6-7: Some trust
- 8-9: Trusts you significantly
- 10: Complete trust

#### **Respect**
How much they respect your abilities/character
- 0-2: No respect
- 3-4: Little respect
- 5: Basic courtesy
- 6-7: Growing respect
- 8-9: High respect
- 10: Immense respect

#### **Fear**
How afraid they are of you
- 0-2: Not afraid
- 3-5: Slightly wary
- 6-7: Afraid
- 8-9: Very afraid
- 10: Terrified

#### **Annoyance**
How annoyed/frustrated they are with you
- 0-2: Not annoyed
- 3-5: Mildly annoyed
- 6-7: Quite annoyed
- 8-9: Very annoyed
- 10: Furious

### How NPCs React Based on These Values

**High Affection + High Trust:**
- Give you special quests
- Offer discounts
- Share secrets
- Help you in tough situations

**High Fear + Low Respect:**
- May betray you
- Spread rumors about you
- Avoid you

**High Annoyance:**
- Refuse to deal with you
- Increase prices
- Give you harder quests
- May report you to authorities

**Combined "Disposition"** (calculated from all values):
- "Adores you" (20+ points)
- "Very friendly" (15-19)
- "Friendly" (10-14)
- "Neutral" (5-9)
- "Unfriendly" (0-4)
- "Hostile" (-5 to -1)
- "Deeply hostile" (<-5)

### 2. Player Conditions

#### Boolean Conditions (true/false)

**Physical:**
- `is_bleeding` - Taking damage over time
- `is_poisoned` - Poisoned status
- `is_cursed` - Under a curse (various negative effects)
- `is_blessed` - Under divine blessing (positive effects)
- `is_hungry` - Need food
- `is_exhausted` - Too tired, penalties to combat
- `is_drunk` - Impaired decision making

**Magical:**
- `has_mana` - Can cast magic (false = completely drained)
- `magic_available` - Magic works in this area
- `is_silenced` - Cannot cast spells

**Social:**
- `is_wanted` - Criminal status, guards attack on sight
- `is_disguised` - Hiding identity
- `is_famous` - Well-known hero
- `is_infamous` - Well-known villain

**Special:**
- `can_fly` - Ability to fly
- `can_swim` - Can swim (some races can't!)
- `is_invisible` - Cannot be seen
- `is_transformed` - Changed form (werewolf, etc.)

#### Intensity Stats (0-10)

- `health_condition` - Overall physical health (10=perfect, 0=near death)
- `stamina` - Energy for physical actions
- `sanity` - Mental stability (low = hallucinations, bad decisions)
- `corruption` - Dark magic corruption level

### 3. World State

#### Time and Environment
- `time_of_day` - dawn, morning, midday, afternoon, evening, night, midnight
  - Shops close at night
  - Some NPCs only appear at certain times
  - Monsters are stronger at night

- `weather` - clear, cloudy, raining, storming, snowing, foggy
  - Affects travel difficulty
  - Some spells are stronger/weaker in certain weather

- `season` - spring, summer, autumn, winter
  - Affects available resources
  - Some areas only accessible in certain seasons

#### World Events (boolean)
- `is_war_happening` - Kingdom at war
- `is_festival_active` - Festival in progress (higher prices, more NPCs)
- `is_plague_active` - Disease spreading
- `is_apocalypse` - End times scenario

#### Location States
- `village_safe` (boolean) - Are villagers safe?
- `village_prosperity` (0-10) - Economic health of village
- `forest_darkness` (0-10) - How dangerous the forest is
- `cave_explored` (boolean) - Have you explored the cave?
- `dragon_alive` (boolean) - Is the dragon still alive?

#### Reputation
- `player_fame` (-10 to +10)
  - Negative = infamy (feared/hated)
  - Positive = fame (respected/admired)

- `villages_saved` - Count of villages you've saved
- `monsters_slain` - Total monsters defeated
- `people_helped` - Number of NPCs you've helped
- `crimes_committed` - Criminal acts

#### Economy
- `market_open` (boolean) - Can you shop?
- `prices_inflated` (boolean) - Everything costs more
- `rare_items_available` (boolean) - Special items in stock

#### Magical State
- `magic_surge_active` - Magic is more powerful
- `magic_dead_zone` - Magic doesn't work at all
- `portal_open` - Portal to another realm is open

## How Variables Affect Gameplay

### Action Gating

Certain actions are **impossible** based on simulation state:

```python
# Trying to cast a spell
if not has_mana:
    ❌ "You have no mana left!"
if is_silenced:
    ❌ "You cannot speak to cast the spell!"
if magic_dead_zone:
    ❌ "Magic doesn't work in this area!"
```

```python
# Trying to enter the shop
if not market_open:
    ❌ "The shops are closed at this hour!"
if is_wanted:
    ❌ "Guards spot you and attack!"
```

```python
# Trying to fight
if is_exhausted:
    ❌ "You're too tired to fight effectively!"
if health_condition <= 2:
    ❌ "You're too wounded to attack!"
```

### NPC Reactions

NPCs respond differently based on their relationship with you:

**Village Elder:**
- Affection: 8, Trust: 9, Respect: 7
- Will give you important quests
- Shares village secrets
- Offers help when needed

**Blacksmith:**
- Affection: 3, Trust: 5, Respect: 2, Annoyance: 8
- Refuses to sell to you
- Charges extra if she does sell
- Won't upgrade your equipment

**Merchant:**
- Affection: 5, Fear: 7, Respect: 8
- Nervous around you
- Gives you good deals (because he's afraid)
- Won't report your crimes

## Viewing Simulation State

### In-Game Commands

Type `simulation` or `sim` to see current simulation state:

```
> simulation

======================================================================
  SIMULATION STATE (Claude manages this!)
======================================================================

🧍 PLAYER CONDITIONS:
  Active Conditions: Bleeding, Exhausted
  Has Mana: Yes
  Health Condition: 6/10
  Stamina: 3/10
  Sanity: 10/10

🌍 WORLD STATE:
  Time: evening
  Weather: raining
  Season: autumn
  Player Fame: 5
  Village Safe: Yes
  Monsters Slain: 12

👥 NPC RELATIONSHIPS:

  Village Elder (very friendly):
    Affection: 8/10
    Trust: 9/10
    Respect: 7/10
    Fear: 0/10
    Annoyance: 1/10
    Times Met: 5

  Blacksmith (unfriendly):
    Affection: 3/10
    Trust: 5/10
    Respect: 2/10
    Fear: 0/10
    Annoyance: 8/10
    Times Met: 7

======================================================================
```

## How Claude Uses the Simulation

As the AI Game Master, Claude actively manages these variables:

### During Narration

Claude naturally mentions simulation changes:

> "The village elder smiles warmly as you return victorious. You can see the **trust** in his eyes has grown. (trust: 7→9)"

> "You've been walking for hours. **Exhaustion sets in** (is_exhausted=true, stamina: 8→4)"

> "As the sun sets, **time advances to evening**. The shops begin to close."

> "The merchant's eyes widen with **fear** as you draw your bloodied sword. (fear: 2→6)"

### Realistic Consequences

```
YOU: "I threaten the shopkeeper for a discount"

CLAUDE: The shopkeeper's hands tremble as she nods quickly. "F-fine!
Take it for 20% off!"

[shopkeeper.fear: 2→7, shopkeeper.affection: 5→2]

However, you notice other villagers watching nervously.
Word of this will spread...

[player_fame: 3→1, villages_helped: unchanged, crimes_committed: 0→1]

Later, when you return:

YOU: "I want to buy more supplies"

CLAUDE: The shopkeeper locks the door as she sees you approaching.
Through the window she mouths "We're closed!"

[Action blocked: shopkeeper.fear too high + crimes_committed > 0]
```

### Dynamic Difficulty

Claude adjusts challenges based on your reputation:

```
# Low fame = easier encounters
player_fame = 2
→ "A young goblin warrior challenges you"

# High fame = harder encounters
player_fame = 8
→ "A legendary orc warlord, hearing of your reputation, seeks you out
   to test his strength against yours"
```

## Examples of Simulation in Action

### Example 1: Building Trust

```
> I help the blacksmith retrieve materials from the dangerous cave

CLAUDE: The blacksmith's stern expression softens. "You actually did it.
I... I misjudged you. Thank you."

[blacksmith.affection: 3→5, blacksmith.trust: 5→7,
 blacksmith.annoyance: 8→4, blacksmith.respect: 2→5]

> I try to buy a weapon from the blacksmith

CLAUDE: "Alright, I'll sell to you now. And... since you helped me out,
take 15% off as thanks."

[Discount available due to trust >= 7!]
```

### Example 2: Resource Management

```
> I cast fireball three times in a row

CLAUDE: You unleash magical fire! But you feel your mana reserves
draining rapidly...

[MP: 50→35→20→5]

> I cast fireball again

CLAUDE: You attempt to gather magical energy, but there's nothing left!
Your mana is completely exhausted.

[has_mana: false]

> I try to cast heal

CLAUDE: You cannot cast spells without mana!
[Action blocked: has_mana=false]

> I drink a mana potion

CLAUDE: The magical liquid restores your energy!
[has_mana: true, MP: 5→35]
```

### Example 3: Time-Based Events

```
> I spend the afternoon exploring the forest

CLAUDE: As you venture deeper, you notice the sun sinking lower.
Time passes... it's now evening.

[time_of_day: afternoon→evening]

The forest grows darker and more ominous. You hear howling in the
distance - night creatures are emerging.

[forest_darkness: 5→7]

> I want to return to the village shop

CLAUDE: You return to the village as dusk settles. The shops have
already closed for the night. Lanterns flicker in windows as
villagers retire for the evening.

[market_open: false]
[Action blocked: shops closed at night]
```

### Example 4: Reputation Cascade

```
> I slay the dragon terrorizing the village

CLAUDE: With a final blow, the mighty dragon falls! The village
erupts in celebration!

[dragon_alive: false, player_fame: 3→8,
 monsters_slain: 5→6, villages_saved: 0→1]

The village elder rushes to you: "You've saved us all! You're a
true hero!"

[village_elder.affection: 6→9, village_elder.respect: 5→10,
 village_elder.trust: 7→9]

[village_safe: true, village_prosperity: 5→8]

> I return to the blacksmith who previously hated me

CLAUDE: The blacksmith looks up as you enter. "I heard what you did.
Slaying that dragon... I was wrong about you. You're a true warrior."

[blacksmith.respect: 2→7 (influenced by player_fame)]

"Let me forge you something special, on the house."

[Special quest unlocked due to high fame + high respect!]
```

## Technical Details

### File Location
`rpg_engine/simulation.py`

### Key Classes

- `SimulationEngine` - Main engine managing all systems
- `NPCRelationship` - Tracks one NPC's feelings toward player
- `PlayerConditions` - Player's current states
- `WorldState` - World environmental and event states

### Persistence

Simulation state is saved with the game:
```json
{
  "npcs": {
    "blacksmith": {
      "affection": 3,
      "trust": 5,
      "respect": 2,
      "fear": 0,
      "annoyance": 8
    }
  },
  "player_conditions": {
    "has_mana": true,
    "is_bleeding": false,
    "health_condition": 10
  },
  "world": {
    "time": "midday",
    "weather": "clear",
    "fame": 5
  }
}
```

## For Developers: Adding New Simulation Variables

Want to add new tracked variables? Edit `rpg_engine/simulation.py`:

### Adding a New Player Condition

```python
class PlayerConditions:
    def __init__(self):
        # Add your new condition
        self.is_frozen = False
        self.is_on_fire = False
```

### Adding a New NPC Emotion

```python
class NPCRelationship:
    def __init__(self, npc_id, npc_name):
        # Add new emotion
        self.loyalty = 5  # 0-10

    def update_loyalty(self, delta, reason=""):
        """Change loyalty level"""
        old_value = self.loyalty
        self.loyalty = max(0, min(10, self.loyalty + delta))
        return {"metric": "loyalty", "old_value": old_value,
                "new_value": self.loyalty, "change": delta, "reason": reason}
```

### Adding a New World State

```python
class WorldState:
    def __init__(self):
        # Add new state
        self.moon_phase = "full"  # new, crescent, half, gibbous, full
        self.magical_alignment = "neutral"  # dark, neutral, light
```

Then type `reload` in-game to activate!

## Summary

The simulation engine makes this RPG unique:

✅ **NPCs remember** how you treat them
✅ **Actions have consequences** that persist
✅ **The world evolves** dynamically
✅ **Realistic gating** - can't do things you shouldn't be able to
✅ **Claude actively manages** all variables
✅ **Fully transparent** - you can see all the numbers

This creates an immersive, reactive world where your choices truly matter!

---

**View simulation state anytime:** Type `simulation` or `sim` in-game
