from langchain_text_splitters import RecursiveCharacterTextSplitter
import ast
from typing import List
import uuid
import os


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""]
)


def worker(files: List, embedding_model, vector_store):

    for file in files:

        try:

            with open(file, "r", errors="ignore") as f:
                content = f.read()

        except Exception as e:
            print(f"Could not read {file}: {e}")
            continue

        # PYTHON FILES → AST CHUNKING
        if file.endswith(".py"):
            try:
                tree = ast.parse(content)
                lines = content.splitlines()
                for node in tree.body:
                    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                        document = "\n".join(lines[node.lineno - 1: node.end_lineno])
                        embedding = embedding_model.generate_embeddings([document])
                        metadata = {
                            "file_path": file,
                            "folder": os.path.dirname(file),
                            "file_name": os.path.basename(file),
                            "symbol_name": node.name,
                            "language": "python",
                            "type": "class" if isinstance(node, ast.ClassDef) else "function"
                        }

                        vector_store.add_documents(
                            documents=[document],
                            embeddings=embedding,
                            ids=[str(uuid.uuid4())],
                            metadatas=[metadata]
                        )

            except Exception as e:
                print(f"AST parsing failed for {file}: {e}")
        # NON-PYTHON FILES
        else:
            documents = text_splitter.split_text(content)
            embeddings = embedding_model.generate_embeddings(documents)
            metadatas = []
            for _ in documents:
                metadatas.append({
                    "file_path": file,
                    "folder": os.path.dirname(file),
                    "file_name": os.path.basename(file),
                    "language": "text",
                    "type": "text_chunk"
                })
            vector_store.add_documents(
                documents=documents,
                embeddings=embeddings,
                ids=[str(uuid.uuid4()) for _ in documents],
                metadatas=metadatas
            )