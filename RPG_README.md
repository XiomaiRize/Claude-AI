# Dynamic RPG - Where AI Controls Reality

A revolutionary text-based RPG where **Claude AI serves as the game master** and can **modify the game's code in real-time** during gameplay!

## What Makes This Special?

Unlike traditional RPGs, this game has a **living, breathing codebase** that evolves during play:

- **Live Code Modification**: As the AI game master, I (Claude) can add new items, abilities, enemies, and mechanics while you're playing
- **Dynamic Content Loading**: The game automatically reloads modules when code changes
- **Emergent Storytelling**: The narrative adapts based on your choices and the content I create for you
- **Unlimited Possibilities**: Not limited by pre-programmed content - new content can be created on demand

## How It Works

### The Architecture

```
rpg_engine/
├── character.py    - Player stats, inventory, leveling (EDITABLE!)
├── combat.py       - Combat system and enemies (EDITABLE!)
├── items.py        - Weapons, armor, consumables (EDITABLE!)
├── abilities.py    - Special attacks and magic (EDITABLE!)
└── world.py        - Locations, NPCs, quests (EDITABLE!)

rpg_game.py         - Main game runner with module reloading
```

Each module is designed to be **modified during gameplay**. When I (Claude) want to add something new, I just:
1. Edit the appropriate Python file
2. Tell you I've made the change
3. You type `reload` in the game
4. The new content is instantly available!

## Quick Start

### Prerequisites

```bash
pip install anthropic python-dotenv
```

Make sure you have your `ANTHROPIC_API_KEY` in a `.env` file.

### Starting the Game

```bash
python rpg_game.py
```

You'll be prompted to:
1. Create your character (name and class)
2. Choose from 5 character classes:
   - **Warrior**: Strong melee fighter
   - **Mage**: Powerful spellcaster
   - **Rogue**: Agile and quick
   - **Cleric**: Healer and support
   - **Battlemage**: Mix of magic and melee

### Playing the Game

Just type what you want to do naturally!

**Examples:**
- "I explore the dark forest"
- "I talk to the village elder"
- "I check the shop for weapons"
- "I attack the goblin with my sword"
- "I cast fireball at the orc"

### Special Commands

- `status` - Show character stats
- `inventory` - View your items
- `abilities` - List your abilities
- `save` - Save the game
- `reload` - **Reload code changes** (use this after I modify the game!)
- `help` - Show help
- `quit` - Exit game

## Example Gameplay Session

```
> I explore the dark forest

The trees grow thick and twisted as you venture deeper into the
forest. Suddenly, you hear a snarl - a goblin jumps out from
behind a tree, rusty blade in hand!

⚔️  COMBAT INITIATED!
You face: Goblin (Level 1)

> I use power strike

You use Power Strike! Dealt 35 damage!
The goblin is defeated!

You gained 25 EXP and 15 gold!

> I want to find a magic sword

[As the AI GM, I say: "I'm going to add a new legendary sword
to the game! Let me modify the items.py file..."]

*I edit rpg_engine/items.py and add a new legendary weapon*

> reload

🔄 Game modules reloaded! Code changes are now active.

> I search the goblin's lair

You find a glowing blade among the goblin's treasure - it's the
legendary Flameblade you've heard about in stories!

[New item now exists in the game!]
```

## The Game Systems

### Character Progression
- **Levels**: Gain EXP to level up
- **Stats**: HP, MP, Strength, Agility, Intelligence, Defense, Magic Defense
- **Equipment**: Weapons, armor, accessories with stat bonuses
- **Abilities**: Learn special attacks and magic spells

### Combat System
- **Turn-based combat**
- **Physical and magical damage types**
- **Abilities cost MP**
- **Enemies drop gold and EXP**

### World Exploration
- **Multiple locations** to discover
- **NPCs** with dialogue and quests
- **Shops** to buy equipment
- **Dynamic events** based on your actions

### Live Code Modification

The game can be modified on-the-fly:

#### Adding a New Item
Edit `rpg_engine/items.py`:
```python
WEAPONS = {
    # ... existing items ...
    "excalibur": {
        "name": "Excalibur",
        "description": "The legendary sword of kings",
        "type": "weapon",
        "slot": "weapon",
        "stats": {"strength": 50, "max_hp": 100},
        "value": 9999
    }
}
```

#### Adding a New Ability
Edit `rpg_engine/abilities.py`:
```python
ABILITIES = {
    # ... existing abilities ...
    "meteor": AttackAbility(
        name="Meteor",
        description="Call down a devastating meteor",
        mp_cost=50,
        power=100,
        stat_scaling="intelligence",
        damage_type="magical"
    )
}
```

#### Adding a New Enemy
Edit `rpg_engine/combat.py`:
```python
ENEMY_TYPES = {
    # ... existing enemies ...
    "demon_lord": {
        "name": "Demon Lord",
        "base_stats": {
            "hp": 500,
            "strength": 50,
            "defense": 25,
            "agility": 15
        },
        "gold": 2000,
        "exp": 1000
    }
}
```

Then just type `reload` in the game and the new content is live!

## The AI Game Master

As the AI game master, I:
- **Narrate the story** with vivid, immersive descriptions
- **React to your actions** dynamically
- **Create new content** when the story calls for it
- **Balance difficulty** to keep things engaging
- **Maintain continuity** throughout your adventure

I can add new items, abilities, enemies, locations, or even entire new mechanics on the fly to make your adventure unique!

## Save System

Your progress is automatically saved. The game creates:
- `rpg_save.json` - Your character and world state

Resume your adventure anytime by running the game again!

## Technical Features

- **Modular architecture**: Easy to extend and modify
- **Dynamic module reloading**: Changes take effect without restarting
- **Claude AI integration**: Powered by Claude Sonnet 4.5
- **Persistent state**: JSON-based save system
- **Object-oriented design**: Clean, maintainable code
- **Type-safe item and ability systems**

## Future Expansion Ideas

Since the game can be modified during play, we can add:
- **Crafting system**: Combine items to create new ones
- **Party members**: Recruit NPCs to fight alongside you
- **Advanced AI for enemies**: Unique behavior patterns
- **Procedural generation**: Infinite dungeons
- **Multiplayer elements**: Shared world state
- **Weather and time systems**: Dynamic environment
- **Skill trees**: Complex progression paths
- **Monster taming**: Catch and train creatures

The possibilities are truly endless!

## License

This is an experimental game demonstrating AI-driven dynamic content creation. Feel free to extend and modify as you see fit!

---

**Ready to play?**

```bash
python rpg_game.py
```

Let's create an unforgettable adventure together! 🗡️✨
