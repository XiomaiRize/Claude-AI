"""
Item Database - Weapons, armor, consumables, and treasures
LIVE EDITABLE: Add new items during gameplay by editing this file!
"""

# Weapons
WEAPONS = {
    "rusty_sword": {
        "name": "Rusty Sword",
        "description": "A worn blade, but better than bare fists",
        "type": "weapon",
        "slot": "weapon",
        "stats": {"strength": 5},
        "value": 50
    },
    "iron_sword": {
        "name": "Iron Sword",
        "description": "A sturdy iron blade",
        "type": "weapon",
        "slot": "weapon",
        "stats": {"strength": 12},
        "value": 200
    },
    "steel_sword": {
        "name": "Steel Sword",
        "description": "A well-crafted steel weapon",
        "type": "weapon",
        "slot": "weapon",
        "stats": {"strength": 20},
        "value": 500
    },
    "magic_staff": {
        "name": "Magic Staff",
        "description": "A staff imbued with magical energy",
        "type": "weapon",
        "slot": "weapon",
        "stats": {"intelligence": 15, "max_mp": 20},
        "value": 400
    }
}

# Armor
ARMOR = {
    "leather_armor": {
        "name": "Leather Armor",
        "description": "Basic leather protection",
        "type": "armor",
        "slot": "armor",
        "stats": {"defense": 5, "max_hp": 20},
        "value": 100
    },
    "iron_armor": {
        "name": "Iron Armor",
        "description": "Heavy iron plating",
        "type": "armor",
        "slot": "armor",
        "stats": {"defense": 12, "max_hp": 50},
        "value": 300
    },
    "mage_robes": {
        "name": "Mage Robes",
        "description": "Enchanted robes for spellcasters",
        "type": "armor",
        "slot": "armor",
        "stats": {"magic_defense": 10, "intelligence": 5, "max_mp": 30},
        "value": 350
    }
}

# Accessories
ACCESSORIES = {
    "power_ring": {
        "name": "Ring of Power",
        "description": "Increases physical strength",
        "type": "accessory",
        "slot": "accessory",
        "stats": {"strength": 8},
        "value": 250
    },
    "wisdom_amulet": {
        "name": "Amulet of Wisdom",
        "description": "Enhances magical ability",
        "type": "accessory",
        "slot": "accessory",
        "stats": {"intelligence": 8},
        "value": 250
    },
    "health_pendant": {
        "name": "Health Pendant",
        "description": "Boosts vitality",
        "type": "accessory",
        "slot": "accessory",
        "stats": {"max_hp": 100},
        "value": 300
    }
}

# Consumables
CONSUMABLES = {
    "health_potion": {
        "name": "Health Potion",
        "description": "Restores 50 HP",
        "type": "consumable",
        "effect": "heal",
        "power": 50,
        "value": 30
    },
    "mana_potion": {
        "name": "Mana Potion",
        "description": "Restores 30 MP",
        "type": "consumable",
        "effect": "restore_mp",
        "power": 30,
        "value": 25
    },
    "elixir": {
        "name": "Elixir",
        "description": "Fully restores HP and MP",
        "type": "consumable",
        "effect": "full_restore",
        "power": 999,
        "value": 150
    }
}

# Combine all items into one registry
ALL_ITEMS = {}
ALL_ITEMS.update(WEAPONS)
ALL_ITEMS.update(ARMOR)
ALL_ITEMS.update(ACCESSORIES)
ALL_ITEMS.update(CONSUMABLES)


def get_item(item_id):
    """Get item by ID"""
    return ALL_ITEMS.get(item_id, None)


def create_item(item_id):
    """Create a copy of an item"""
    item_template = ALL_ITEMS.get(item_id)
    if item_template:
        return dict(item_template)
    return None


def use_consumable(item, character):
    """Use a consumable item on a character"""
    if item["type"] != "consumable":
        return False, "This item cannot be consumed"

    effect = item["effect"]
    power = item["power"]

    if effect == "heal":
        healed = character.heal(power)
        return True, f"Restored {healed} HP!"
    elif effect == "restore_mp":
        restored = character.restore_mp(power)
        return True, f"Restored {restored} MP!"
    elif effect == "full_restore":
        character.stats["hp"] = character.stats["max_hp"]
        character.stats["mp"] = character.stats["max_mp"]
        return True, "Fully restored HP and MP!"

    return False, "Unknown effect"
