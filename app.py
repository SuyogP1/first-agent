from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool, tool
#from smolagents import ToolCallingAgent
import requests

model = InferenceClientModel(
    model_id="Qwen/Qwen3-Next-80B-A3B-Instruct"
)

@tool
def get_weather(city:str) ->str:
    """
    Get the current weather of the city

    Args:
        city:Name of the city

    Returns:
        Current weather of the city
    """
    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1
        }
    )

    geo_data = geo_response.json()

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    response = requests.get("https://api.open-meteo.com/v1/forecast",params={"latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m"})
    data = response.json()

    temperature = data["current"]["temperature_2m"]
    wind_speed = data["current"]["wind_speed_10m"]

    return f"{city}:{temperature}°C, {wind_speed}"

@tool
def calculator(a :float, b: float, operation: str) -> float:
    """
    Perform a mathematical calculation on two numbers.

    Args:
        a: First number.
        b: Second number.
        operation: Mathematical operation to perform (+, -, *, /).

    Returns:
        The result of the calculation.
    """
    if(operation in ["+","add"]):
        return a + b
        
    elif(operation in ["-","subtract"]):
        return a - b

    elif(operation in ["*","multiply"]):
            return a * b

    elif(operation in ["/","divide"]):
            if(b == 0):
                  raise ValueError("Cannot divide by zero")
            return a / b

    else:
        raise ValueError("Invalid operation")

# Uses JSON
# agent = ToolCallingAgent(
#     tools=[DuckDuckGoSearchTool(), get_weather, calculator],
#     model=model
# )

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(),get_weather,calculator],
    model=model
)

query = input("What do you want to search?\n")

result = agent.run(query)

print(result)