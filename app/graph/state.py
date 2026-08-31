from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class RAGState(TypedDict):
  messages: Annotated[list[BaseMessage], add_messages]
  context: list
  is_relevant: bool