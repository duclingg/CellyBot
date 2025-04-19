import os
import discord

from tiktok import *
from dotenv import load_dotenv
from discord.ext import commands

class DiscordBot:
    def __init__(self):
        load_dotenv()
        
        self.tiktok = TikTok("nahcelly")
        
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.VERIFIED_ROLE_NAME = os.getenv("VERIFIED_ROLE_NAME")
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        self.setup()
        self.commands()
        
    def setup(self):
        @self.bot.event
        async def on_ready():
            print("\n----------------------------------------------------")
            print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
            print("----------------------------------------------------\n")
            
            # wait for discord bot to start
            if self.tiktok:
                asyncio.create_task(self.tiktok.run())
            
    def commands(self):
        @self.bot.command()
        async def verify(ctx, username: str):
            await ctx.send(f"Checking if `{username}` follows `nahcelly`")
            
            # FAKE PASS
            verified = True
            
            if verified:
                guild = discord.utils.get(self.bot.guilds, id=self.GUILD_ID)
                member = guild.get_member(ctx.author.id)
                role = discord.utils.get(guild.roles, name="testing") # TODO: change to actual role name
                
                if role not in member.roles:
                    await member.add_roles(role)
                    await ctx.send(f"You've been verified!")
                else:
                    await ctx.send("You're already verified!")
            else:
                await ctx.send(f"Could not verify `{username}` as a follower.\nPlease follow `@nahcelly` on TikTok and try again.")
                
    async def run(self):
        await self.bot.start(self.TOKEN)
            