
from dotenv import load_dotenv
import os
import time

from src.helper import (
    load_pdf_file,
    filter_to_minimal_docs,
    text_split,
    download_hugging_face_embeddings,
)

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore


# 1. Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError(
        "PINECONE_API_KEY is missing. Check your .env file."
    )


# 2. Load and process medical PDFs
print("\n[1/4] Loading medical PDF files...")
extracted_data = load_pdf_file(data="data/")

print(f"PDF documents loaded: {len(extracted_data)}")

filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = list(text_split(filter_data))

if not text_chunks:
    raise ValueError(
        "No text chunks found. Check your PDF files in data/."
    )

print(f"Total text chunks: {len(text_chunks)}")


# 3. Load embedding model
print("\n[2/4] Loading embedding model...")
embeddings = download_hugging_face_embeddings()

# Detect the actual embedding dimension
embedding_dimension = len(
    embeddings.embed_query("dimension check")
)

print(f"Embedding dimension: {embedding_dimension}")


# 4. Connect to Pinecone and prepare the index
print("\n[3/4] Connecting to Pinecone...")

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-chatbot"

if not pc.has_index(index_name):
    print(f"Creating index: {index_name}")

    pc.create_index(
        name=index_name,
        dimension=embedding_dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        ),
    )

    print("Waiting for Pinecone index to become ready...")

    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index_info = pc.describe_index(index_name)

if index_info.dimension != embedding_dimension:
    raise ValueError(
        f"Index dimension is {index_info.dimension}, "
        f"but the embedding model produces {embedding_dimension}. "
        "Use an index with the correct dimension."
    )

index = pc.Index(index_name)

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings,
)


# OPTIONAL:
# If you need to restart indexing from scratch, and this index
# contains ONLY disposable test data, clear its default namespace
# once by uncommenting the next line:
#
# index.delete(delete_all=True)


# Upload documents in small batches
print("\n[4/4] Uploading medical text chunks...")
batch_size = 16
total_chunks = len(text_chunks)

for start in range(0, total_chunks, batch_size):
    batch = text_chunks[start:start + batch_size]

    # Stable IDs help avoid duplicates on repeated runs
    ids = [
        f"medical-chunk-{i}"
        for i in range(start, start + len(batch))
    ]

    vector_store.add_documents(
        documents=batch,
        ids=ids,
    )

    uploaded = min(start + len(batch), total_chunks)
    print(f"Progress: {uploaded}/{total_chunks} chunks uploaded")

print("\nSUCCESS: Medical documents indexed in Pinecone!")