"""
Simulation Engine - Realistic world state tracking
Manages NPC relationships, world conditions, and player states
Claude (Game Master) actively manages these variables for realistic simulation!
"""

from typing import Dict, Any, List, Optional
import json


class NPCRelationship:
    """Tracks relationship with a single NPC"""

    def __init__(self, npc_id: str, npc_name: str):
        self.npc_id = npc_id
        self.npc_name = npc_name

        # Relationship metrics (0-10 scale)
        self.affection = 5      # How much they like you
        self.trust = 5          # How much they trust you
        self.respect = 5        # How much they respect you
        self.fear = 0           # How afraid they are of you
        self.annoyance = 0      # How annoyed they are with you

        # Interaction tracking
        self.times_met = 0
        self.last_interaction = None
        self.quests_completed_for = 0
        self.times_helped = 0
        self.times_wronged = 0

        # Relationship status
        self.friendship_level = "neutral"  # hostile, unfriendly, neutral, friendly, close_friend, best_friend
        self.is_romanceable = False
        self.romance_level = 0

    def update_affection(self, delta: int, reason: str = ""):
        """Change affection level"""
        old_value = self.affection
        self.affection = max(0, min(10, self.affection + delta))
        return {
            "metric": "affection",
            "old_value": old_value,
            "new_value": self.affection,
            "change": delta,
            "reason": reason
        }

    def update_trust(self, delta: int, reason: str = ""):
        """Change trust level"""
        old_value = self.trust
        self.trust = max(0, min(10, self.trust + delta))
        return {
            "metric": "trust",
            "old_value": old_value,
            "new_value": self.trust,
            "change": delta,
            "reason": reason
        }

    def update_respect(self, delta: int, reason: str = ""):
        """Change respect level"""
        old_value = self.respect
        self.respect = max(0, min(10, self.respect + delta))
        return {
            "metric": "respect",
            "old_value": old_value,
            "new_value": self.respect,
            "change": delta,
            "reason": reason
        }

    def update_fear(self, delta: int, reason: str = ""):
        """Change fear level"""
        old_value = self.fear
        self.fear = max(0, min(10, self.fear + delta))
        return {
            "metric": "fear",
            "old_value": old_value,
            "new_value": self.fear,
            "change": delta,
            "reason": reason
        }

    def update_annoyance(self, delta: int, reason: str = ""):
        """Change annoyance level"""
        old_value = self.annoyance
        self.annoyance = max(0, min(10, self.annoyance + delta))
        return {
            "metric": "annoyance",
            "old_value": old_value,
            "new_value": self.annoyance,
            "change": delta,
            "reason": reason
        }

    def get_overall_disposition(self) -> str:
        """Calculate overall how NPC feels about player"""
        score = self.affection + self.trust + self.respect - self.fear - self.annoyance

        if score >= 20:
            return "adores you"
        elif score >= 15:
            return "very friendly"
        elif score >= 10:
            return "friendly"
        elif score >= 5:
            return "neutral"
        elif score >= 0:
            return "unfriendly"
        elif score >= -5:
            return "hostile"
        else:
            return "deeply hostile"

    def to_dict(self):
        """Serialize to dict"""
        return {
            "npc_id": self.npc_id,
            "npc_name": self.npc_name,
            "affection": self.affection,
            "trust": self.trust,
            "respect": self.respect,
            "fear": self.fear,
            "annoyance": self.annoyance,
            "times_met": self.times_met,
            "friendship_level": self.friendship_level,
            "disposition": self.get_overall_disposition()
        }


