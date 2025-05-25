import asyncio

from bot import *

async def cellybot():
    bot = Bot(tiktok="nahcelly")
    
    await bot.run()

if __name__ == "__main__":
    try:
        print("Starting CellyBot...")
        asyncio.run(cellybot())
    except KeyboardInterrupt:
        print("\nShutting down...")