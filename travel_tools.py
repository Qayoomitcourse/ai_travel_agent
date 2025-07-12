from agents import function_tool

@function_tool
def get_flights(destination: str) -> str:
    return f"✈️ Flights to {destination}: \n- Air Blue at 9AM\n- Serene Air at 2PM\n- PIA at 6PM"

@function_tool
def suggest_hotels(destination: str) -> str:
    return f"🏨 Hotels in {destination}: \n- Hotel Elite\n- Grand Inn\n- BudgetStayz\n- Royal Suites"