class PlayerConditions:
    """Tracks player's current conditions and states"""

    def __init__(self):
        # Physical conditions (boolean)
        self.is_bleeding = False
        self.is_poisoned = False
        self.is_cursed = False
        self.is_blessed = False
        self.is_hungry = False
        self.is_exhausted = False
        self.is_drunk = False

        # Magical states (boolean)
        self.has_mana = True
        self.magic_available = True
        self.is_silenced = False  # Can't cast magic

        # Equipment states
        self.weapon_equipped = False
        self.armor_equipped = False

        # Social states
        self.is_wanted = False  # Criminal status
        self.is_disguised = False
        self.is_famous = False
        self.is_infamous = False

        # Special states
        self.can_fly = False
        self.can_swim = False
        self.is_invisible = False
        self.is_transformed = False

        # Status intensities (0-10)
        self.health_condition = 10  # 10=perfect, 0=near death
        self.stamina = 10
        self.sanity = 10
        self.corruption = 0  # Dark magic corruption

    def set_condition(self, condition: str, value: bool, reason: str = ""):
        """Set a boolean condition"""
        if hasattr(self, condition):
            old_value = getattr(self, condition)
            setattr(self, condition, value)
            return {
                "condition": condition,
                "old_value": old_value,
                "new_value": value,
                "reason": reason
            }
        return None

    def update_intensity(self, stat: str, delta: int, reason: str = ""):
        """Update an intensity stat"""
        if hasattr(self, stat):
            old_value = getattr(self, stat)
            new_value = max(0, min(10, old_value + delta))
            setattr(self, stat, new_value)
            return {
                "stat": stat,
                "old_value": old_value,
                "new_value": new_value,
                "change": delta,
                "reason": reason
            }
        return None

    def get_active_conditions(self) -> List[str]:
        """Get list of active negative conditions"""
        conditions = []
        if self.is_bleeding: conditions.append("Bleeding")
        if self.is_poisoned: conditions.append("Poisoned")
        if self.is_cursed: conditions.append("Cursed")
        if self.is_silenced: conditions.append("Silenced")
        if self.is_hungry: conditions.append("Hungry")
        if self.is_exhausted: conditions.append("Exhausted")
        if self.is_drunk: conditions.append("Drunk")
        return conditions

    def get_active_buffs(self) -> List[str]:
        """Get list of active positive conditions"""
        buffs = []
        if self.is_blessed: buffs.append("Blessed")
        if self.is_invisible: buffs.append("Invisible")
        if self.can_fly: buffs.append("Flying")
        if self.is_disguised: buffs.append("Disguised")
        return buffs

    def to_dict(self):
        """Serialize conditions"""
        return {
            "physical": {
                "bleeding": self.is_bleeding,
                "poisoned": self.is_poisoned,
                "cursed": self.is_cursed,
                "hungry": self.is_hungry,
                "exhausted": self.is_exhausted
            },
            "magical": {
                "has_mana": self.has_mana,
                "magic_available": self.magic_available,
                "silenced": self.is_silenced
            },
            "status_levels": {
                "health_condition": self.health_condition,
                "stamina": self.stamina,
                "sanity": self.sanity,
                "corruption": self.corruption
            },
            "active_conditions": self.get_active_conditions(),
            "active_buffs": self.get_active_buffs()
        }


