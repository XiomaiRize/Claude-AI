# CLAUDE.md - AI Assistant Development Guide

This document provides a comprehensive guide for AI assistants working with the Claude-AI life simulation game codebase.

## Project Overview

This is a text-based life simulation game powered by Anthropic's Claude AI. The game allows players to create characters and make choices that dynamically shape their story, with Claude AI acting as the game master to simulate realistic (or fantastical) outcomes.

**Core Purpose**: Create an immersive, infinite-possibility life simulation where player agency drives emergent narratives through AI-powered scenario generation.

## Architecture Overview

The codebase consists of three main interaction patterns:

```
┌─────────────────────────────────────────┐
│  User Interaction Layer                 │
├─────────────────────────────────────────┤
│  • life_sim_game.py (Interactive CLI)   │
│  • game_session.py (Stateful Sessions)  │
│  • play.py + game_master.py (Async)     │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Claude AI API Layer                    │
│  (Anthropic Python SDK)                 │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  State Management                       │
│  • In-memory (life_sim_game.py)         │
│  • JSON files (game_session.py, play.py)│
└─────────────────────────────────────────┘
```

## File Structure

### Core Game Files

#### `life_sim_game.py` (176 lines)
**Purpose**: Original standalone interactive CLI game.

**Key Components**:
- `LifeSimGame` class: Main game controller
- `conversation_history`: List of message dicts maintaining full context
- `display_welcome()`: ASCII art welcome screen
- `start_new_life()`: Character creation and initial scenario generation
- `process_action()`: Sends actions to Claude and returns outcomes
- `play()`: Main game loop with input/output

**State Management**: In-memory only (lost on exit)

**Usage Pattern**:
```python
game = LifeSimGame()
game.play()  # Blocks until user quits
```

#### `game_session.py` (173 lines)
**Purpose**: Non-interactive session handler for chat/async environments.

**Key Components**:
- `GameSession` class: Persistent session manager
- `STATE_FILE`: `/home/user/Claude-AI/game_state.json`
- `load_state()` / `save_state()`: JSON-based persistence
- `start_game(character_desc)`: Initialize with optional character
- `take_action(action)`: Process single action and save state
- `reset()`: Clear all state

**State Format**:
```json
{
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "started": true/false
}
```

**Usage Pattern**:
```bash
python game_session.py start "character description"
python game_session.py action "what you do"
python game_session.py reset
```

#### `play.py` (131 lines)
**Purpose**: Simplified player interface for async Claude interactions.

**Key Components**:
- `GAME_FILE`: `/home/user/Claude-AI/game_state.json`
- `load_game()` / `save_game()`: Simpler state structure
- `add_action(action)`: Records player actions
- `display_story()`: Pretty-prints full story with emojis

**State Format**:
```json
{
  "history": [
    {
      "speaker": "YOU" | "CLAUDE AI" | "SYSTEM",
      "text": "...",
      "isPlayer": true/false,
      "timestamp": "ISO8601"
    }
  ],
  "character": "...",
  "started": true/false
}
```

**Design Intent**: Player records actions; Claude (via separate command) adds responses.

#### `game_master.py` (81 lines)
**Purpose**: Companion to `play.py` - allows Claude to respond to player actions.

**Key Functions**:
- `view_latest()`: Show last 5 history entries
- `add_response(text)`: Add Claude's response with timestamp
- `start_game(character)`: Initialize game state

**Usage Pattern**:
```bash
python game_master.py view          # See recent actions
python game_master.py respond "..."  # Add AI response
python game_master.py start "..."    # Initialize game
```

### Configuration Files

#### `requirements.txt`
```
anthropic>=0.39.0
python-dotenv>=1.0.0
```

#### `.env.example`
Template for API key configuration. Users copy to `.env` and add their key.

#### `.gitignore`
Standard Python ignores + `.env` + `game_state.json` (runtime state)

### Frontend

#### `game.html` (estimated ~300 lines)
Web-based game interface (not analyzed in detail - HTML/JS frontend).

## Development Workflows

### For AI Assistants Working on This Codebase

#### 1. Adding New Features

**Before implementing**:
- Identify which file(s) to modify based on use case:
  - `life_sim_game.py`: For standalone CLI enhancements
  - `game_session.py`: For stateful/async features
  - `play.py` / `game_master.py`: For chat-based interfaces

**Common patterns**:
- Always preserve `conversation_history` structure for Claude API
- Use consistent `system_prompt` across files (see System Prompt Pattern below)
- Handle API errors gracefully (see Error Handling Pattern)

