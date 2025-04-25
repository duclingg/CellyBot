import os
import discord
import sys

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tiktok import *
from database.follower_store import FollowerStore
from dotenv import load_dotenv
from discord.ext import commands

class DiscordBot:
    def __init__(self, tiktok: str):
        """
        This object initializes the Discord Bot, setting the required intents to be used by the bot.

        Args:
            tiktok (str): The username of the TikTok streamer to be used. `@` symbol is not required.
        """
        load_dotenv(override=True)
        
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.VERIFIED_ROLE_NAME = os.getenv("VERIFIED_ROLE_NAME")
        self.CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
        
        self.tiktok = tiktok
        self.tiktok_client = TikTok(self, self.tiktok)
        self.tiktok_task = None
        
        # intents required
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        # initialize bot with commands
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        self.setup()
        self.verify()
        
    def setup(self):
        @self.bot.event
        async def on_ready():
            print("\n---------------------------------------------------------------------")
            print(f"[CellyBot] INFO: Logged in as {self.bot.user} (ID: {self.bot.user.id})")
            print("---------------------------------------------------------------------\n")
            
            # wait for discord bot to start and check live status
            if self.tiktok_client:
                self.tiktok_task = await self.tiktok_client.run_client()
            
    def verify(self):
        @self.bot.command()
        async def verify(ctx, username: str):
            await ctx.send(f"Checking if `@{username}` follows `@{self.tiktok}`")
            
            verified = self.verify_follower(username)
            print(f"\n[CellyBot] INFO - Verifying user `@{username}`")
            
            await asyncio.sleep(1)
            
            if verified:
                guild = discord.utils.get(self.bot.guilds, id=self.GUILD_ID)
                member = guild.get_member(ctx.author.id)
                role = discord.utils.get(guild.roles, name=self.VERIFIED_ROLE_NAME)
                
                if role not in member.roles:
                    await member.add_roles(role)
                    await ctx.send(f"You've been verified!")
                    print(f"[CellyBot] INFO - `@{username}` verified.\n")
                else:
                    print(f"[CellyBot] ERROR - `@{username}` already verified.\n") # TODO: Remove after testing
            else:
                await ctx.send(f"Could not verify `@{username}` as a follower.\nPlease follow `@{self.tiktok}` on TikTok and try again.")
                print(f"[CellyBot] INFO - `@{username}` could not be verified.\n")
                
    def verify_follower(self, username):
        store = FollowerStore()
        return store.check_follower(username)
                
    async def run(self):
        await self.bot.start(self.TOKEN)