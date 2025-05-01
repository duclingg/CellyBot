import os
import discord
import sys

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger import CellyBotLogger
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
        load_dotenv(override=True)
        
        self.logger = CellyBotLogger()
        
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.VERIFIED_ROLE_NAME = os.getenv("VERIFIED_ROLE_NAME")
        self.VERIFICATION_MESSAGE_ID = int(os.getenv("VERIFICATION_MESSAGE_ID"))
        self.CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
        
        self.tiktok = tiktok
        self.tiktok_client = TikTok(self, self.tiktok)
        self.tiktok_task = None
        
        # intents required
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.members = True

        # initialize bot with commands
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        self.setup()
        self.verify()
        self.commands()
        
    def setup(self):
        @self.bot.event
        async def on_ready():
            """
            Starts the bot when ready. Starts the TikTokLive client after bot is initialized.
            """
            self.logger.start_log(self.bot.user, self.bot.user.id)
            
            # wait for discord bot to start and check live status
            if self.tiktok_client:
                self.tiktok_task = await self.tiktok_client.run_client()
            
    def verify(self):
        @self.bot.event
        async def on_raw_reaction_add(payload):
            """
            Verifies the user when joining with a reaction to a message. Assigns the role to the member to allow access to all channels.
            
            Args:
                payload: Discord payload
            """            
            # ignore bot reactions
            if payload.member and payload.member.bot:
                self.logger.info("Ignoring bot reaction")
                return
            
            # check if correct message
            if payload.message_id == self.VERIFICATION_MESSAGE_ID:
                self.logger.info(f"Reaction on verification message - Emoji: {payload.emoji}")
                
                # check if it's the correct emoji
                if str(payload.emoji) == "✅":
                    self.logger.info("Correct emoji detected")
                    
                    try:
                        guild = self.bot.get_guild(payload.guild_id)
                        if not guild:
                            self.logger.error(f"Could not find guild with ID {payload.guild_id}")
                            return
                        
                        # add verified role to member
                        role = discord.utils.get(guild.roles, name=self.VERIFIED_ROLE_NAME)
                        if not role:
                            self.logger.error(f"Could not find role with name {self.VERIFIED_ROLE_NAME}")
                            return
                        
                        if payload.member and role not in payload.member.roles:
                            await payload.member.add_roles(role)
                            self.logger.info(f"Successfully added role {self.VERIFIED_ROLE_NAME} to {payload.member.display_name}")
                        elif payload.member:
                            self.logger.info(f"User {payload.member.display_name} already has the role {self.VERIFIED_ROLE_NAME}")
                        else:
                            self.logger.error("Could not get member information from payload")
                    except Exception as e:
                        self.logger.error(f"Error assigning role: {str(e)}")
                        
    def commands(self):
        @self.bot.command()
        async def info(ctx):
            text = """
                # CellyBot Info
                ## Available Commands:  
                \n`!info` - Pulls up this info box
                \n`!greet` - Say hi to CellyBot
                \n`!bullyNik` - Bullies Nikalaus
                
                ## Want information about `@nahcelly`?
                ### Check out <#1362957662366728405> for annoucments of when he's live!
                ### Socials:
                \nTikTok: <https://www.tiktok.com/@nahcelly?_t=ZT-8veRvjBgeru&_r=1>
                \nYouTube: <https://youtube.com/@nahcelly?si=dELq4_AFHoVUcmml>
                \nTwitch: <https://www.twitch.tv/nahcelly>
            """
            await ctx.send(text)
                
    async def run(self):
        await self.bot.start(self.TOKEN)