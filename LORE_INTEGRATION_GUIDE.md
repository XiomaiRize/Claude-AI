# Lore Integration Guide

## How the Lore Connects to Game Systems

This guide explains how the rich world lore integrates with the simulation engine and gameplay mechanics.

## Quick Reference

- **`WORLD_LORE.md`** - Complete historical and cultural documentation
- **`rpg_engine/races.py`** - 7 playable races with mechanics
- **`rpg_engine/classes.py`** - 9-tier class system + Inherited Classes
- **`rpg_engine/simulation.py`** - NPC emotions and world state tracking

---

## Race Selection Impact

When creating a character, race choice affects:

### Immediate Mechanical Effects

**Stat Modifiers** (from `races.py`):
```python
Elf: +20% mana regen, +15% magic resistance
Orc: +30% physical damage, -10% magic affinity
Dwarf: +25% crafting speed, +15% defense
Human: +15% experience gain, can learn ANY race's skills
Dragon-kin: +20% all stats BUT discovery = death
Furry: +20% agility, +30% enhanced senses
```

**Awakening Potential**:
- Age when you awakened determines lifetime potential
- Younger = stronger (1.5x multiplier at youngest)
- Each race has different age ranges (elves awaken at 25-40)

### Simulation Engine Integration

**NPC Reactions** (tracked in `simulation.py`):

Playing as **Elf**:
```
Elven NPCs:
- Start with affection: 7/10, trust: 7/10 (racial kinship)
- Respect ancient wisdom

Human NPCs:
- Neutral affection: 5/10, trust: 5/10
- May seek magical knowledge

Orc NPCs:
- Lower trust: 4/10 (ancient rivalries)
- Respect magical power: 6/10
```

Playing as **Dragon-kin** (EXTREME DANGER):
```
ALL NPCs if discovered:
- Affection: 0/10 (universal hatred)
- Fear: 10/10 (terrified of dragonkin)
- Will report to authorities immediately
- world_state.is_wanted = true
- Universal execution order issued
```

Playing as **Human**:
```
ALL NPCs:
- Generally neutral starting relationships
- Can improve relationships with any race
- Diplomatic bridges built more easily
```

---

## Class System Integration

### Class Tiers and Power

From `classes.py`:

**Power Hierarchy Rule**:
```
Higher Tier > Lower Tier (regardless of awakening rank)

Example:
F-rank [Mythic] Devourer > A-rank [Legendary] God Slayer

Within same tier:
A-rank [Rare] Paladin > E-rank [Rare] Void Walker
```

### How Classes Affect Simulation

**Class-Based NPC Reactions**:

**[Normal] Warrior**:
```
Village Guards: affection +1, respect +1 (fellow warrior)
Merchants: neutral (common class)
Nobles: respect -1 (peasant soldier)
```

**[Legendary] God Slayer**:
```
Religious NPCs: fear +5, respect +8 (killed a god!)
Common folk: fear +7, affection -3 (terrifying)
Divine beings: respect +10, annoyance +10 (you killed their kin)
Player fame: +8 (legendary achievement)
```

**[Mythic] Devourer** (Inherited):
```
ALL NPCs: fear +8 (know the curse)
Ambitious NPCs: annoyance +10 (want to kill you for class)
World state: everyone_wants_to_kill_you = true
Constant assassination attempts
```

---

## Inherited Classes - Special Mechanics

### The Inheritance Curse

From `classes.py`:

**When you have an Inherited Class**:
```python
if player_dies:
    killer.gains_class(inherited_class)
    killer.gains_all_accumulated_power()

Result:
- Everyone knows about the curse
- Every ambitious adventurer wants to kill you
- simulation.world_state.bounty_on_head = MAXIMUM
- NPCs with high respect might still betray you for power
```

### Current World State (Year 2987)

**Sixth Inheritance Active**:
```
Fate Weaver (Godly tier):
- Holder: Unknown human merchant
- Last seen: Year 2756 (231 years ago)
- Ability: Rewrite destinies, manipulate probability
- World status: ALL kingdoms searching

NPC Reactions:
- High paranoia: trust -2 across all NPCs
- Investigations: random identity checks
- Suspicion: anyone too lucky gets questioned
```

**Seventh Inheritance Approaching** (Rumors):
```
world_state.tension_level = HIGH
world_state.inheritance_rumors = true

NPC Behavior Changes:
- Ambitious NPCs: more aggressive
- Scholars: researching inheritance patterns
- Kingdoms: increased military readiness
```

---

## Race-Specific Storylines

### Dragon-kin Survival Story

**If playing as Dragon-kin**:

**Starting Conditions**:
```python
simulation.player_conditions.is_disguised = true
simulation.player_conditions.true_race_hidden = true
world_state.dragonkin_hunt_active = true (always)
```

