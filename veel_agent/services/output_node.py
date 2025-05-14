from veel_agent.schemas.state import StateDict
from veel_agent.configs.logging_config import logging

logger = logging.getLogger(__name__)

def output_node(state: StateDict) -> StateDict:
    logger.info("Compiling final output.")
    output = f"""Final Output:
Trend: {state.get('trend', 'N/A')}
Hashtags: {state.get('hashtags', [])}
Script: {state.get('script', 'N/A')}
"""
    state["output"] = output
    return state
