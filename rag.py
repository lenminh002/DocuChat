import pypdf
from config import supabase, openai
from langchain_text_splitters import RecursiveCharacterTextSplitter


# This is the instruction we give the AI before every conversation.
# It tells the AI to only answer based on the document the user uploaded.
system_prompt = """
You are a precise, knowledgeable assistant. Answer questions using only the provided context from the uploaded document.

Rules:
- If the context fully answers the question — answer clearly and concisely.
- If the question is ambiguous, ask one clarifying question before answering.
- Answer only what the context supports — cite relevant parts when helpful.
- If the context partially answers the question, share what you can and flag what's missing.
- If the answer isn't in the context, say: "I don't have that information in the provided context."
- Never invent facts, infer beyond the context, or use prior knowledge to fill gaps.
- Be concise, direct, and accurate.
"""


def read_file(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    if uploaded_file.type == "application/pdf":
        reader = pypdf.PdfReader(uploaded_file)
        return "".join(page.extract_text() for page in reader.pages)

    return uploaded_file.read().decode("utf-8")


# Split the document text into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400, 
    chunk_overlap=40
)
def split_document(document_text: str) -> list:
    if not document_text or not document_text.strip():
        return []
    return splitter.create_documents([document_text])


# Convert each chunk into an embedding (a list of numbers)
def create_embeddings(document_chunks: list) -> list[dict]:
    texts = [chunk.page_content for chunk in document_chunks]

    embedding_response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )

    # Pair each chunk's text with its embedding vector
    return [
        {
            "text": texts[i],
            "embedding": embedding_response.data[i].embedding
        }
        for i in range(len(texts))
    ]


# Store the embeddings in Supabase
def store_embeddings(embeddings: list[dict]):
    supabase.table("documents").delete().neq("id", 0).execute()
    supabase.table("documents").insert(embeddings).execute()



def retrieve_context(user_prompt: str, match_count: int = 5) -> str:
    # Turn the question into an embedding vector
    query_embedding = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=user_prompt
    ).data[0].embedding

    # Semantic search
    result = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "similarity_threshold": 0.60,
        "match_count": match_count
    }).execute()

    # Join into one big context string
    return "\n\n".join(row["text"] for row in result.data)


def getChatCompletion(user_prompt: str, context: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_prompt}"},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


# 1. Read the file → 2. Split → 3. Embed → 4. Store → 5. Retrieve → 6. Answer
def rag_pipeline(uploaded_file, user_prompt: str) -> str:
    document_text = read_file(uploaded_file)
    document_chunks = split_document(document_text)
    embeddings = create_embeddings(document_chunks)
    store_embeddings(embeddings)
    context = retrieve_context(user_prompt)
    return getChatCompletion(user_prompt, context)