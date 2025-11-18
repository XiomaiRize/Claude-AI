#!/usr/bin/env python3
"""
Interactive Life Simulation Game Session Handler
Designed to work in chat/non-interactive environments
"""

import os
import sys
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

STATE_FILE = "/home/user/Claude-AI/game_state.json"

class GameSession:
    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY not found")
            sys.exit(1)
        self.client = Anthropic(api_key=api_key)
        self.load_state()

    def load_state(self):
        """Load game state from file or create new"""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                self.conversation_history = data.get('history', [])
                self.started = data.get('started', False)
        else:
            self.conversation_history = []
            self.started = False

    def save_state(self):
        """Save game state to file"""
        with open(STATE_FILE, 'w') as f:
            json.dump({
                'history': self.conversation_history,
                'started': self.started
            }, f, indent=2)

    def start_game(self, character_desc=None):
        """Start a new game"""
        if self.started:
            print("Game already started! Use 'action' to continue or 'reset' to restart.")
            return

        if not character_desc or character_desc.strip() == "":
            character_desc = "Create a random character for me"

        system_prompt = """You are a creative and immersive life simulation game master.
Your role is to:
1. Create vivid, detailed scenarios based on player choices
2. Simulate realistic (or fantastical) consequences of actions
3. Keep the story engaging and dynamic
4. Allow for infinite possibilities - the player can try anything
5. Remember previous events and maintain consistency
6. Describe outcomes in 2-4 paragraphs with rich detail
7. End each response with the current situation and ask what the player does next

Keep responses concise but immersive. Make the world feel alive and responsive."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Start a life simulation game. Character description: {character_desc}\n\nCreate an engaging opening scenario that introduces this character's current situation. Make it interesting and give them options for what to do."
            }]
        )

        scenario = response.content[0].text
        self.conversation_history.append({
            "role": "user",
            "content": f"Character: {character_desc}"
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": scenario
        })
        self.started = True
        self.save_state()

        print("\n" + "="*60)
        print("   LIFE SIMULATION - INFINITE POSSIBILITIES")
        print("="*60)
        print(scenario)
        print("="*60)

    def take_action(self, action):
        """Process a player action"""
        if not self.started:
            print("Game not started! Use 'start' command first.")
            return

        system_prompt = """You are a creative and immersive life simulation game master.
Your role is to:
1. Create vivid, detailed scenarios based on player choices
2. Simulate realistic (or fantastical) consequences of actions
3. Keep the story engaging and dynamic
4. Allow for infinite possibilities - the player can try anything
5. Remember previous events and maintain consistency
6. Describe outcomes in 2-4 paragraphs with rich detail
7. End each response with the current situation and ask what the player does next

Keep responses concise but immersive. Make the world feel alive and responsive."""

        self.conversation_history.append({
            "role": "user",
            "content": f"I choose to: {action}"
        })

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                system=system_prompt,
                messages=self.conversation_history
            )

            outcome = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": outcome
            })
            self.save_state()

            print("\n" + "-"*60)
            print(outcome)
            print("-"*60)
        except Exception as e:
            print(f"\nError: {e}")
            self.conversation_history.pop()

    def reset(self):
        """Reset the game"""
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        print("Game reset! Use 'start' to begin a new game.")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python game_session.py start [character description]")
        print("  python game_session.py action <your action>")
        print("  python game_session.py reset")
        sys.exit(1)

    command = sys.argv[1].lower()
    session = GameSession()

    if command == "start":
        character = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        session.start_game(character)
    elif command == "action":
        if len(sys.argv) < 3:
            print("Please provide an action!")
            sys.exit(1)
        action = " ".join(sys.argv[2:])
        session.take_action(action)
    elif command == "reset":
        session.reset()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
