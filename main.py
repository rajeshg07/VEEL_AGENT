# from veel_agent.configs.logging_config import logging
# from veel_agent.services.graph_builder import build_graph
# from veel_agent.schemas.state import StateDict

# logging.basicConfig(filename="/Users/user/Documents/Veel Project/veel_agent/veel_agent/logs/app.log", 
#                     level=logging.INFO, 
#                     format="%(asctime)s [%(levelname)s] %(message)s")

# def main():
#     query = input("Enter your content generation prompt: ")
#     state: StateDict = {"query": query}
#     app = build_graph()
#     final_state = app.invoke(state)
#     print("\n--- Output ---\n")
#     print(final_state.get("output"))

# if __name__ == "__main__":
#     main()


import os
from dotenv import load_dotenv
from veel_agent.schemas.status import Status  ##need to change
from veel_agent.services.agent import build_graph  #need to change

# Load environment variables from .env file
load_dotenv()

def main():
    graph = build_graph()
    
    print("LangGraph AI Agent")
    print("Supports: Marketing Trend Analysis & Hashtag Analysis")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        state = Status(input=user_input)
        result = graph.invoke(state)
        
        # LangGraph returns an AddableValuesDict, access values with dict-like notation
        output = result.get("output", "No output generated")
        
        print("\nAgent:", output)
        print("-" * 50)

if __name__ == "__main__":
    main()
