from discord_bot import *
from tiktok import *

if __name__ == "__main__":
    discord_bot = DiscordBot()
    discord_bot.run()
    
    tiktok = TikTok("nahcelly")
    tiktok.run()