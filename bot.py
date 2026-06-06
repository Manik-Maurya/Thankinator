"""
╔══════════════════════════════════════════════════════════╗
║           You're Welcome!  — Discord Bot                 ║
║   A premium, gamified thank-you counter for Discord      ║
║   Author: gifted with 🙏 to a very cool professor        ║
╚══════════════════════════════════════════════════════════╝

Usage:
  !lb / /leaderboard     →  Hall of Gratitude 🏆
  !mythanks / /mythanks  →  Your personal stats 📊
  !serverstats           →  Server-wide gratitude analytics
  !yw                    →  Show commands list
"""

import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import re
import os
import random
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("DISCORD_TOKEN", "")
DB_FILE   = "yourewelcome.db"

# ══════════════════════════════════════════════════════════
#   COLOUR PALETTE
# ══════════════════════════════════════════════════════════
COLORS = {
    "gold":    0xFFD700,
    "silver":  0xC0C0C0,
    "bronze":  0xCD7F32,
    "blurple": 0x5865F2,
    "green":   0x57F287,
    "red":     0xED4245,
    "purple":  0x9B59B6,
    "pink":    0xFF73FA,
    "teal":    0x1ABC9C,
}

# ══════════════════════════════════════════════════════════
#   THANK-YOU DETECTION ENGINE
#   Covers: standard | abbreviated | typo'd | stretched |
#           multi-word | multi-language
# ══════════════════════════════════════════════════════════
_THANK_PATTERNS = [
    # ── Standard + spaced + hyphenated ──
    r"\bthank\s*you\b",
    r"\bthank-you\b",
    r"\bthankyou+\b",           # thankyou, thankyouu …
    r"\bthank\s*u+\b",          # thank u, thank uuu …
    r"\bthanku+\b",
    r"\bthanks+\b",             # thanks, thankss …
    r"\bthankies\b",
    r"\bthankie\b",

    # ── Abbreviations & internet shorthand ──
    r"\bty+\b",                 # ty, tyy, tyyy …
    r"\bthx+\b",                # thx, thxx …
    r"\bthnx+\b",
    r"\bthnks+\b",
    r"\bthnku+\b",
    r"\btnx\b",
    r"\bthku\b",

    # ── Common typos ──
    r"\btank\s*you\b",          # tanks you
    r"\btanks\b",               # tanks
    r"\btankyu\b",
    r"\bthankyu+\b",

    # ── Formal / extended ──
    r"\bmany\s+thanks\b",
    r"\bbig\s+thanks\b",
    r"\bgreat\s+thanks\b",
    r"\bmuch\s+thanks\b",
    r"\bheaps\s+of\s+thanks\b",
    r"\bdeepest\s+thanks\b",
    r"\bsincere\s+thanks\b",
    r"\bthanks\s+a\s+(lot|ton|bunch|million|billion|heap|load|zillion|tonne)\b",
    r"\bthank\s+you\s+(so\s+)?(very\s+)?much\b",
    r"\bthank\s+you\s+(so\s+)?kindly\b",
    r"\bthankful\b",
    r"\bthankfulness\b",

    # ── Appreciation synonyms ──
    r"\bappreciate\s+(it|this|that|you|your|everything|the\s+help)\b",
    r"\bi?\s*much\s+appreciated\b",
    r"\bgreatly\s+appreciated\b",
    r"\bvery\s+much\s+appreciated\b",
    r"\bcheers\b",              # British
    r"\bta\b",                  # British informal

    # ── Multi-language bonus 🌍 ──
    r"\bgracias\b",             # Spanish
    r"\bmerci\b",               # French
    r"\bdanke\b",               # German
    r"\bdankeschoen\b",
    r"\bspasibo\b",             # Russian (romanised)
    r"\bdhanyavaad\b",          # Hindi
    r"\bdhanyawad\b",
    r"\bshukriya+\b",           # Urdu/Hindi
    r"\bshukriyaa+\b",
    r"\bshukran\b",             # Arabic
    r"\barigatou?\b",           # Japanese (romanised)
    r"\bkamsahamnida\b",        # Korean (romanised)
    r"\bxie\s*xie\b",           # Mandarin (romanised)
    r"\bnamaskaar\b",           # Hindi gratitude
]

