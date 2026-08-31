# Company Knowledge RAG Bot

A simple, local **Retrieval-Augmented Generation (RAG)** chatbot that allows employees to ask questions about company documentation.

The project uses:

* **Python** — Application language
* **LangChain** — LLM and prompt integration
* **LangGraph** — Bot workflow and conversation state
* **Ollama** — Local embeddings and LLM
* **ChromaDB** — Local vector database
* **Markdown** — Company knowledge source

The company knowledge is stored as Markdown files inside the `documents/` directory.

---

# What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique where an LLM retrieves relevant information from an external knowledge source before generating an answer.

Instead of expecting the LLM to know all company-specific information, we provide the relevant company documentation to the LLM at question time.

For example:

```text
Employee:
"How many annual leave days do I get?"
```

The system searches the company's documentation and finds:

```text
documents/leave-policy.md

Employees receive 20 days of paid annual leave
for every calendar year.
```

That information is then provided to the LLM, which generates the final answer.

This allows the knowledge base to be updated without changing or retraining the LLM.

---

# RAG Flow

The project has two main flows:

## 1. Document Ingestion

Documents are converted into embeddings and stored in ChromaDB.

```text
Markdown Documents
        |
        v
Document Loader
        |
        v
Document Chunking
        |
        v
Ollama Embedding Model
        |
        v
Vector Embeddings
        |
        v
ChromaDB
```

The documents are stored in:

```text
documents/
```

For example:

```text
documents/
├── benefits.md
├── company-overview.md
├── employee-onboarding.md
├── leave-policy.md
└── remote-work-policy.md
```

Running `store.py` processes these documents and stores their embeddings in:

```text
chroma_db/
```

---

## 2. Question Answering

When an employee asks a question:

```text
Employee Question
        |
        v
LangGraph
        |
        v
Retrieve Relevant Documents
        |
        v
ChromaDB
        |
        v
Relevant Context
        |
        v
Relevance Check
       / \
      /   \
 Relevant  Irrelevant
    |          |
    v          v
 Generate    Fallback
 Answer      Response
    |
    v
Ollama LLM
    |
    v
Final Answer
```

The bot also maintains conversation history so that follow-up questions can use previous conversation context.

For example:

```text
You:
How many annual leave days do I get?

Bot:
You get 20 days of paid annual leave per year.

You:
Can I carry them forward?

Bot:
Yes. You can carry forward up to 5 unused annual leave days.
```

---

# Project Structure

```text
RAG/
├── app/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   └── graph.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   └── store.py
│   │
│   └── retrieval/
│       ├── __init__.py
│       └── search.py
│
├── documents/
│   ├── benefits.md
│   ├── company-overview.md
│   ├── employee-onboarding.md
│   ├── leave-policy.md
│   └── remote-work-policy.md
│
├── chroma_db/
├── .venv/
├── .gitignore
└── README.md
```

`chroma_db/` and `.venv/` are local/generated directories and should not be committed to Git.

---

# Local Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd RAG
```

If you are creating the project from scratch, simply enter the project directory.

---

## 2. Create a Python virtual environment

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

You should see:

```text
(.venv)
```

in your terminal.

---

## 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# Install Dependencies

Install the required packages:

```bash
python -m pip install -U \
  langchain \
  langgraph \
  langchain-ollama \
  langchain-community \
  langchain-text-splitters \
  langchain-chroma \
  chromadb
```

The main dependencies are:

| Package                    | Purpose                             |
| -------------------------- | ----------------------------------- |
| `langchain`                | LLM and application abstractions    |
| `langgraph`                | Bot workflow and state management   |
| `langchain-ollama`         | LangChain integration with Ollama   |
| `langchain-community`      | Document loaders                    |
| `langchain-text-splitters` | Document chunking                   |
| `langchain-chroma`         | LangChain integration with ChromaDB |
| `chromadb`                 | Vector database                     |

---

# Install Ollama

Install Ollama on your machine and make sure the Ollama service is running.

Verify the installation:

```bash
ollama --version
```

Check the currently installed models:

```bash
ollama list
```

---

# Install the Embedding Model

This project uses:

```text
nomic-embed-text
```

Pull the model:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

You should see:

```text
nomic-embed-text
```

The embedding model converts document chunks and user questions into vectors.

---

# Install the LLM

The bot also needs a chat/generative model.

For example:

```bash
ollama pull llama3.2
```

Verify:

```bash
ollama list
```

You should have both:

```text
nomic-embed-text
llama3.2
```

The models are used for different purposes:

```text
nomic-embed-text
        |
        v
