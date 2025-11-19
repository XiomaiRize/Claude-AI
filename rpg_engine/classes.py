"""
Class System - From [Normal] to [Godly] tier classes
Includes the legendary Inherited Classes system
"""

from typing import Dict, List, Optional


# Class Rarity Tiers
CLASS_TIERS = [
    "Normal",
    "Uncommon",
    "Rare",
    "Special",
    "Unique",
    "Epic",
    "Legendary",
    "Mythic",
    "Godly"
]


class GameClass:
    """Represents a character class"""

    def __init__(self, class_id: str, name: str, tier: str):
        self.class_id = class_id
        self.name = name
        self.tier = tier
        self.description = ""
        self.acquisition_method = ""
        self.stat_bonuses = {}
        self.unique_abilities = []
        self.is_inherited = False
        self.curse = None  # For inherited classes


# Class Database
CLASSES = {
    # ===== NORMAL TIER =====
    "warrior": {
        "name": "Warrior",
        "tier": "Normal",
        "description": "Basic melee fighter trained in combat fundamentals",
        "acquisition": "Taught at military academies worldwide",
        "stat_bonuses": {
            "strength": 2,
            "defense": 1,
            "max_hp": 10
        },
        "primary_stat": "aura",
        "abilities": ["power_strike", "shield"],
        "passive": "Combat Stance Mastery - Gradual improvement in all physical combat"
    },

    "mage": {
        "name": "Mage",
        "tier": "Normal",
        "description": "Spellcaster trained in elemental magic",
        "acquisition": "Taught at magic schools and academies",
        "stat_bonuses": {
            "intelligence": 3,
            "max_mp": 20
        },
        "primary_stat": "mana",
        "abilities": ["fireball", "heal"],
        "passive": "Spell Efficiency - Reduced mana costs over time"
    },

    "archer": {
        "name": "Archer",
        "tier": "Normal",
        "description": "Ranged specialist with bow and arrow mastery",
        "acquisition": "Taught at hunter guilds and ranger academies",
        "stat_bonuses": {
            "agility": 3,
            "strength": 1
        },
        "primary_stat": "aura",
        "abilities": ["precise_shot", "quick_draw"],
        "passive": "Eagle Eye - Increased accuracy and critical hit chance"
    },

    # ===== UNCOMMON TIER =====
    "battle_mage": {
        "name": "Battle Mage",
        "tier": "Uncommon",
        "description": "Hybrid fighter combining magic and melee combat",
        "acquisition": "Advanced academies teaching both martial and magical arts",
        "stat_bonuses": {
            "strength": 2,
            "intelligence": 2,
            "max_hp": 5,
            "max_mp": 10
        },
        "primary_stat": "mana/aura",
        "abilities": ["power_strike", "fireball"],
        "passive": "Combat Versatility - Can switch between physical and magical damage"
    },

    # ===== RARE TIER =====
    "paladin": {
        "name": "Paladin",
        "tier": "Rare",
        "description": "Holy warrior blessed by divine forces",
        "acquisition": "Complete holy trials at sacred temples",
        "stat_bonuses": {
            "strength": 2,
            "intelligence": 1,
            "defense": 2,
            "max_hp": 15
        },
        "primary_stat": "faith",
        "abilities": ["divine_smite", "heal", "shield"],
        "passive": "Divine Protection - Natural resistance to dark magic and curses"
    },

    "void_walker": {
        "name": "Void Walker",
        "tier": "Rare",
        "description": "One who survived direct void exposure and mastered reality manipulation",
        "acquisition": "Survive void exposure without dying or going mad",
        "stat_bonuses": {
            "intelligence": 3,
            "agility": 2
        },
        "primary_stat": "void_essence",
        "abilities": ["void_step", "reality_tear"],
        "passive": "Void Touched - Can perceive dimensional rifts and use void magic"
    },

    "assassin": {
        "name": "Assassin",
        "tier": "Rare",
        "description": "Master of stealth, precision kills, and shadow arts",
        "acquisition": "Complete shadow guild initiation trials",
        "stat_bonuses": {
            "agility": 4,
            "strength": 1
        },
        "primary_stat": "aura",
        "abilities": ["backstab", "shadow_step", "poison_blade"],
        "passive": "Silent Death - Undetectable when initiating combat from stealth"
    },

    # ===== SPECIAL TIER =====
    "blood_knight": {
        "name": "Blood Knight",
        "tier": "Special",
        "description": "Warrior who harnesses life force as power",
        "acquisition": "Survive Blood Magic ritual without corruption",
        "stat_bonuses": {
            "strength": 3,
            "max_hp": 25
        },
        "primary_stat": "life_force",
        "abilities": ["blood_strike", "life_drain", "crimson_rage"],
        "passive": "Sanguine Power - Convert HP into devastating attacks"
    },

    # ===== UNIQUE TIER =====
    "dragon_knight": {
        "name": "Dragon Knight",
        "tier": "Unique",
        "description": "Legendary warrior bonded with an actual dragon",
        "acquisition": "Save/bond with an actual dragon - extremely rare",
        "stat_bonuses": {
            "all_stats": 5,
            "fire_resistance": 50
        },
        "primary_stat": "dragon_bond",
        "abilities": ["dragon_breath", "draconic_fury", "summon_dragon"],
        "passive": "Dragon Bond - Share power with bonded dragon, immunity to fire"
    },

    "phoenix_reborn": {
        "name": "Phoenix Reborn",
        "tier": "Unique",
        "description": "One who died and was resurrected by phoenix fire",
        "acquisition": "Literally die and resurrect under phoenix blessing",
        "stat_bonuses": {
            "intelligence": 4,
            "max_mp": 40
        },
        "primary_stat": "rebirth_flame",
        "abilities": ["phoenix_fire", "resurrection", "immortal_flame"],
        "passive": "Death Defiance - Automatically revive once per day when killed"
    },

    # ===== EPIC TIER =====
    "world_guardian": {
        "name": "World Guardian",
        "tier": "Epic",
        "description": "Defender who successfully protected an entire continent",
        "acquisition": "Successfully defend a continent from major existential threat",
        "stat_bonuses": {
            "all_stats": 8,
            "max_hp": 100,
            "defense": 10
        },
        "primary_stat": "guardian_will",
        "abilities": ["continental_barrier", "mass_protection", "world_heal"],
        "passive": "Guardian's Resolve - Allies within range gain massive defensive bonuses"
    },

    # ===== LEGENDARY TIER =====
    "god_slayer": {
        "name": "God Slayer",
        "tier": "Legendary",
        "description": "One who has actually killed a divine being",
        "acquisition": "Actually kill a god or divine entity",
        "stat_bonuses": {
            "all_stats": 12,
            "divine_resistance": 100
        },
        "primary_stat": "deicide_power",
        "abilities": ["god_killer_strike", "divine_nullification", "ascension_breaker"],
        "passive": "Deicide - All attacks ignore divine protection and resistances"
    },

    # ===== INHERITED CLASSES (MYTHIC/GODLY) =====
    # These are special - only 1-3 per millennium

    "devourer": {
        "name": "Devourer",
        "tier": "Mythic",
        "description": "Can absorb defeated enemies' classes and skills",
        "acquisition": "Inherited from previous Devourer (last one Year 2134)",
        "is_inherited": True,
        "curse": "If you die, your killer inherits this class and all absorbed powers",
        "stat_bonuses": {
            "all_stats": 15,
            "growth_rate": 3.0  # 300% stat growth
        },
        "primary_stat": "consumption",
        "abilities": ["devour", "skill_absorption", "class_steal"],
        "passive": "Endless Hunger - Absorb any defeated enemy's strongest skill",
        "warning": "⚠️ EXTREMELY WEAK AT START - grows exponentially with each kill"
    },

    "gods_descendant": {
        "name": "God's Descendant",
        "tier": "Godly",
        "description": "Chosen by a deity to wield divine authority",
        "acquisition": "Inherited from previous God's Descendant",
        "is_inherited": True,
        "curse": "If you die, your killer becomes the new God's Descendant",
        "stat_bonuses": {
            "all_stats": 20,
            "divine_power": 100
        },
        "primary_stat": "divine_authority",
        "abilities": ["summon_angels", "divine_smite", "holy_dominion", "reality_command"],
        "passive": "Divine Authority - Can command all angels and impose divine will",
        "warning": "⚠️ World-dominating power but everyone wants to kill you for it"
    },

    "world_eater": {
        "name": "World Eater",
        "tier": "Mythic",
        "description": "Can consume pieces of reality itself to grow stronger",
        "acquisition": "Inherited from previous World Eater (current: unknown)",
        "is_inherited": True,
        "curse": "If you die, your killer inherits your consumed power",
        "stat_bonuses": {
            "all_stats": 18,
            "reality_consumption": 5.0
        },
        "primary_stat": "consumed_worlds",
        "abilities": ["consume_reality", "world_destruction", "existence_erasure"],
        "passive": "Reality Consumption - Grow stronger by consuming space, time, matter",
        "warning": "⚠️ Starts weak, becomes unstoppable. Universe-level threat."
    },

    "fate_sovereign": {
        "name": "Fate Sovereign",
        "tier": "Godly",
        "description": "Can rewrite destinies and manipulate probability itself",
        "acquisition": "Inherited - Current bearer: 'Fate Weaver' (Year 2756, location unknown)",
        "is_inherited": True,
        "curse": "If you die, your killer controls all fates you've manipulated",
        "stat_bonuses": {
            "all_stats": 22,
            "luck": 999
        },
        "primary_stat": "destiny_threads",
        "abilities": ["rewrite_fate", "probability_manipulation", "destiny_sight", "causality_control"],
        "passive": "Fate Manipulation - Alter probability, guarantee outcomes, rewrite destinies",
        "warning": "⚠️ CURRENT HOLDER ALIVE - Cannot be obtained unless Fate Weaver dies"
    },

    "deaths_heir": {
        "name": "Death's Heir",
        "tier": "Godly",
        "description": "Master of life and death, collector of souls",
        "acquisition": "Inherited from Death's Champion (Year 1205 - Century of Skulls)",
        "is_inherited": True,
        "curse": "If you die, your killer commands all souls you've collected",
        "stat_bonuses": {
            "all_stats": 20,
            "death_mastery": 100
        },
        "primary_stat": "collected_souls",
        "abilities": ["soul_harvest", "life_death_control", "undead_mastery", "death_touch"],
        "passive": "Death's Domain - Control over life/death, collect souls, command all undead",
        "warning": "⚠️ Last holder caused Century of Skulls (millions died)"
    },

    "time_keeper": {
        "name": "Time Keeper",
        "tier": "Mythic",
        "description": "Can manipulate time flow without breaking causality",
        "acquisition": "Inherited - Last holder: Furry pack leader (Year 2134, deceased)",
        "is_inherited": True,
        "curse": "If you die, your killer gains all your temporal anchors",
        "stat_bonuses": {
            "all_stats": 19,
            "temporal_resistance": 100
        },
        "primary_stat": "time_threads",
        "abilities": ["time_slow", "temporal_anchor", "timeline_preservation", "age_manipulation"],
        "passive": "Time Manipulation - Slow/speed time locally, prevent timeline collapses",
        "warning": "⚠️ Cannot go back in time, but can prevent catastrophic timeline damage"
    }
}