**Discovery Triggers**:
- Taking too much damage (dragon scales appear)
- Using dragon-specific abilities
- NPC with high perception succeeds check
- Magical detection spells
- Betrayal by someone who knows

**Discovery Consequences**:
```python
def trigger_dragonkin_discovery():
    world_state.player_fame = -10  # Maximum infamy
    world_state.universal_hunt_active = true

    for npc in all_npcs:
        npc.affection = 0
        npc.fear = 10
        npc.will_betray = true

    spawn_assassins(difficulty="EXTREME")
    close_all_shops()
    lock_all_safe_houses()

    return "⚠️ YOUR DRAGONKIN IDENTITY HAS BEEN REVEALED!"
```

**True Dragons Involved**:
```
Hidden true dragons (in disguise):
- Secretly funding your hunt
- Providing intelligence to assassins
- Ensuring no safe locations exist
- Eliminating evidence of "breeding with lesser races"
```

---

## World State Tracking

### How Lore Affects `simulation.py`

**Kingdom Relationships**:
```python
world_state.elf_human_relations = FRIENDLY  # Diplomatic ties
world_state.orc_dwarf_alliance = STRONG  # Forge Brotherhood
world_state.dragonkin_universal_status = HUNTED  # Genocide

# NPC behaviors adjust based on kingdom relations
if player.race == "human" and npc.race == "elf":
    npc.trust += 1  # Diplomatic friendship
```

**Political Climate** (Year 2987):
```python
world_state.year = 2987
world_state.fate_weaver_search_active = true
world_state.inheritance_tension = HIGH
world_state.dragonkin_genocide_formalized = true

# This affects:
- Border security: HEIGHTENED
- Identity checks: FREQUENT
- NPC paranoia: ELEVATED
- Assassination attempts: COMMON (for powerful players)
```

**Technology-Magic Level**:
```python
world_state.magitech_development = "ADVANCED"
world_state.airships_available = true
world_state.magical_communication = true

# Affects:
- Fast travel options
- Information spread speed
- Shop inventory (magitech items available)
```

---

## Example Gameplay Scenarios

### Scenario 1: Elf Mage in Elven Territory

**Character**:
- Race: Elf (awakened age 28 - Early Blessed)
- Class: Mage [Uncommon]
- Location: Silverleaf Dominion

**Simulation State**:
```
Elven NPCs:
├─ Affection: 7/10 (racial kinship)
├─ Trust: 7/10 (fellow elf)
└─ Respect: 6/10 (mage is respected)

Council Members:
├─ Respect: 8/10 (magical knowledge)
├─ Will offer quests
└─ May invite to research projects

world_state.in_elven_territory = true
access_to_ancient_libraries = true
magical_research_bonus = +20%
```

### Scenario 2: Dragon-kin Rogue Hiding in Human Lands

**Character**:
- Race: Dragon-kin (disguised as human)
- Class: Assassin [Rare]
- Location: Human Commonwealth

**Simulation State**:
```
player_conditions:
├─ is_disguised = true
├─ true_race_hidden = true
├─ paranoia_level = 9/10
└─ trust_no_one = true

Human NPCs (if disguise holds):
├─ Affection: 5/10 (appear human)
├─ Trust: 5/10 (neutral)
└─ Suspicion: 2/10 (some notice oddities)

world_state:
├─ dragonkin_bounty = MAXIMUM
├─ assassins_searching = true
└─ safe_locations = ["hidden_human_sympathizer_homes"]

Discovery Risk Factors:
- Taking damage: 30% reveal dragon scales
- Using dragon abilities: 100% reveal
- High perception NPCs: 15% detect
- Magical scanners: 60% detect
```

### Scenario 3: Human with [Legendary] God Slayer

**Character**:
- Race: Human
- Class: God Slayer [Legendary]
- Achievement: Killed minor deity

**Simulation State**:
```
world_state:
├─ player_fame = 9/10 (legendary hero)
├─ divine_beings_hostile = true
└─ commoners_fear_and_respect = true

Religious NPCs:
├─ Affection: 1/10 (killed a god!)
├─ Fear: 9/10 (terrifying power)
├─ Respect: 10/10 (ultimate achievement)
└─ Will NOT attack (too afraid)

Common NPCs:
├─ Affection: 4/10 (scary but impressive)
├─ Fear: 8/10 (god-killer legend)
└─ Respect: 10/10 (ultimate warrior)

Divine Entities:
├─ Will send champions to kill you
├─ Constant divine assassination attempts
└─ Some may offer alliances (pragmatic gods)
```

### Scenario 4: Orc with Inherited [Mythic] Devourer Class

