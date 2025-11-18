#!/usr/bin/env python3
"""
Game Master Interface - Allows Claude to respond to player actions
"""
import json
import os
from datetime import datetime

GAME_FILE = "/home/user/Claude-AI/game_state.json"

def load_game():
    """Load current game state"""
    if os.path.exists(GAME_FILE):
        with open(GAME_FILE, 'r') as f:
            return json.load(f)
    return {"history": [], "character": "", "started": False}

def save_game(state):
    """Save game state"""
    with open(GAME_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def add_response(response_text):
    """Add Claude's response to the game"""
    state = load_game()
    state["history"].append({
        "speaker": "CLAUDE AI",
        "text": response_text,
        "isPlayer": False,
        "timestamp": datetime.now().isoformat()
    })
    save_game(state)
    print("Response added to game!")
    print(f"\n{response_text}\n")

def view_latest():
    """View the latest player action"""
    state = load_game()
    if not state["history"]:
        print("No actions yet!")
        return

    print("\n=== GAME HISTORY ===\n")
    for entry in state["history"][-5:]:  # Show last 5 entries
        speaker = entry["speaker"]
        text = entry["text"]
        print(f"{speaker}: {text}\n")

def start_game(character_desc):
    """Initialize a new game"""
    state = {
        "started": True,
        "character": character_desc,
        "history": []
    }
    save_game(state)
    print(f"Game started with character: {character_desc}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Commands:")
        print("  python game_master.py view - View recent actions")
        print("  python game_master.py respond 'your response text'")
        print("  python game_master.py start 'character description'")
        sys.exit(1)

    command = sys.argv[1]

    if command == "view":
        view_latest()
    elif command == "respond" and len(sys.argv) > 2:
        response = " ".join(sys.argv[2:])
        add_response(response)
    elif command == "start" and len(sys.argv) > 2:
        char = " ".join(sys.argv[2:])
        start_game(char)
    else:
        print("Invalid command")
