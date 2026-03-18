-- Enable pgvector extension (only need to do this once)
create extension if not exists vector;

-- Create the documents table
create table documents (
    id bigint primary key generated always as identity,
    text text,
    embedding vector(1536)  -- 1536 dimensions for text-embedding-ada-002
);

-- Create the match_documents function
create or replace function match_documents (
    query_embedding vector(1536),
    match_count int,
    similarity_threshold float default 0.7  -- only return chunks above this score
)
returns table (
    id bigint,
    text text,
    similarity float
)
language sql
as $$
    select
        id,
        text,
        1 - (embedding <=> query_embedding) as similarity
    from documents
    where 1 - (embedding <=> query_embedding) > similarity_threshold  -- filter low matches
    order by embedding <=> query_embedding
    limit match_count;
$$;