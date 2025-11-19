"""
Flask Web Server for Dynamic RPG
Serves the HTML GUI and handles game logic via API
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import os
import sys
from dotenv import load_dotenv

# Import RPG engine
from rpg_engine.character import Character
from rpg_engine.combat import CombatSystem, create_enemy
from rpg_engine.world import GameState, get_location, get_npc, LOCATIONS
from rpg_engine.simulation import SimulationEngine
from rpg_engine.personality import get_default_personality
from rpg_engine import items, abilities

from anthropic import Anthropic

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Game instances (stored per session)
games = {}


class WebRPG:
    """RPG instance for web interface"""

    def __init__(self, session_id, custom_prompt=None):
        self.session_id = session_id

        # Setup Claude AI (optional - demo mode if not available)
        api_key = os.getenv('ANTHROPIC_API_KEY')
        self.demo_mode = not api_key

        if api_key:
            self.client = Anthropic(api_key=api_key)
        else:
            self.client = None
            print("⚠️  Running in DEMO MODE - No API key found")

        self.conversation_history = []

        # Game state
        self.game_state = GameState(f"/home/user/Claude-AI/saves/session_{session_id}.json")
        self.player = None
        self.in_combat = False
        self.combat = None

        # Simulation engine
        self.simulation = SimulationEngine()

        # System prompt
        self.system_prompt = custom_prompt if custom_prompt else get_default_personality()

    def create_character(self, name, char_class):
        """Create player character"""
        self.player = Character(name, char_class)

        # Give starting abilities
        starting_abilities = abilities.get_abilities_for_class(char_class)
        for ability in starting_abilities:
            self.player.learn_ability(ability)

        # Starting equipment
        starter_weapon = items.create_item("rusty_sword")
        if starter_weapon:
            self.player.add_item(starter_weapon)
            self.player.equip_item(starter_weapon)

        # Starter potions
        for _ in range(3):
            potion = items.create_item("health_potion")
            if potion:
                self.player.add_item(potion)

        self.game_state.player = self.player
        return self.player

    def start_game(self, character_name, character_class):
        """Initialize game with opening narrative"""
        self.create_character(character_name, character_class)

        # Demo mode - return static narrative
        if self.demo_mode:
            narrative = f"""🎮 **DEMO MODE** - Interface Testing 🎮

Welcome, {character_name} the {character_class}!

You stand at the edge of {LOCATIONS['village']['name']}, a peaceful settlement nestled in a verdant valley. The morning sun casts long shadows across cobblestone streets as villagers begin their daily routines.

An elderly merchant waves to you from his cart. "Ah, another adventurer! We've had strange reports from the forest lately. Perhaps you could investigate?"

**This is DEMO MODE** - The full AI game master requires an Anthropic API key. However, you can:
✓ Test the interface layout and responsiveness
✓ Try all the buttons and navigation
✓ Create characters and explore the UI
✓ See how it looks on your iOS device

Type any action to see a demo response, or ask about setting up the full AI experience!"""
            return narrative

        # Full AI mode
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

        return narrative

    def process_action(self, action):
        """Process player action and get AI response"""

        # Demo mode - return demo responses
        if self.demo_mode:
            action_lower = action.lower()

            if "help" in action_lower or "api" in action_lower:
                return """📋 **Setting Up Full AI Mode**

To enable the full AI game master experience, you need an Anthropic API key:

1. Get an API key from: https://console.anthropic.com/settings/keys
2. Create a `.env` file in the game directory
3. Add: `ANTHROPIC_API_KEY=your-key-here`
4. Restart the server

For now, enjoy testing the interface! All buttons, navigation, and UI elements are fully functional."""

            elif "inventory" in action_lower or "bag" in action_lower:
                inv_items = [item['name'] for item in self.player.inventory]
                return f"""🎒 **Inventory Check** (Demo)

You rummage through your pack and find:
{chr(10).join('• ' + item for item in inv_items)}

Gold: {self.player.gold}g

In full mode, the AI would create rich descriptions and let you interact with items dynamically!"""

            elif "look" in action_lower or "around" in action_lower:
                return """👀 **Looking Around** (Demo)

