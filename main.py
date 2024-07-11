from src.controllers import MainController
import asyncio


async def main():
    controller = MainController()
    await controller.initialize()
    await controller.start_telegram_listener()

if __name__ == '__main__':
    asyncio.run(main())