#### 2. Testing Changes

**Local testing**:
```bash
# Test standalone game
python life_sim_game.py

# Test session-based game
python game_session.py start "test character"
python game_session.py action "test action"

# Test async play interface
python play.py start "test character"
python game_master.py view
```

**API key testing**:
```bash
# Verify .env is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Key found' if os.getenv('ANTHROPIC_API_KEY') else 'No key')"
```

#### 3. Debugging Common Issues

**Issue**: "ANTHROPIC_API_KEY not found"
- Check `.env` file exists and is in correct directory
- Verify no quotes around key in `.env`
- Ensure `load_dotenv()` is called before accessing env vars

**Issue**: "Error processing your action"
- Check API key validity at console.anthropic.com
- Verify internet connection
- Check API rate limits/credits
- Review exception details in error message

**Issue**: State file conflicts
- `game_session.py` and `play.py` use same `game_state.json` but different formats
- Don't mix these interfaces in the same session
- Use `reset` command to clear state between different modes

## Code Conventions

### Python Style

**Imports**:
```python
# Standard library first
import os
import sys
import json
from datetime import datetime

# Third-party libraries
from anthropic import Anthropic
from dotenv import load_dotenv
```

**Docstrings**: All functions use brief one-line docstrings.

**Error handling**:
```python
try:
    # API call
except Exception as e:
    print(f"\nError: {e}")
    # Rollback state if needed
```

### Claude API Patterns

#### System Prompt Pattern

All files use consistent game master instructions:

```python
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
```

**Why this matters**: The system prompt defines Claude's behavior as game master. Changes here affect the entire game experience.

#### API Call Pattern

```python
response = self.client.messages.create(
    model="claude-sonnet-4-5-20250929",  # Latest Sonnet model
    max_tokens=1024,                      # ~768 words max response
    system=system_prompt,
    messages=self.conversation_history    # Full context
)

outcome = response.content[0].text  # Extract text from content blocks
```

**Key details**:
- Uses Sonnet 4.5 (latest as of Jan 2025)
- `max_tokens=1024` balances response length with cost
- Passes entire conversation history for context
- Extracts text from first content block

#### Conversation History Pattern

```python
# Format for Claude API
self.conversation_history = [
    {"role": "user", "content": "Character: [description]"},
    {"role": "assistant", "content": "[scenario]"},
    {"role": "user", "content": "I choose to: [action]"},
    {"role": "assistant", "content": "[outcome]"},
    # ... continues
]
```

**Rules**:
- Must alternate user/assistant roles
- First message must be from user
- Content is always a string (not list of content blocks)
- On error, pop the last user message to maintain consistency

### State Management Patterns

#### In-Memory State (`life_sim_game.py`)
```python
class LifeSimGame:
    def __init__(self):
        self.conversation_history = []  # List of message dicts
        self.game_context = ""          # Currently unused
```

**Pros**: Simple, fast, no I/O overhead
**Cons**: Lost on exit, can't resume sessions

#### File-Based State (`game_session.py`)
```python
def save_state(self):
    with open(STATE_FILE, 'w') as f:
        json.dump({
            'history': self.conversation_history,
            'started': self.started
        }, f, indent=2)
```

**Pros**: Persistent, resumable sessions
**Cons**: Disk I/O overhead, potential file conflicts

## Key Design Patterns

### 1. Game Loop Pattern

```python
while True:
    action = input("> ").strip()

    if action.lower() in ['quit', 'exit', 'q']:
        break

    try:
        outcome = self.process_action(action)
        print(outcome)
    except Exception as e:
        print(f"Error: {e}")
        self.conversation_history.pop()  # Rollback on error
```

**Key principle**: Always rollback conversation history on API errors to maintain valid alternating user/assistant pattern.

### 2. Error Recovery Pattern

```python
except Exception as e:
    print(f"\nError: {e}")
    print("There was an issue processing your action. Please try again.")
    if self.conversation_history:
        self.conversation_history.pop()  # Remove failed user message
```

**Why**: Claude API requires strict message alternation. Failed API call leaves orphaned user message.

### 3. Character Creation Pattern

```python
character_input = input("> ").strip()

if not character_input:
    character_input = "Create a random character for me"

# Send to Claude with special instructions
messages = [{
    "role": "user",
    "content": f"Start a life simulation game. Character description: {character_input}\n\nCreate an engaging opening scenario..."
}]
```

