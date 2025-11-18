"""
Character System - Player stats, inventory, and progression
LIVE EDITABLE: Modify stats, add new attributes, or change mechanics during gameplay!
"""

class Character:
    """Player character with RPG stats and inventory"""

    def __init__(self, name, char_class="Adventurer"):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.experience = 0

        # Core Stats (modifiable!)
        self.stats = {
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "defense": 5,
            "magic_defense": 5
        }

        # Inventory
        self.inventory = []
        self.gold = 100
        self.equipped = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }

        # Abilities (can be dynamically added!)
        self.abilities = []

        # Status effects
        self.status_effects = []

    def take_damage(self, damage, damage_type="physical"):
        """Apply damage to character"""
        if damage_type == "physical":
            actual_damage = max(1, damage - self.stats["defense"])
        elif damage_type == "magical":
            actual_damage = max(1, damage - self.stats["magic_defense"])
        else:
            actual_damage = damage

        self.stats["hp"] = max(0, self.stats["hp"] - actual_damage)
        return actual_damage

    def heal(self, amount):
        """Restore HP"""
        old_hp = self.stats["hp"]
        self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"] + amount)
        return self.stats["hp"] - old_hp

    def restore_mp(self, amount):
        """Restore MP"""
        old_mp = self.stats["mp"]
        self.stats["mp"] = min(self.stats["max_mp"], self.stats["mp"] + amount)
        return self.stats["mp"] - old_mp

    def is_alive(self):
        """Check if character is alive"""
        return self.stats["hp"] > 0

    def add_item(self, item):
        """Add item to inventory"""
        self.inventory.append(item)

    def remove_item(self, item_name):
        """Remove item from inventory"""
        for item in self.inventory:
            if item["name"] == item_name:
                self.inventory.remove(item)
                return item
        return None

    def equip_item(self, item):
        """Equip an item"""
        slot = item.get("slot")
        if slot in self.equipped:
            # Unequip current item
            if self.equipped[slot]:
                old_item = self.equipped[slot]
                self._remove_item_stats(old_item)

            # Equip new item
            self.equipped[slot] = item
            self._apply_item_stats(item)
            return True
        return False

    def _apply_item_stats(self, item):
        """Apply item stat bonuses"""
        if "stats" in item:
            for stat, value in item["stats"].items():
                if stat in self.stats:
                    self.stats[stat] += value

    def _remove_item_stats(self, item):
        """Remove item stat bonuses"""
        if "stats" in item:
            for stat, value in item["stats"].items():
                if stat in self.stats:
                    self.stats[stat] -= value

    def learn_ability(self, ability):
        """Learn a new ability"""
        if ability not in self.abilities:
            self.abilities.append(ability)
            return True
        return False

    def gain_experience(self, exp):
        """Gain experience and potentially level up"""
        self.experience += exp
        exp_needed = self.level * 100

        if self.experience >= exp_needed:
            self.level_up()
            return True
        return False

    def level_up(self):
        """Level up and increase stats"""
        self.level += 1
        self.experience = 0

        # Stat increases (modifiable!)
        self.stats["max_hp"] += 20
        self.stats["max_mp"] += 10
        self.stats["strength"] += 2
        self.stats["agility"] += 2
        self.stats["intelligence"] += 2
        self.stats["defense"] += 1
        self.stats["magic_defense"] += 1

        # Restore HP/MP on level up
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["mp"] = self.stats["max_mp"]

    def get_status(self):
        """Get character status summary"""
        return {
            "name": self.name,
            "class": self.char_class,
            "level": self.level,
            "hp": f"{self.stats['hp']}/{self.stats['max_hp']}",
            "mp": f"{self.stats['mp']}/{self.stats['max_mp']}",
            "stats": {
                "STR": self.stats["strength"],
                "AGI": self.stats["agility"],
                "INT": self.stats["intelligence"],
                "DEF": self.stats["defense"],
                "MDEF": self.stats["magic_defense"]
            },
            "gold": self.gold,
            "experience": self.experience
        }
