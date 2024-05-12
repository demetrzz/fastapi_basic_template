import asyncio

from task_manager.main.web import run_api

if __name__ == "__main__":
    asyncio.run(run_api())
