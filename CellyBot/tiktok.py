import asyncio
import pytz

from datetime import datetime, time
from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
from TikTokLive.events import ConnectEvent, DisconnectEvent, LiveEndEvent

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
        self.live_link = f"https://www.tiktok.com/@{self.tiktok}/live"
                
        # attach event handlers
        self.client.add_listener(ConnectEvent, self.on_connect)
        self.client.add_listener(DisconnectEvent, self.on_disconnect)
        self.client.add_listener(LiveEndEvent, self.on_live_end)
        
        self.client.logger.setLevel(LogLevel.INFO.value)
        
        self.alert_sent = False
        self.alert_sent_date = None
        self.tz = pytz.timezone('US/Central')
        
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
        self.client.logger.info(f"(ConnectEvent) Connected to @{event.unique_id}")
        
        now = datetime.now(self.tz)
        current_date = now.date()
        
        if self.alert_sent_date != current_date:
            self.alert_sent_date = None
        
        if self.alert_sent_date is None:
            # send and publish alert with link and timestamp if live
            channel = self.discord_bot.bot.get_channel(self.discord_bot.CHANNEL_ID)
            if channel:
                now = datetime.now(pytz.timezone('US/Central'))
                timestamp = now.strftime("`%m/%d/%y`\n`%I:%M %p`")
                msg = await channel.send(
                    f"# `@{self.tiktok}` is **LIVE** on TikTok!\n### Date/Time: \n{timestamp} ***Central***\n## Join the stream:\n{self.live_link}"
                )
                await msg.publish()
                self.client.logger.info("Alert sent and published to `stream-schedule` channel.")
                self.alert_sent_date = current_date
        
    async def on_disconnect(self, event: DisconnectEvent):
        self.client.logger.info(f"(DisconnectEvent) Disconnected from @{self.tiktok}, reconnecting...")
    
    async def on_live_end(self, event: LiveEndEvent):
        self.client.logger.info(f"(LiveEndEvent) Live streaming ending, disconnecting from @{self.tiktok}")
            
    def in_timeframe(self, current_time):
        start_time = time(11, 0)
        end_time = time(23, 0)
        
        return start_time <= current_time <= end_time
    
    async def run_client(self):
        now = datetime.now(self.tz)
        current_time = now.time()
        
        if self.in_timeframe(current_time):
            await self.check_live()
        
    def check_followers(self):
        pass