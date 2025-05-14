from veel_agent.schemas.state import StateDict
from veel_agent.configs.logging_config import logging

logger = logging.getLogger(__name__)

def step_planner(state: StateDict) -> StateDict:
    query = state.get("query", "").lower()
    logger.info(f"Step planner received query: {query}")
    
    steps = []
    if "trend" in query:
        steps.append("trend")
    if "hashtag" in query:
        steps.append("hashtag")
    if "script" in query or not steps:
        steps.append("script")

    flags = {step: False for step in steps}

    state["steps"] = steps
    state["flags"] = flags
    state["current_step"] = 0

    logger.info(f"Planned steps: {steps}")
    return state
