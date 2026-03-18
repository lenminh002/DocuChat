# DocuChat 🗂️

Chat with your documents using AI. Upload a PDF or text file and ask questions — DocuChat finds the most relevant parts of your document and answers based only on what's in it.

## How to Run

### 1. Install dependencies

```bash
uv sync
```

### 2. Set up environment variables

Create a `.env` file in the root:

```
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_api_key
```

### 3. Set up Supabase

In your Supabase project, go to the **SQL Editor** and run `document.sql`. This will:

- Enable the pgvector extension
- Create the `documents` table
- Create the `match_documents` similarity search function

### 4. Run the app

```bash
uv run streamlit run main.py
```

Then open `http://localhost:8501` in your browser.

## Built With

- **Streamlit** — frontend UI
- **OpenAI** — embeddings (`text-embedding-ada-002`) + chat (`gpt-4o-mini`)
- **Supabase** — vector storage with pgvector for semantic search
- **LangChain** — document splitting (`RecursiveCharacterTextSplitter`)
- **pypdf** — PDF text extraction

## How It Works

Every time you ask a question, the app runs a 6-step RAG pipeline:

```
1. Read     → extract text from uploaded PDF or .txt file
2. Split    → break text into overlapping chunks (400 chars, 40 overlap)
3. Embed    → convert chunks into vectors using OpenAI embeddings
4. Store    → save vectors + text to Supabase
5. Retrieve → embed the question, find the most similar chunks in Supabase
6. Answer   → send retrieved chunks as context to GPT and return the answer
```

The AI only answers based on the document — it will not make up information.

## Project Structure

```
DocuChat/
├── main.py          # Streamlit UI
├── rag.py           # RAG pipeline (read, split, embed, store, retrieve, answer)
├── config.py        # OpenAI + Supabase client setup
├── document.sql     # Supabase table + match_documents function
├── .env             # API keys (not committed)
└── pyproject.toml   # Dependencies
```
