from dotenv import load_dotenv
import os
from agents import Runner,Agent,WebSearchTool
import asyncio

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found.")


agent = Agent(
    name="News Agent",
    instructions="You are a news agent that can search the web for the latest news on a given topic."
                 " Compile the information you find to into a concise 1 paragraph summary. No markdown, just plain text.",
    tools=[WebSearchTool()]
    )

async def main():
    while True:
        query = input("Enter your news query (or 'quit' to exit): ")
        if query.lower() == "quit":
            break

        result= await Runner.run(agent, input=query)
        print(f"\nresult:")
        print(result.final_output )
        print("\n"+"-"*50+"\n")


if __name__ == "__main__":
    asyncio.run(main())