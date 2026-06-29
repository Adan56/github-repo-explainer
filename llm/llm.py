from google import genai

client = genai.Client(api_key="api-key")


def generate_answer(query, retrieved_chunks):

    context = ""

    for chunk in retrieved_chunks:

        metadata = chunk["metadata"]

        context += f"""
    FILE: {metadata.get("file_path", "")}

    TYPE: {metadata.get("type", "")}

    SYMBOL: {metadata.get("symbol_name", "")}

    CONTENT:
    {chunk['content']}

    ----------------------------------------
    """

        prompt = f"""
    You are an AI assistant that explains GitHub repositories.

    Answer the user's question ONLY using the provided context.

    If the answer is not present in the context, say:
    "I could not find relevant information in the repository."

    QUESTION:
    {query}

    CONTEXT:
    {context}
    """

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    return response.text