**Design choice**: Empty input triggers random character generation by Claude rather than forcing user input.

## AI Assistant Guidelines

### When Adding Features

1. **Preserve Core Behavior**
   - Don't change the system prompt without understanding impact
   - Maintain conversation history alternation pattern
   - Keep error rollback logic intact

2. **Follow Existing Patterns**
   - Use consistent error handling across files
   - Match docstring style and format
   - Keep API call structure uniform

3. **Consider All Three Modes**
   - Will your change work in CLI mode? (`life_sim_game.py`)
   - Will it work in session mode? (`game_session.py`)
   - Will it work in async mode? (`play.py` + `game_master.py`)

4. **Test Thoroughly**
   - Test with API key present and missing
   - Test with network errors (mock if needed)
   - Test state persistence and recovery
   - Test edge cases (empty input, very long input, special characters)

### When Modifying API Interactions

**DO**:
- Keep model as `claude-sonnet-4-5-20250929` (or latest Sonnet)
- Maintain `max_tokens=1024` unless you have a specific reason to change
- Always pass full conversation history for context
- Handle `response.content[0].text` safely (check if content exists)

**DON'T**:
- Don't switch to older models (Opus/Haiku) without justification
- Don't reduce max_tokens below 512 (responses become too brief)
- Don't increase max_tokens above 4096 (cost and quality concerns)
- Don't modify message history format (breaks API compatibility)

### When Refactoring

**Safe refactorings**:
- Extract duplicate system prompts to a constant
- Create helper functions for common operations
- Add type hints to function signatures
- Improve variable naming

**Risky refactorings**:
- Changing conversation history structure
- Modifying error handling flow
- Altering state persistence format (breaks compatibility)
- Changing API call patterns

### Security Considerations

1. **API Key Protection**
   - Never commit `.env` to git (already in `.gitignore`)
   - Don't log or print API keys
   - Don't expose keys in error messages

2. **User Input Handling**
   - All user input goes to Claude API (validated by Anthropic)
   - No local code execution based on user input
   - JSON state files could be injection vectors if extended

3. **State File Security**
   - `game_state.json` is world-readable by default
   - Consider adding file permission restrictions for multi-user systems
   - No sensitive data currently stored in state

## Common Modification Scenarios

### Adding a New Command

**In `life_sim_game.py`**:
```python
# In play() method, modify game loop:
if action.lower() == 'help':
    self.show_help()
    continue
elif action.lower() in ['quit', 'exit', 'q']:
    # ... existing quit logic
```

**In `game_session.py`**:
```python
# In main(), add new command:
elif command == "help":
    session.show_help()
```

### Changing System Prompt

**Best practice**: Extract to a constant at module level:

```python
# At top of file
GAME_MASTER_PROMPT = """You are a creative and immersive life simulation game master.
Your role is to:
1. Create vivid, detailed scenarios based on player choices
2. [... etc ...]
"""

# In functions, reference the constant:
response = self.client.messages.create(
    system=GAME_MASTER_PROMPT,
    # ...
)
```

**Impact**: Affects all future Claude responses in that module.

### Adding State Fields

**In `game_session.py`**:
```python
def save_state(self):
    with open(STATE_FILE, 'w') as f:
        json.dump({
            'history': self.conversation_history,
            'started': self.started,
            'player_stats': self.player_stats,  # NEW FIELD
        }, f, indent=2)

def load_state(self):
    # ...
    self.player_stats = data.get('player_stats', {})  # NEW FIELD WITH DEFAULT
```

**Important**: Always provide defaults in `load_state()` for backward compatibility.

### Changing Response Length

```python
# Shorter responses (faster, cheaper, less detailed):
max_tokens=512

# Standard responses (current):
max_tokens=1024

# Longer responses (slower, pricier, more detailed):
max_tokens=2048
```

**Cost impact**: 2x tokens ≈ 2x cost. Test with smaller sessions first.

## File Path References

When working with this codebase, note these absolute paths:

- State file: `/home/user/Claude-AI/game_state.json`
- Environment: `/home/user/Claude-AI/.env`
- Project root: `/home/user/Claude-AI/`

**Why absolute paths?**: `game_master.py` and `play.py` can be called from any directory.

## Git Workflow

### Current Branch Structure

```bash
# Main development branch
main

# Feature branches for Claude Code sessions
claude/claude-md-*

# Current branch (as of this guide)
claude/claude-md-mi5kcf3y7xsjzvya-01FMqiUtCxdMZQcQJZuwuWq5
```

