"""
Personality System - Customize the AI Game Master's behavior
Load, save, and manage custom system prompts
"""

import json
import os
from typing import Optional


class PersonalityManager:
    """Manages AI Game Master personalities"""

    def __init__(self, config_dir="/home/user/Claude-AI/personalities"):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)

    def list_personalities(self):
        """List all saved personalities"""
        if not os.path.exists(self.config_dir):
            return []

        files = [f for f in os.listdir(self.config_dir) if f.endswith('.json')]
        personalities = []

        for filename in files:
            try:
                with open(os.path.join(self.config_dir, filename), 'r') as f:
                    data = json.load(f)
                    personalities.append({
                        "id": filename[:-5],  # Remove .json
                        "name": data.get("name", filename[:-5]),
                        "description": data.get("description", "No description")
                    })
            except:
                continue

        return personalities

    def load_personality(self, personality_id: str) -> Optional[str]:
        """Load a personality by ID"""
        filepath = os.path.join(self.config_dir, f"{personality_id}.json")

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get("system_prompt", "")
        except:
            return None

    def save_personality(self, personality_id: str, name: str, description: str, system_prompt: str):
        """Save a personality"""
        filepath = os.path.join(self.config_dir, f"{personality_id}.json")

        data = {
            "name": name,
            "description": description,
            "system_prompt": system_prompt
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def delete_personality(self, personality_id: str):
        """Delete a personality"""
        filepath = os.path.join(self.config_dir, f"{personality_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)


def get_default_personality():
    """Get the default game master personality"""
    return """You are an expert RPG Game Master for a dynamic text-based RPG with REALISTIC SIMULATION.

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


def personality_setup_menu():
    """Interactive menu for selecting/creating personality"""
    manager = PersonalityManager()

    print("\n" + "="*70)
    print("  AI GAME MASTER PERSONALITY CONFIGURATION")
    print("="*70)

    while True:
        print("\nOptions:")
        print("1. Use default personality")
        print("2. Load saved personality")
        print("3. Create new custom personality")
        print("4. Edit existing personality")
        print("5. View personality details")

        choice = input("\nChoice (1-5): ").strip()

        if choice == "1":
            return get_default_personality()

        elif choice == "2":
            personalities = manager.list_personalities()
            if not personalities:
                print("\nNo saved personalities found.")
                continue

            print("\nSaved Personalities:")
            for i, p in enumerate(personalities, 1):
                print(f"{i}. {p['name']} - {p['description']}")

            try:
                idx = int(input(f"\nSelect (1-{len(personalities)}): ").strip()) - 1
                if 0 <= idx < len(personalities):
                    prompt = manager.load_personality(personalities[idx]['id'])
                    if prompt:
                        print(f"\n✓ Loaded: {personalities[idx]['name']}")
                        return prompt
            except:
                print("Invalid selection.")

        elif choice == "3":
            print("\n" + "="*70)
            print("  CREATE CUSTOM PERSONALITY")
            print("="*70)

            name = input("\nPersonality name: ").strip()
            if not name:
                name = "Custom"

            description = input("Short description: ").strip()
            if not description:
                description = "Custom AI personality"

            print("\nEnter your custom system prompt for the AI Game Master.")
            print("This controls how the AI narrates and manages the game.")
            print("Press Enter twice when done (empty line to finish):\n")

            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    lines.pop()  # Remove last empty line
                    break
                lines.append(line)

            system_prompt = "\n".join(lines)

            if system_prompt.strip():
                # Create ID from name
                personality_id = name.lower().replace(" ", "_")
                manager.save_personality(personality_id, name, description, system_prompt)
                print(f"\n✓ Saved as: {name}")
                return system_prompt
            else:
                print("\nNo prompt entered. Using default.")
                return get_default_personality()

        elif choice == "4":
            personalities = manager.list_personalities()
            if not personalities:
                print("\nNo saved personalities found.")
                continue

            print("\nSaved Personalities:")
            for i, p in enumerate(personalities, 1):
                print(f"{i}. {p['name']}")

            try:
                idx = int(input(f"\nSelect to edit (1-{len(personalities)}): ").strip()) - 1
                if 0 <= idx < len(personalities):
                    current_prompt = manager.load_personality(personalities[idx]['id'])

                    print(f"\nCurrent prompt for '{personalities[idx]['name']}':")
                    print("-" * 70)
                    print(current_prompt[:500] + "..." if len(current_prompt) > 500 else current_prompt)
                    print("-" * 70)

                    print("\nEnter new prompt (press Enter twice when done):\n")

                    lines = []
                    while True:
                        line = input()
                        if line == "" and lines and lines[-1] == "":
                            lines.pop()
                            break
                        lines.append(line)

                    new_prompt = "\n".join(lines)

                    if new_prompt.strip():
                        manager.save_personality(
                            personalities[idx]['id'],
                            personalities[idx]['name'],
                            personalities[idx]['description'],
                            new_prompt
                        )
                        print(f"\n✓ Updated: {personalities[idx]['name']}")
            except:
                print("Invalid selection.")

        elif choice == "5":
            personalities = manager.list_personalities()
            if not personalities:
                print("\nNo saved personalities found.")
                continue

            print("\nSaved Personalities:")
            for i, p in enumerate(personalities, 1):
                print(f"{i}. {p['name']}")

            try:
                idx = int(input(f"\nSelect to view (1-{len(personalities)}): ").strip()) - 1
                if 0 <= idx < len(personalities):
                    prompt = manager.load_personality(personalities[idx]['id'])
                    print(f"\n{personalities[idx]['name']}")
                    print(f"Description: {personalities[idx]['description']}")
                    print("\n" + "="*70)
                    print(prompt)
                    print("="*70)
                    input("\nPress Enter to continue...")
            except:
                print("Invalid selection.")

        else:
            print("Invalid choice.")


def quick_custom_prompt():
    """Quick way to enter custom prompt without menu"""
    print("\n" + "="*70)
    print("  CUSTOM AI GAME MASTER PROMPT")
    print("="*70)
    print("\nEnter your custom system prompt (press Enter twice when done):\n")

    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            lines.pop()
            break
        lines.append(line)

    system_prompt = "\n".join(lines)
    return system_prompt if system_prompt.strip() else get_default_personality()
