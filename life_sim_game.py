#!/usr/bin/env python3
"""
Life Simulation Game with Claude AI
A text-based life simulation where your choices shape your destiny,
powered by Claude AI for infinite possibilities.
"""

import os
import sys
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LifeSimGame:
    def __init__(self):
        """Initialize the game with Claude AI client."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY not found in environment variables.")
            print("Please create a .env file with your API key or set it as an environment variable.")
            sys.exit(1)

        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        self.game_context = ""

    def display_welcome(self):
        """Display the welcome screen and game introduction."""
        print("\n" + "="*60)
        print("   LIFE SIMULATION - INFINITE POSSIBILITIES")
        print("   Powered by Claude AI")
        print("="*60)
        print("\nWelcome to your new life!")
        print("\nIn this simulation, you can be anyone, do anything, and")
        print("experience infinite possibilities. Your choices matter, and")
        print("Claude AI will simulate the outcomes of your actions.")
        print("\nType 'quit' or 'exit' at any time to end the simulation.")
        print("="*60 + "\n")

    def start_new_life(self):
        """Initialize a new life simulation."""
        print("Let's begin your life simulation...\n")
        print("Who are you? Describe yourself (name, age, background, situation):")
        print("(Or press Enter for a random character)\n")

        character_input = input("> ").strip()

        if not character_input:
            character_input = "Create a random character for me"

        # Create the initial game context with Claude
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

        # Get initial scenario
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Start a life simulation game. Character description: {character_input}\n\nCreate an engaging opening scenario that introduces this character's current situation. Make it interesting and give them options for what to do."
            }]
        )

        scenario = response.content[0].text
        self.conversation_history.append({
            "role": "user",
            "content": f"Character: {character_input}"
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": scenario
        })

        print("\n" + "-"*60)
        print(scenario)
        print("-"*60 + "\n")

    def process_action(self, action):
        """Send player action to Claude and get the simulated outcome."""
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

        # Add player action to history
        self.conversation_history.append({
            "role": "user",
            "content": f"I choose to: {action}"
        })

        # Get Claude's response
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history
        )

        outcome = response.content[0].text

        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": outcome
        })

        return outcome

    def play(self):
        """Main game loop."""
        self.display_welcome()
        self.start_new_life()

        while True:
            print("\nWhat do you do?")
            action = input("> ").strip()

            if not action:
                print("Please enter an action.")
                continue

            if action.lower() in ['quit', 'exit', 'q']:
                print("\nThanks for playing! Your life simulation has ended.")
                print("="*60)
                break

            print("\n" + "-"*60)
            print("Simulating your action...")
            print("-"*60 + "\n")

            try:
                outcome = self.process_action(action)
                print(outcome)
                print("\n" + "-"*60)
            except Exception as e:
                print(f"\nError: {e}")
                print("There was an issue processing your action. Please try again.")
                # Remove the failed action from history
                if self.conversation_history:
                    self.conversation_history.pop()

def main():
    """Entry point for the game."""
    try:
        game = LifeSimGame()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