**Character**:
- Race: Orc
- Class: Devourer [Mythic] (Inherited)
- Status: Recently inherited, still weak

**Simulation State**:
```
world_state:
├─ inherited_class_bearer = true
├─ bounty_hunters_active = MAXIMUM
├─ every_kingdom_searching = true
└─ assassination_attempts_per_day = 5-10

ALL NPCs (regardless of race):
├─ Know about the curse
├─ Ambitious ones: will try to kill you
├─ Fearful ones: will betray your location
├─ Even friends: tempted by power

Devourer Mechanics:
├─ Start weak: base stats HALF normal
├─ Each kill: absorb strongest skill
├─ Each class absorbed: gain that class's abilities
└─ After 100 kills: unstoppable world threat

Former Allies:
├─ Affection drops to 3/10 (tempted)
├─ Trust drops to 2/10 (curse too valuable)
└─ 40% chance of betrayal even at max affection
```

---

## Using Lore in Custom Personalities

### Custom Prompt Examples

**Dark Souls Dragon-kin Survivor**:
```
You are narrating for a dragon-kin in hiding.

Constant paranoia - every NPC might discover them
Trust no one completely
Discovery = death, no exceptions
Mention disguise maintenance
Random identity checks
Assassins appear periodically

Track:
- Disguise integrity (damage reveals scales)
- NPC suspicion levels
- Hunter proximity

Make survival feel desperate and tense.
```

**Epic Inheritance Holder**:
```
You narrate for someone with an Inherited [Mythic] class.

Everyone wants to kill them for the power
Constant assassination attempts
Former friends turn on them
Bounty hunters track them
Kingdoms send champions

BUT: They're growing exponentially stronger with each victory

Track:
- Number of absorbed powers
- Assassination attempts survived
- Former allies who've betrayed them
- Power level increasing

Balance: Extreme danger vs ultimate power
```

**Elven Scholar's Journey**:
```
You narrate for an ancient elf (400 years old).

Long-term thinking - decisions echo for centuries
Remember historical events personally
Interact with Council of Ancients
Access to millennium of knowledge

Track:
- Relationships built over decades
- Historical connections
- Ancient knowledge unlocked
- Long-view consequences

Make time feel different for immortal perspective.
```

---

## Quick Integration Checklist

When starting a new game:

✅ **Character Creation**:
- [ ] Choose race (affects NPCs, stats, awakening age)
- [ ] Determine awakening age (affects lifetime potential)
- [ ] Select class tier (affects power hierarchy)
- [ ] Note special conditions (dragonkin = hunted, inherited = cursed)

✅ **Simulation Setup**:
- [ ] Set racial NPC relationships
- [ ] Configure world_state for current year (2987)
- [ ] Enable class-specific flags
- [ ] Track inheritance status if applicable

✅ **Narrative Integration**:
- [ ] Reference historical events (3000 year timeline)
- [ ] Acknowledge racial politics
- [ ] React to class tier appropriately
- [ ] Maintain lore consistency

---

## Developer Notes

### Adding New Content

**New Race**:
1. Add to `rpg_engine/races.py`
2. Define stat modifiers
3. Set awakening parameters
4. Create cultural background
5. Update NPC relationship defaults

**New Class**:
1. Add to `rpg_engine/classes.py`
2. Assign rarity tier
3. Define acquisition method
4. Set stat bonuses and abilities
5. If Inherited: define curse mechanic

**New Historical Event**:
1. Add to timeline in `WORLD_LORE.md`
2. Update world_state flags if current
3. Add NPC dialogue references
4. Consider long-term consequences

### Simulation Variables for Lore

```python
# Racial tracking
world_state.racial_tensions = {}
world_state.kingdom_relations = {}

# Inheritance tracking
world_state.active_inheritances = []
world_state.inheritance_search_active = bool

# Historical flags
world_state.current_year = 2987
world_state.major_events = []

# Dragon-kin genocide
world_state.dragonkin_genocide_active = true (ALWAYS)
world_state.dragonkin_bounty = MAXIMUM
world_state.true_dragons_infiltrated = true (ALWAYS)
```

---

## Summary

The lore integration creates:

✓ **Deep character customization** - Race and class dramatically affect gameplay
✓ **Reactive world** - NPCs respond to your heritage and achievements
✓ **Historical weight** - Your actions matter in a 3000-year timeline
✓ **High-stakes choices** - Dragonkin survival, inheritance curses
✓ **Political intrigue** - Kingdom relations, hidden rulers, genocide
✓ **Power progression** - Clear hierarchy from [Normal] to [Godly]
✓ **Emergent stories** - Lore + simulation = infinite unique narratives

Everything is interconnected:
Race → NPC reactions → Class choices → World events → Your story

**Play the game you want with the personality and lore depth you choose!**