_COMPILED = re.compile("|".join(_THANK_PATTERNS), re.IGNORECASE)

def detect_thank_you(text: str) -> bool:
    """Return True if the message contains any recognised thank-you form."""
    return bool(_COMPILED.search(text))


# ══════════════════════════════════════════════════════════
#   RANK SYSTEM  (threshold → emoji title, subtitle)
# ══════════════════════════════════════════════════════════
_RANKS = [
    (500, "🌌 Cosmic Gratitude God",       "Has thanked their way to another dimension"),
    (250, "🏆 Gratitude Guru",              "The undisputed oracle of appreciation"),
    (150, "👑 Thanks Titan",                "Basically a walking thank-you card"),
    (100, "🚀 Appreciation Astronaut",      "Shooting thanks into the stratosphere"),
    (75,  "🔥 Thankful Inferno",            "Cannot stop. Will not stop. Thanking."),
    (50,  "⚡ Lightning Thanker",           "Faster than you can say 'you're welcome'"),
    (30,  "🌟 Thank You Enthusiast",        "Genuinely, aggressively enthusiastic"),
    (20,  "🎯 Consistent Acknowledger",     "Shows up, says thanks, no drama"),
    (10,  "🌱 Budding Appreciator",         "Just starting to bloom"),
    ( 5,  "🐣 Gratitude Hatchling",         "Freshly hatched from the thankfulness egg"),
    ( 1,  "🫣 Reluctant Acknowledger",      "Fine. They said it once. Happy?"),
    ( 0,  "👻 Ghost of Gratitude",          "Theoretically exists in this server"),
]

def get_rank(count: int) -> tuple[str, str]:
    for threshold, title, subtitle in _RANKS:
        if count >= threshold:
            return title, subtitle
    return "👻 Ghost of Gratitude", "Theoretically exists in this server"

def position_medal(pos: int) -> str:
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(pos, f"`#{pos:02}`")

_MILESTONES: frozenset[int] = frozenset({5, 10, 25, 50, 75, 100, 150, 250, 500, 1000})

# ══════════════════════════════════════════════════════════
#   RANDOM "YOU'RE WELCOME" REPLIES  (fires ~15% of time)
# ══════════════════════════════════════════════════════════
_YW_REPLIES = [
    "You're welcome… oh wait, nobody said that to *me*. 😌",
    "Gratitude detected. Logging for eternity. 📋",
    "Another one for the Hall of Gratitude. 🙏",
    "The algorithm acknowledges your politeness. ✅",
    "Appreciation: noted, timestamped, immortalised. 🏛️",
    "Thank you noted! You are statistically kinder than average. 📊",
    "A thank you? In THIS economy?! Respect. 👏",
    "Your mom raised you right. Thank you counter goes brrr. 🔢",
    "Manners? In a Discord server? Unprecedented. 🫡",
    "Logged. Filed. Framed. Hung on the wall. 🖼️",
    "Somewhere, a gratitude fairy gets its wings. 🧚",
    "This thank you has been added to your permanent record. 📁",
]

# ══════════════════════════════════════════════════════════
#   DATABASE
# ══════════════════════════════════════════════════════════
def init_db() -> None:
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS thanks (
                user_id      INTEGER NOT NULL,
                guild_id     INTEGER NOT NULL,
                username     TEXT    NOT NULL,
                count        INTEGER NOT NULL DEFAULT 0,
                last_thanked TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, guild_id)
            )
        """)
        conn.commit()

def increment_thanks(user_id: int, guild_id: int, username: str) -> int:
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO thanks (user_id, guild_id, username, count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(user_id, guild_id)
            DO UPDATE SET
                count        = count + 1,
                username     = excluded.username,
                last_thanked = CURRENT_TIMESTAMP
        """, (user_id, guild_id, username))
        conn.commit()
        row = conn.execute(
            "SELECT count FROM thanks WHERE user_id=? AND guild_id=?",
            (user_id, guild_id)
        ).fetchone()
        return row[0] if row else 1

