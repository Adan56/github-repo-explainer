def retrieve(
    query,
    embedding_model,
    vector_store,
    top_k=5,
    where=None
):

    # Convert query → embedding
    query_embedding = embedding_model.generate_embeddings(
        [query]
    )[0]

    # Search vector DB
    results = vector_store.search(
        query_embedding=query_embedding,
        n_results=top_k,
        where=where
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for doc, meta in zip(documents, metadatas):

        retrieved_chunks.append({
            "content": doc,
            "metadata": meta
        })

    return retrieved_chunks