The village square bustles with activity. You notice:
• A weathered notice board with various quests
• A blacksmith's forge, smoke rising from the chimney
• An old temple with mysterious symbols
• Merchants selling wares from colorful stalls

The interface is working perfectly! Try the sidebar buttons or type other actions."""

            else:
                return f"""⚔️ **Demo Response**

You attempt to: "{action}"

The interface registered your input successfully! In full AI mode, I would:
• Understand your action contextually
• Update NPC emotions and world state
• Create dynamic story branches
• Track simulation variables in real-time

Try clicking the buttons on the sidebar (or mobile nav menu) to test all features!"""

        # Full AI mode
        sim_summary = self.simulation.get_simulation_summary()

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

=== SIMULATION STATE ===
{sim_summary}

Player Conditions:
- has_mana: {self.simulation.player_conditions.has_mana}
- health_condition: {self.simulation.player_conditions.health_condition}/10
- stamina: {self.simulation.player_conditions.stamina}/10

World State:
- Time: {self.simulation.world_state.time_of_day}
- Weather: {self.simulation.world_state.weather}
- Player Fame: {self.simulation.world_state.player_fame}

Process this action and narrate what happens. Update simulation variables as needed."""

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

        return narrative

    def get_player_stats(self):
        """Get current player stats for UI"""
        if not self.player:
            return None

        return {
            "name": self.player.name,
            "class": self.player.char_class,
            "level": self.player.level,
            "hp": self.player.stats['hp'],
            "max_hp": self.player.stats['max_hp'],
            "mp": self.player.stats['mp'],
            "max_mp": self.player.stats['max_mp'],
            "gold": self.player.gold,
            "exp": self.player.experience,
            "stats": {
                "str": self.player.stats['strength'],
                "agi": self.player.stats['agility'],
                "int": self.player.stats['intelligence'],
                "def": self.player.stats['defense'],
                "mdef": self.player.stats['magic_defense']
            }
        }

    def get_simulation_state(self):
        """Get simulation data for UI"""
        return {
            "player_conditions": self.simulation.player_conditions.to_dict(),
            "world_state": self.simulation.world_state.to_dict(),
            "npcs": {npc_id: rel.to_dict() for npc_id, rel in self.simulation.npc_relationships.items()}
        }


# Routes
@app.route('/')
def index():
    """Serve main game page"""
    return render_template('game.html')


@socketio.on('connect')
def handle_connect():
    """Handle new client connection"""
    session_id = request.sid
    games[session_id] = WebRPG(session_id)
    emit('connected', {'session_id': session_id})


@socketio.on('create_character')
def handle_create_character(data):
    """Create character and start game"""
    session_id = request.sid
    game = games.get(session_id)

    if game:
        name = data.get('name', 'Hero')
        char_class = data.get('class', 'Warrior')

        narrative = game.start_game(name, char_class)
        stats = game.get_player_stats()

        emit('game_started', {
            'narrative': narrative,
            'stats': stats
        })


@socketio.on('player_action')
def handle_player_action(data):
    """Process player action"""
    session_id = request.sid
    game = games.get(session_id)

    if game and game.player:
        action = data.get('action', '')

        # Process action
        narrative = game.process_action(action)
        stats = game.get_player_stats()
        simulation = game.get_simulation_state()

        emit('action_result', {
            'narrative': narrative,
            'stats': stats,
            'simulation': simulation
        })


@socketio.on('get_stats')
def handle_get_stats():
    """Get current player stats"""
    session_id = request.sid
    game = games.get(session_id)

    if game and game.player:
        emit('stats_update', game.get_player_stats())


@socketio.on('get_simulation')
def handle_get_simulation():
    """Get simulation state"""
    session_id = request.sid
    game = games.get(session_id)

    if game:
        emit('simulation_update', game.get_simulation_state())


@socketio.on('disconnect')
def handle_disconnect():
    """Clean up on disconnect"""
    session_id = request.sid
    if session_id in games:
        del games[session_id]


if __name__ == '__main__':
    # Create saves directory
    os.makedirs('/home/user/Claude-AI/saves', exist_ok=True)

    # Run server
    print("🎮 Starting Dynamic RPG Server...")
    print("📡 Open your browser to: http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
