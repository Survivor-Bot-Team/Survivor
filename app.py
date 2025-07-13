import discord
from discord import app_commands
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
from itertools import combinations
from typing import Optional
import re
import datetime
import asyncio

# Load environment variables
load_dotenv()

# Set Windows event loop policy for asyncio
import sys
if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Role IDs for permission checking
PERMISSION_ROLES = {
    "SKULL_CLUB": 1192766852317859871,
    "COMMANDER": 1172453428052631593,
    "SUPPORT": 1246056095768772658
}

# Role and channel IDs
ROLE_IDS = {
    "Joined-Main": 1194644728755519549,
    "Joined-Parallel": 1194644860939022366,
    "Round1-Main": 1195645662965010492,
    "Round1-Parllel": 1195646439573946439,
    "Warzone#1.1": 1051103004461379674,  
    "Warzone#1.2": 1051424554112798770,
    "Warzone#1.3": 1051424558365806622,
    "Warzone#1.4": 1051424560072884254,
    "Warzone#1.5": 1051424562342002701,
    "Warzone#1.6": 1061338706516131871,
    "Warzone#1.7": 1061338718948044943,
    "Warzone#1.8": 1061338724304175226,
    "Warzone#1.9": 1061338727407956009,
    "Warzone#1.10": 1061338733472907274,
    "Warzone#1.11": 1137659945769242645,
    "Warzone#1.12": 1137659985787093045,
    "Warzone#1.13": 1137659991457796207,
    "Warzone#1.14": 1137659995173945374,
    "Warzone#1.15": 1137659998911078431,
    "Warzone#1.16": 1137660006947360858,
    "Warzone#1.17": 1183715079007510558,
    "Warzone#1.18": 1183715140969975849,
    "Warzone#1.19": 1183715182149644289,
    "Warzone#1.20": 1183724483274612737,
    "Warzone#1.21": 1246445772367724644,
    "Warzone#1.22": 1246445773709770844,
    "Warzone#1.23": 1246445775899066398,
    "Warzone#1.24": 1246445776859566191,
    "Warzone#1.25": 1246445876793315358,
    "Warzone#1.1Extra": 1251814011629211659,
    "Warzone#1.2Extra": 1251814119187681290,
    "2.0": 1101476481651179581,     
    "Warzone#2.1": 1055482548836388994,
    "Warzone#2.2": 1055482753237393458,
    "Warzone#2.3": 1055482763337285663,
    "Warzone#2.4": 1055482928097927198,
    "Warzone#2.5": 1055482933567311952,
    "Warzone#2.6": 1137681647257518180,
    "Warzone#2.7": 1183339990739070986,
    "Warzone#2.8": 1183752529650135040,
    "Warzone#2.9": 1183752614098243654,
    # TODO: Add actual Discord role IDs for extended R2 warzones (2.10-2.14)
    "Warzone#2.10": 1389931690348253274,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "Warzone#2.11": 1389931717388795977,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "Warzone#2.12": 1389931756198690856,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "Warzone#2.13": 1389931835613773915,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "Warzone#2.14": 1389931859810717800,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "3.0": 1122461158771789895,
    "Warzone#3.1": 1058313518174179358,
    "Warzone#3.2": 1058313529041621012,
    "Warzone#3.3": 1058313540089413643,
    "Warzone#3.4": 1183753000574009415,
    "Warzone#3.5": 1183753078525153330,
    "Warzone#3.6": 1389931457916702790,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "Warzone#3.7": 1389931486857396224,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "Warzone#3.8": 1389931514787139604,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "Warzone#3.9": 1389931554100346932,  # PLACEHOLDER - UPDATE WITH ACTUAL ROLE ID
    "4.0": 1146687128324018226,
    "Warzone#4.1": 1061496973485682710,
    "Warzone#4.2": 1061497162812370994,
    "Warzone#4.3": 1183753888420073482,
    "FINALIST": 1055502005482823811,
    'Main-Judge': 1051425023962919013,
    'Commander': 1172453428052631593,
}
CHANNEL_IDS = {
    "warzone-lobby": 1051472774889222154,
    "warzone-r1-selfrole": 1062826235190849607,
    "War-zone-1": 1234063969602371656,
    "War-zone-2": 1234059291686862869,
    "War-zone-3": 1234060314559905805,
    "War-zone-4": 1226447193817354291,
    "War-zone-5": 1234066500743073824,
    "War-zone-6": 1061493333018550272,
    "War-zone-7": 1234067842312175705,
    "War-zone-8": 1061493819159363664,
    "War-zone-9": 1234069097864626196,
    "War-zone-10": 1061494274568486943,
    "War-zone-11": 1147489946853199892,
    "War-zone-12": 1147490073814761483,
    "War-zone-13": 1147490100851253249,
    "War-zone-14": 1147490127849996369,
    "War-zone-15": 1147490152541868142,
    "War-zone-16": 1147490186071121943,
    "War-zone-17": 1183714809829654548,
    "War-zone-18": 1183714913546412042,
    "War-zone-19": 1183714937747546132,
    "War-zone-20": 1183714965522239498,
    "War-zone-21": 1246445541915758612,
    "War-zone-22": 1246445577726726253,
    "War-zone-23": 1246445607665537116,
    "War-zone-24": 1246445633485672479,
    "War-zone-25": 1246445665811431465,
    "war-chat-2-0": 1152874713882837012,
    "warzone-r2-selfrole": 1101483727479128165,
    "War-zone-2-1": 1055482444528222279,
    "War-zone-2-2": 1055483638004854814,
    "War-zone-2-3": 1055484150829830164,
    "War-zone-2-4": 1055484370955284501,
    "War-zone-2-5": 1060850799917416519,
    "War-zone-2-6": 1137681372765499392,
    "War-zone-2-7": 1183751886537510963,
    "War-zone-2-8": 1183751930674167839,
    "War-zone-2-9": 1183751956511072256,
    "Warzone#2.10": 1389931690348253274,  
    "Warzone#2.11": 1389931717388795977,  
    "Warzone#2.12": 1389931756198690856,  
    "Warzone#2.13": 1389931835613773915,  
    "Warzone#2.14": 1389931859810717800,  
    "war-chat-3-0": 1135140460277538849,
    "warzone-r3-selfrole": 1124994401001820240,
    "War-zone-3-1": 1060891251672629268,
    "War-zone-3-2": 1066610535476498452,
    "War-zone-3-3": 1060891377153622056,
    "War-zone-3-4": 1183752054204792912,
    "War-zone-3-5": 1183752085779533924,
    "Warzone#3.6": 1389931457916702790,  
    "Warzone#3.7": 1389931486857396224, 
    "Warzone#3.8": 1389931514787139604,  
    "Warzone#3.9": 1389931554100346932,  
    "war-chat-4-0": 1180761129090306138,
    "warzone-r4-selfrole": 1180761027827212438,
    "War-zone-4-1": 1089462251263635476,
    "War-zone-4-2": 1173214822737916015,
    "War-zone-4-3": 1183754369292845107,
    "FINALIST": 1198241810062000298,
    "🏁┊main-results": 1080828920535982092,  
    "🏁┊parlell-results": 1190251379881693254, 
    "🔥┊registration": 1051428633106972762,
    "💖┊sat-registration": 1210456226505170964,
    "🔥┊main-registered": 1207686322765045842,
    "💖┊sat-registered": 1251221878086041690,
    "warzone-r1-checkedin": 1266731900655898694,
    "support-ʟᴏɢs": 1246124687021314140
}
# Map channel to allowed role
CHANNEL_ROLE_MAP = {
    "warzone-r1-selfrole": [ROLE_IDS["Joined-Main"], ROLE_IDS["Joined-Parallel"]],
    "War-zone-1": [ROLE_IDS["Warzone#1.1"]],
    "War-zone-2": [ROLE_IDS["Warzone#1.2"]],
    "War-zone-3": [ROLE_IDS["Warzone#1.3"]],
    "War-zone-4": [ROLE_IDS["Warzone#1.4"]],
    "War-zone-5": [ROLE_IDS["Warzone#1.5"]],
    "War-zone-6": [ROLE_IDS["Warzone#1.6"]],
    "War-zone-7": [ROLE_IDS["Warzone#1.7"]],
    "War-zone-8": [ROLE_IDS["Warzone#1.8"]],
    "War-zone-9": [ROLE_IDS["Warzone#1.9"]],
    "War-zone-10": [ROLE_IDS["Warzone#1.10"]],
    "War-zone-11": [ROLE_IDS["Warzone#1.11"]],
    "War-zone-12": [ROLE_IDS["Warzone#1.12"]],
    "War-zone-13": [ROLE_IDS["Warzone#1.13"]],
    "War-zone-14": [ROLE_IDS["Warzone#1.14"]],
    "War-zone-15": [ROLE_IDS["Warzone#1.15"]],
    "War-zone-16": [ROLE_IDS["Warzone#1.16"]],
    "War-zone-17": [ROLE_IDS["Warzone#1.17"]],
    "War-zone-18": [ROLE_IDS["Warzone#1.18"]],
    "War-zone-19": [ROLE_IDS["Warzone#1.19"]],
    "War-zone-20": [ROLE_IDS["Warzone#1.20"]],
    "War-zone-21": [ROLE_IDS["Warzone#1.21"]],
    "War-zone-22": [ROLE_IDS["Warzone#1.22"]],
    "War-zone-23": [ROLE_IDS["Warzone#1.23"]],
    "War-zone-24": [ROLE_IDS["Warzone#1.24"]],
    "War-zone-25": [ROLE_IDS["Warzone#1.25"]],
    "War-zone-1Extra": [ROLE_IDS["Warzone#1.1Extra"]],
    "War-zone-2Extra": [ROLE_IDS["Warzone#1.2Extra"]],
    "warzone-r2-selfrole": [ROLE_IDS["2.0"]],
    "War-zone-2-1": [ROLE_IDS["Warzone#2.1"]],
    "War-zone-2-2": [ROLE_IDS["Warzone#2.2"]],
    "War-zone-2-3": [ROLE_IDS["Warzone#2.3"]],
    "War-zone-2-4": [ROLE_IDS["Warzone#2.4"]],
    "War-zone-2-5": [ROLE_IDS["Warzone#2.5"]],
    "War-zone-2-6": [ROLE_IDS["Warzone#2.6"]],
    "War-zone-2-7": [ROLE_IDS["Warzone#2.7"]],
    "War-zone-2-8": [ROLE_IDS["Warzone#2.8"]],
    "War-zone-2-9": [ROLE_IDS["Warzone#2.9"]],
    # Extended R2 warzone mappings (2.10-2.14)
    "War-zone-2-10": [ROLE_IDS["Warzone#2.10"]],
    "War-zone-2-11": [ROLE_IDS["Warzone#2.11"]],
    "War-zone-2-12": [ROLE_IDS["Warzone#2.12"]],
    "War-zone-2-13": [ROLE_IDS["Warzone#2.13"]],
    "War-zone-2-14": [ROLE_IDS["Warzone#2.14"]],
    "warzone-r3-selfrole": [ROLE_IDS["3.0"]],
    "War-zone-3-1": [ROLE_IDS["Warzone#3.1"]],
    "War-zone-3-2": [ROLE_IDS["Warzone#3.2"]],
    "War-zone-3-3": [ROLE_IDS["Warzone#3.3"]],
    "War-zone-3-4": [ROLE_IDS["Warzone#3.4"]],
    "War-zone-3-5": [ROLE_IDS["Warzone#3.5"]],
    # Extended R3 warzone mappings (3.6-3.9)
    "War-zone-3-6": [ROLE_IDS["Warzone#3.6"]],
    "War-zone-3-7": [ROLE_IDS["Warzone#3.7"]],
    "War-zone-3-8": [ROLE_IDS["Warzone#3.8"]],
    "War-zone-3-9": [ROLE_IDS["Warzone#3.9"]],
    "warzone-r4-selfrole": [ROLE_IDS["4.0"]],
    "War-zone-4-1": [ROLE_IDS["Warzone#4.1"]],
    "War-zone-4-2": [ROLE_IDS["Warzone#4.2"]],
    "War-zone-4-3": [ROLE_IDS["Warzone#4.3"]],
    "FINALIST": [ROLE_IDS["FINALIST"]],
}

