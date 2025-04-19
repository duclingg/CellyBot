import os
import discord

from tiktok import *
from dotenv import load_dotenv
from discord.ext import commands

class DiscordBot:
    def __init__(self, tiktok: str):
        """
        This object initializes the Discord Bot, setting the required intents to be used by the bot.

        Args:
            tiktok (str): The username of the TikTok streamer to be used. `@` symbol is not required.
        """
        load_dotenv()
        
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
        self.commands()
        
    def setup(self):
        @self.bot.event
        async def on_ready():
            print("\n----------------------------------------------------")
            print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
            print("----------------------------------------------------\n")
            
            # wait for discord bot to start and check live status
            if self.tiktok_client:
                self.tiktok_task = asyncio.create_task(self.tiktok_client.check_live())
            
    def commands(self):
        @self.bot.command()
        async def verify(ctx, username: str):
            await ctx.send(f"Checking if `@{username}` follows `@{self.tiktok}`")
            
            # FAKE PASS
            verified = True
            
            if verified:
                guild = discord.utils.get(self.bot.guilds, id=self.GUILD_ID)
                member = guild.get_member(ctx.author.id)
                role = discord.utils.get(guild.roles, name="dev-testing") # TODO: change to actual role name
                
                if role not in member.roles:
                    await member.add_roles(role)
                    await ctx.send(f"You've been verified!")
                else:
                    await ctx.send("You're already verified!")
            else:
                await ctx.send(f"Could not verify `@{username}` as a follower.\nPlease follow `@{self.tiktok}` on TikTok and try again.")
                
    async def run(self):
        await self.bot.start(self.TOKEN)            
        
    async def shutdown(self):
        if self.tiktok_task:
            self.tiktok_task.cancel()
            try:
                await self.tiktok_task
            except asyncio.CancelledError:
                pass
            
        if self.tiktok_client.client.is_connected:
            await self.tiktok_client.client.disconnect()
            
        await self.bot.close()
            