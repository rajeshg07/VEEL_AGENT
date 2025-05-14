# from langgraph.graph import StateGraph, END
# from veel_agent.schemas.state import StateDict
# from veel_agent.services.step_planner import step_planner
# from veel_agent.services.trend_analyzer import TrendAnalyzer
# from veel_agent.services.hashtag_finder import HashtagFinder
# from veel_agent.services.script_writer import ScriptWriter
# from veel_agent.routes.step_router import get_next_step
# from veel_agent.services.output_node import output_node  # Fixed import path

# def build_graph():
#     graph = StateGraph(StateDict)

#     graph.add_node("planner", step_planner)
#     graph.add_node("trend", TrendAnalyzer("trend").process)
#     graph.add_node("hashtag", HashtagFinder("hashtag").process)
#     graph.add_node("script", ScriptWriter("script").process)
#     graph.add_node("output", output_node)

#     graph.set_entry_point("planner")

#     for source in ["planner", "trend", "hashtag", "script"]:
#         graph.add_conditional_edges(
#             source,
#             get_next_step,
#             {
#                 "trend": "trend",
#                 "hashtag": "hashtag",
#                 "script": "script",
#                 "output": "output"
#             }
#         )

#     graph.add_edge("output", END)
#     return graph.compile()



import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from veel_agent.schemas.status import Status
from veel_agent.services.serpapi_trend_node import SerpApiTrendNode #need to change
from veel_agent.services.serpapi_hashtag_node import SerpApiHashtagNode #need to change
from veel_agent.services.script_node import ScriptNode  #need to change

# Load environment variables from .env file
load_dotenv()

def build_graph():
    builder = StateGraph(Status)

    builder.add_node("trend", SerpApiTrendNode())
    builder.add_node("hashtag", SerpApiHashtagNode())
    builder.add_node("script", ScriptNode())

    builder.set_entry_point("trend")
    builder.add_edge("trend", "hashtag")
    builder.add_edge("hashtag", "script")
    builder.set_finish_point("script")

    print("Graph compiled successfully.")
    return builder.compile()