# Map round to list of 10-player Warzone voice channel IDs
WARZONE_VOICE_CHANNELS = {
    1: [CHANNEL_IDS["War-zone-1"], CHANNEL_IDS["War-zone-2"], CHANNEL_IDS["War-zone-3"]],
    2: [CHANNEL_IDS["War-zone-2-1"]],
    3: [CHANNEL_IDS["FINALIST"]],
}


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="warzone-", intents=intents)
tree = bot.tree

# At the top of your file, add a set to track logged registrations
if not hasattr(bot, "logged_registrations"):
    bot.logged_registrations = set()

def has_skull_club_role(interaction):
    """Check if user has Skull-Club role"""
    skull_club_role = discord.utils.get(interaction.user.roles, id=PERMISSION_ROLES["SKULL_CLUB"])
    return skull_club_role is not None

def has_commander_role(interaction):
    """Check if user has Commander role"""
    commander_role = discord.utils.get(interaction.user.roles, id=PERMISSION_ROLES["COMMANDER"])
    return commander_role is not None

def has_support_role(interaction):
    """Check if user has Support role"""
    support_role = discord.utils.get(interaction.user.roles, id=PERMISSION_ROLES["SUPPORT"])
    return support_role is not None

def is_staff(interaction):
    """Check if user has any staff role (Skull-Club, Commander, or Support)"""
    return has_skull_club_role(interaction) or has_commander_role(interaction) or has_support_role(interaction)

def is_commander_or_higher(interaction):
    """Check if user has Commander or Skull-Club role"""
    return has_skull_club_role(interaction) or has_commander_role(interaction)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"📊 Connected to {len(bot.guilds)} guild(s)")
    
    # Sync commands
    try:
        print("🔄 Syncing slash commands...")
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
    
    print("🎯 Bot is ready to receive commands!")

@tree.command(name="start", description="Start the Warzone system (Staff Only)")
async def start(interaction: discord.Interaction):
    if not is_staff(interaction):
        await interaction.response.send_message("🚫 You are not authorized to use this command.", ephemeral=True)
        return
    await interaction.response.send_message("✅ Warzone system has been activated.")

@tree.command(name="shutdown", description="Shutdown the bot (Staff Only)")
async def shutdown(interaction: discord.Interaction):
    if not is_staff(interaction):
        await interaction.response.send_message("🚫 You are not authorized to use this command.", ephemeral=True)
        return
    await interaction.response.send_message("🛑 Bot is shutting down...")
    await bot.close()


        
