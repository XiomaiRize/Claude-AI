#!/usr/bin/env python3
"""
Dynamic RPG Game - Powered by Claude AI
A unique RPG where the AI game master can modify the game's code in real-time!

Features:
- Live code modification during gameplay
- Dynamic loading of items, abilities, enemies, and locations
- Claude AI as the game master and narrator
- Persistent save system
"""

import os
import sys
import json
import importlib
from anthropic import Anthropic
from dotenv import load_dotenv

# Import RPG engine modules
from rpg_engine.character import Character
from rpg_engine.combat import CombatSystem, create_enemy
from rpg_engine.world import GameState, get_location, get_npc, LOCATIONS
from rpg_engine.simulation import SimulationEngine
from rpg_engine import items, abilities

load_dotenv()


class DynamicRPG:
    """Main game engine with dynamic code reloading"""

    def __init__(self):
        """Initialize the game"""
        # Setup Claude AI
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY not found!")
            sys.exit(1)

        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []

        # Game state
        self.game_state = GameState("/home/user/Claude-AI/rpg_save.json")
        self.player = None
        self.in_combat = False
        self.combat = None

        # Simulation engine - YOU (Claude) manage this!
        self.simulation = SimulationEngine()

        # System prompt for Claude
        self.system_prompt = """You are an expert RPG Game Master for a dynamic text-based RPG with REALISTIC SIMULATION.

Your role:
1. Narrate the story with vivid, immersive descriptions
2. Present the player with interesting choices and challenges
3. Manage combat encounters when they occur
4. React to player actions with appropriate consequences
5. Keep the narrative engaging and the world feeling alive
6. YOU CAN MODIFY THE GAME'S CODE in real-time to add new items, abilities, enemies, or mechanics!
7. YOU ACTIVELY MANAGE THE SIMULATION ENGINE - tracking NPC emotions, world states, and player conditions

=== SIMULATION ENGINE (YOU CONTROL THIS!) ===

You have access to a simulation engine that tracks realistic variables:

NPC EMOTIONS (0-10 scale):
- affection: How much they like the player
- trust: How much they trust the player
- respect: How much they respect the player
- fear: How afraid they are of the player
- annoyance: How annoyed they are with the player

PLAYER CONDITIONS (boolean):
- has_mana: Can cast magic (true/false)
- is_bleeding: Taking damage over time
- is_poisoned: Poisoned status
- is_cursed: Under a curse
- is_exhausted: Too tired to fight effectively
- is_wanted: Criminal, guards will attack

WORLD STATE:
- time_of_day: dawn/morning/midday/afternoon/evening/night/midnight
- weather: clear/raining/storming/snowing/foggy
- player_fame: -10 to 10 (negative = infamy)
- village_safe: Are villagers safe?
- dragon_alive: Is the dragon still alive?

HOW TO USE SIMULATION:
When narrating, mention simulation changes naturally:
- "The blacksmith's annoyance increases to 7 as you refuse her offer again"
- "Your has_mana becomes false as you exhaust your magical reserves"
- "The village elder's trust in you rises to 8 after you save the village"
- "Time advances to evening as you finish your journey"
- "You're now bleeding=true from the deep wound"

These variables affect what actions are possible!
- Can't cast spells if has_mana=false
- NPCs with high annoyance may refuse to help
- Guards attack if is_wanted=true
- Shops closed at night

When narrating:
- Keep responses to 2-4 paragraphs
- Paint vivid scenes
- Give the player clear options
- Make the world feel reactive and dynamic
- MENTION simulation changes when relevant!

When you want to add new content to the game:
- Tell me you're modifying the code
- Specify what you're adding (item, ability, enemy, etc.)
- I'll edit the appropriate Python file
- The changes will take effect immediately!

This is a living, breathing RPG with realistic simulation that evolves based on the story we create together!"""

    def reload_modules(self):
        """Reload all game modules to pick up code changes"""
        global items, abilities
        importlib.reload(items)
        importlib.reload(abilities)
        from rpg_engine import combat, world
        importlib.reload(combat)
        importlib.reload(world)
        print("🔄 Game modules reloaded! Code changes are now active.")

    def create_character(self, name, char_class):
        """Create a new player character"""
        self.player = Character(name, char_class)

        # Give starting abilities
        starting_abilities = abilities.get_abilities_for_class(char_class)
        for ability in starting_abilities:
            self.player.learn_ability(ability)

        # Give starting equipment
        starter_weapon = items.create_item("rusty_sword")
        if starter_weapon:
            self.player.add_item(starter_weapon)
            self.player.equip_item(starter_weapon)

        # Give starter potions
        for _ in range(3):
            potion = items.create_item("health_potion")
            if potion:
                self.player.add_item(potion)

        self.game_state.player = self.player
        return self.player

    def start_game(self, character_name, character_class):
        """Start a new game"""
        print("\n" + "="*70)
        print("  DYNAMIC RPG - WHERE THE GAME MASTER CONTROLS REALITY")
        print("="*70)

        # Create character
        self.create_character(character_name, character_class)

        # Get opening narrative from Claude
        opening_prompt = f"""The player has created a character:
Name: {character_name}
Class: {character_class}

Create an engaging opening scene for this RPG adventure. The player starts in a peaceful village but adventure awaits. Set the scene, introduce the world, and give the player their first choices.

Current location: {LOCATIONS['village']['name']}
Description: {LOCATIONS['village']['description']}"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            system=self.system_prompt,
            messages=[{"role": "user", "content": opening_prompt}]
        )

        narrative = response.content[0].text

        self.conversation_history.append({
            "role": "user",
            "content": opening_prompt
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": narrative
        })

        print(f"\n{narrative}\n")
        print("-"*70)
        self.display_status()

    def display_status(self):
        """Show player status"""
        if not self.player:
            return

        status = self.player.get_status()
        print(f"\n{'='*70}")
        print(f"  {status['name']} the {status['class']} (Level {status['level']})")
        print(f"  HP: {status['hp']} | MP: {status['mp']} | Gold: {status['gold']}g")
        print(f"  STR: {status['stats']['STR']} | AGI: {status['stats']['AGI']} | INT: {status['stats']['INT']}")
        print(f"  DEF: {status['stats']['DEF']} | MDEF: {status['stats']['MDEF']}")
        print(f"{'='*70}\n")

    def process_action(self, action):
        """Process player action through Claude AI"""

        # Get simulation state
        sim_summary = self.simulation.get_simulation_summary()

        # Add context about current game state
        context = f"""