def get_class(class_id: str) -> Optional[Dict]:
    """Get class information by ID"""
    return CLASSES.get(class_id.lower())


def get_classes_by_tier(tier: str) -> List[Dict]:
    """Get all classes of a specific tier"""
    return [cls for cls in CLASSES.values() if cls["tier"] == tier]


def get_teachable_classes() -> List[Dict]:
    """Get classes that can be learned from teachers"""
    return [cls for cls in CLASSES.values()
            if cls.get("tier") in ["Normal", "Uncommon"]]


def get_inherited_classes() -> List[Dict]:
    """Get all inherited classes (Mythic/Godly tier)"""
    return [cls for cls in CLASSES.values() if cls.get("is_inherited", False)]


def can_obtain_class(class_id: str, character_achievements: List[str]) -> tuple[bool, str]:
    """Check if character meets requirements to obtain a class"""
    cls = get_class(class_id)
    if not cls:
        return False, "Class not found"

    # Inherited classes have special rules
    if cls.get("is_inherited", False):
        return False, "Inherited classes can only be obtained through special inheritance events"

    # Check tier-specific requirements
    tier = cls["tier"]

    if tier in ["Normal", "Uncommon"]:
        return True, "Can be learned from teachers"

    if tier == "Rare":
        required_quest = cls.get("acquisition", "")
        # This would check if player completed required quest
        return False, f"Must complete: {required_quest}"

    if tier == "Unique":
        required_achievement = cls.get("acquisition", "")
        return False, f"Must achieve: {required_achievement}"

    if tier in ["Epic", "Legendary"]:
        required_feat = cls.get("acquisition", "")
        return False, f"Must accomplish: {required_feat}"

    return False, "Unknown requirement"


