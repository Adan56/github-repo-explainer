import chromadb
from chromadb import config
import numpy as np
import os
from typing import List, Dict, Optional




class VectorStore:

    def __init__(self, collection_name: str = "github_repo", persist_directory: str = "../Repo_explainer/repo_explainer/data/VectorStore"):
        
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_or_create_collection(
                name = self.collection_name,
                metadata={"description": "embeddings store"}
            )

            print(f"Vector Store initialised. Collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count()}")
        
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise

    def add_documents(
        self,
        documents: List[str],
        embeddings: List[np.ndarray],
        ids: List[str],
        metadatas: Optional[List[Dict]] = None
    ):

        try:

            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids,
                metadatas=metadatas
            )

            print(f"Added {len(documents)} documents")

        except Exception as e:
            print(f"Error adding documents: {e}")

    def search(
        self,
        query_embedding: List[float],
        n_results: int = 3,
        where: Optional[Dict] = None
    ):

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )

            return results

        except Exception as e:
            print(f"Search error: {e}")