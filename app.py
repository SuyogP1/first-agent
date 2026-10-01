from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool

model = InferenceClientModel(
    model_id="Qwen/Qwen3-Next-80B-A3B-Instruct"
)

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model
)
query = input("What do you want to search?\n")
result = agent.run(query)

print(result)