### Commit Message Convention

Based on recent commits:

```
Add [feature/component] [description]

Examples:
- Add interactive game interface with Claude as game master
- Add interactive game session handler for chat environments
- Add life simulation game powered by Claude AI
```

**Pattern**: `Add [what] [context/purpose]`

### Making Changes

```bash
# Ensure on correct feature branch
git status

# Make changes, test thoroughly
python life_sim_game.py  # or other test commands

# Stage changes
git add [files]

# Commit with descriptive message
git commit -m "Add [feature description]"

# Push to feature branch
git push -u origin claude/claude-md-mi5kcf3y7xsjzvya-01FMqiUtCxdMZQcQJZuwuWq5
```

## API Cost Optimization

### Current Usage Pattern

**Per game session** (estimated):
- Initial scenario: ~300 tokens (input) + ~400 tokens (output)
- Each action: ~500 tokens (input, growing) + ~400 tokens (output)
- 10 actions ≈ 9,000 total tokens ≈ $0.03-0.05

### Optimization Strategies

1. **Reduce Context Window** (risky - loses continuity):
```python
# Keep only last N messages
MAX_HISTORY = 20
messages = self.conversation_history[-MAX_HISTORY:]
```

2. **Summarize Old History** (complex - requires extra API calls):
```python
# Periodically summarize old messages into single context message
if len(self.conversation_history) > 30:
    summary = self.summarize_history(self.conversation_history[:-10])
    self.conversation_history = [summary] + self.conversation_history[-10:]
```

3. **Use Haiku for Simple Responses** (changes experience):
```python
# For simple acknowledgments, use cheaper model
model = "claude-haiku-4-5" if is_simple_action else "claude-sonnet-4-5-20250929"
```

**Recommendation**: Current approach is reasonable. Optimize only if cost becomes a problem.

## Testing Checklist

When making changes, verify:

- [ ] Game starts successfully with character creation
- [ ] Actions receive appropriate responses from Claude
- [ ] Conversation history maintains continuity
- [ ] Error handling works (test with invalid API key)
- [ ] State saves and loads correctly (for `game_session.py`)
- [ ] Quit commands work gracefully
- [ ] No API keys are logged or exposed
- [ ] `.env` file is properly loaded
- [ ] Python 3.7+ compatibility maintained

## Future Enhancement Ideas

Based on codebase analysis, potential improvements:

1. **Save/Load Named Sessions**
   - Multiple save slots
   - Session naming and metadata

2. **Character Stats Tracking**
   - Health, wealth, skills, relationships
   - Persistent across actions

3. **Achievements System**
   - Track unique outcomes
   - Unlock special scenarios

4. **Context Window Management**
   - Automatic summarization of old history
   - Reduce token usage for long sessions

5. **Multi-Model Support**
   - Use Haiku for simple actions (cheaper)
   - Use Sonnet for complex scenarios (current)
   - Use Opus for critical story moments (premium)

6. **Web Interface Integration**
   - Connect `game.html` to Python backend
   - Real-time streaming responses
   - Visual character/stat display

7. **Multiplayer/Shared Worlds**
   - Multiple players in same simulation
   - Turn-based or simultaneous actions

8. **Export Story to Formats**
   - Markdown export of full story
   - PDF generation with formatting
   - HTML story viewer

## Quick Reference

### Environment Setup
```bash
git clone https://github.com/XiomaiRize/Claude-AI.git
cd Claude-AI
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
```

### Run Commands
```bash
# Standalone CLI
python life_sim_game.py

# Session-based (persistent state)
python game_session.py start "character"
python game_session.py action "what you do"
python game_session.py reset

# Async play mode
python play.py start "character"
python play.py action "what you do"
python game_master.py view
python game_master.py respond "AI response"
```

### Key Files for Common Tasks

| Task | File(s) to Modify |
|------|-------------------|
| Change AI behavior | All files with `system_prompt` |
| Add new command | `*_game.py` game loop / `main()` |
| Modify state structure | `game_session.py`, `play.py` |
| Change API model/params | All files with `client.messages.create()` |
| Update dependencies | `requirements.txt` |
| Add frontend features | `game.html` |

---

**Last Updated**: 2025-11-19
**Compatible Versions**: Python 3.7+, anthropic>=0.39.0
**Claude Model**: claude-sonnet-4-5-20250929

For questions or issues, refer to the repository README or open a GitHub issue.