@tree.command(name="help", description="Show all available Warzone slash commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 Warzone Tournament Bot - Command Guide",
        description="Complete list of available slash commands for tournament management.",
        color=discord.Color.blue()
    )

    # System Commands
    embed.add_field(
        name="⚙️ **System Commands**",
        value=(
            "`/start` - Activate the Warzone bot system (Staff only)\n"
            "`/shutdown` - Safely shut down the bot (Staff only)\n"
            "`/help` - Display this command guide"
        ),
        inline=False
    )

    # Tournament Management
    embed.add_field(
        name="🏆 **Tournament Management**",
        value=(
            "`/winners` - Declare match winners and manage role transitions\n"
            "• Automatically logs winners to Give Sheet - H\n"
            "• Posts results to main/parallel results channels\n"
            "• Manages role removal/addition for winners"
        ),
        inline=False
    )

    # Queue & Distribution
    embed.add_field(
        name="📋 **Queue & Distribution System**",
        value=(
            "`/cc-all` - **Main distribution command** (Commanders only)\n"
            "• **R1:** 5v5 mode (7-10 players per warzone)\n"
            "• **R2:** 4v4 mode (7-8 players per warzone)\n"
            "• **R3:** 3v3 mode (5-6 players per warzone)\n"
            "• **R4:** 2v2 mode (3-4 players per warzone)\n"
            "• **Finalist:** 1v1 mode (2 players)\n\n"
            "**Features:**\n"
            "🔄 Auto-loads Discord IDs from Get R12345 Sheet\n"
            "🎯 Interactive warzone buttons (1-24 for R1, 1-14 for R2, etc.)\n"
            "🎤 Auto-moves players to voice channels\n"
            "🏷️ Auto-assigns warzone roles\n"
            "🔄 Removes previous round roles automatically"
        ),
        inline=False
    )

    # Check-in System
    embed.add_field(
        name="📝 **Check-in System**",
        value=(
            "`/check_in` - Start Round 1 check-in process (Commanders only)\n"
            "• **Saturday:** ⚔️ emoji → Round1-Parallel role\n"
            "• **Sunday:** 🗡️ emoji → Round1-Main role\n"
            "• Auto-logs to Give Sheet - H [1.0] tab\n"
            "• 20-minute timer with warnings\n"
            "• Auto-removes access roles after check-in"
        ),
        inline=False
    )

    # Team Tools
    embed.add_field(
        name="⚖️ **Team Management**",
        value=(
            "`/team_balance` - Balance two teams by player levels\n"
            "• Input: Comma-separated levels (e.g., 48,50,51,35,51,50,50,37,51,52)\n"
            "• Output: Optimized team splits with level differences"
        ),
        inline=False
    )

    # Support Tools
    embed.add_field(
        name="🛡️ **Support & Moderation**",
        value=(
            "`/support-give-role` - Assign roles to users (Staff only)\n"
            "`/support-remove-role` - Remove roles from users (Staff only)\n"
            "• All actions logged to support-logs channel"
        ),
        inline=False
    )

    # Google Sheets Integration
    embed.add_field(
        name="📊 **Google Sheets Integration**",
        value=(
            "**Two-Sheet System:**\n\n"
            "**📋 Get R12345 Sheet** - Queue Distribution\n"
            "• R1-5vs5 tab → R1 warzones (1.1-1.24)\n"
            "• R2-4vs4 tab → R2 warzones (2.1-2.14)\n"
            "• R3-3vs3 tab → R3 warzones (3.1-3.9)\n"
            "• R4-2vs2 tab → R4 warzones (4.1-4.4)\n"
            "• R5-1vs1 tab → Finalist warzone\n\n"
            "**📝 Give Sheet - H** - Results & Check-ins\n"
            "• [1.0] tab → Check-in logs (⚔️/🗡️)\n"
            "• [2.0] tab → R2 winners\n"
            "• [3.0] tab → R3 winners\n"
            "• [4.0] tab → R4 winners\n"
            "• [5.0] tab → Finalist winners"
        ),
        inline=False
    )

    # Workflow Summary
    embed.add_field(
        name="🔄 **Complete Tournament Workflow**",
        value=(
            "1️⃣ **Check-in:** `/check_in` → Give Sheet [1.0]\n"
            "2️⃣ **Distribution:** `/cc-all` → Get R12345 Sheet → Voice + Roles\n"
            "3️⃣ **Results:** `/winners` → Give Sheet [2.0-5.0] + Results Channels\n"
            "4️⃣ **Repeat:** For each round until Finalist"
        ),
        inline=False
    )

    embed.set_footer(text="🎯 Metal Wings Tournament System • Powered by Discord.py")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    
