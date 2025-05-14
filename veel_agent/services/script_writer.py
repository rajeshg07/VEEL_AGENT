# from veel_agent.services.base_node import BaseNode
# from veel_agent.schemas.state import StateDict
# from veel_agent.configs.logging_config import logging

# logger = logging.getLogger(__name__)


# class ScriptWriter(BaseNode):
#     def process(self, state: StateDict) -> StateDict:
#         logger.info(f"Running script writer for: {state['query']}")
#         if not state["flags"].get("script"):
        
#             state["script"] = f"Script based on: {state['query']}"
#             state["flags"]["script"] = True
#         state["current_step"] += 1
#         return state


import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from veel_agent.services.base import BaseNode  #need to change

# Load environment variables from .env file
load_dotenv()

class ScriptNode(BaseNode):
    def __init__(self):
        super().__init__(name="Script Node")
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def __call__(self, state):
        self.log(state, "Generating final script using LLM")
        prompt = f"""
        User asked: {state.input}
        Trend info: {state.trends}
        Hashtags: {state.hashtags}
        Provide a concise marketing recommendation.
        """
        try:
            response = self.llm.invoke(prompt)
            state.output = response.content
        except Exception as e:
            state.output = "Failed to generate output."
            self.log(state, f"LLM error: {e}", level="ERROR")
        return state

