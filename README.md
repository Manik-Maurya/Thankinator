#🤖 Thankinator

> *It's been watching. It's always been watching.* 👀

**Thankinator** is a free, open-source Discord bot that silently counts every "thank you" said in your server — in every form, every spelling, every language — and ranks everyone on a gamified leaderboard with 12 hilariously judgemental tiers.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![discord.py](https://img.shields.io/badge/discord.py-2.3%2B-5865F2?logo=discord)](https://discordpy.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Free Hosting](https://img.shields.io/badge/Hosting-Free%2024%2F7-brightgreen)](https://wispbyte.com)

---

## ✨ What It Does

Thankinator watches every message in your server and detects every known form of "thank you" — from the standard to the unhinged:

| Detected | Examples |
|---|---|
| Standard | `thank you`, `thanks`, `thank u` |
| Abbreviated | `ty`, `thx`, `thnks`, `thnx` |
| Typo'd | `tanks`, `tank you`, `tankyu` |
| Stretched | `tyyy`, `thankssss`, `thxxx` |
| Formal | `much appreciated`, `greatly appreciated`, `appreciate it` |
| Extended | `thanks a lot`, `thanks a million`, `many thanks` |
| Informal | `cheers`, `ta` |
| Multilingual | `gracias`, `merci`, `danke`, `dhanyavaad`, `shukriya`, `arigatou`, `shukran` |

All **case-insensitive**. `THANK YOU` = `thank you` = `ThAnK yOu`.

---

## 🎖️ The 12 Rank Tiers

| Rank | Required |
|---|---|
| 🌌 Cosmic Gratitude God | 500+ |
| 🏆 Gratitude Guru | 250+ |
| 👑 Thanks Titan | 150+ |
| 🚀 Appreciation Astronaut | 100+ |
| 🔥 Thankful Inferno | 75+ |
| ⚡ Lightning Thanker | 50+ |
| 🌟 Thank You Enthusiast | 30+ |
| 🎯 Consistent Acknowledger | 20+ |
| 🌱 Budding Appreciator | 10+ |
| 🐣 Gratitude Hatchling | 5+ |
| 🫣 Reluctant Acknowledger | 1+ |
| 👻 Ghost of Gratitude | 0 |

Each rank has its own lore. Yes, lore.

---

## 🚀 Features

- **Auto-detection** — no commands needed, just talk naturally
- **🙏 reaction** on every detected thank you
- **Witty replies** — occasional funny responses (15% chance, auto-delete)
- **Milestone celebrations** — server-wide announcements at 5, 10, 25, 50, 100, 250, 500
- **Gamified leaderboard** with 12 rank tiers
- **Personal stats** for any member
- **Server-wide analytics**
- **Both slash commands and prefix commands**
- **SQLite storage** — no external database needed
- **40+ detection patterns** including multilingual
- **Completely free to run**

---

## 📋 Commands

| Command | Aliases | Description |
|---|---|---|
| `!lb` | `!leaderboard` `!ranking` `!top` | Hall of Gratitude leaderboard 🏆 |
| `!mythanks` | `!me` `!score` | Your personal stats 📊 |
| `!mythanks @user` | | Check someone else's stats |
| `!serverstats` | `!server` `!total` | Server-wide analytics 🌐 |
| `!ranks` | `!tiers` `!levels` | View all rank tiers 🎖️ |
| `!yw` | `!help` | Command list |
| `/leaderboard` | | Slash version |
| `/mythanks` | | Slash version |

---

## 🛠️ Self-Hosting Setup

### Prerequisites

- Python 3.10 or higher
- A Discord account
- 5 minutes

### Step 1 — Create your Discord Bot

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application** → name it **Thankinator**
3. Go to **Bot** in the sidebar
4. Click **Add Bot** → confirm
5. Enable these under **Privileged Gateway Intents**:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
6. Click **Reset Token** → copy it (keep it secret!)

### Step 2 — Invite the Bot to Your Server

1. Go to **OAuth2 → URL Generator**
2. Check scopes: `bot` and `applications.commands`
3. Check permissions: `Read Messages`, `Send Messages`, `Add Reactions`, `Read Message History`, `Use Application Commands`
4. Copy the generated URL → open in browser → select your server → Authorize

### Step 3 — Run Locally

```bash
# Clone the repo
git clone https://github.com/Manik-Maurya/Thankinator.git
cd Thankinator

# Install dependencies
pip install -r requirements.txt

# Set up your token
cp .env.example .env
# Open .env in any text editor and paste your bot token

# Run
python bot.py
```

You should see:
```
✅  You're Welcome! is online as Thankinator#XXXX
📡  Connected to 1 server(s)
🔄  Synced 2 slash command(s).
```

---

## ☁️ Free 24/7 Hosting Options

### Option 1 — Wispbyte (Recommended, Free Forever)

1. Sign up at [wispbyte.com](https://wispbyte.com)
2. Create a new server → select **Python**
3. Upload `bot.py` and `requirements.txt`
4. Add environment variable: `DISCORD_TOKEN` = your token
5. Set startup command to `python bot.py`
6. Hit Start ✅

### Option 2 — Railway ($5/month, easiest)

1. Push this repo to GitHub
2. Sign up at [railway.app](https://railway.app) with GitHub
3. New Project → Deploy from GitHub repo → select this repo
4. Add environment variable: `DISCORD_TOKEN` = your token
5. Deploy ✅

### Option 3 — Fly.io (Free tier available)

Follow [Fly.io's Python app guide](https://fly.io/docs/languages-and-frameworks/python/) and set `DISCORD_TOKEN` as a secret.

---

## 🗄️ Data & Privacy

- Stores: Discord **user IDs**, **display names**, and **thank-you counts** only
- Does **not** store message content
- All data lives in a local `yourewelcome.db` SQLite file
- Users can request data deletion by contacting the server admin

---

## 🤝 Contributing

Pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas for contributions:
- New language detections
- Additional rank tiers
- Per-channel leaderboards
- Weekly/monthly stats reset
- Web dashboard

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details. Free to use, modify, and distribute.

---

## 🙏 Credits

Built with [discord.py](https://discordpy.readthedocs.io) — an excellent Python library for Discord bots.

Originally built as a surprise gift for a professor who casually joked about wanting a thank-you counter. She got one. With 12 rank tiers and lore.

---

*Made with 🙏 and an unreasonable amount of regex.*