Document/question embeddings


llama3.2
        |
        v
Answer generation
```

Update the model name in:

```text
app/config.py
```

if you are using a different Ollama model.

---

# Configure the Application

The main configuration is stored in:

```text
app/config.py
```

Example:

```python
from pathlib import Path


DOCUMENTS_DIR = Path("documents")

CHROMA_PERSISTENCE_DIR = "./chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"

LLM_MODEL = "llama3.2"

CHROMA_COLLECTION_NAME = "company_documents"
```

Keep model names, Chroma collection names, and persistence locations here rather than duplicating them throughout the application.

---

# Build the Vector Database

Before running the bot for the first time, the Markdown documents need to be indexed.

Run:

```bash
python -m app.ingestion.store
```

The ingestion process will:

```text
documents/
    |
    v
Load Markdown files
    |
    v
Chunk documents
    |
    v
Generate embeddings using Ollama
    |
    v
Store embeddings in ChromaDB
```

After successful execution, a local directory will be created:

```text
chroma_db/
```

This contains the local ChromaDB data.

You do not need to manually create this directory.

---

# Run the Bot

After the vector database has been created, run:

```bash
python -m app.graph.graph
```

The application will start an interactive chat:

```text
You: How many annual leave days do I get?

Bot: Employees receive 20 days of paid annual leave per year.

You: Can I carry them forward?

Bot: Yes, employees can carry forward up to 5 unused annual leave days.

You: exit
```

Use:

```text
exit
```

or:

```text
quit
```

to stop the application.

---

# Using the Bot for Different Knowledge

The project is designed so that the application code does not need to change when the knowledge changes.

The Markdown files inside:

```text
documents/
```

are the knowledge source.

For example, you could replace the company documents with documentation about:

```text
documents/
├── product-overview.md
├── api-documentation.md
├── architecture.md
├── troubleshooting.md
└── faq.md
```

Or:

```text
documents/
├── university-courses.md
├── admission-policy.md
├── examination-rules.md
├── hostel-rules.md
└── student-faq.md
```

Or:

```text
documents/
├── software-documentation.md
├── installation.md
├── configuration.md
├── troubleshooting.md
└── faq.md
```

The RAG application can remain the same.

---

# Updating the Knowledge Base

When you change, add, or replace Markdown files:

```text
documents/
```

NOTE : update the system prompt in app/graph/graph.py if the knowledge domain changes.

run the ingestion process again:

```bash
python -m app.ingestion.store
```

Then start the bot:

```bash
python -m app.graph.graph
```

The general workflow is:

```text
1. Update documents/
        |
        v
2. Run store.py
        |
        v
3. ChromaDB is updated
        |
        v
4. Run the bot
        |
        v
5. Ask questions
```

The Markdown documentation is therefore the **source of truth** for the RAG system.

---

# Example Questions

With the current company documentation, you can ask:

```text
How many annual leave days do employees get?

Can I work from home?

What happens during employee onboarding?

Does the company provide health insurance?

How much is the learning budget?

How many sick leave days do employees get?

Can unused annual leave be carried forward?

What are the requirements for production deployment?
```

You can also ask follow-up questions:

```text
You:
How many annual leave days do I get?

Bot:
You get 20 days of annual leave.

You:
Can I carry them forward?

Bot:
Yes, up to 5 unused annual leave days can be carried forward.
```

For information that is not available in the documentation, the bot should respond with a fallback such as:

```text
I don't have much information regarding this.
```

rather than inventing company information.

---

# Summary

This project implements a local conversational RAG system:

```text
                    Documents
                        |
                        v
                    Chunking
                        |
                        v
                Ollama Embeddings
                        |
                        v
                    ChromaDB
                        |
                        |
                  User Question
                        |
                        v
                    LangGraph
                        |
                        v
                  Semantic Search
                        |
                        v
                 Relevant Context
                        |
                        v
                  LangChain Prompt
                        |
                        v
                    Ollama LLM
                        |
                        v
                      Answer
```

The core idea is simple:

> **Keep the knowledge in Markdown files, index those documents into ChromaDB, and let the RAG bot retrieve the relevant information when answering questions.**