def get_user_stats(user_id: int, guild_id: int) -> dict:
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT username, count FROM thanks WHERE user_id=? AND guild_id=?",
            (user_id, guild_id)
        ).fetchone()
    if not row:
        return {"count": 0, "rank": None, "username": "Unknown"}
    lb = get_leaderboard(guild_id, limit=9999)
    rank = next((i + 1 for i, r in enumerate(lb) if r["user_id"] == user_id), None)
    return {"username": row[0], "count": row[1], "rank": rank}

def get_leaderboard(guild_id: int, limit: int = 10) -> list[dict]:
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("""
            SELECT user_id, username, count
            FROM   thanks
            WHERE  guild_id = ?
            ORDER  BY count DESC
            LIMIT  ?
        """, (guild_id, limit)).fetchall()
    return [{"user_id": r[0], "username": r[1], "count": r[2]} for r in rows]

def get_guild_total(guild_id: int) -> int:
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT SUM(count), COUNT(*) FROM thanks WHERE guild_id=?",
            (guild_id,)
        ).fetchone()
    return row[0] or 0, row[1] or 0


# ══════════════════════════════════════════════════════════
#   BOT SETUP
# ══════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot  = commands.Bot(command_prefix="!", intents=intents, help_command=None)
tree = bot.tree


# ══════════════════════════════════════════════════════════
#   EVENTS
# ══════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"\n✅  You're Welcome! is online as {bot.user}")
    print(f"📡  Connected to {len(bot.guilds)} server(s)")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="for thank yous 🙏 | !yw for help"
        )
    )
    try:
        synced = await tree.sync()
        print(f"🔄  Synced {len(synced)} slash command(s).\n")
    except Exception as exc:
        print(f"❌  Slash command sync failed: {exc}\n")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return

    if detect_thank_you(message.content):
        new_count = increment_thanks(
            message.author.id,
            message.guild.id,
            message.author.display_name,
        )

        # Always add a 🙏 reaction
        try:
            await message.add_reaction("🙏")
        except discord.HTTPException:
            pass

        # ~15% chance of a witty reply
        if random.random() < 0.15:
            try:
                await message.reply(
                    random.choice(_YW_REPLIES),
                    mention_author=False,
                    delete_after=12,
                )
            except discord.HTTPException:
                pass

        # Milestone celebration
        if new_count in _MILESTONES:
            rank_title, _ = get_rank(new_count)
            embed = discord.Embed(
                title="🎉  GRATITUDE MILESTONE UNLOCKED!",
                description=(
                    f"{message.author.mention} just crossed "
                    f"**{new_count:,} thank yous!** 🔥\n\n"
                    f"New rank: **{rank_title}**"
                ),
                color=COLORS["gold"],
            )
            embed.set_footer(text="You're Welcome! • !lb to see the leaderboard")
            try:
                await message.channel.send(embed=embed, delete_after=20)
            except discord.HTTPException:
                pass

    await bot.process_commands(message)


