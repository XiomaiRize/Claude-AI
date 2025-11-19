"""
Race System - The seven playable races with unique traits
Integrated with the Awakening system and world lore
"""

from typing import Dict, List


class Race:
    """Base race class"""

    def __init__(self, race_id: str, name: str):
        self.race_id = race_id
        self.name = name
        self.lifespan_min = 0
        self.lifespan_max = 0
        self.awakening_rate = 0.0
        self.awakening_age_min = 0
        self.awakening_age_max = 0
        self.interface_style = ""
        self.unique_traits = []
        self.stat_modifiers = {}
        self.society_type = ""
        self.cultural_notes = ""


# Define all seven races
RACES = {
    "elf": {
        "name": "Elf",
        "lifespan": (800, 1200),
        "awakening_rate": 0.95,
        "awakening_age": (25, 40),  # Equivalent to human 8-12
        "interface_style": "Elegant, nature-themed with flowing script",
        "unique_traits": [
            "Can sense other awakened within 50 meters",
            "Ancient wisdom and long-term thinking",
            "Natural magical affinity"
        ],
        "stat_modifiers": {
            "mana_regen": 1.20,  # +20%
            "magic_resistance": 1.15,  # +15%
            "intelligence": 1.10,
            "strength": 0.95  # -5%
        },
        "society": "Ruled by Council of First Awakened (800+ years old)",
        "culture": "Awakening seen as 'returning to ancestral wisdom'",
        "description": "Long-lived magical beings who view awakening as reconnecting with ancient heritage"
    },

    "orc": {
        "name": "Orc",
        "lifespan": (60, 80),
        "awakening_rate": 0.60,
        "awakening_age": (6, 10),  # Mature faster
        "interface_style": "Crude, runic stone tablets",
        "unique_traits": [
            "Explosive raw stat growth",
            "Prefer traditional strength over system",
            "Natural crafting intuition"
        ],
        "stat_modifiers": {
            "strength": 1.30,  # +30%
            "physical_damage": 1.25,
            "intelligence": 0.90,  # -10%
            "magic_affinity": 0.90
        },
        "society": "Chieftains often non-awakened who proved themselves through pure strength",
        "culture": "View system as 'spirit talking', prefer traditional methods",
        "description": "Powerful warriors who value strength and innovation, reluctant system users"
    },

    "dwarf": {
        "name": "Dwarf",
        "lifespan": (150, 200),
        "awakening_rate": 0.70,
        "awakening_age": (12, 18),
        "interface_style": "Geometric blueprints and measurements",
        "unique_traits": [
            "Natural affinity for crafting and alchemy",
            "Engineering excellence",
            "Precision-focused abilities"
        ],
        "stat_modifiers": {
            "crafting_speed": 1.25,  # +25%
            "defense": 1.15,
            "max_hp": 1.10,
            "agility": 0.90  # -10%
        },
        "society": "Ruled by master engineers and craft guild leaders",
        "culture": "Value precision, engineering excellence, and scientific approach",
        "description": "Master craftsmen who combine technical expertise with magical enhancement"
    },

    "human": {
        "name": "Human",
        "lifespan": (60, 80),
        "awakening_rate": 0.82,
        "awakening_age": (8, 16),
        "interface_style": "Varies wildly by individual",
        "unique_traits": [
            "Can learn techniques from ANY race",
            "Extreme adaptability",
            "Cultural diversity"
        ],
        "stat_modifiers": {
            "experience_gain": 1.15,  # +15%
            "versatility": 1.20,
            "racial_learning": 1.0  # Can learn any race's techniques
        },
        "society": "Democratic assemblies with multi-racial representation",
        "culture": "Most diverse, accepting of all paths and peoples",
        "description": "Adaptable beings who excel at learning from others and bridging cultures"
    },

    "dragonkin": {
        "name": "Dragon-kin",
        "lifespan": (2000, 3000),
        "awakening_rate": 0.99,
        "awakening_age": (100, 150),  # Their adolescence
        "interface_style": "Ancient draconic glyphs wreathed in flame",
        "unique_traits": [
            "Perfect Racial Mimicry - can perfectly replicate non-dragon parent's race",
            "Dragon Form - can transform into powerful dragon shape",
            "Hoard-Bond - can share interface with chosen allies",
            "No Pride Markers - cannot manifest draconic eyes or scales"
        ],
        "stat_modifiers": {
            "fire_immunity": 1.0,
            "scale_armor": 1.25,
            "strength": 1.20,
            "all_stats": 1.15,
            "social_penalty": 0.0  # Massive social penalties if discovered
        },
        "society": "NO KINGDOM - hunted survivors (50-100 worldwide)",
        "culture": "Complete assimilation into other races, perfect lies to survive",
        "description": "**HUNTED SPECIES** - Children of true dragons, universally persecuted. Survival rate <1%",
        "warning": "⚠️ PLAYING AS DRAGONKIN IS EXTREMELY DANGEROUS - Discovery means death"
    },

    "furry": {
        "name": "Furry (Beast-folk)",
        "lifespan": (40, 60),
        "awakening_rate": 0.85,
        "awakening_age": (3, 8),  # Earliest of all races
        "interface_style": "Territorial markings and scent-trails",
        "unique_traits": [
            "Pack Interface Clusters - share buffs with pack members",
            "Enhanced Senses - superior hearing, smell, vision",
            "Pack Coordination - bonus when fighting alongside pack",
            "Early maturity - contribute to society quickly"
        ],
        "stat_modifiers": {
            "agility": 1.20,  # +20%
            "senses": 1.30,
            "pack_bonus": 1.25,  # When with allies
            "max_hp": 0.95  # -5%
        },
        "society": "Led by 'Alpha Awakened' - earliest awakened in each pack",
        "culture": "Awakening ceremonies are massive pack celebrations, community-first values",
        "description": "Pack-oriented beings with enhanced senses and strong communal bonds"
    },

    "true_dragon": {
        "name": "True Dragon",
        "lifespan": (99999, 99999),  # Immortal
        "awakening_rate": 1.00,
        "awakening_age": (0, 0),  # At hatching
        "interface_style": "Reality-warping cosmic script",
        "unique_traits": [
            "⚠️ UNPLAYABLE - NPC ONLY",
            "Perfect shapeshifting (maintains draconic eyes and scales on neck/arms)",
            "Parental Instinct - knows when offspring exist but not location",
            "Reality-level magic",
            "Immense power suppression"
        ],
        "stat_modifiers": {
            "all_stats": 10.0,  # 1000% bonus
            "magic_power": 50.0,
            "shapeshifting": 1.0
        },
        "society": "NO FORMAL KINGDOM - Infiltrate all governments in disguise",
        "culture": "Supremely proud, fund genocide of their own dragonkin children",
        "description": "**NPC ONLY** - Ancient immortal powers who secretly rule from shadows",
        "note": "TRUE DRAGONS ARE NOT PLAYABLE - They are antagonists and hidden rulers"
    }
}


