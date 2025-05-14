
# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from veel_agent.schemas.status import Status
# from veel_agent.services.agent import build_graph

# # Load environment variables from .env file
# load_dotenv()

# app = FastAPI(title="LangGraph AI Agent API")
# graph = build_graph()

# class Query(BaseModel):
#     input: str

# @app.post("/analyze")
# def analyze(query: Query):
#     if not query.input:
#         raise HTTPException(status_code=400, detail="Input cannot be empty")

#     state = Status(input=query.input)
#     result = graph.invoke(state)
    
#     return {
#         "output": result.get("output", "No output generated"),
#         "hashtags": result.get("hashtags", []),
#         "trends": result.get("trends", {}),
#         "logs": result.get("logs", [])
#     }


import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from veel_agent.schemas.state import Status
from veel_agent.services.graph_builder import build_graph, display_graph

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="LangGraph AI Agent API")
graph = build_graph()

class Query(BaseModel):
    input: str

@app.post("/analyze")
def analyze(query: Query):
    if not query.input:
        raise HTTPException(status_code=400, detail="Input cannot be empty")

    state = Status(input=query.input)
    result = graph.invoke(state)

    return {
        "output": result.get("output", "No output generated"),
        "hashtags": result.get("hashtags", []),
        "trends": result.get("trends", {}),
        "logs": result.get("logs", [])
    }

@app.get("/graph")
def show_graph():
    """Endpoint to display the graph structure."""
    display_graph(graph)
    return {"message": "Graph visualization saved as 'langgraph_workflow.png' and displayed."}