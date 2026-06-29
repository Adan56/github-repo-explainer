from input.github_loader import (
    download_repo,
    extract_zip
)

from input.file_reader import get_all_files

from chunking_and_embeddings_and_storing.chunking_and_embeddings_and_storing import worker

from chunking_and_embeddings_and_storing.EmbeddingModel import EmbeddingManager

from chunking_and_embeddings_and_storing.VectorStore import VectorStore

from retrieval.retrieval import retrieve

from llm.llm import generate_answer

import os

# initialising part
embedding_model = EmbeddingManager()

vector_store = VectorStore()


# downloading repo
repo_url = input("Enter GitHub repo URL: ")
download_repo(repo_url, "repo_explainer/data/repo.zip")
repo_path = extract_zip("repo_explainer/data/repo.zip", "repo_explainer/data/")
print(f"\nRepository extracted to:\n{repo_path}")


# get all files
files = get_all_files(repo_path)

print(f"\nFound {len(files)} files")


# storing in vector db
worker(
    files,
    embedding_model,
    vector_store
)

print("\nRepository indexed successfully!")


# QUESTION LOOP
while True:

    query = input("\nAsk a question (type exit to stop): ")

    if query.lower() == "exit":
        break

    retrieved_chunks = retrieve(
        query,
        embedding_model,
        vector_store
    )

    answer = generate_answer(
        query,
        retrieved_chunks
    )

    print("\nANSWER:\n")

    print(answer)

    print("\nSOURCES:\n")

    shown = set()

    for chunk in retrieved_chunks:

        path = chunk["metadata"]["file_path"]

        if path not in shown:

            print(path)

            shown.add(path)