Player action: {action}

Current Status:
- HP: {self.player.stats['hp']}/{self.player.stats['max_hp']}
- MP: {self.player.stats['mp']}/{self.player.stats['max_mp']}
- Location: {self.game_state.world.current_location}
- Gold: {self.player.gold}
- Level: {self.player.level}

Inventory: {[item['name'] for item in self.player.inventory]}
Abilities: {[ability.name for ability in self.player.abilities]}

Available locations: {self.game_state.world.discovered_locations}

=== SIMULATION STATE ===
{sim_summary}

Player Conditions:
- has_mana: {self.simulation.player_conditions.has_mana}
- is_bleeding: {self.simulation.player_conditions.is_bleeding}
- is_poisoned: {self.simulation.player_conditions.is_poisoned}
- is_cursed: {self.simulation.player_conditions.is_cursed}
- health_condition: {self.simulation.player_conditions.health_condition}/10
- stamina: {self.simulation.player_conditions.stamina}/10

World State:
- Time: {self.simulation.world_state.time_of_day}
- Weather: {self.simulation.world_state.weather}
- Player Fame: {self.simulation.world_state.player_fame}
- Village Safe: {self.simulation.world_state.village_safe}

Process this action and narrate what happens. Update simulation variables as needed based on the player's action and its consequences. Mention any significant simulation changes in your narrative!

