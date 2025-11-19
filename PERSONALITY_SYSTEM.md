# AI Game Master Personality System

## Overview

The Dynamic RPG now includes a **fully customizable AI Game Master personality system**. You have complete control over how the AI narrates your game by providing your own custom system prompt!

## How It Works

When you start the game (`python rpg_game.py`), you'll see a personality configuration menu with these options:

### Menu Options

```
======================================================================
  AI GAME MASTER PERSONALITY CONFIGURATION
======================================================================

Options:
1. Use default personality
2. Load saved personality
3. Create new custom personality
4. Edit existing personality
5. View personality details
```

## Option 1: Use Default Personality

The default personality is a balanced game master that:
- Narrates with vivid, immersive descriptions
- Manages the simulation engine (NPC emotions, world state, conditions)
- Can modify game code in real-time
- Keeps responses to 2-4 paragraphs
- Presents clear choices and consequences

**Use this if**: You want the standard RPG experience

## Option 2: Load Saved Personality

Load a previously saved custom personality from your library.

**How to use:**
1. Select option 2
2. Choose from your saved personalities
3. The game will use that personality for the AI Game Master

Personalities are saved in: `/home/user/Claude-AI/personalities/`

## Option 3: Create New Custom Personality

**This is where you write your own AI Game Master behavior!**

### Steps:

1. Select option 3
2. Enter a name for your personality (e.g., "Dark Souls Style")
3. Enter a short description (e.g., "Brutal, unforgiving narrator")
4. Enter your custom system prompt
5. Press Enter twice (empty line) to finish

### Custom Prompt Example

Here's an example of a custom personality:

```
You are a brutal, unforgiving Game Master for a dark fantasy RPG.

Your style:
- Narrate with grim, atmospheric descriptions
- The world is harsh and uncaring
- NPCs are suspicious and self-serving
- Combat is deadly - one mistake can be fatal
- No hand-holding - players must figure things out
- Emphasize consequences of every action
- Dark humor and irony in narration

Manage the simulation engine:
- NPCs quickly become annoyed or fearful
- The world is dangerous (high forest_darkness)
- Player fame is hard to gain, easy to lose
- Mention simulation changes in a grim tone

Example narration:
"The blacksmith eyes you with suspicion. 'You want a weapon? Pay triple
or get out.' [blacksmith.annoyance: 5→7, blacksmith.trust: 5→3]"

Make every choice matter. Make death feel close.
```

### Writing Tips

Your custom prompt can control:

**Narrative Style:**
- Tone (serious, humorous, dark, lighthearted)
- Length (brief, detailed, epic)
- Perspective (objective narrator, character-driven)

**Simulation Management:**
- How quickly NPC emotions change
- How harsh or forgiving the world is
- How fame/infamy is gained/lost
- Weather and time progression speed

**Game Difficulty:**
- Combat lethality
- Resource scarcity
- Puzzle complexity
- Consequences severity

**Content Type:**
- Fantasy, sci-fi, horror, comedy
- Realistic vs. fantastical
- Serious vs. silly
- Gritty vs. whimsical

### Example Custom Personalities

#### Comedy/Anime Style
```
You are an over-the-top anime-style Game Master.

Style:
- Dramatic, exaggerated narration
- Lots of action and fanservice
- NPCs have extreme personalities
- Combat has cool named attacks
- Everything is turned up to 11

Simulation:
- NPC emotions swing wildly
- Affection can go from 0 to 10 in one action
- The world is colorful and chaotic
- Fame increases quickly for dramatic actions

Narrate like an anime episode!
```

#### Lovecraftian Horror
```
You are a cosmic horror Game Master in the style of H.P. Lovecraft.

Style:
- Emphasis on the unknowable and terrifying
- Atmosphere of creeping dread
- NPCs are either oblivious or slowly going mad
- Describe things that defy comprehension
- Sanity is constantly at risk

Simulation:
- Track sanity stat closely - decrease it often
- NPCs slowly become more fearful/paranoid
- Weather is often foggy, storms, unnatural
- Unknown things lurk in the shadows
- Corruption increases when using forbidden knowledge

Make players question reality itself.
```

#### Wholesome Adventure
```
You are a warm, friendly Game Master for a cozy adventure.

Style:
- Kind, encouraging narration
- NPCs are generally friendly and helpful
- Focus on exploration and discovery
- Combat is light - more about problem-solving
- Celebrate small victories

Simulation:
- NPCs have high starting affection and trust
- World is generally safe and welcoming
- Weather is pleasant most of the time
- Fame builds through helping others

Create a comforting, feel-good adventure!
```

## Option 4: Edit Existing Personality

Modify a saved personality:
1. Select option 4
2. Choose which personality to edit
3. View the current prompt
4. Enter the new version
5. Press Enter twice to save

