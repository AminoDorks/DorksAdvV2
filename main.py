from nest_asyncio import apply
from asyncio import run

from src._bot import Bot
apply()


async def main():
    await Bot().run()

if __name__ == "__main__":
    run(main())
