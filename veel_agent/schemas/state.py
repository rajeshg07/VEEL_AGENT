from typing import TypedDict, List, Optional

class StateDict(TypedDict, total=False):
    query: str
    steps: List[str]
    flags: dict[str, bool]
    current_step: int

    trend: str
    hashtags: List[str]
    script: str
    output: str


