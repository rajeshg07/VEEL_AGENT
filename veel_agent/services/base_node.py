# from veel_agent.schemas.state import StateDict
# from veel_agent.configs.logging_config import logging

# logger = logging.getLogger(__name__)

# class BaseNode:
#     def __init__(self, name: str):
#         self.name = name

#     def process(self, state: StateDict) -> StateDict:
#         raise NotImplementedError


from datetime import datetime
from veel_agent.schemas.status import Status  ##need to change

class BaseNode:
    def __init__(self, name: str):
        self.name = name

    def log(self, state: Status, message: str, level: str = "INFO"):
        state.logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "node": self.name,
            "level": level,
            "message": message
        })

    def __call__(self, state: Status) -> Status:
        raise NotImplementedError(f"{self.__class__.__name__} must implement __call__ method")