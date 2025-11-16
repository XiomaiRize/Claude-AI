# Life Simulation Game - Powered by Claude AI

An immersive text-based life simulation game where your choices create infinite possibilities. Powered by Claude AI, this game dynamically generates scenarios, outcomes, and consequences based on your actions.

## Features

- **Infinite Possibilities**: Every playthrough is unique with AI-generated scenarios
- **Dynamic Storytelling**: Claude AI creates immersive, contextual responses to your actions
- **Memory & Continuity**: The game remembers your choices and maintains story consistency
- **Complete Freedom**: Try anything - the AI will simulate realistic (or fantastical) outcomes
- **Easy to Play**: Simple text-based interface with natural language input

## Prerequisites

- Python 3.7 or higher
- An Anthropic API key ([Get one here](https://console.anthropic.com/settings/keys))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/XiomaiRize/Claude-AI.git
   cd Claude-AI
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:

   Create a `.env` file in the project directory:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

   Alternatively, you can set it as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

## How to Play

1. **Start the game**:
   ```bash
   python life_sim_game.py
   ```

2. **Create your character**:
   - You'll be prompted to describe yourself (name, age, background)
   - Or press Enter for a random character

3. **Make choices**:
   - Read the scenario Claude AI presents
   - Type what you want to do
   - Claude AI will simulate the outcome

4. **Continue your story**:
   - Keep making choices to see where your life leads
   - The AI remembers everything and maintains continuity

5. **Exit the game**:
   - Type `quit`, `exit`, or `q` at any time
   - Or press `Ctrl+C`

## Example Gameplay

```
=============================================================
   LIFE SIMULATION - INFINITE POSSIBILITIES
   Powered by Claude AI
=============================================================

Welcome to your new life!

Let's begin your life simulation...

Who are you? Describe yourself (name, age, background, situation):
(Or press Enter for a random character)

> I'm Alex, a 25-year-old aspiring musician living in New York City

------------------------------------------------------------
You are Alex, a 25-year-old musician in the heart of New York City...
[AI generates your starting scenario]
------------------------------------------------------------

What do you do?
> I decide to perform at the subway station to earn some money

------------------------------------------------------------
Simulating your action...
------------------------------------------------------------

[AI simulates the outcome of your street performance]
```

## Game Tips

- **Be creative**: Try anything! Want to start a business? Travel the world? Learn magic? The AI will simulate it.
- **Be specific**: More detailed actions lead to more interesting outcomes
- **Embrace the unexpected**: The AI might surprise you with consequences you didn't anticipate
- **Build your story**: Each choice builds on the previous ones, creating a unique narrative

## Technical Details

- **Model**: Uses Claude Sonnet 4.5 for high-quality, creative responses
- **Context**: Maintains full conversation history for consistency
- **Error Handling**: Gracefully handles API errors and network issues
- **Privacy**: Your API key stays local in your `.env` file

## Troubleshooting

**"ERROR: ANTHROPIC_API_KEY not found"**
- Make sure you've created a `.env` file with your API key
- Check that the key is correct and active at console.anthropic.com

**"Error processing your action"**
- Check your internet connection
- Verify your API key has available credits
- Try rephrasing your action

## Cost Considerations

This game uses the Claude API, which has associated costs:
- Each action costs a small amount based on token usage
- Typical gameplay costs a few cents per session
- Monitor your usage at console.anthropic.com

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Credits

- Powered by [Anthropic's Claude AI](https://www.anthropic.com/)
- Built with the [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)

---

**Enjoy your infinite life simulation!** 🎮✨