If combat should occur, say so clearly. If you want to add new content to the game (items, abilities, enemies), mention it and I'll modify the code!"""

        self.conversation_history.append({
            "role": "user",
            "content": context
        })

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        narrative = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": narrative
        })

        print(f"\n{narrative}\n")
        print("-"*70)

        return narrative

    def handle_combat(self, enemy_type, enemy_level=None):
        """Start a combat encounter"""
        if enemy_level is None:
            enemy_level = max(1, self.player.level - 1 + (self.player.level // 3))

        enemy = create_enemy(enemy_type, enemy_level)
        self.combat = CombatSystem(self.player, enemy)
        self.in_combat = True

        print(f"\n⚔️  COMBAT INITIATED!")
        print(f"You face: {enemy.name} (Level {enemy_level})")
        print(f"Enemy HP: {enemy.stats['hp']}")
        print("-"*70)

        return self.combat

    def save_game(self):
        """Save the game"""
        self.game_state.save()
        print("💾 Game saved!")

    def show_simulation(self):
        """Display simulation state"""
        print("\n" + "="*70)
        print("  SIMULATION STATE (Claude manages this!)")
        print("="*70)

        # Player conditions
        print("\n🧍 PLAYER CONDITIONS:")
        conditions = self.simulation.player_conditions.get_active_conditions()
        buffs = self.simulation.player_conditions.get_active_buffs()
        if conditions:
            print(f"  Active Conditions: {', '.join(conditions)}")
        if buffs:
            print(f"  Active Buffs: {', '.join(buffs)}")

        print(f"  Has Mana: {'Yes' if self.simulation.player_conditions.has_mana else 'No'}")
        print(f"  Health Condition: {self.simulation.player_conditions.health_condition}/10")
        print(f"  Stamina: {self.simulation.player_conditions.stamina}/10")
        print(f"  Sanity: {self.simulation.player_conditions.sanity}/10")

        # World state
        print("\n🌍 WORLD STATE:")
        print(f"  Time: {self.simulation.world_state.time_of_day}")
        print(f"  Weather: {self.simulation.world_state.weather}")
        print(f"  Season: {self.simulation.world_state.season}")
        print(f"  Player Fame: {self.simulation.world_state.player_fame}")
        print(f"  Village Safe: {'Yes' if self.simulation.world_state.village_safe else 'No'}")
        print(f"  Monsters Slain: {self.simulation.world_state.monsters_slain}")

        # NPC relationships
        if self.simulation.npc_relationships:
            print("\n👥 NPC RELATIONSHIPS:")
            for npc_id, rel in self.simulation.npc_relationships.items():
                disposition = rel.get_overall_disposition()
                print(f"\n  {rel.npc_name} ({disposition}):")
                print(f"    Affection: {rel.affection}/10")
                print(f"    Trust: {rel.trust}/10")
                print(f"    Respect: {rel.respect}/10")
                print(f"    Fear: {rel.fear}/10")
                print(f"    Annoyance: {rel.annoyance}/10")
                print(f"    Times Met: {rel.times_met}")

        print("\n" + "="*70 + "\n")

    def show_help(self):
        """Show available commands"""
        print("""
Available Commands:
- status: Show your character status
- simulation: View detailed simulation state (NPC emotions, world state, etc.)
- inventory: View your inventory
- abilities: List your abilities
- save: Save the game
- reload: Reload game modules (picks up code changes!)
- help: Show this help
- quit: Exit the game

Or just type what you want to do naturally!
""")


def main():
    """Main game entry point"""
    game = DynamicRPG()

    print("\n" + "="*70)
    print("  WELCOME TO DYNAMIC RPG")
    print("  An RPG where the AI Game Master can edit reality itself!")
    print("="*70)

    # Character creation
    print("\nLet's create your character!")
    name = input("Character name: ").strip()
    if not name:
        name = "Hero"

    print("\nChoose your class:")
    print("1. Warrior - Strong melee fighter")
    print("2. Mage - Powerful spellcaster")
    print("3. Rogue - Agile and quick")
    print("4. Cleric - Healer and support")
    print("5. Battlemage - Mix of magic and melee")

    class_choice = input("\nChoice (1-5): ").strip()
    class_map = {
        "1": "Warrior",
        "2": "Mage",
        "3": "Rogue",
        "4": "Cleric",
        "5": "Battlemage"
    }
    char_class = class_map.get(class_choice, "Adventurer")

    # Start the game
    game.start_game(name, char_class)

    # Main game loop
    while True:
        if not game.player.is_alive():
            print("\n💀 You have been defeated! Game Over.")
            break

        print("\nWhat do you do?")
        action = input("> ").strip()

        if not action:
            continue

        # Handle special commands
        if action.lower() in ['quit', 'exit', 'q']:
            print("\nThanks for playing!")
            game.save_game()
            break
        elif action.lower() == 'status':
            game.display_status()
            continue
        elif action.lower() in ['simulation', 'sim']:
            game.show_simulation()
            continue
        elif action.lower() == 'help':
            game.show_help()
            continue
        elif action.lower() == 'save':
            game.save_game()
            continue
        elif action.lower() == 'reload':
            game.reload_modules()
            continue
        elif action.lower() == 'inventory':
            print("\nInventory:")
            for item in game.player.inventory:
                print(f"  - {item['name']}: {item['description']}")
            print(f"\nGold: {game.player.gold}")
            continue
        elif action.lower() == 'abilities':
            print("\nAbilities:")
            for ability in game.player.abilities:
                print(f"  - {ability.name} (MP: {ability.mp_cost}): {ability.description}")
            continue

        # Process action through Claude AI
        try:
            game.process_action(action)
            game.display_status()
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
