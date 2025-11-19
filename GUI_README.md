# Dynamic RPG - Web GUI Edition

## 🎮 Beautiful HTML/CSS Interface

A fully graphical RPG interface with:
- **Top Panel**: Character stats with animated HP/MP/EXP bars
- **Center Panel**: Large narrative display where the story unfolds
- **Bottom Panel**: Text input for your actions
- **Left Sidebar**: Quick action buttons (Inventory, Abilities, Stats, Simulation)
- **Right Sidebar**: Real-time world state and condition tracking

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Make Sure You Have Your API Key

Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Start the Server

```bash
python rpg_server.py
```

You'll see:
```
🎮 Starting Dynamic RPG Server...
📡 Open your browser to: http://localhost:5000
```

### 4. Open Your Browser

Go to: **http://localhost:5000**

## 🎨 The Interface

### Character Creation Screen

When you first load, you'll see a modal with:
- Name input field
- 5 class options (Warrior, Mage, Rogue, Cleric, Battlemage)
- Start Adventure button

### Main Game Screen

#### Top Stats Panel
```
┌──────────────────────────────────────────────────────┐
│ Character: Hero   Level: 1   Class: Warrior   Gold: 100g│
│                                                        │
│ Health:  [████████████████████] 100/100              │
│ Mana:    [████████████        ] 50/50                │
│ Exp:     [███                 ] 0/100                │
└──────────────────────────────────────────────────────┘
```

#### Left Sidebar - Action Buttons
- 📦 **Inventory** - View your items
- ✨ **Abilities** - List your skills
- 📊 **Stats** - Full character stats
- 🔬 **Simulation** - See NPC emotions, world state
- 💾 **Save** - Save your progress
- ❓ **Help** - Show help info

#### Center - Narrative Display
Scrolling story text where the AI narrates your adventure:
```
┌───────────────────────────────────────┐
│ NARRATIVE DISPLAY                     │
│                                       │
│ You enter the peaceful village...    │
│ The elder approaches you...           │
│                                       │
│ > I talk to the elder                │
│                                       │
│ The elder smiles warmly...            │
└───────────────────────────────────────┘
```

#### Right Sidebar - Info
- **Quick Stats**: STR, AGI, INT, DEF, MDEF
- **World State**: Time, Weather, Fame
- **Conditions**: Active buffs/debuffs

#### Bottom - Input Panel
```
┌───────────────────────────────────────┐
│ 🎭 What do you do?                    │
│ ┌───────────────────────────────────┐ │
│ │ Type your action here...          │ │
│ │                                   │ │
│ └───────────────────────────────────┘ │
│                                       │
│ Quick Actions:                        │
│ [👀 Look] [🎒 Inventory] [💬 Talk]   │
└───────────────────────────────────────┘
```

## 🎯 How to Play

### Type Natural Actions

Just type what you want to do in the text box:
- "I explore the dark forest"
- "I talk to the blacksmith"
- "I attack the goblin with my sword"
- "I cast fireball at the orc"
- "I check my inventory"

### Use Quick Actions

Click the quick action buttons for common commands:
- 👀 Look Around
- 🎒 Check Inventory
- 💬 Talk
- 🗺️ Explore

### Click Sidebar Buttons

Access game systems via the left sidebar:
- **Inventory**: See all your items
- **Abilities**: View learned skills
- **Stats**: Full character sheet
- **Simulation**: See ALL tracked variables (NPC emotions, world state, conditions)

## 🎨 Visual Features

### Animated Stat Bars
- HP bar fills/depletes in **red gradient**
- MP bar in **blue gradient**
- EXP bar in **green gradient**
- Smooth animations on stat changes

### Color-Coded Messages
- **Blue border**: System/GM messages
- **Green border**: Your actions
- **Orange border**: Special events

### Hover Effects
- Buttons glow on hover
- Interactive elements have visual feedback
- Smooth transitions throughout

### Scrolling Narrative
- Auto-scrolls to latest message
- Styled scrollbars
- Fade-in animations for new text

## 📡 Technical Details

### Backend (Python)
- **Flask** server handling HTTP requests
- **Flask-SocketIO** for real-time WebSocket communication
- **Anthropic API** for Claude AI game master
- All game logic from `rpg_engine/` modules

### Frontend (HTML/CSS/JavaScript)
- **Pure HTML/CSS** - no frameworks needed
- **Socket.IO** client for real-time updates
- **Responsive design** - adapts to window size
- **Custom CSS** for RPG aesthetic

### Real-Time Updates
- Player actions sent via WebSocket
- AI responses stream back instantly
- Stats update in real-time
- Simulation state syncs automatically

## 🔧 Customization

### Change Colors

Edit `/templates/game.html`, look for CSS variables:
```css
/* Main accent color */
border: 2px solid #4a9eff; /* Change this blue */

/* Background gradient */
background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
```

### Adjust Layout

The grid layout is defined in `.game-container`:
```css
grid-template-columns: 250px 1fr 250px;  /* Left | Center | Right */
grid-template-rows: 150px 1fr 180px;     /* Top | Middle | Bottom */
```

### Add Custom Quick Actions

In the HTML, add more quick action buttons:
```html
<div class="quick-action" onclick="quickAction('your action here')">
    🎯 Your Action
</div>
```

## 🎮 Gameplay Features

### Character Stats Tracked
- Name, Level, Class, Gold
- HP, MP, EXP (with bars)
- STR, AGI, INT, DEF, MDEF

### Simulation Variables Visible
- NPC Emotions (affection, trust, respect, fear, annoyance)
- Player Conditions (bleeding, poisoned, cursed, etc.)
- World State (time, weather, fame, safety)

### Real-Time AI
- Claude processes every action
- Manages simulation variables
- Can modify game code on the fly
- Creates dynamic narrative

## 📱 Browser Compatibility

Works on:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Most modern browsers

## 🐛 Troubleshooting

### Can't connect to server
- Make sure server is running (`python rpg_server.py`)
- Check if port 5000 is available
- Try `http://127.0.0.1:5000` instead of `localhost`

### Stats not updating
- Check browser console for errors (F12)
- Refresh the page
- Restart the server

### API errors
- Verify `ANTHROPIC_API_KEY` is set in `.env`
- Check your API key is valid
- Ensure you have API credits

## 🎯 Next Steps

1. Start the server: `python rpg_server.py`
2. Open browser: `http://localhost:5000`
3. Create your character
4. Type your first action!

**The AI Game Master is ready to run your adventure!** 🎮✨

---

## File Structure

```
/home/user/Claude-AI/
├── rpg_server.py          # Flask backend server
├── templates/
│   └── game.html          # GUI interface
├── rpg_engine/            # Game logic modules
│   ├── character.py
│   ├── combat.py
│   ├── items.py
│   ├── abilities.py
│   ├── world.py
│   ├── simulation.py
│   ├── races.py
│   ├── classes.py
│   └── personality.py
└── saves/                 # Player save files
```

Enjoy your adventure! ⚔️🔮✨
