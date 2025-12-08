from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI # this is the LLM model
from langchain.tools import tool
from langchain.agents import create_agent


from dotenv import load_dotenv

load_dotenv() 


@tool
def calculator_tool(x: float, y: float) -> str:
    """Tool to perform addition calculations."""
    try: 
        result = x + y
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
    model = ChatOpenAI(temperature=0)
    tools = [calculator_tool]
    agent_executor = create_agent(model, tools=tools)

    start_agent(agent_executor)
if __name__ == "__main__":
    main()