class WorldState:
    """Tracks world conditions and states"""

    def __init__(self):
        # Time and weather
        self.time_of_day = "midday"  # dawn, morning, midday, afternoon, evening, night, midnight
        self.weather = "clear"  # clear, cloudy, raining, storming, snowing, foggy
        self.season = "spring"  # spring, summer, autumn, winter

        # World events (boolean)
        self.is_war_happening = False
        self.is_festival_active = False
        self.is_plague_active = False
        self.is_apocalypse = False

        # Location states
        self.village_safe = True
        self.village_prosperity = 7  # 0-10
        self.forest_darkness = 5  # How dangerous the forest is
        self.cave_explored = False
        self.dragon_alive = True

        # World reputation
        self.player_fame = 0  # -10 to 10 (negative = infamy)
        self.villages_saved = 0
        self.monsters_slain = 0
        self.people_helped = 0
        self.crimes_committed = 0

        # Economic state
        self.market_open = True
        self.prices_inflated = False
        self.rare_items_available = False

        # Magical state
        self.magic_surge_active = False  # Increased magic power
        self.magic_dead_zone = False  # No magic works
        self.portal_open = False

        # Quest states
        self.main_quest_stage = 0
        self.active_quests = []

    def set_state(self, state: str, value: Any, reason: str = ""):
        """Set a world state"""
        if hasattr(self, state):
            old_value = getattr(self, state)
            setattr(self, state, value)
            return {
                "state": state,
                "old_value": old_value,
                "new_value": value,
                "reason": reason
            }
        return None

    def advance_time(self):
        """Move time forward"""
        time_order = ["dawn", "morning", "midday", "afternoon", "evening", "night", "midnight"]
        current_idx = time_order.index(self.time_of_day)
        next_idx = (current_idx + 1) % len(time_order)
        old_time = self.time_of_day
        self.time_of_day = time_order[next_idx]
        return f"Time advances from {old_time} to {self.time_of_day}"

    def to_dict(self):
        """Serialize world state"""
        return {
            "environment": {
                "time": self.time_of_day,
                "weather": self.weather,
                "season": self.season
            },
            "world_events": {
                "war": self.is_war_happening,
                "festival": self.is_festival_active,
                "plague": self.is_plague_active
            },
            "locations": {
                "village_safe": self.village_safe,
                "village_prosperity": self.village_prosperity,
                "forest_danger": self.forest_darkness,
                "dragon_alive": self.dragon_alive
            },
            "reputation": {
                "fame": self.player_fame,
                "monsters_slain": self.monsters_slain,
                "people_helped": self.people_helped,
                "crimes": self.crimes_committed
            }
        }