# ══════════════════════════════════════════════════════════
#   SHARED EMBED BUILDERS
# ══════════════════════════════════════════════════════════
def build_leaderboard_embed(guild: discord.Guild) -> discord.Embed:
    results             = get_leaderboard(guild.id)
    total_thanks, total_people = get_guild_total(guild.id)

    embed = discord.Embed(
        title="🙏  THE HALL OF GRATITUDE",
        description=(
            f"*Where appreciation is measured, immortalised, and mildly judged.*\n"
            f"**{total_thanks:,}** thank yous from **{total_people}** people in this server!\n"
            f"{'─' * 42}"
        ),
        color=COLORS["blurple"],
        timestamp=datetime.utcnow(),
    )

    if not results:
        embed.add_field(
            name="No entries yet!",
            value="Start saying thank you — it's free and it absolutely counts! 🙏",
            inline=False,
        )
    else:
        for i, row in enumerate(results, 1):
            medal            = position_medal(i)
            rank_title, rank_sub = get_rank(row["count"])
            embed.add_field(
                name=f"{medal}  {row['username']}",
                value=(
                    f"{rank_title}\n"
                    f"> *{rank_sub}*\n"
                    f"> **{row['count']:,}** thank yous"
                ),
                inline=False,
            )

    embed.set_footer(text="You're Welcome! Bot  •  !mythanks to see your own stats")
    return embed


def build_stats_embed(target: discord.Member, guild: discord.Guild) -> discord.Embed:
    stats       = get_user_stats(target.id, guild.id)
    count       = stats["count"]
    rank        = stats.get("rank")
    rank_title, rank_sub = get_rank(count)

    color = (
        COLORS["gold"]   if rank == 1 else
        COLORS["silver"] if rank == 2 else
        COLORS["bronze"] if rank == 3 else
        COLORS["blurple"]
    )

    embed = discord.Embed(
        title=f"📊  {target.display_name}'s Gratitude Dossier",
        color=color,
        timestamp=datetime.utcnow(),
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="🙏 Thank Yous Said",  value=f"**{count:,}**",             inline=True)
    embed.add_field(name="🏅 Server Rank",       value=f"**#{rank}**" if rank else "**Unranked**", inline=True)
    embed.add_field(name="\u200b",               value="\u200b",                     inline=True)
    embed.add_field(name="🎖️ Title",            value=rank_title,                   inline=False)
    embed.add_field(name="📝 Lore",             value=f"*{rank_sub}*",              inline=False)
    embed.set_footer(text="You're Welcome! Bot  •  !lb for the full leaderboard")
    return embed


# ══════════════════════════════════════════════════════════
#   LEADERBOARD  (!lb, !leaderboard, !ranking, /leaderboard)
# ══════════════════════════════════════════════════════════
@bot.command(name="leaderboard", aliases=["lb", "board", "ranking", "rank", "top", "hall"])
async def leaderboard_prefix(ctx: commands.Context):
    await ctx.send(embed=build_leaderboard_embed(ctx.guild))

@tree.command(name="leaderboard", description="Show the Hall of Gratitude 🏆")
async def leaderboard_slash(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_leaderboard_embed(interaction.guild))


# ══════════════════════════════════════════════════════════
#   PERSONAL STATS  (!mythanks, /mythanks)
# ══════════════════════════════════════════════════════════
@bot.command(name="mythanks", aliases=["me", "myscore", "mystats", "score"])
async def my_thanks_prefix(ctx: commands.Context, member: Optional[discord.Member] = None):
    target = member or ctx.author
    await ctx.send(embed=build_stats_embed(target, ctx.guild))

