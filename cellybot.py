import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VERIFIED_ROLE_NAME = os.getenv("VERIFIED_ROLE_NAME")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('---------')
    
@bot.command()
async def verify(ctx, tiktok_username: str):
    await ctx.send(f'Checking if `{tiktok_username}` follows NahCelly... ')
    
    # FAKE PASS
    verified = True
    
    if verified:
        guild = discord.utils.get(bot.guilds, id=GUILD_ID)
        member = guild.get_member(ctx.author.id)
        role = discord.utils.get(guild.roles, name='testing')
        
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f"You've been verified!")
        else:
            await ctx.send("You're already verified!")
    else:
        await ctx.send("Could not verify you as a follower, Please follow @NahCelly on TikTok and try again.")

bot.run(TOKEN)