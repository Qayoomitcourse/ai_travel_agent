import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from travel_tools import get_flights, suggest_hotels

load_dotenv

api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

destination_agent = Agent(
    name="Destination Agent",
    instructions="""
You are a travel expert. Based on the user's mood or interests, suggest one destination only. 
Reply with just the destination name, e.g., "Tokyo" or "Istanbul" — no explanation.
""",
    model=model
)

# 2. Booking agent
booking_agent = Agent(
    name="Booking Agent",
    instructions="You help book flights and hotels using available tools. Input will be a destination name.",
    model=model,
    tools=[get_flights, suggest_hotels]
)

# 3. Explore agent
explore_agent = Agent(
    name="Explore Agent",
    instructions="You suggest top attractions, activities, and local food for the given destination.",
    model=model
)

def main():
    print("🧳 AI Travel Designer Agent")
    mood = input("What's your travel mood or interest (e.g., beach, adventure, culture)? -> ").strip()

    # Step 1: Get destination
    result1 = Runner.run_sync(destination_agent, mood, run_config=config)
    destination = result1.final_output.strip().split("\n")[0]
    print("\n📍 Suggested Destination:", destination)

    # Step 2: Booking info
    result2 = Runner.run_sync(booking_agent, destination, run_config=config)
    print("\n🛏️ Travel Booking Info:\n", result2.final_output)

    # Step 3: Explore suggestions
    result3 = Runner.run_sync(explore_agent, destination, run_config=config)
    print("\n🎒 Explore & Food Guide:\n", result3.final_output)

if __name__ == "__main__":
    main()