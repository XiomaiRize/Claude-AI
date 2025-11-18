#!/usr/bin/env python3
"""
Simple Life Simulation Game - Play Here!
Run this and tell Claude what you want to do
"""
import json
import os
import sys

GAME_FILE = "/home/user/Claude-AI/game_state.json"

def load_game():
    if os.path.exists(GAME_FILE):
        with open(GAME_FILE, 'r') as f:
            return json.load(f)
    return {"history": [], "character": "", "started": False}

def save_game(state):
    with open(GAME_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def display_story():
    """Display the current story"""
    state = load_game()
    print("\n" + "="*60)
    print("   LIFE SIMULATION - YOUR STORY SO FAR")
    print("="*60 + "\n")

    if not state["history"]:
        print("No story yet! Start the game first.")
        return

    for entry in state["history"]:
        speaker = entry["speaker"]
        text = entry["text"]
        is_player = entry.get("isPlayer", False)

        if is_player:
            print(f"\n🎮 YOU: {text}")
        else:
            print(f"\n🤖 {speaker}: {text}")

    print("\n" + "="*60 + "\n")

def add_action(action):
    """Add player action"""
    state = load_game()

    if not state["started"]:
        # This is character creation
        state["started"] = True
        state["character"] = action
        state["history"].append({
            "speaker": "SYSTEM",
            "text": f"Character created: {action}",
            "isPlayer": False
        })
        state["history"].append({
            "speaker": "YOU",
            "text": f"I am: {action}",
            "isPlayer": True
        })
        save_game(state)
        print("\n✅ Character created! Waiting for Claude to start your story...")
        print("(Claude will respond with your opening scenario)")
    else:
        state["history"].append({
            "speaker": "YOU",
            "text": action,
            "isPlayer": True
        })
        save_game(state)
        print("\n✅ Action recorded! Waiting for Claude to respond...")
        print(f"You: {action}")

def reset_game():
    """Reset the game"""
    if os.path.exists(GAME_FILE):
        os.remove(GAME_FILE)
    print("Game reset! Start a new life.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
LIFE SIMULATION GAME - Commands:

  python play.py start "your character description"
    - Start a new game with your character

  python play.py action "what you do"
    - Take an action in the game

  python play.py story
    - View your full story so far

  python play.py reset
    - Reset and start over

Example:
  python play.py start "I'm Alex, a 25 year old musician in NYC"
  python play.py action "I go to the subway to perform"
  python play.py story
""")
        sys.exit(0)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 3:
            char = "random character"
        else:
            char = " ".join(sys.argv[2:])
        add_action(char)

    elif command == "action":
        if len(sys.argv) < 3:
            print("Please provide an action!")
            sys.exit(1)
        action = " ".join(sys.argv[2:])
        add_action(action)

    elif command == "story":
        display_story()

    elif command == "reset":
        reset_game()

    else:
        print(f"Unknown command: {command}")
        print("Use 'python play.py' for help")
