import asyncio
from src.workflow import Workflow
from src.models import URLPrompt
from dotenv import load_dotenv

load_dotenv()


async def main():
    workflow = Workflow()
    while True:
        query = input("Developer Tools query: ").strip()
        if query.lower() in ["quit","exit"]:
            break
        else:
            url = input("Resource (web link, swagger html, etc...): ")
            result = await workflow.run(query=URLPrompt(url=url, task=query))
    # workflow.save_graph("workflow.png")


if __name__ == "__main__":
    asyncio.run(main())