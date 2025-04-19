import asyncio

from discord_bot import *

async def cellybot():
    discord_bot = DiscordBot()
    
    await discord_bot.run()

if __name__ == "__main__":
    try:
        print("Starting CellyBot...")
        asyncio.run(cellybot())
    except KeyboardInterrupt:
        print("\nShutting down...")