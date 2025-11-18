"""
Ability System - Special attacks, magic spells, and skills
LIVE EDITABLE: Add new abilities during gameplay by editing this file!
"""

import random


class Ability:
    """Base class for abilities"""

    def __init__(self, name, description, mp_cost, ability_type="attack"):
        self.name = name
        self.description = description
        self.mp_cost = mp_cost
        self.ability_type = ability_type

    def can_use(self, user):
        """Check if user can use this ability"""
        return user.stats["mp"] >= self.mp_cost

    def use(self, user, target=None):
        """Use the ability (override in subclasses)"""
        if not self.can_use(user):
            return False, "Not enough MP!"

        user.stats["mp"] -= self.mp_cost
        return True, "Ability used!"


class AttackAbility(Ability):
    """Offensive ability"""

    def __init__(self, name, description, mp_cost, power, stat_scaling="strength", damage_type="physical"):
        super().__init__(name, description, mp_cost, "attack")
        self.power = power
        self.stat_scaling = stat_scaling
        self.damage_type = damage_type

    def use(self, user, target):
        """Execute attack"""
        if not self.can_use(user):
            return False, "Not enough MP!"

        user.stats["mp"] -= self.mp_cost

        # Calculate damage
        stat_value = user.stats.get(self.stat_scaling, 10)
        base_damage = self.power + (stat_value * 0.5)
        damage = int(base_damage * random.uniform(0.9, 1.1))

        # Apply to target
        if target:
            actual_damage = target.take_damage(damage, self.damage_type)
            return True, f"{user.name} uses {self.name}! Dealt {actual_damage} damage!"

        return True, f"{user.name} uses {self.name}!"


class HealAbility(Ability):
    """Healing ability"""

    def __init__(self, name, description, mp_cost, power):
        super().__init__(name, description, mp_cost, "heal")
        self.power = power

    def use(self, user, target=None):
        """Execute heal"""
        if not self.can_use(user):
            return False, "Not enough MP!"

        user.stats["mp"] -= self.mp_cost

        if target is None:
            target = user

        healed = target.heal(self.power)
        return True, f"{user.name} uses {self.name}! Restored {healed} HP!"


class BuffAbility(Ability):
    """Stat-boosting ability"""

    def __init__(self, name, description, mp_cost, stat, boost, duration=3):
        super().__init__(name, description, mp_cost, "buff")
        self.stat = stat
        self.boost = boost
        self.duration = duration

    def use(self, user, target=None):
        """Apply buff"""
        if not self.can_use(user):
            return False, "Not enough MP!"

        user.stats["mp"] -= self.mp_cost

        if target is None:
            target = user

        # Apply temporary buff
        target.stats[self.stat] += self.boost

        return True, f"{user.name} uses {self.name}! {self.stat.upper()} increased by {self.boost}!"


# Ability Database (ADD NEW ABILITIES HERE!)
ABILITIES = {
    # Basic Attacks
    "power_strike": AttackAbility(
        name="Power Strike",
        description="A devastating melee attack",
        mp_cost=10,
        power=30,
        stat_scaling="strength",
        damage_type="physical"
    ),

    "quick_slash": AttackAbility(
        name="Quick Slash",
        description="A fast attack based on agility",
        mp_cost=8,
        power=20,
        stat_scaling="agility",
        damage_type="physical"
    ),

    # Magic Attacks
    "fireball": AttackAbility(
        name="Fireball",
        description="Launch a ball of fire at your enemy",
        mp_cost=15,
        power=40,
        stat_scaling="intelligence",
        damage_type="magical"
    ),

    "lightning_bolt": AttackAbility(
        name="Lightning Bolt",
        description="Strike with elemental lightning",
        mp_cost=20,
        power=50,
        stat_scaling="intelligence",
        damage_type="magical"
    ),

    "ice_shard": AttackAbility(
        name="Ice Shard",
        description="Pierce enemies with frozen shards",
        mp_cost=12,
        power=35,
        stat_scaling="intelligence",
        damage_type="magical"
    ),

    # Healing
    "heal": HealAbility(
        name="Heal",
        description="Restore HP with magic",
        mp_cost=15,
        power=50
    ),

    "greater_heal": HealAbility(
        name="Greater Heal",
        description="Restore a large amount of HP",
        mp_cost=30,
        power=100
    ),

    # Buffs
    "power_up": BuffAbility(
        name="Power Up",
        description="Temporarily increase strength",
        mp_cost=12,
        stat="strength",
        boost=10,
        duration=3
    ),

    "shield": BuffAbility(
        name="Shield",
        description="Temporarily increase defense",
        mp_cost=10,
        stat="defense",
        boost=8,
        duration=3
    ),

    "focus": BuffAbility(
        name="Focus",
        description="Temporarily increase intelligence",
        mp_cost=12,
        stat="intelligence",
        boost=10,
        duration=3
    )
}


def get_ability(ability_id):
    """Get ability by ID"""
    return ABILITIES.get(ability_id)


def get_abilities_for_class(char_class):
    """Get starting abilities for a character class"""
    class_abilities = {
        "Warrior": ["power_strike", "shield"],
        "Mage": ["fireball", "heal"],
        "Rogue": ["quick_slash"],
        "Cleric": ["heal", "shield"],
        "Battlemage": ["power_strike", "fireball"]
    }

    ability_ids = class_abilities.get(char_class, [])
    return [get_ability(aid) for aid in ability_ids if aid in ABILITIES]