class SimulationEngine:
    """Main simulation engine that Claude manages"""

    def __init__(self):
        self.npc_relationships: Dict[str, NPCRelationship] = {}
        self.player_conditions = PlayerConditions()
        self.world_state = WorldState()
        self.simulation_log: List[Dict] = []

    def get_or_create_npc_relationship(self, npc_id: str, npc_name: str) -> NPCRelationship:
        """Get existing or create new NPC relationship"""
        if npc_id not in self.npc_relationships:
            self.npc_relationships[npc_id] = NPCRelationship(npc_id, npc_name)
        return self.npc_relationships[npc_id]

    def update_npc_emotion(self, npc_id: str, npc_name: str, emotion: str, delta: int, reason: str = ""):
        """Update NPC emotion toward player"""
        npc = self.get_or_create_npc_relationship(npc_id, npc_name)

        update_methods = {
            "affection": npc.update_affection,
            "trust": npc.update_trust,
            "respect": npc.update_respect,
            "fear": npc.update_fear,
            "annoyance": npc.update_annoyance
        }

        if emotion in update_methods:
            result = update_methods[emotion](delta, reason)
            result["npc"] = npc_name
            self.log_change("npc_emotion", result)
            return result
        return None

    def check_npc_relationship(self, npc_id: str) -> Optional[NPCRelationship]:
        """Check current relationship with NPC"""
        return self.npc_relationships.get(npc_id)

    def can_perform_action(self, action_type: str) -> tuple[bool, str]:
        """Check if player can perform an action based on current state"""
        # Magic actions
        if action_type == "cast_spell":
            if not self.player_conditions.has_mana:
                return False, "You have no mana!"
            if self.player_conditions.is_silenced:
                return False, "You are silenced and cannot cast magic!"
            if self.world_state.magic_dead_zone:
                return False, "Magic doesn't work in this area!"
            if not self.player_conditions.magic_available:
                return False, "You cannot use magic right now!"

        # Physical actions
        if action_type == "melee_attack":
            if self.player_conditions.is_exhausted:
                return False, "You're too exhausted to fight!"
            if self.player_conditions.health_condition <= 2:
                return False, "You're too injured to attack effectively!"

        # Social actions
        if action_type == "enter_shop":
            if not self.world_state.market_open:
                return False, "The shops are closed at this time!"
            if self.player_conditions.is_wanted:
                return False, "Guards spot you! You can't enter town while wanted!"

        if action_type == "talk_to_guard":
            if self.player_conditions.is_wanted:
                return False, "The guards recognize you! They attack!"

        # Special abilities
        if action_type == "fly":
            if not self.player_conditions.can_fly:
                return False, "You don't have the ability to fly!"

        return True, "Action allowed"

    def log_change(self, change_type: str, data: Dict):
        """Log a simulation change"""
        self.simulation_log.append({
            "type": change_type,
            "data": data
        })

        # Keep log manageable
        if len(self.simulation_log) > 100:
            self.simulation_log = self.simulation_log[-100:]

    def get_simulation_summary(self) -> str:
        """Get a summary of current simulation state"""
        summary = []

        # Player conditions
        conditions = self.player_conditions.get_active_conditions()
        buffs = self.player_conditions.get_active_buffs()

        if conditions:
            summary.append(f"Active Conditions: {', '.join(conditions)}")
        if buffs:
            summary.append(f"Active Buffs: {', '.join(buffs)}")

        # World state
        summary.append(f"Time: {self.world_state.time_of_day}, Weather: {self.world_state.weather}")
        summary.append(f"Player Fame: {self.world_state.player_fame}")

        # NPC relationships (significant ones)
        for npc_id, relationship in self.npc_relationships.items():
            disposition = relationship.get_overall_disposition()
            if disposition not in ["neutral"]:
                summary.append(f"{relationship.npc_name} {disposition}")

        return "\n".join(summary) if summary else "No significant simulation states"

    def get_debug_state(self) -> Dict:
        """Get full simulation state for debugging"""
        return {
            "npc_relationships": {npc_id: rel.to_dict() for npc_id, rel in self.npc_relationships.items()},
            "player_conditions": self.player_conditions.to_dict(),
            "world_state": self.world_state.to_dict(),
            "recent_changes": self.simulation_log[-10:]
        }

    def save_simulation_state(self) -> Dict:
        """Export simulation state for saving"""
        return {
            "npcs": {npc_id: {
                "affection": rel.affection,
                "trust": rel.trust,
                "respect": rel.respect,
                "fear": rel.fear,
                "annoyance": rel.annoyance,
                "times_met": rel.times_met
            } for npc_id, rel in self.npc_relationships.items()},
            "player_conditions": {
                "is_bleeding": self.player_conditions.is_bleeding,
                "is_poisoned": self.player_conditions.is_poisoned,
                "is_cursed": self.player_conditions.is_cursed,
                "has_mana": self.player_conditions.has_mana,
                "health_condition": self.player_conditions.health_condition,
                "stamina": self.player_conditions.stamina
            },
            "world": {
                "time": self.world_state.time_of_day,
                "weather": self.world_state.weather,
                "fame": self.world_state.player_fame,
                "village_safe": self.world_state.village_safe,
                "dragon_alive": self.world_state.dragon_alive
            }
        }

    def load_simulation_state(self, state: Dict):
        """Import simulation state from save"""
        # Load NPC relationships
        for npc_id, npc_data in state.get("npcs", {}).items():
            rel = self.get_or_create_npc_relationship(npc_id, npc_id)
            rel.affection = npc_data.get("affection", 5)
            rel.trust = npc_data.get("trust", 5)
            rel.respect = npc_data.get("respect", 5)
            rel.fear = npc_data.get("fear", 0)
            rel.annoyance = npc_data.get("annoyance", 0)
            rel.times_met = npc_data.get("times_met", 0)

        # Load player conditions
        pc_data = state.get("player_conditions", {})
        self.player_conditions.is_bleeding = pc_data.get("is_bleeding", False)
        self.player_conditions.is_poisoned = pc_data.get("is_poisoned", False)
        self.player_conditions.is_cursed = pc_data.get("is_cursed", False)
        self.player_conditions.has_mana = pc_data.get("has_mana", True)
        self.player_conditions.health_condition = pc_data.get("health_condition", 10)
        self.player_conditions.stamina = pc_data.get("stamina", 10)

        # Load world state
        world_data = state.get("world", {})
        self.world_state.time_of_day = world_data.get("time", "midday")
        self.world_state.weather = world_data.get("weather", "clear")
        self.world_state.player_fame = world_data.get("fame", 0)
        self.world_state.village_safe = world_data.get("village_safe", True)
        self.world_state.dragon_alive = world_data.get("dragon_alive", True)
