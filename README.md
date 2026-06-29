# GitHub Repository Explainer

An AI-powered GitHub repository assistant that ingests public GitHub repositories and enables semantic question answering over their codebases using Retrieval-Augmented Generation (RAG).

---

## Features

* Download and process public GitHub repositories directly from repository URLs.
* Parse Python source files using Python AST for function-level and class-level chunking.
* Chunk documentation and non-Python files using recursive text splitting.
* Generate semantic embeddings using Sentence Transformers.
* Store embeddings and metadata in ChromaDB for efficient similarity search.
* Answer repository-specific questions using Gemini Flash.
* Display source files used to generate answers.

---

## Architecture

```text
GitHub URL
    ↓
Download Repository ZIP
    ↓
Extract Repository
    ↓
Traverse Repository Files
    ↓
Python Files:
    AST Parsing
    → Function/Class Chunks

Other Files:
    Recursive Text Splitting
    → Text Chunks

    ↓
Sentence Transformer Embeddings
    ↓
ChromaDB Vector Store
    ↓
User Question
    ↓
Semantic Retrieval (Top-K Chunks)
    ↓
Gemini Flash
    ↓
Repository-Aware Answer + Sources
```

---

## Project Structure

```text
repo_explainer/
│
├── ingestion/
│   ├── github_loader.py
│   └── file_reader.py
│
├── retrieval/
│   └── retrieval.py
│
├── llm/
│   └── llm.py
│
├── chunking_and_embeddings_and_storing/
│   ├── EmbeddingModel.py
│   ├── VectorStore.py
│   └── chunking_and_embeddings_and_storing.py
│
├── data/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Technologies Used

* Python
* Sentence Transformers
* ChromaDB
* Gemini Flash
* LangChain Text Splitters
* Python AST
* NumPy

---

## Example Questions

### Repository Overview

* What is the purpose of this repository?
* Explain the architecture of this project.

### Code Understanding

* How is authentication implemented?
* What happens when a user logs in?
* How are refresh tokens generated?

### Code Navigation

* Which files are involved in JWT authentication?
* Where is token validation handled?

---

## Example Output

### Query

```
How do refresh tokens work?
```

### Answer

```
Refresh tokens are long-lived tokens used to create new access tokens once an existing access token expires.

Refresh tokens cannot access endpoints protected using jwt_required() while access tokens cannot access endpoints protected with jwt_refresh_token_required().
```

### Sources

```
docs/usage/refresh.md
docs/usage/freshness.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd repo_explainer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add your Gemini API key:

```python
genai.configure(api_key="YOUR_API_KEY")
```

Run the project:

```bash
python main.py
```

---

## Current Limitations

* Python files receive AST-based processing while other languages use text chunking.
* Large repositories may require additional filtering and optimization.
* Route-level metadata extraction for frameworks such as FastAPI is not yet implemented.

---

## Future Improvements

* Support additional programming languages using language-specific parsers.
* Hybrid retrieval using metadata and semantic search.
* Repository-level summaries using README analysis.
* Web interface for interactive repository exploration.

---

## Motivation

Understanding large repositories can be difficult for students and developers joining new projects. This project aims to reduce onboarding time by allowing developers to ask natural language questions directly against a repository's codebase.
