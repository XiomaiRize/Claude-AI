"""
Combat System - Battle mechanics and enemy AI
LIVE EDITABLE: Modify combat rules, add new enemy types, change AI behavior!
"""

import random
from .character import Character


class Enemy:
    """Enemy character"""

    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.is_enemy = True

        # Scale stats with level
        self.stats = {
            "hp": 50 + (level * 20),
            "max_hp": 50 + (level * 20),
            "strength": 8 + (level * 2),
            "defense": 3 + level,
            "agility": 5 + level
        }

        self.abilities = []
        self.gold_reward = 20 + (level * 10)
        self.exp_reward = 30 + (level * 15)

    def take_damage(self, damage, damage_type="physical"):
        """Apply damage to enemy"""
        actual_damage = max(1, damage - self.stats["defense"])
        self.stats["hp"] = max(0, self.stats["hp"] - actual_damage)
        return actual_damage

    def is_alive(self):
        """Check if enemy is alive"""
        return self.stats["hp"] > 0

    def basic_attack(self, target):
        """Perform a basic attack"""
        base_damage = self.stats["strength"] + random.randint(-3, 3)
        damage = max(1, base_damage)
        actual_damage = target.take_damage(damage)
        return actual_damage


# Enemy Templates (ADD NEW ENEMIES HERE!)
ENEMY_TYPES = {
    "goblin": {
        "name": "Goblin",
        "base_stats": {
            "hp": 40,
            "strength": 8,
            "defense": 2,
            "agility": 7
        },
        "gold": 15,
        "exp": 25
    },
    "orc": {
        "name": "Orc",
        "base_stats": {
            "hp": 80,
            "strength": 15,
            "defense": 6,
            "agility": 4
        },
        "gold": 35,
        "exp": 50
    },
    "skeleton": {
        "name": "Skeleton",
        "base_stats": {
            "hp": 50,
            "strength": 10,
            "defense": 4,
            "agility": 6
        },
        "gold": 20,
        "exp": 30
    },
    "dragon": {
        "name": "Dragon",
        "base_stats": {
            "hp": 200,
            "strength": 30,
            "defense": 15,
            "agility": 10
        },
        "gold": 500,
        "exp": 300
    },
    "slime": {
        "name": "Slime",
        "base_stats": {
            "hp": 30,
            "strength": 5,
            "defense": 1,
            "agility": 3
        },
        "gold": 10,
        "exp": 15
    }
}


def create_enemy(enemy_type, level=1):
    """Create an enemy from a template"""
    if enemy_type not in ENEMY_TYPES:
        enemy_type = "goblin"

    template = ENEMY_TYPES[enemy_type]
    enemy = Enemy(template["name"], level)

    # Apply template stats
    for stat, value in template["base_stats"].items():
        enemy.stats[stat] = value + (level * 10)
        if stat == "hp":
            enemy.stats["max_hp"] = enemy.stats[stat]

    enemy.gold_reward = template["gold"] + (level * 10)
    enemy.exp_reward = template["exp"] + (level * 15)

    return enemy


class CombatSystem:
    """Handles combat encounters"""

    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies if isinstance(enemies, list) else [enemies]
        self.turn = 0
        self.combat_log = []

    def log(self, message):
        """Add message to combat log"""
        self.combat_log.append(message)

    def player_attack(self, enemy_index=0):
        """Player performs basic attack"""
        if enemy_index >= len(self.enemies):
            return False, "Invalid target!"

        enemy = self.enemies[enemy_index]
        if not enemy.is_alive():
            return False, "Target is already defeated!"

        # Calculate damage
        base_damage = self.player.stats["strength"] + random.randint(-2, 5)
        damage = max(1, base_damage)
        actual_damage = enemy.take_damage(damage)

        message = f"{self.player.name} attacks {enemy.name} for {actual_damage} damage!"
        self.log(message)

        if not enemy.is_alive():
            defeat_msg = f"{enemy.name} has been defeated!"
            self.log(defeat_msg)

        return True, message

    def player_use_ability(self, ability, enemy_index=0):
        """Player uses an ability"""
        if enemy_index >= len(self.enemies):
            return False, "Invalid target!"

        enemy = self.enemies[enemy_index]

        # Use the ability
        success, message = ability.use(self.player, enemy)
        self.log(message)

        if success and not enemy.is_alive():
            defeat_msg = f"{enemy.name} has been defeated!"
            self.log(defeat_msg)

        return success, message

    def enemies_turn(self):
        """All living enemies take their turn"""
        messages = []

        for enemy in self.enemies:
            if enemy.is_alive():
                damage = enemy.basic_attack(self.player)
                message = f"{enemy.name} attacks for {damage} damage!"
                self.log(message)
                messages.append(message)

        return messages

    def is_combat_over(self):
        """Check if combat has ended"""
        # Player defeated
        if not self.player.is_alive():
            return True, "defeat"

        # All enemies defeated
        if all(not e.is_alive() for e in self.enemies):
            return True, "victory"

        return False, None

    def get_rewards(self):
        """Calculate rewards from defeated enemies"""
        total_gold = sum(e.gold_reward for e in self.enemies)
        total_exp = sum(e.exp_reward for e in self.enemies)
        return total_gold, total_exp

    def get_status(self):
        """Get current combat status"""
        return {
            "player": {
                "name": self.player.name,
                "hp": f"{self.player.stats['hp']}/{self.player.stats['max_hp']}",
                "mp": f"{self.player.stats['mp']}/{self.player.stats['max_mp']}"
            },
            "enemies": [
                {
                    "name": e.name,
                    "hp": f"{e.stats['hp']}/{e.stats['max_hp']}",
                    "alive": e.is_alive()
                }
                for e in self.enemies
            ]
        }
