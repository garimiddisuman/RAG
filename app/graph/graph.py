from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.config import LLM_MODEL
from app.graph.state import RAGState
from app.retrieval.search import search


llm = ChatOllama(
  model=LLM_MODEL,
)


prompt = ChatPromptTemplate.from_messages([
  (
    "system",
    """
You are a Thoughtworks STEP program knowledge assistant. Answer questions using only the provided STEP documentation and clearly say when the information is unavailable.
Do not make up or assume STEP information, and prefer current program information over historical information when they conflict.
Retrieved STEP documentation:

{context}
""",
  ),
  (
    "placeholder",
    "{messages}",
  ),
])


def retrieve(state: RAGState):
  question = state["messages"][-1].content

  documents = search(question)

  return {
    "context": documents,
  }


def generate(state: RAGState):
  context = "\n\n".join(
    document.page_content
    for document in state["context"]
  )

  messages = prompt.invoke({
    "context": context,
    "messages": state["messages"],
  })

  response = llm.invoke(messages)

  return {
    "messages": [response],
  }


builder = StateGraph(RAGState)

builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)


checkpointer = InMemorySaver()

graph = builder.compile(
  checkpointer=checkpointer,
)


if __name__ == "__main__":
  config = {
    "configurable": {
      "thread_id": "employee-001",
    },
  }

  while True:
    question = input("\nYou: ")

    if question.lower() in {"exit", "quit"}:
      break

    result = graph.invoke(
      {
        "messages": [
          HumanMessage(content=question),
        ],
        "context": [],
      },
      config,
    )

    print(f"\nBot: {result['messages'][-1].content}")