def trigger_inheritance_event(inheritor_class_id: str, previous_holder_name: str) -> Dict:
    """Trigger an inheritance class transfer event

    This happens when:
    1. Current holder dies
    2. Their killer inherits the class
    """
    cls = get_class(inheritor_class_id)

    if not cls or not cls.get("is_inherited", False):
        return {"error": "Not an inherited class"}

    return {
        "event": "CLASS_INHERITANCE",
        "class": cls["name"],
        "tier": cls["tier"],
        "from": previous_holder_name,
        "curse": cls.get("curse", ""),
        "message": f"⚡ YOU HAVE INHERITED THE {cls['tier'].upper()} CLASS: {cls['name'].upper()}!",
        "warning": cls.get("warning", ""),
        "consequences": [
            f"You now wield {cls['tier'].lower()}-tier power",
            "Everyone will want to kill you to claim this power",
            "You start extremely weak but have unlimited potential",
            cls.get("curse", "")
        ]
    }


def get_class_power_comparison(class_a_id: str, rank_a: str, class_b_id: str, rank_b: str) -> str:
    """Compare power between two classes considering tier and awakening rank

    Rules:
    - Higher class tier dominates lower tier regardless of rank
    - Within same tier, awakening rank determines winner
    - Mythic override: F-rank Mythic > any Legendary or lower
    """
    cls_a = get_class(class_a_id)
    cls_b = get_class(class_b_id)

    tier_a = CLASS_TIERS.index(cls_a["tier"])
    tier_b = CLASS_TIERS.index(cls_b["tier"])

    # Mythic override rule
    if tier_a >= CLASS_TIERS.index("Mythic") and tier_b < CLASS_TIERS.index("Mythic"):
        return f"{cls_a['name']} dominates (Mythic override)"

    if tier_b >= CLASS_TIERS.index("Mythic") and tier_a < CLASS_TIERS.index("Mythic"):
        return f"{cls_b['name']} dominates (Mythic override)"

    # Class tier comparison
    if tier_a > tier_b:
        return f"{cls_a['name']} wins (higher class tier)"
    elif tier_b > tier_a:
        return f"{cls_b['name']} wins (higher class tier)"

    # Same tier - rank matters
    # This is simplified - would need full rank comparison system
    return f"Within same tier - awakening rank determines winner"


