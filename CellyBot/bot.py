import os
import discord
import sys
import random

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger import CellyBotLogger
from tiktok import *
from dotenv import load_dotenv
from discord.ext import commands

class Bot:
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
            
            try:
                synced = await self.bot.tree.sync(guild=discord.Object(id=self.GUILD_ID))
                self.logger.info(f"Synced {len(synced)} commands to guild: {self.GUILD_ID}")
            except Exception as e:
                self.logger.error(f"Error syncing to command tree: {e}")
            
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
        @self.bot.tree.command(name="info", description="Display information about CellyBot commands", guild=discord.Object(id=self.GUILD_ID))
        async def info(interaction: discord.Interaction):
            message = """
                # CellyBot Info
                ## Available Commands:  
                \n`!info` - Pulls up this info box
                \n`!socials` - Get Celly's socials!
                \n`!greet` - Say hi to CellyBot
                \n`!bullyNik` - CellyBot will bully Nikalaus
            """
            await interaction.response.send_message(message)
            
        @self.bot.tree.command(name="socials", description="Lists NahCelly's socials", guild=discord.Object(id=self.GUILD_ID))
        async def socials(interaction: discord.Interaction):
            message = f"""
                ## NahCelly's Socials:
                ### Check out <#{self.CHANNEL_ID}> for annoucments of when he's live!
                \nTikTok: https://www.tiktok.com/@nahcelly?_t=ZT-8veRvjBgeru&_r=1
                \nYouTube: https://youtube.com/@nahcelly?si=dELq4_AFHoVUcmml
                \nTwitch: https://www.twitch.tv/nahcelly
            """
            await interaction.response.send_message(message)
            
        @self.bot.tree.command(name="greet", description="Greet CellyBot!", guild=discord.Object(id=self.GUILD_ID))
        async def greet(interaction: discord.Interaction):
            messages = [
                "Hey there CellyFam!",
                "What the Celly?",
                "Yoooooo",
                "Thanks for the follow!",
                "Beep boop."
            ]
            await interaction.response.send_message(random.choice(messages))
            
        @self.bot.tree.command(name="bully-nik", description="Bully Nikalaus :)", guild=discord.Object(id=self.GUILD_ID))
        async def bully_nik(interaction: discord.Interaction):
            messages = [
                "Nik is a good boy",
                "Nik can't beat me in a 1v1",
                "Nik sucks!",
                "I heard Nik uses simple edit"
            ]
            await interaction.response.send_message(random.choice(messages))
                
    async def run(self):
        await self.bot.start(self.TOKEN)