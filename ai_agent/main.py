from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent


from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def main():

    # initialize a chat model
    model = ChatOpenAI(temperature=0)

    # tools for the agent 
    tools = []


    # initialize an agent with the chat model
    agent_executor = create_agent(model, tools=tools)

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
if __name__ == "__main__":
    main()