# Historical Inherited Class Events
INHERITANCE_HISTORY = [
    {
        "number": "First",
        "year": 127,
        "class": "world_shaper",
        "holder": "Hidden Dragon-kin",
        "achievement": "Created the Great Barrier Mountains",
        "outcome": "Identity revealed, executed",
        "duration": "3 years"
    },
    {
        "number": "Second",
        "year": 742,
        "class": "eternal_sage",
        "holder": "Elven Noble",
        "achievement": "Advanced all magical knowledge by centuries",
        "outcome": "Died of old age at 1,200 years, class lost",
        "duration": "458 years"
    },
    {
        "number": "Third",
        "year": 1205,
        "class": "deaths_champion",
        "holder": "Dragon-kin Outcast",
        "achievement": "Caused the Century of Skulls (millions died)",
        "outcome": "Combined forces killed holder in Year 1305",
        "duration": "100 years",
        "note": "Led to increased dragon-kin persecution"
    },
    {
        "number": "Fourth",
        "year": 1678,
        "class": "star_caller",
        "holder": "Dragon-kin Princess",
        "achievement": "Terraformed wastelands into fertile lands",
        "outcome": "Assassinated Year 1723, killer gained class then died",
        "duration": "45 years"
    },
    {
        "number": "Fifth",
        "year": 2134,
        "class": "time_keeper",
        "holder": "Furry Pack Leader",
        "achievement": "Prevented catastrophic timeline collapse",
        "outcome": "Died preventing temporal disaster, class transferred",
        "duration": "Unknown (still active?)"
    },
    {
        "number": "Sixth",
        "year": 2756,
        "class": "fate_weaver",
        "holder": "Human Merchant",
        "achievement": "Unknown",
        "outcome": "CURRENT - Whereabouts unknown",
        "duration": "231 years and counting",
        "note": "All kingdoms searching"
    },
    {
        "number": "Seventh",
        "year": "???",
        "class": "???",
        "holder": "PENDING",
        "achievement": "Rumors suggest inheritance approaching",
        "outcome": "UNKNOWN",
        "duration": "N/A",
        "note": "Year 2987 - tensions rising"
    }
]


def get_inheritance_history() -> List[Dict]:
    """Get complete historical record of inherited classes"""
    return INHERITANCE_HISTORY