@tree.command(name="mythanks", description="Check your (or someone else's) thank-you stats 📊")
@app_commands.describe(member="The member to look up (defaults to you)")
async def my_thanks_slash(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    target = member or interaction.user
    await interaction.response.send_message(embed=build_stats_embed(target, interaction.guild))


# ══════════════════════════════════════════════════════════
#   SERVER STATS  (!serverstats)
# ══════════════════════════════════════════════════════════
@bot.command(name="serverstats", aliases=["server", "total"])
async def server_stats(ctx: commands.Context):
    total_thanks, total_people = get_guild_total(ctx.guild.id)
    top = get_leaderboard(ctx.guild.id, limit=1)

    embed = discord.Embed(
        title=f"🌐  {ctx.guild.name} — Gratitude Analytics",
        color=COLORS["teal"],
        timestamp=datetime.utcnow(),
    )
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
    embed.add_field(name="🙏 Total Thank Yous",  value=f"**{total_thanks:,}**",    inline=True)
    embed.add_field(name="👥 Thankful Members",   value=f"**{total_people}**",      inline=True)

    if total_people:
        avg = round(total_thanks / total_people, 1)
        embed.add_field(name="📈 Avg per Person", value=f"**{avg}**",              inline=True)

    if top:
        embed.add_field(
            name="👑 Most Grateful Member",
            value=f"**{top[0]['username']}** with **{top[0]['count']:,}** thank yous",
            inline=False,
        )

    embed.set_footer(text="You're Welcome! Bot")
    await ctx.send(embed=embed)


# ══════════════════════════════════════════════════════════
#   RANK GUIDE  (!ranks)
# ══════════════════════════════════════════════════════════
@bot.command(name="ranks", aliases=["tiers", "levels"])
async def ranks_cmd(ctx: commands.Context):
    embed = discord.Embed(
        title="🎖️  Rank Progression Guide",
        description="*How many thank yous does it take to ascend?*",
        color=COLORS["purple"],
    )
    for threshold, title, subtitle in _RANKS:
        embed.add_field(
            name=title,
            value=f"*{subtitle}*\nRequires: **{threshold}+** thank yous" if threshold > 0
                  else f"*{subtitle}*\nFor the silent observers.",
            inline=False,
        )
    embed.set_footer(text="You're Welcome! Bot  •  Your journey starts with one 🙏")
    await ctx.send(embed=embed)


# ══════════════════════════════════════════════════════════
#   HELP  (!yw)
# ══════════════════════════════════════════════════════════
@bot.command(name="yw", aliases=["help", "ywhelp", "commands", "bothelp"])
async def help_cmd(ctx: commands.Context):
    embed = discord.Embed(
        title="🤖  You're Welcome!  —  Command Reference",
        description="*Your server's official gratitude surveillance unit.*",
        color=COLORS["pink"],
    )
    embed.add_field(
        name="📋  Commands",
        value=(
            "`!lb` or `/leaderboard` — Hall of Gratitude 🏆\n"
            "`!mythanks` or `/mythanks` — Your personal stats 📊\n"
            "`!mythanks @user` — Check someone else's stats\n"
            "`!serverstats` — Server-wide analytics 🌐\n"
            "`!ranks` — View all rank tiers 🎖️\n"
            "`!yw` — This help menu\n"
        ),
        inline=False,
    )
    embed.add_field(
        name="👀  What I detect",
        value=(
            "`thank you` · `thanks` · `ty` · `thx` · `thnks` · `thnx`\n"
            "`thank u` · `tanks` · `appreciate it` · `cheers` · `ta`\n"
            "`many thanks` · `thanks a lot` · `much appreciated`\n"
            "typos like `tankyu`, `thankyu`, stretched like `tyyy`\n"
            "…and a few non-English ones too 🌍\n"
            "*(case-insensitive — THANK YOU = thank you = ThAnK yOu)*"
        ),
        inline=False,
    )
    embed.add_field(
        name="🎉  Milestone Celebrations",
        value="Hit 5, 10, 25, 50, 75, 100, 150, 250, 500, or 1000 — and the whole server knows. 🎊",
        inline=False,
    )
    embed.set_footer(text="You're Welcome! Bot • Built with 🙏 and an unreasonable amount of regex")
    await ctx.send(embed=embed)


# ══════════════════════════════════════════════════════════
#   ENTRY POINT
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌  DISCORD_TOKEN is not set. Create a .env file with your token.")
        print("    See README.md for instructions.")
        raise SystemExit(1)

    init_db()
    print("🗄️   Database ready.")
    print("🚀  Starting You're Welcome! bot…\n")
    bot.run(BOT_TOKEN)
