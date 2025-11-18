"""
Game World & State - Locations, quests, and dynamic events
LIVE EDITABLE: Add new locations, quests, and events during gameplay!
"""

import json
import os


class GameWorld:
    """Manages game world state, locations, and progression"""

    def __init__(self):
        self.current_location = "village"
        self.discovered_locations = ["village"]
        self.quests = []
        self.flags = {}  # For tracking game events
        self.npcs_met = []

    def discover_location(self, location_id):
        """Unlock a new location"""
        if location_id not in self.discovered_locations:
            self.discovered_locations.append(location_id)
            return True
        return False

    def set_flag(self, flag_name, value=True):
        """Set a game flag"""
        self.flags[flag_name] = value

    def get_flag(self, flag_name):
        """Get a game flag"""
        return self.flags.get(flag_name, False)

    def add_quest(self, quest):
        """Add a quest to the quest log"""
        self.quests.append(quest)

    def complete_quest(self, quest_id):
        """Mark a quest as complete"""
        for quest in self.quests:
            if quest["id"] == quest_id:
                quest["completed"] = True
                return True
        return False


# Location Database (ADD NEW LOCATIONS HERE!)
LOCATIONS = {
    "village": {
        "name": "Peaceful Village",
        "description": "A quiet village where your adventure begins. Thatched roofs, a central fountain, and friendly villagers create a welcoming atmosphere.",
        "connections": ["forest", "shop"],
        "npcs": ["village_elder", "blacksmith"],
        "events": ["village_introduction"]
    },

    "forest": {
        "name": "Dark Forest",
        "description": "Ancient trees block out the sunlight. You hear rustling in the undergrowth. Danger lurks here, but so do opportunities for adventure.",
        "connections": ["village", "cave", "clearing"],
        "enemies": ["goblin", "slime"],
        "events": ["forest_encounter"]
    },

    "cave": {
        "name": "Mysterious Cave",
        "description": "A dark cavern with glittering crystals on the walls. The air is damp and cold, and you can hear water dripping somewhere in the darkness.",
        "connections": ["forest", "deep_cave"],
        "enemies": ["skeleton", "orc"],
        "items": ["health_potion", "iron_sword"],
        "events": ["cave_exploration"]
    },

    "deep_cave": {
        "name": "Deep Cave",
        "description": "The deepest part of the cave system. Ancient ruins suggest this was once something more. A powerful presence can be felt here.",
        "connections": ["cave"],
        "enemies": ["dragon"],
        "items": ["steel_sword", "elixir"],
        "boss": True
    },

    "clearing": {
        "name": "Sunlit Clearing",
        "description": "A peaceful clearing in the forest where sunlight breaks through. Wildflowers grow here, and the air is fresh and clean.",
        "connections": ["forest"],
        "npcs": ["mysterious_merchant"],
        "events": ["merchant_encounter"]
    },

    "shop": {
        "name": "Village Shop",
        "description": "A cozy shop filled with adventuring supplies, weapons, and potions. The shopkeeper greets you warmly.",
        "connections": ["village"],
        "npcs": ["shopkeeper"],
        "shop": True
    }
}


# NPC Database (ADD NEW NPCs HERE!)
NPCS = {
    "village_elder": {
        "name": "Village Elder",
        "description": "A wise old man with a long white beard",
        "dialogue": [
            "Welcome, traveler! Our village has been peaceful, but dark forces stir in the forest.",
            "The ancient cave holds many secrets. Be careful if you venture there.",
            "You have the look of a hero about you. I sense great potential in you."
        ],
        "quests": ["clear_forest"]
    },

    "blacksmith": {
        "name": "Blacksmith",
        "description": "A muscular woman with soot-covered arms",
        "dialogue": [
            "Looking for quality weapons? You've come to the right place!",
            "I can upgrade your equipment if you bring me the right materials.",
            "Heard there's good ore in those caves. Dangerous though."
        ],
        "shop_items": ["iron_sword", "leather_armor", "iron_armor"]
    },

    "shopkeeper": {
        "name": "Shopkeeper",
        "description": "A cheerful merchant with a ready smile",
        "dialogue": [
            "Welcome to my shop! Everything an adventurer needs!",
            "Potions are essential for survival. Stock up!",
            "I've got some rare items if you've got the gold."
        ],
        "shop_items": ["health_potion", "mana_potion", "rusty_sword", "leather_armor"]
    },

    "mysterious_merchant": {
        "name": "Mysterious Merchant",
        "description": "A hooded figure with glowing eyes",
        "dialogue": [
            "Greetings, traveler. I have... special items for those brave enough to pay the price.",
            "Power comes at a cost. Are you willing to pay it?",
            "The strongest items require the strongest wills."
        ],
        "shop_items": ["steel_sword", "mage_robes", "power_ring", "wisdom_amulet", "elixir"]
    }
}


# Quest Database (ADD NEW QUESTS HERE!)
QUESTS = {
    "clear_forest": {
        "id": "clear_forest",
        "name": "Clear the Dark Forest",
        "description": "The village elder asks you to defeat the monsters in the Dark Forest",
        "objectives": ["Defeat 5 enemies in the forest"],
        "rewards": {"gold": 100, "exp": 150},
        "completed": False
    },

    "explore_cave": {
        "id": "explore_cave",
        "name": "Explore the Mysterious Cave",
        "description": "Investigate the ancient cave and discover its secrets",
        "objectives": ["Enter the cave", "Reach the deep cave"],
        "rewards": {"gold": 200, "exp": 250},
        "completed": False
    },

    "slay_dragon": {
        "id": "slay_dragon",
        "name": "Slay the Dragon",
        "description": "Defeat the dragon that dwells in the deep cave",
        "objectives": ["Defeat the dragon"],
        "rewards": {"gold": 1000, "exp": 500},
        "completed": False
    }
}


def get_location(location_id):
    """Get location data"""
    return LOCATIONS.get(location_id)


def get_npc(npc_id):
    """Get NPC data"""
    return NPCS.get(npc_id)


def get_quest(quest_id):
    """Get quest data"""
    return QUESTS.get(quest_id)


class GameState:
    """Persistent game state"""

    def __init__(self, save_file="game_save.json"):
        self.save_file = save_file
        self.player = None
        self.world = GameWorld()
        self.turn_count = 0

    def save(self):
        """Save game state to file"""
        if not self.player:
            return

        state = {
            "player": {
                "name": self.player.name,
                "class": self.player.char_class,
                "level": self.player.level,
                "experience": self.player.experience,
                "stats": self.player.stats,
                "inventory": self.player.inventory,
                "gold": self.player.gold,
                "equipped": self.player.equipped,
                "abilities": [a.name for a in self.player.abilities]
            },
            "world": {
                "current_location": self.world.current_location,
                "discovered_locations": self.world.discovered_locations,
                "flags": self.world.flags,
                "npcs_met": self.world.npcs_met,
                "quests": self.world.quests
            },
            "turn_count": self.turn_count
        }

        with open(self.save_file, 'w') as f:
            json.dump(state, f, indent=2)

    def load(self):
        """Load game state from file"""
        if not os.path.exists(self.save_file):
            return False

        with open(self.save_file, 'r') as f:
            state = json.load(f)

        # Restore world
        self.world.current_location = state["world"]["current_location"]
        self.world.discovered_locations = state["world"]["discovered_locations"]
        self.world.flags = state["world"]["flags"]
        self.world.npcs_met = state["world"]["npcs_met"]
        self.world.quests = state["world"]["quests"]
        self.turn_count = state["turn_count"]

        return True

    def delete_save(self):
        """Delete save file"""
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
