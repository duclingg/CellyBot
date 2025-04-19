import asyncio

from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
from TikTokLive.events import ConnectEvent

class TikTok:
    """
    
    """
    def __init__(self, tiktok: str):
        self.tiktok = tiktok.lstrip("@")
        self.client = TikTokLiveClient(unique_id=f"@{self.tiktok}")
        self.is_live = False
        
        # attach event handlers
        self.client.on(ConnectEvent)(self.on_connect)
        
        self.client.logger.setLevel(LogLevel.INFO.value)
    
    """
    
    """    
    async def on_connect(self, event: ConnectEvent):
        self.client.logger.info(f"Connected to @{event.unique_id}")
        
    async def check_live(self):
        while True:
            while not await self.client.is_live():
                self.client.logger.info("\nClient is currently not live.\nChecking again in 60 seconds.")
                await asyncio.sleep(60)
                
            self.client.logger.info("Requested client is live.")
            await self.client.connect()
                
    def run(self):
        asyncio.run(self.check_live())
        
    def check_followers():
        pass

if __name__ == "__main__":
    tiktok = TikTok("nahcelly")
    tiktok.run()