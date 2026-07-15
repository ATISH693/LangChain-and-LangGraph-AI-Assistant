from typing import TypedDict, List, Optional, Literal

class ChunksState(TypedDict):
    content: str
    source: str
    score: float


class FlowState(TypedDict):
    question : str
    chunks : List[ChunksState]
    best_score : float
    answer : Optional[str]
    review_decision : Optional[ Literal["approved", "rejected"] ]
    status: Literal["retrieve", "generate", "review", "finished", "error"]
