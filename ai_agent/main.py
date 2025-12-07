from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent


from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# toll is a external service that the agent can use to perform specific tasks
#@tool decorator to define a tool for the agent
# the decorator takes care of registering the tool with the agent and making it available for use
#
@tool
def calculator_tool(x: float, y: float) -> str:
    """Tool to perform calculations."""
    try:
        # Evaluate the mathematical expression provided in the query   
        result = x + y# if user ask for subtr
        print("Calculator_tool called with")
        return f"The result of adding {x} and {y} is {result}."
    except Exception as e:
        return f"Error in calculation: {e}" 

def start_agent(agent_executor):
    print("Hello I am your AI agent!")
    print("Ask me anything to perform calculations, or chat with me.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input == "quit":
            break
        
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
        #  print(chunk.keys(), end="")  # Print the raw chunk for debugging
            
            if "model" in chunk and "messages" in chunk["model"]:
                    for message in chunk["model"]["messages"]:
                        print(message.content, end="")
        print()

def main():

    # initialize a chat model
    model = ChatOpenAI(temperature=0)

    # tools for the agent 
    tools = []


    # initialize an agent with the chat model
    agent_executor = create_agent(model, tools=tools)

    start_agent(agent_executor)
if __name__ == "__main__":
    main()


# REAct
# I need to find the the number of kids in each grade in the school
# Action: calculator_tool
# Action Input: "What is 30 kids in grade 1 + 25 kids in grade 2 + 20 kids in grade 3?"
# Observation: "The result of adding 30 and 25 is 55. The result of adding 55 and 20 is 75."
# Thought: I now know the total number of kids in the school
# Final Answer: "The total number of kids in the school is 75."
