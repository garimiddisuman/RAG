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


answer_prompt = ChatPromptTemplate.from_messages([
  (
    "system",
    """
You are an internal company knowledge assistant.

Answer the user's question using only the provided company documentation.

If the documentation does not contain enough information to answer
the question, say that you don't know.

Do not make up or assume information that is not present in the
provided documentation.

Retrieved company documentation:

{context}
""",
  ),
  (
    "placeholder",
    "{messages}",
  ),
])


relevance_prompt = ChatPromptTemplate.from_messages([
  (
    "system",
    """
You are a document relevance checker.

Determine whether the provided company documentation contains
information that can help answer the user's question.

Return only one word:

RELEVANT

or

IRRELEVANT
""",
  ),
  (
    "human",
    """
Question:
{question}

Company documentation:
{context}
""",
  ),
])


def retrieve(state: RAGState):
  question = state["messages"][-1].content

  documents = search(question)

  return {
    "context": documents,
  }


def check_relevance(state: RAGState):
  question = state["messages"][-1].content

  context = "\n\n".join(
    document.page_content
    for document in state["context"]
  )

  messages = relevance_prompt.invoke({
    "question": question,
    "context": context,
  })

  response = llm.invoke(messages)

  result = response.content.strip().upper()

  return {
    "is_relevant": result == "RELEVANT",
  }


def generate(state: RAGState):
  context = "\n\n".join(
    document.page_content
    for document in state["context"]
  )

  messages = answer_prompt.invoke({
    "context": context,
    "messages": state["messages"],
  })

  response = llm.invoke(messages)

  return {
    "messages": [response],
  }


def fallback(state: RAGState):
  return {
    "messages": [
      {
        "role": "assistant",
        "content": "I don't have much information regarding this.",
      }
    ],
  }


def route_after_relevance_check(state: RAGState):
  if state["is_relevant"]:
    return "generate"

  return "fallback"


builder = StateGraph(RAGState)

builder.add_node("retrieve", retrieve)
builder.add_node("check_relevance", check_relevance)
builder.add_node("generate", generate)
builder.add_node("fallback", fallback)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "check_relevance")

builder.add_conditional_edges(
  "check_relevance",
  route_after_relevance_check,
  {
    "generate": "generate",
    "fallback": "fallback",
  },
)

builder.add_edge("generate", END)
builder.add_edge("fallback", END)


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
        "is_relevant": False,
      },
      config,
    )

    print(f"\nBot: {result['messages'][-1].content}")