def get_race(race_id: str) -> Dict:
    """Get race information by ID"""
    return RACES.get(race_id.lower(), RACES["human"])


def get_playable_races() -> List[str]:
    """Get list of playable race IDs (excludes true_dragon)"""
    return [race_id for race_id in RACES.keys() if race_id != "true_dragon"]


def get_race_stat_modifiers(race_id: str) -> Dict[str, float]:
    """Get stat modifiers for a race"""
    race = get_race(race_id)
    return race.get("stat_modifiers", {})


def apply_racial_bonuses(character, race_id: str):
    """Apply racial stat bonuses to a character"""
    modifiers = get_race_stat_modifiers(race_id)

    for stat, modifier in modifiers.items():
        if stat == "experience_gain":
            character.exp_modifier = modifier
        elif stat == "mana_regen":
            character.mana_regen_rate = modifier
        elif stat in character.stats:
            # Apply percentage modifier to base stat
            character.stats[stat] = int(character.stats[stat] * modifier)


def get_awakening_age_category(awakening_age: int) -> str:
    """Determine awakening category based on age (for humans, adjust for other races)"""
    if awakening_age <= 10:
        return "Prodigy (Extremely Rare)"
    elif awakening_age <= 13:
        return "Early Blessed (Strong Foundation)"
    elif awakening_age <= 16:
        return "Standard Awakened (Average Potential)"
    else:
        return "Late Bloomer (Unique Insights)"


