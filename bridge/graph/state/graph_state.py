import operator
from typing import TypedDict, Annotated, Sequence, List

from langchain_core.messages import BaseMessage


class N8State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    requirements: List[str]
    generated_workflow: dict
    publish_result: dict
    is_successfulLy_published: bool