@tree.command(name="winners", description="Post winners and move roles by tournament type")
@app_commands.describe(
    tour_type="Select the tournament type",
    close_role="Role to remove from winners",
    new_role="Role to add to winners",
    user_1="First winner",
    user_2="Second winner",
    user_3="Third winner",
    user_4="Fourth winner",
    user_5="Fifth winner (optional)",
    judge="Skull Judge",
    screenshot="Match screenshot file (upload)"
)
@app_commands.choices(
    tour_type=[
        app_commands.Choice(name="Main-Tour", value="Main-Tour"),
        app_commands.Choice(name="Parllel-Tour", value="Parllel-Tour")
    ]
)
async def winners(
    interaction: discord.Interaction,
    tour_type: app_commands.Choice[str],
    close_role: discord.Role,
    new_role: discord.Role,
    user_1: discord.Member,
    user_2: Optional[discord.Member],
    user_3: Optional[discord.Member],
    user_4: Optional[discord.Member],
    user_5: Optional[discord.Member],
    judge: discord.Member,
    screenshot: discord.Attachment = None
):
    user_roles = [role.id for role in interaction.user.roles]
    # Allow staff in any channel
    if not is_staff(interaction):
        return await interaction.response.send_message("🚫 Only staff can use this command.", ephemeral=True)

    # 🆕 FIX: Defer immediately after permission check to prevent timeout
    await interaction.response.defer()

    winners = [u for u in [user_1, user_2, user_3, user_4, user_5] if u]
    error_msgs = []
    for winner in winners:
        try:
            bot_member = interaction.guild.me
            if not bot_member.guild_permissions.manage_roles:
                raise Exception("Bot lacks 'Manage Roles' permission.")
            if new_role >= bot_member.top_role:
                raise Exception("Bot's role is not high enough in the role hierarchy to manage the target role.")
            await winner.remove_roles(close_role)
            await winner.add_roles(new_role)
        except Exception as e:
            error_msgs.append(
                f"❌ Error updating roles for {winner.mention}: `{e}`\n"
                "Make sure the bot's role is above the target role and has Manage Roles permission."
            )
            print(f"Error updating roles for {winner.display_name}: {e}")

    embed = discord.Embed(
        title=f"Metal Wings - Survivor",
        description=f"Winner of the Current Round!! By\n**_{interaction.user.display_name}_**",
        color=discord.Color.purple(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    # List all winners in a single field
    winner_mentions = "\n".join(f"{winner.mention}" for winner in winners)
    embed.add_field(name="Winners", value=winner_mentions or "No winners", inline=False)

    embed.add_field(name="Closed Role", value=close_role.mention, inline=True)
    embed.add_field(name="New Role", value=new_role.mention, inline=True)
    embed.add_field(name="Skull Judge", value=judge.mention, inline=False)
    embed.add_field(name="Posted By", value=interaction.user.mention, inline=False)

    if screenshot:
        embed.set_image(url=screenshot.url)
    embed.set_footer(text="Powered By Metal Wings")

    # Always post in current channel (already deferred at start of command)
    await interaction.followup.send(embed=embed, ephemeral=False)

    # Post a copy in the appropriate results channel
    backup_channel_key = "🏁┊main-results" if tour_type.value == "Main-Tour" else "🏁┊parlell-results"
    backup_channel_id = CHANNEL_IDS.get(backup_channel_key)
    backup_channel = interaction.guild.get_channel(backup_channel_id) if backup_channel_id else None

    if backup_channel:
        try:
            await backup_channel.send(embed=embed)
        except Exception as e:
            print(f"Error posting to {backup_channel_key}: {e}")

    # 🆕 NEW: Log winners to Give Sheet - H (all rounds)
    try:
        # Determine round selection based on new role
        round_selection = None
        if "2.0" in new_role.name or new_role.id == ROLE_IDS.get("2.0"):
            round_selection = "2.0"
        elif "3.0" in new_role.name or new_role.id == ROLE_IDS.get("3.0"):
            round_selection = "3.0"  
        elif "4.0" in new_role.name or new_role.id == ROLE_IDS.get("4.0"):
            round_selection = "4.0"
        elif "FINALIST" in new_role.name or new_role.id == ROLE_IDS.get("FINALIST"):
            round_selection = "5.0"
        
        if round_selection:
            # Prepare winners data with Discord ID and username (NO display names, NO timestamps)
            winners_data = []
            for winner in winners:
                winners_data.append([winner.id, winner.name])  # Discord ID and username only
            
            # Log winners to Give Sheet - H with appropriate tabs (2.0, 3.0, 4.0, 5.0)
            success = log_winners(winners_data, round_selection)
            if success:
                print(f"✅ Winners logged to Give Sheet - H tab {round_selection}")
            else:
                print(f"❌ Failed to log winners for round {round_selection}")
        else:
            print(f"⚠️ Could not determine round selection for role: {new_role.name}")
            
    except Exception as e:
        print(f"❌ Error logging winners: {e}")

    # Enhancement: Ping commanders and announce warzone closure
    try:
        # Get the Commander role
        commander_role = interaction.guild.get_role(ROLE_IDS.get('Commander'))
        commander_ping = commander_role.mention if commander_role else "@Commanders"
        
        # Create warzone closure announcement
        closure_embed = discord.Embed(
            title="🔒 Warzone Closed",
            description=(
                f"**Warzone is now closed!**\n\n"
                f"📊 **Please check the results with the screenshot above**\n\n"
                f"🚫 **This channel will be closed soon so players cannot chat after the match**\n\n"
                f"✅ Results have been posted in {backup_channel.mention if backup_channel else 'results channel'}"
            ),
            color=discord.Color.red()
        )
        closure_embed.set_footer(text="Tournament Management • Metal Wings")
        
        # Send the closure message with commander ping
        await interaction.followup.send(
            content=f"{commander_ping}",
            embed=closure_embed,
            ephemeral=False
        )
        
    except Exception as e:
        print(f"Error sending warzone closure message: {e}")

    # Send error messages if any
    if error_msgs:
        await interaction.followup.send("\n".join(error_msgs), ephemeral=True)

# Import three-sheet system functions
from sheet import (
    # Check-in functions (Give Sheet only)
    log_check_in,
    
    # Winners functions (Give Sheet / Get R2345 Sheet)
    log_winners,
    log_winners_to_get_sheet,
    
    # Queue data functions (Get Sheet / Get R2345 Sheet)
    get_queue_data_for_round,
    get_queue_data_with_usernames,
    log_queue_distribution,
    
    # Legacy compatibility
    get_all_players,
    log_player_check_in,
    log_round_winners
)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    reg_messages = getattr(bot, "registration_messages", {})
    if reaction.message.id in reg_messages:
        emoji, role_id = reg_messages[reaction.message.id]
        if str(reaction.emoji) == emoji:
            guild = reaction.message.guild
            member = guild.get_member(user.id)
            role = guild.get_role(role_id)
            # Prevent duplicate role assignment
            if member and role and role not in member.roles:
                try:
                    await member.add_roles(role)
                    await user.send(f"✅ You have been registered and given the role: {role.name}")
                    # Fetch updated member for accurate logging
                    member = await guild.fetch_member(user.id)
                except Exception as e:
                    print(f"Error assigning registration role: {e}")
            # Prevent duplicate logging for the same user/message
            log_key = (user.id, reaction.message.id)
            if log_key not in bot.logged_registrations:
                bot.logged_registrations.add(log_key)
                log_channel_id = None
                if emoji == "🔥":
                    log_channel_id = CHANNEL_IDS.get("🔥┊main-registered")
                elif emoji == "💖":
                    log_channel_id = CHANNEL_IDS.get("💖┊sat-registered")
                if log_channel_id:
                    log_channel = guild.get_channel(log_channel_id)
                    if log_channel:
                        reg_roles = []
                        join_main = guild.get_role(ROLE_IDS["Joined-Main"])
                        join_parallel = guild.get_role(ROLE_IDS["Joined-Parallel"])
                        if join_main and join_main in member.roles:
                            reg_roles.append("Joined-Main")
                        if join_parallel and join_parallel in member.roles:
                            reg_roles.append("Joined-Parallel")
                        roles_str = ", ".join(reg_roles) if reg_roles else "None"
                        await log_channel.send(f"Registered : {member.mention} | Roles: {roles_str}")
        return
    # Check-in logic for Saturday (⚔️) and Sunday (🗡️)
    if hasattr(bot, "checkin_messages") and reaction.message.id in bot.checkin_messages:
        checkin_info = bot.checkin_messages[reaction.message.id]
        expected_emoji = checkin_info.get("emoji")
        
        if str(reaction.emoji) == expected_emoji:
            channel = reaction.message.channel
            if channel.name != "warzone-r1-selfrole":
                return
            guild = reaction.message.guild
            member = guild.get_member(user.id)
            
            # Determine roles based on day
            if checkin_info["day"] == "saturday":
                round_role = guild.get_role(ROLE_IDS["Round1-Parllel"])
                access_role_to_remove = guild.get_role(ROLE_IDS["Joined-Parallel"])
            else:  # sunday
                round_role = guild.get_role(ROLE_IDS["Round1-Main"])
                access_role_to_remove = guild.get_role(ROLE_IDS["Joined-Main"])
            
            if member and round_role and round_role not in member.roles:
                try:
                    # Add the round role
                    await member.add_roles(round_role)
                    
                    # Remove the access role if user has it
                    if access_role_to_remove and access_role_to_remove in member.roles:
                        await member.remove_roles(access_role_to_remove)
                        await user.send(f"✅ You have been checked-in for the tournament! Given role: {round_role.name} | Removed access role: {access_role_to_remove.name}")
                    else:
                        await user.send(f"✅ You have been checked-in and given the role: {round_role.name}")
                    
                    # Fetch updated member for accurate logging
                    member = await guild.fetch_member(user.id)
                except Exception as e:
                    print(f"Error assigning round role: {e}")
            
            # 🆕 NEW: Sheet logging - Log to Give Sheet only
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success = log_check_in(user.display_name, timestamp)
            
            if success:
                await channel.send(f"{expected_emoji} {user.mention} checked-in for {checkin_info['day_name']}! ✅ Logged to Give Sheet", delete_after=5)
                print(f"✅ {user.name} check-in logged to Give Sheet - H")
            else:
                await channel.send(f"{expected_emoji} {user.mention} checked-in for {checkin_info['day_name']}! ⚠️ Sheet log failed", delete_after=5)
                print(f"❌ Failed to log {user.name} check-in to Give Sheet")
        return

    # WZ signup logic
    if hasattr(bot, "wz_signup_messages") and reaction.message.id in bot.wz_signup_messages:
        entry = bot.wz_signup_messages[reaction.message.id]
        expected_emoji = entry.get("round_emoji", "🛡️")
        
        if str(reaction.emoji) == expected_emoji:
            # Check if user is already in this warzone
            if user.id in entry["users"]:
                return
            
            entry["users"].add(user.id)
            max_players = entry.get("max_players", 10)
            voice_channel = entry.get("voice_channel")
            role = entry.get("role")
            mode = entry.get("mode", "5v5")
            
            # Get the member object
            member = reaction.message.guild.get_member(user.id)
            if not member:
                return
            
            # Move player to voice channel if they're in voice
            if member.voice and voice_channel:
                try:
                    await member.move_to(voice_channel)
                except Exception as e:
                    print(f"Error moving {member.display_name} to voice channel: {e}")
            
            # Assign warzone role
            if role and role not in member.roles:
                try:
                    await member.add_roles(role)
                except Exception as e:
                    print(f"Error assigning role to {member.display_name}: {e}")
            
            await reaction.message.channel.send(
                f"{expected_emoji} {user.mention} joined **{entry['room_code']}** ({mode})! "
                f"({len(entry['users'])}/{max_players}) "
                f"{'🔊 ' + voice_channel.mention if voice_channel else ''}", 
                delete_after=3
            )
            
            # Check if warzone is full
            if len(entry["users"]) >= max_players:
                # Warzone is full - send completion message
                completion_embed = discord.Embed(
                    title="✅ Warzone Full!",
                    description=f"**Room {entry['room_code']}** is now full! ({max_players}/{max_players} players)\n\n"
                               f"**Mode:** {mode}\n"
                               f"**Voice Channel:** {voice_channel.mention if voice_channel else 'N/A'}\n"
                               f"**Role:** {role.mention if role else 'N/A'}",
                    color=discord.Color.gold()
                )
                completion_embed.set_footer(text="Good luck in your match! • Metal Wings Tournament")
                
                await reaction.message.channel.send(embed=completion_embed, delete_after=15)
                
                # Delete the signup message and remove from tracking
                try:
                    await entry["message"].delete()
                except:
                    pass
                del bot.wz_signup_messages[reaction.message.id]
        return

    # Queue system for cc-all command has been removed (no longer uses emoji reactions)
    # Players are now manually added to queue by commanders

@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    
    # Queue removal for cc-all command has been removed (no longer uses emoji reactions)
    # Players are now manually managed by commanders

# Warzone distribution view with buttons
class WarzoneDistributionView(discord.ui.View):
    def __init__(self, match_mode: str, round_type: str, sheet_usernames: dict = None):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.match_mode = match_mode
        self.round_type = round_type
        self.queue = []  # Store user IDs in queue
        self.sheet_usernames = sheet_usernames or {}  # Store sheet usernames
        
        # Determine players per warzone based on match mode
        self.players_per_warzone = {
            "2v2": 4,
            "3v3": 6,
            "4v4": 8,
            "5v5": 10
        }.get(match_mode, 10)
        
        # Add buttons based on round type (all start with green color - success)
        if round_type == "R1":
            # Add buttons for warzones 1.1 to 1.24 (24 buttons + 1 close = 25 total - Discord limit)
            for i in range(1, 25):  # 1 to 24
                warzone_id = f"1.{i}"
                button = discord.ui.Button(
                    label=warzone_id,
                    style=discord.ButtonStyle.success,  # Green color
                    custom_id=f"wz_{warzone_id}"
                )
                button.callback = self.create_warzone_callback(warzone_id, "1", button)
                self.add_item(button)
        elif round_type == "R2":
            # Add buttons for warzones 2.1 to 2.14
            for i in range(1, 15):  # 1 to 14
                warzone_id = f"2.{i}"
                button = discord.ui.Button(
                    label=warzone_id,
                    style=discord.ButtonStyle.success,  # Green color
                    custom_id=f"wz_{warzone_id}"
                )
                button.callback = self.create_warzone_callback(warzone_id, "2", button)
                self.add_item(button)
        elif round_type == "R3":
            # Add buttons for warzones 3.1 to 3.9
            for i in range(1, 10):  # 1 to 9
                warzone_id = f"3.{i}"
                button = discord.ui.Button(
                    label=warzone_id,
                    style=discord.ButtonStyle.success,  # Green color
                    custom_id=f"wz_{warzone_id}"
                )
                button.callback = self.create_warzone_callback(warzone_id, "3", button)
                self.add_item(button)
        elif round_type == "R4":
            # Add buttons for warzones 4.1 to 4.4
            for i in range(1, 5):  # 1 to 4
                warzone_id = f"4.{i}"
                button = discord.ui.Button(
                    label=warzone_id,
                    style=discord.ButtonStyle.success,  # Green color
                    custom_id=f"wz_{warzone_id}"
                )
                button.callback = self.create_warzone_callback(warzone_id, "4", button)
                self.add_item(button)
        elif round_type == "Finalist":
            # Add single Finalist button
            warzone_id = "Finalist"
            button = discord.ui.Button(
                label="🏆 Finalist",
                style=discord.ButtonStyle.success,  # Green color
                custom_id="wz_finalist"
            )
            button.callback = self.create_warzone_callback(warzone_id, "F", button)
            self.add_item(button)
        
        # Add close button (available for all round types)
        close_button = discord.ui.Button(
            label="❌ Close Queue",
            style=discord.ButtonStyle.danger,
            custom_id="close_queue",
            row=4  # Put close button on bottom row
        )
        close_button.callback = self.close_queue_callback()
        self.add_item(close_button)
    
    def close_queue_callback(self):
        async def callback(interaction):
            # Check if user is commander or higher
            if not is_commander_or_higher(interaction):
                await interaction.response.send_message("🚫 Only Commanders can close the queue.", ephemeral=True)
                return
            
            # Find and remove this queue from tracking
            msg_to_delete = None
            for msg_id, entry in bot.queue_messages.items():
                if entry["view"] is self:
                    msg_to_delete = msg_id
                    break
            
            if msg_to_delete:
                del bot.queue_messages[msg_to_delete]
            
            # Send confirmation and delete the queue message
            embed = discord.Embed(
                title="🔒 Queue Closed",
                description=f"**{self.round_type} Queue System** has been closed by {interaction.user.mention}.",
                color=discord.Color.red()
            )
            
            await interaction.response.send_message(embed=embed)
            
            # Delete the original queue message after a short delay
            try:
                await asyncio.sleep(3)  # Wait 3 seconds
                await interaction.message.delete()
            except Exception as e:
                print(f"Error deleting queue message: {e}")
        
        return callback

    def create_warzone_callback(self, warzone_id, round_prefix, button):
        async def warzone_callback(interaction):
            # Defer the interaction immediately to prevent timeout
            await interaction.response.defer()
            
            # Check if user is commander or higher
            if not is_commander_or_higher(interaction):
                await interaction.followup.send("🚫 Only Commanders can distribute players.", ephemeral=True)
                return
            
            # Flexible player count logic based on round
            if self.round_type == "R1":
                # R1 is very flexible - allow 7-10 players
                min_players = 7
                max_players = 10
            else:
                # Other rounds allow 1 less than standard
                min_players = self.players_per_warzone - 1
                max_players = self.players_per_warzone
            
            if len(self.queue) < min_players:
                await interaction.followup.send(f"❌ Not enough players in queue. Need {min_players}-{max_players}, have {len(self.queue)}", ephemeral=True)
                return
            
            # Get the appropriate number of players (between min and max)
            players_to_distribute = min(len(self.queue), max_players)
            players_to_assign = self.queue[:players_to_distribute]
            self.queue = self.queue[players_to_distribute:]  # Remove assigned players from queue
            
            # Get voice channel and role for this warzone based on round
            voice_channel_key = None
            role_key = None
            
            if round_prefix == "1":
                # Round 1 mapping
                warzone_to_channel = {
                    "1.1": "War-zone-1", "1.2": "War-zone-2", "1.3": "War-zone-3",
                    "1.4": "War-zone-4", "1.5": "War-zone-5", "1.6": "War-zone-6",
                    "1.7": "War-zone-7", "1.8": "War-zone-8", "1.9": "War-zone-9",
                    "1.10": "War-zone-10", "1.11": "War-zone-11", "1.12": "War-zone-12",
                    "1.13": "War-zone-13", "1.14": "War-zone-14", "1.15": "War-zone-15",
                    "1.16": "War-zone-16", "1.17": "War-zone-17", "1.18": "War-zone-18",
                    "1.19": "War-zone-19", "1.20": "War-zone-20"
                }
                voice_channel_key = warzone_to_channel.get(warzone_id)
                role_key = f"Warzone#{warzone_id}"
            elif round_prefix == "2":
                # Round 2 mapping (extended to 2.14)
                warzone_to_channel = {
                    "2.1": "War-zone-2-1", "2.2": "War-zone-2-2", "2.3": "War-zone-2-3",
                    "2.4": "War-zone-2-4", "2.5": "War-zone-2-5", "2.6": "War-zone-2-6",
                    "2.7": "War-zone-2-7", "2.8": "War-zone-2-8", "2.9": "War-zone-2-9",
                    "2.10": "War-zone-2-10", "2.11": "War-zone-2-11", "2.12": "War-zone-2-12",
                    "2.13": "War-zone-2-13", "2.14": "War-zone-2-14"
                }
                voice_channel_key = warzone_to_channel.get(warzone_id)
                role_key = f"Warzone#{warzone_id}"
            elif round_prefix == "3":
                # Round 3 mapping (reduced to 3.9, removed 3.10)
                warzone_to_channel = {
                    "3.1": "War-zone-3-1", "3.2": "War-zone-3-2", "3.3": "War-zone-3-3",
                    "3.4": "War-zone-3-4", "3.5": "War-zone-3-5", "3.6": "War-zone-3-6",
                    "3.7": "War-zone-3-7", "3.8": "War-zone-3-8", "3.9": "War-zone-3-9"
                }
                voice_channel_key = warzone_to_channel.get(warzone_id)
                role_key = f"Warzone#{warzone_id}"
            elif round_prefix == "4":
                # Round 4 mapping
                warzone_to_channel = {
                    "4.1": "War-zone-4-1", "4.2": "War-zone-4-2", "4.3": "War-zone-4-3",
                    "4.4": "War-zone-4-4"
                }
                voice_channel_key = warzone_to_channel.get(warzone_id)
                role_key = f"Warzone#{warzone_id}"
            elif round_prefix == "F":
                # Finalist mapping
                voice_channel_key = "FINALIST"
                role_key = "FINALIST"
            
            voice_channel_id = CHANNEL_IDS.get(voice_channel_key) if voice_channel_key else None
            role_id = ROLE_IDS.get(role_key) if role_key else None
            
            if not voice_channel_key:
                await interaction.followup.send(f"❌ Warzone {warzone_id} not configured.", ephemeral=True)
                return
                
            if not voice_channel_id or not role_id:
                await interaction.followup.send(f"❌ Voice channel ({voice_channel_key}) or role ({role_key}) for {warzone_id} not found.", ephemeral=True)
                return
            
            voice_channel = interaction.guild.get_channel(voice_channel_id)
            role = interaction.guild.get_role(role_id)
            
            assigned_msgs = []
            
            for user_id in players_to_assign:
                member = interaction.guild.get_member(user_id)
                if not member:
                    continue
                
                # Move to voice channel if they're in voice
                if member.voice and voice_channel:
                    try:
                        await member.move_to(voice_channel)
                    except Exception as e:
                        pass
                
                # 🆕 Remove old roles before assigning new warzone role
                roles_to_remove = []
                round1_main = interaction.guild.get_role(ROLE_IDS.get("Round1-Main"))
                round1_parallel = interaction.guild.get_role(ROLE_IDS.get("Round1-Parllel"))
                role_2_0 = interaction.guild.get_role(ROLE_IDS.get("2.0"))
                role_3_0 = interaction.guild.get_role(ROLE_IDS.get("3.0"))
                role_4_0 = interaction.guild.get_role(ROLE_IDS.get("4.0"))
                
                # Check which old roles to remove based on current roles
                if round1_main and round1_main in member.roles:
                    roles_to_remove.append(round1_main)
                if round1_parallel and round1_parallel in member.roles:
                    roles_to_remove.append(round1_parallel)
                if role_2_0 and role_2_0 in member.roles:
                    roles_to_remove.append(role_2_0)
                if role_3_0 and role_3_0 in member.roles:
                    roles_to_remove.append(role_3_0)
                if role_4_0 and role_4_0 in member.roles:
                    roles_to_remove.append(role_4_0)
                
                # Remove old roles
                if roles_to_remove:
                    try:
                        await member.remove_roles(*roles_to_remove)
                    except Exception as e:
                        print(f"Error removing old roles from {member.display_name}: {e}")
                
                # Assign warzone role
                if role and role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except Exception as e:
                        print(f"Error assigning warzone role to {member.display_name}: {e}")
                
                assigned_msgs.append(f"{member.mention}")
            
            if assigned_msgs:
                # Change button style to gray (secondary) to show it's been used
                button.style = discord.ButtonStyle.secondary
                button.disabled = True  # Optional: disable the button after use
                
                # Check if we're in a selfrole channel (don't show Distribution Complete there)
                selfrole_channels = [
                    CHANNEL_IDS.get("warzone-r1-selfrole"),
                    CHANNEL_IDS.get("warzone-r2-selfrole"),
                    CHANNEL_IDS.get("warzone-r3-selfrole"),
                    CHANNEL_IDS.get("warzone-r4-selfrole")
                ]
                
                # Only send Distribution Complete message if NOT in selfrole channels
                if interaction.channel.id not in selfrole_channels:
                    embed = discord.Embed(
                        title=f"✅ {warzone_id} Distribution Complete",
                        description=f"**Mode:** {self.match_mode}\n**Players:** {len(assigned_msgs)} distributed\n**Voice:** {voice_channel.mention if voice_channel else 'N/A'}\n**Queue Remaining:** {len(self.queue)} players\n\n**Assigned Players:**\n" + "\n".join(assigned_msgs),
                        color=discord.Color.green()
                    )
                    await interaction.followup.send(embed=embed)
                
                # Log the distribution to the warzone channel
                try:
                    import datetime
                    
                    # Create distribution log embed
                    log_embed = discord.Embed(
                        title=f"📋 {warzone_id} Distribution Log",
                        description=f"**Commander:** {interaction.user.mention}\n**Mode:** {self.match_mode}\n**Players Assigned:** {len(assigned_msgs)}",
                        color=discord.Color.blue(),
                        timestamp=discord.utils.utcnow()
                    )
                    
                    # Add player list with actual Discord usernames (not sheet usernames)
                    player_list = []
                    for discord_id in players_to_assign:
                        member = interaction.guild.get_member(discord_id)
                        if member:
                            # Use actual Discord username and mention
                            player_list.append(f"{member.mention}")
                        else:
                            # Fallback to sheet username if member not found
                            username = self.sheet_usernames.get(discord_id, f"Unknown User")
                            player_list.append(f"**{username}** (`{discord_id}`)")
                    
                    log_embed.add_field(
                        name="👥 Assigned Players",
                        value="\n".join(player_list) if player_list else "No players",
                        inline=False
                    )
                    
                    log_embed.set_footer(text=f"Warzone: {warzone_id} | Voice: {voice_channel.name if voice_channel else 'N/A'}")
                    
                    # Send log to the warzone channel
                    if voice_channel:
                        await voice_channel.send(embed=log_embed)
                    
                except Exception as e:
                    print(f"Error sending distribution log: {e}")
                
                # Update the main queue message to show remaining queue count and button state
                try:
                    queue_msg = None
                    for msg_id, entry in bot.queue_messages.items():
                        if entry["view"] is self:
                            queue_msg = entry["message"]
                            break
                    
                    if queue_msg:
                        # Show updated player count with sheet usernames
                        queue_display = f"{len(self.queue)} players"
                        if len(self.queue) > 0:
                            usernames = []
                            for discord_id in self.queue[:5]:  # Show first 5 players
                                username = self.sheet_usernames.get(discord_id, f"ID:{discord_id}")
                                usernames.append(username)
                            if usernames:
                                preview = ", ".join(usernames)
                                if len(self.queue) > 5:
                                    preview += f", +{len(self.queue) - 5} more"
                                queue_display = f"{len(self.queue)} players ({preview})"
                        
                        updated_embed = discord.Embed(
                            title=f"🎯 {self.round_type} Queue System",
                            description=f"**Match Mode:** {self.match_mode}\n**Players per Warzone:** {self.players_per_warzone}\n\n**Queue:** {queue_display}",
                            color=discord.Color.blue()
                        )
                        updated_embed.add_field(
                            name="📋 Instructions", 
                            value="1️⃣ Discord IDs loaded from **Get R12345 Sheet** automatically\n2️⃣ Click warzone buttons to distribute players to rooms\n3️⃣ Players get voice channel + warzone roles assigned\n🟢 Green = Available | 🔘 Gray = Used",
                            inline=False
                        )
                        updated_embed.set_footer(text="Commanders: Use the buttons below to distribute players to warzones")
                        await queue_msg.edit(embed=updated_embed, view=self)
                except Exception as e:
                    print(f"Error updating main queue message: {e}")
            else:
                await interaction.followup.send(f"❌ No players could be assigned to {warzone_id}.", ephemeral=True)
        
        return warzone_callback

@tree.command(name="cc-all", description="Start queue system with warzone distribution buttons")
@app_commands.describe(
    round_type="Select round type"
)
@app_commands.choices(
    round_type=[
        app_commands.Choice(name="R1 (1-24 buttons) - 5v5", value="R1"),
        app_commands.Choice(name="R2 (1-14 buttons) - 4v4", value="R2"),
        app_commands.Choice(name="R3 (1-9 buttons) - 3v3", value="R3"),
        app_commands.Choice(name="R4 (1-4 buttons) - 2v2", value="R4"),
        app_commands.Choice(name="Finalist (1 button) - 1v1", value="Finalist")
    ]
)
async def cc_all(interaction: discord.Interaction, round_type: app_commands.Choice[str]):
    if not is_commander_or_higher(interaction):
        return await interaction.response.send_message("🚫 Only Commanders can use this command.", ephemeral=True)
    
    # Determine allowed channels based on round type
    allowed_channels = []
    if round_type.value == "R1":
        allowed_channels = [CHANNEL_IDS["warzone-r1-selfrole"]]
    elif round_type.value == "R2":
        allowed_channels = [CHANNEL_IDS["warzone-r2-selfrole"]]
    elif round_type.value == "R3":
        allowed_channels = [CHANNEL_IDS["warzone-r3-selfrole"]]
    elif round_type.value == "R4":
        allowed_channels = [CHANNEL_IDS["warzone-r4-selfrole"]]
    elif round_type.value == "Finalist":
        allowed_channels = [CHANNEL_IDS.get("FINALIST", 0)]
    
    if interaction.channel.id not in allowed_channels:
        return await interaction.response.send_message(f"❌ Use this command in the appropriate channel for {round_type.value}.", ephemeral=True)
    
    # Automatically determine match mode based on round type
    def get_match_mode_for_round(round_type):
        """Return match modes for each round"""
        round_modes = {
            "R1": "5v5",        # R1 uses 5v5
            "R2": "4v4",        # R2 uses 4v4
            "R3": "3v3",        # R3 uses 3v3
            "R4": "2v2",        # R4 uses 2v2
            "Finalist": "1v1"   # Finalist uses 1v1
        }
        return round_modes.get(round_type, "5v5")
    
    def get_players_per_warzone_for_round(match_mode):
        """Get the number of players per warzone for each round"""
        players_map = {
            "1v1": 2,
            "2v2": 4,
            "3v3": 6,
            "4v4": 8,
            "5v5": 10
        }
        return players_map.get(match_mode, 10)
    
    # Automatically determine match mode based on round type
    actual_mode = get_match_mode_for_round(round_type.value)
    mode_name = actual_mode.upper()
    
    # Determine players per warzone using the actual mode
    players_per_warzone = get_players_per_warzone_for_round(actual_mode)
    
    # Initialize sheet_usernames before creating the view
    sheet_usernames = {}  # Store sheet usernames for display
    
    # Create the view with warzone buttons first (before loading sheet data)
    view = WarzoneDistributionView(actual_mode, round_type.value, sheet_usernames)
    
    # 🆕 CORRECTED: Get queue data from Get R12345 Sheet for ALL rounds
    initial_queue_count = 0
    if round_type.value in ["R1", "R2", "R3", "R4", "Finalist"]:
        # Map round_type to sheet round identifier  
        sheet_round = round_type.value
        if round_type.value == "Finalist":
            sheet_round = "R5"  # Finalist maps to R5 in sheets
        
        # Get Discord IDs and usernames from Get R12345 Sheet (ALL rounds)
        player_data = get_queue_data_with_usernames(sheet_round)
        
        if player_data:
            # Extract Discord IDs for the queue and store usernames for display
            discord_ids = []
            for discord_id, username in player_data:
                discord_ids.append(discord_id)
                sheet_usernames[discord_id] = username
            
            view.queue = discord_ids
            initial_queue_count = len(view.queue)
            
            # Simple logging - no need for complex queue distribution data
            # Just log that queue was loaded
            print(f"📋 Queue loaded: {initial_queue_count} Discord IDs for {sheet_round}")
            
            print(f"✅ Loaded {initial_queue_count} players from Get R12345 Sheet for {sheet_round}")
        else:
            print(f"⚠️ No queue data found in Get R12345 Sheet for {sheet_round}")
    
    # Create embed for queue management with sheet usernames
    queue_display = f"{initial_queue_count} players"
    if initial_queue_count > 0:
        # Show first few usernames from the sheet (not Discord usernames)
        usernames = []
        for discord_id in view.queue[:5]:  # Show first 5 players
            username = sheet_usernames.get(discord_id, f"ID:{discord_id}")
            usernames.append(username)
        if usernames:
            preview = ", ".join(usernames)
            if initial_queue_count > 5:
                preview += f", +{initial_queue_count - 5} more"
            queue_display = f"{initial_queue_count} players ({preview})"
    
    embed = discord.Embed(
        title=f"🎯 {round_type.value} Queue System",
        description=f"**Match Mode:** {mode_name}\n**Players per Warzone:** {players_per_warzone}\n\n**Queue:** {queue_display}",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📋 Instructions",
        value="1️⃣ Players Please Wait in the Queue\n2️⃣ commanders will use warzone buttons to distribute players to rooms\n3️⃣ Players get Warzone room + warzone roles assigned\n🟢 Green = Available | 🔘 Gray = Used",
        inline=False
    )
    
    embed.set_footer(text="Commanders: Use the buttons below to distribute players to warzones")
    
    # Send response
    await interaction.response.send_message(embed=embed, view=view)
    msg = await interaction.original_response()
    
    # Track this message for queue management
    if not hasattr(bot, "queue_messages"):
        bot.queue_messages = {}
    bot.queue_messages[msg.id] = {
        "view": view,
        "message": msg,
        "match_mode": actual_mode,
        "players_per_warzone": players_per_warzone,
        "round_type": round_type.value
    }




@tree.command(name="wz-all", description="Distribute queue for a specific round and warzone with match mode")
@app_commands.describe(
    mode="Select match mode (2v2, 3v3, 4v4, or 5v5)",
    round_no="Round number (e.g., 2, 3, 4, ...)",
    warzone_no="Warzone number (e.g., 1, 2, 3, ...)"
)
@app_commands.choices(
    mode=[
        app_commands.Choice(name="2 vs 2", value="2v2"),
        app_commands.Choice(name="3 vs 3", value="3v3"),
        app_commands.Choice(name="4 vs 4", value="4v4"),
        app_commands.Choice(name="5 vs 5", value="5v5")
    ]
)
async def wz_all(interaction: discord.Interaction, mode: app_commands.Choice[str], round_no: int, warzone_no: int):
    if not is_commander_or_higher(interaction):
        await interaction.response.send_message("🚫 Only Commanders can use this command.", ephemeral=True)
        return
    allowed_channels = [
        CHANNEL_IDS.get("warzone-r2-selfrole"),
        CHANNEL_IDS.get("warzone-r3-selfrole"),
        CHANNEL_IDS.get("warzone-r4-selfrole")
    ]
    if interaction.channel.id not in allowed_channels:
        await interaction.response.send_message("❌ Use this command in warzone-r2-selfrole, warzone-r3-selfrole, or warzone-r4-selfrole only.", ephemeral=True)
        return
    
    room_code = f"{round_no}.{warzone_no}"
    
    # Determine max players based on mode
    max_players = {
        "2v2": 4,
        "3v3": 6,
        "4v4": 8,
        "5v5": 10
    }.get(mode.value, 10)
    
    # Map round numbers to emojis
    round_emojis = {
        2: "2️⃣",
        3: "3️⃣", 
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣"
    }
    
    # Get the appropriate emoji for the round
    round_emoji = round_emojis.get(round_no, "🛡️")
    
    # Get the voice channel and role for this warzone
    voice_channel_key = f"War-zone-{round_no}-{warzone_no}"
    role_key = f"Warzone#{room_code}"
    
    voice_channel_id = CHANNEL_IDS.get(voice_channel_key)
    role_id = ROLE_IDS.get(role_key)
    
    if not voice_channel_id:
        await interaction.response.send_message(f"❌ Voice channel for {voice_channel_key} not found.", ephemeral=True)
        return
    
    if not role_id:
        await interaction.response.send_message(f"❌ Role for {role_key} not found.", ephemeral=True)
        return
    
    voice_channel = interaction.guild.get_channel(voice_channel_id)
    role = interaction.guild.get_role(role_id)
    
    if not voice_channel or not role:
        await interaction.response.send_message(f"❌ Could not find voice channel or role for warzone {room_code}.", ephemeral=True)
        return
    
    # Create embed with round-specific message
    embed = discord.Embed(
        title=f"🎯 Join for Room {room_code} ({mode.name})",
        description=f"Press on {round_emoji} emoji for {room_code} warzone\n\n**Mode:** {mode.name}\n**Max Players:** {max_players}\n**Voice Channel:** {voice_channel.mention}",
        color=discord.Color.green()
    )
    
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction(round_emoji)  # Bot's own reaction (never counted)
    
    # Track this message and room_code for reaction handling
    if not hasattr(bot, "wz_signup_messages"):
        bot.wz_signup_messages = {}
    bot.wz_signup_messages[msg.id] = {
        "room_code": room_code, 
        "users": set(), 
        "message": msg,
        "round_emoji": round_emoji,
        "max_players": max_players,
        "voice_channel": voice_channel,
        "role": role,
        "mode": mode.value
    }
    
    # Auto-delete message after 2 minutes if not full
    async def delete_after_timeout():
        await asyncio.sleep(120)  # 2 minutes = 120 seconds
        try:
            # Only delete if the message still exists in tracking (not full)
            if msg.id in bot.wz_signup_messages:
                await msg.delete()
                del bot.wz_signup_messages[msg.id]
        except Exception as e:
            print(f"Error deleting wz-all message: {e}")
    
    # Start the auto-delete task
    bot.loop.create_task(delete_after_timeout())


@tree.command(name="team_balance", description="Balance two teams based on player levels")
@app_commands.describe(levels="Comma-separated player levels (e.g. 48,50,51,35,51,50,50,37,51,52)")
async def team_balance(interaction: discord.Interaction, levels: str):
    try:
        level_list = [int(x.strip()) for x in levels.split(",") if x.strip()]
        n = len(level_list)
        if n % 2 != 0:
            await interaction.response.send_message("❌ Number of players must be even (e.g., 8 or 10).", ephemeral=True)
            return

        team_size = n // 2
        min_diff = float('inf')
        best_team_a = []
        for combo in combinations(level_list, team_size):
            team_a = list(combo)
            team_b = list(level_list)
            for lvl in team_a:
                team_b.remove(lvl)
            diff = abs(sum(team_a) - sum(team_b))
            if diff < min_diff:
                min_diff = diff
                best_team_a = team_a
        team_b = list(level_list)
        for lvl in best_team_a:
            team_b.remove(lvl)
        sum_a = sum(best_team_a)
        sum_b = sum(team_b)
        diff = abs(sum_a - sum_b)
        await interaction.response.send_message(
            f"**Team A:** {best_team_a} | Total Level: {sum_a}\n"
            f"**Team B:** {team_b} | Total Level: {sum_b}\n"
            f"**Level Difference:** {diff}",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


# Sheet functions already imported above

@tree.command(name="check_in", description="Post Round 1 check-in with Saturday/Sunday options")
@app_commands.describe(
    day="Select tournament day"
)
@app_commands.choices(
    day=[
        app_commands.Choice(name="Saturday (Round1-Parallel)", value="saturday"),
        app_commands.Choice(name="Sunday (Round1-Main)", value="sunday")
    ]
)
async def check_in(interaction: discord.Interaction, day: app_commands.Choice[str]):
    if not is_commander_or_higher(interaction):
        return await interaction.response.send_message(
            "🚫 Only Commanders can activate check-ins.", ephemeral=True
        )
    if interaction.channel.name != "warzone-r1-selfrole":
        return await interaction.response.send_message(
            "❌ Use this command in the #warzone-r1-selfrole channel.", ephemeral=True
        )
    
    # Configure based on selected day
    if day.value == "saturday":
        title = "Saturday Round 1 Check-In"
        description = "⚔️ React with ⚔️ to check-in for Saturday Round 1! (Check-ins close automatically in 20 minutes)"
        color = discord.Color.purple()
        emoji = "⚔️"
        day_name = "Saturday"
    else:  # sunday
        title = "Sunday Round 1 Check-In"
        description = "🗡️ React with 🗡️ to check-in for Sunday Round 1! (Check-ins close automatically in 20 minutes)"
        color = discord.Color.gold()
        emoji = "🗡️"
        day_name = "Sunday"
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    await interaction.response.send_message(embed=embed, ephemeral=False)
    msg = await interaction.original_response()
    try:
        await msg.add_reaction(emoji)
    except Exception as e:
        await interaction.followup.send(f"❌ Could not add reaction: {e}", ephemeral=True)
    
    # Track this message for check-in
    if not hasattr(bot, "checkin_messages"):
        bot.checkin_messages = {}
    bot.checkin_messages[msg.id] = {
        "day": day.value,
        "emoji": emoji,
        "day_name": day_name
    }
    
    # 20-minute auto-deletion with warnings
    async def delete_after_timeout():
        # Wait 18 minutes, then send warning
        await asyncio.sleep(1080)  # 18 minutes = 1080 seconds
        try:
            warning_embed = discord.Embed(
                title="⚠️ Check-In Closing Soon",
                description=f"{emoji} **{day_name} Round 1 Check-In closes in 2 minutes!**\n\nHurry up and react with {emoji} to join!",
                color=discord.Color.orange()
            )
            await msg.reply(embed=warning_embed, delete_after=120)
        except Exception as e:
            print(f"Error sending warning: {e}")
        
        # Wait 2 more minutes, then delete
        await asyncio.sleep(120)  # 2 more minutes = 120 seconds (total 20 minutes)
        try:
            # Send closure message
            closure_embed = discord.Embed(
                title="🔒 Check-In Closed",
                description=f"**{day_name} Round 1** check-ins are now **CLOSED**!",
                color=discord.Color.red()
            )
            await msg.reply(embed=closure_embed, delete_after=30)
            
            # Delete original message
            await msg.delete()
            
            # Remove from tracking
            if msg.id in bot.checkin_messages:
                del bot.checkin_messages[msg.id]
                
        except Exception as e:
            print(f"Error deleting check-in message: {e}")
    
    # Start the auto-delete task
    bot.loop.create_task(delete_after_timeout())
    
    # Log in warzone-r1-checkedin channel
    log_channel = interaction.guild.get_channel(CHANNEL_IDS.get("warzone-r1-checkedin"))
    if log_channel:
        try:
            await log_channel.send(embed=embed)
        except Exception as e:
            print(f"Error posting check-in log: {e}")
    
    # Reminder for Sunday tours
    if day.value == "sunday":
        await interaction.followup.send("⚠️ Please clean the sheet from the previous Sat tour before starting the Sun tour!", ephemeral=True)

@tree.command(name="sign_off", description="Post reaction sign-off message for players")
async def sign_off(interaction: discord.Interaction):
    if interaction.channel.name != "warzone-r1-selfrole":
        return await interaction.response.send_message(
            "❌ Use this command in the #warzone-r1-selfrole channel.", ephemeral=True
        )
    await interaction.response.send_message(
        "🛡️ React with 🛡️ to remove yourself from the Round 1 queue!",
        ephemeral=False
    )
    msg = await interaction.original_response()
    await msg.add_reaction("🛡️")

@tree.command(name="support-give-role", description="Assign a role to a user (Staff Only)")
@app_commands.describe(
    user="User to assign the role to",
    role="Role to assign"
)
async def support_give_role(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    if not is_staff(interaction):
        await interaction.response.send_message("🚫 You are not authorized to use this command.", ephemeral=True)
        return
    try:
        bot_member = interaction.guild.me
        if not bot_member.guild_permissions.manage_roles:
            raise Exception("Bot lacks 'Manage Roles' permission.")
        if role >= bot_member.top_role:
            raise Exception("Bot's role is not high enough in the role hierarchy to manage the target role.")
        await user.add_roles(role)
        await interaction.response.send_message(f"✅ {role.mention} assigned to {user.mention}.", ephemeral=True)
        # Log in support-ʟᴏɢs channel
        log_channel = interaction.guild.get_channel(CHANNEL_IDS.get("support-ʟᴏɢs"))
        if log_channel:
            await log_channel.send(f"[GIVE] {role.mention} assigned to {user.mention} by {interaction.user.mention}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error assigning role: `{e}`", ephemeral=True)

@tree.command(name="support-remove-role", description="Remove a role from a user (Staff Only)")
@app_commands.describe(
    user="User to remove the role from",
    role="Role to remove"
)
async def support_remove_role(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    if not is_staff(interaction):
        await interaction.response.send_message("🚫 You are not authorized to use this command.", ephemeral=True)
        return
    try:
        bot_member = interaction.guild.me
        if not bot_member.guild_permissions.manage_roles:
            raise Exception("Bot lacks 'Manage Roles' permission.")
        if role >= bot_member.top_role:
            raise Exception("Bot's role is not high enough in the role hierarchy to manage the target role.")
        await user.remove_roles(role)
        await interaction.response.send_message(f"✅ {role.mention} removed from {user.mention}.", ephemeral=True)
        # Log in support-ʟᴏɢs channel
        log_channel = interaction.guild.get_channel(CHANNEL_IDS.get("support-ʟᴏɢs"))
        if log_channel:
            await log_channel.send(f"[REMOVE] {role.mention} removed from {user.mention} by {interaction.user.mention}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error removing role: `{e}`", ephemeral=True)



if __name__ == "__main__":
    # Get Discord token from environment or prompt user
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Discord token not found in environment variables.")
        print("Please set your Discord bot token in the DISCORD_TOKEN environment variable.")
        print("You can also create a .env file with: DISCORD_TOKEN=your_token_here")
        exit(1)
    
    try:
        print("🚀 Starting Discord bot...")
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Invalid Discord token. Please check your bot token.")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