def calculate_potential_modifier(awakening_age: int, race_id: str = "human") -> float:
    """Calculate potential power modifier based on awakening age

    Younger awakening = stronger potential
    Returns multiplier for base stats (1.0 = normal, higher = better)
    """
    # Get race's normal awakening range
    race = get_race(race_id)
    min_age, max_age = race["awakening_age"]

    # Calculate how early/late within race's normal range
    age_range = max_age - min_age
    position = (awakening_age - min_age) / age_range

    # Younger = better (inverted scale)
    # Position 0.0 (youngest) = 1.5x multiplier
    # Position 0.5 (middle) = 1.0x multiplier
    # Position 1.0 (oldest) = 0.8x multiplier
    modifier = 1.5 - (position * 0.7)

    return max(0.5, min(2.0, modifier))  # Clamp between 0.5x and 2.0x


def is_dragonkin_discovered(world_state) -> bool:
    """Check if player's dragonkin identity has been discovered

    If playing as dragonkin, this determines if you've been found out
    """
    # Check world state flags
    if hasattr(world_state, 'flags'):
        return world_state.flags.get('dragonkin_identity_revealed', False)
    return False


def trigger_dragonkin_hunt(world_state):
    """Trigger universal hunt for discovered dragonkin

    ALL kingdoms will send assassins
    Bounty will be placed
    No safe locations
    """
    world_state.set_flag('dragonkin_identity_revealed', True)
    world_state.set_flag('universal_hunt_active', True)
    world_state.player_fame = -10  # Maximum infamy

    # All NPCs immediately become hostile or fearful
    return {
        "status": "DISCOVERY",
        "message": "⚠️ YOUR DRAGONKIN IDENTITY HAS BEEN REVEALED! ⚠️",
        "consequences": [
            "Universal execution order issued",
            "All kingdoms sending assassins",
            "Massive bounty on your head",
            "No safe locations",
            "Former allies may betray you",
            "Only hope: flee, hide, or fight"
        ]
    }


# Racial background stories for character creation
RACIAL_BACKGROUNDS = {
    "elf": [
        "Born in the ancient Silverleaf forests, you've studied for decades",
        "A young voice from the Starwood Empire, eager to prove yourself",
        "Moonhaven sailor who's traveled the world's oceans"
    ],
    "orc": [
        "Raised in the mountain forges, you value strength and innovation",
        "A warrior who earned chieftain respect without awakening initially",
        "Engineer who bridges traditional orc strength with modern techniques"
    ],
    "dwarf": [
        "Master craftsman from the deep holds, precision is your life",
        "Young engineer fascinated by magitech possibilities",
        "Guild representative seeking to advance dwarven techniques"
    ],
    "human": [
        "From the Free Ports, you've met people from all walks of life",
        "Crossroads merchant who's learned from every race",
        "Commonwealth citizen who believes in unity and acceptance"
    ],
    "dragonkin": [
        "⚠️ SURVIVOR - You've hidden your true nature your entire life",
        "⚠️ FUGITIVE - Constantly moving, never trusting anyone completely",
        "⚠️ DISGUISED - Perfect mimicry of your non-dragon parent's race"
    ],
    "furry": [
        "Pack-raised with strong bonds to your wolf/cat/otter kin",
        "Alpha's child, destined for leadership and responsibility",
        "Wanderer between packs, seeking to unite the Wild Confederacy"
    ]
}


def get_racial_background_options(race_id: str) -> List[str]:
    """Get background story options for character creation"""
    return RACIAL_BACKGROUNDS.get(race_id, RACIAL_BACKGROUNDS["human"])