## Option 5: View Personality Details

View the full system prompt of any saved personality without loading it.

## File Structure

Personalities are saved as JSON files:

```json
{
  "name": "Dark Souls Style",
  "description": "Brutal, unforgiving narrator",
  "system_prompt": "You are a brutal, unforgiving Game Master..."
}
```

Location: `/home/user/Claude-AI/personalities/<name>.json`

## Advanced: Direct File Creation

You can also create personalities by directly creating JSON files:

1. Create a file in `/home/user/Claude-AI/personalities/`
2. Name it something like `my_style.json`
3. Use this structure:

```json
{
  "name": "My Custom Style",
  "description": "Description here",
  "system_prompt": "Your full system prompt here...\n\nCan span multiple lines..."
}
```

4. Load it using option 2 in the menu

## What You Can Control

Your custom prompt can specify:

### Narrative Elements
- Writing style and tone
- Response length (brief, medium, epic)
- Descriptive detail level
- Dialogue style for NPCs
- Pacing (fast action vs. slow exploration)

### Simulation Behavior
- How NPC emotions change
- Default world states (time, weather, danger)
- How quickly fame/infamy changes
- Economic conditions (prices, availability)
- Magic availability and rules

### Game Mechanics
- Combat difficulty and lethality
- Resource management strictness
- Puzzle complexity
- Consequences for failure
- Rewards for success

### Content Guidelines
- Genre (fantasy, sci-fi, horror, etc.)
- Maturity level
- Humor style
- Realism vs. fantastical elements
- Character agency

### Special Instructions
- When to create new items/abilities
- How to handle player mistakes
- Creative freedom vs. structure
- Meta-game awareness
- 4th wall breaks

## Examples in Practice

### Default Personality in Action
```
> I talk to the blacksmith

You approach the village blacksmith, a muscular woman with soot-covered
arms. She looks up from her forge and nods at you. "Looking for weapons?
I've got some basics in stock."

[blacksmith.affection: 5, trust: 5 - neutral disposition]
```

### Dark Souls Personality
```
> I talk to the blacksmith

The scarred woman barely glances at you, hammer striking hot steel with
rhythmic precision. After a long silence, she grunts. "Coin first. Trust
earned in blood, not words."

[blacksmith.affection: 2, trust: 1, annoyance: 3 - deeply unfriendly]
```

### Comedy Anime Personality
```
> I talk to the blacksmith

"WELCOME!" The blacksmith strikes a dramatic pose, her hammer gleaming in
the sunlight. "I am the LEGENDARY SMITH OF ULTIMATE DESTINY! You! You have
the eyes of a WARRIOR! Let me forge you a blade that will PIERCE THE
HEAVENS!"

[blacksmith.affection: 7, respect: 4, annoyance: 0 - enthusiastically
friendly! But is she for real...?]
```

## Tips for Writing Great Prompts

1. **Be Specific**: Clearly state your desired tone and style
2. **Give Examples**: Show the AI what you want with examples
3. **Set Boundaries**: Specify what you don't want
4. **Include Simulation**: Tell the AI how to manage emotions and world state
5. **Test and Iterate**: Try it, then edit if needed
6. **Balance**: Don't make it too restrictive or too loose

## Default Prompt Reference

The default prompt includes:
- Vivid, immersive narration (2-4 paragraphs)
- Simulation engine management
- NPC emotion tracking
- World state tracking
- Clear player choices
- Live code modification capability
- Reactive world dynamics

You can use this as a template and modify parts!

## Frequently Asked Questions

### Can I switch personalities mid-game?
Not currently - you'd need to restart the game with a new personality.

### Can I have multiple personalities?
Yes! Save as many as you want and switch between them for different playthroughs.

### What if I make a mistake in my prompt?
Use option 4 to edit it, or delete the JSON file and recreate it.

### Can I share personalities with others?
Yes! Just share the JSON file from the personalities folder.

### What's the character limit for prompts?
There's no hard limit, but keep it reasonable (under 2000 words).

### Can I tell the AI to ignore the simulation engine?
Yes, but it's not recommended - the simulation makes the game more immersive.

### Can I make the AI more creative with items/abilities?
Absolutely! Add instructions like "Frequently create new legendary items"
or "Invent unique abilities on demand."

## Troubleshooting

**AI isn't following my prompt:**
- Make your instructions more specific
- Give examples of what you want
- Check for conflicting instructions

**Personality file won't load:**
- Check JSON syntax (use a validator)
- Make sure file is in the personalities folder
- Ensure filename ends with `.json`

**AI is too verbose/brief:**
- Explicitly state desired response length
- Give examples of your preferred length

---

**Have fun creating unique Game Master personalities!**

Your imagination is the only limit. 🎮✨
