
# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI

# load_dotenv()

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.5,
#     openai_api_key=os.getenv("OPENAI_API_KEY")
# )

# def llm_start_node(state):
#     state.logs.append("LLM Start Node: Processing user input")
#     return state

# def llm_end_node(state):
#     prompt = f"User asked: {state.input}\nTrend info: {state.trends}\nHashtags: {state.hashtags}\nPlease provide a marketing recommendation."
#     state.logs.append(f"LLM End Node: Generating response with GPT-4o Mini")
#     response = llm.invoke(prompt)
#     state.output = response.content
#     return state


