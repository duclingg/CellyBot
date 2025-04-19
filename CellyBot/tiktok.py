import asyncio

from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
from TikTokLive.events import ConnectEvent

class TikTok:
    def __init__(self, bot, tiktok: str):
        """
        This TikTok client checks the live status of a user, collects new followers from the live, and cross-checks the specified user's followers list.
        
        Args:
            bot (DiscordBot): The Discord bot to be used for alerts and verification.
            tiktok (str): The username of the TikTok streamer to be used. `@` symbol is not required.
        """      
        self.discord_bot = bot
        
        self.tiktok = tiktok
        self.client = TikTokLiveClient(unique_id=f"@{self.tiktok}")
        self.is_live = False
        
        # attach event handlers
        self.client.on(ConnectEvent)(self.on_connect)
        
        self.client.logger.setLevel(LogLevel.INFO.value)
        
    async def check_live(self):
        """
        Checks whether the specified user is live on TikTok
        """
        while True:
            while not await self.client.is_live():
                self.client.logger.info(f"\n`{self.tiktok}` is currently not live.\nChecking again in 60 seconds.\n")
                await asyncio.sleep(60)
                
            self.client.logger.info("Requested client is live.")
            await self.client.connect()
            
    async def on_connect(self, event: ConnectEvent):
        """
        When connected to live stream, send alert to Discord Channel

        Args:
            event (ConnectEvent): Connects to the Event using the `TikTokLive` API
        """
        self.client.logger.info(f"Connected to @{event.unique_id}")
        
        # send alert if live
        channel = self.discord_bot.bot.get_channel(self.discord_bot.CHANNEL_ID)
        if channel:
            await channel.send(f"@{self.tiktok} is **LIVE** on TikTok!")
                
    async def run(self):
        await self.check_live()
        
    def check_followers():
        pass