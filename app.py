
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

from src.helper import download_hugging_face_embeddings

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt


# ==================================================
# 1. Flask configuration
# ==================================================

app = Flask(__name__)

# Load .env from the same directory as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


# ==================================================
# 2. Load API keys
# ==================================================

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError(
        "PINECONE_API_KEY is missing. Check your .env file."
    )

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. Check your .env file."
    )


# ==================================================
# 3. Load embedding model
# ==================================================

print("\nLoading Hugging Face embedding model...")

embeddings = download_hugging_face_embeddings()

print("Embedding model loaded successfully.")


# ==================================================
# 4. Connect to the existing Pinecone index
# ==================================================

index_name = "medical-chatbot"

print(f"\nConnecting to Pinecone index: {index_name}")

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

print("Pinecone connection configured successfully.")


# ==================================================
# 5. Configure Google Gemini
# ==================================================

print("\nConfiguring Google Gemini...")

chatModel = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
)

print("Gemini configured successfully.")


# ==================================================
# 6. Build the RAG chain
# ==================================================

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(
    chatModel,
    prompt,
)

rag_chain = create_retrieval_chain(
    retriever,
    question_answer_chain,
)

print("RAG chain initialized successfully.")


# ==================================================
# 7. Flask routes
# ==================================================

@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():

    msg = request.values.get("msg", "").strip()

    if not msg:
        return "Please enter a question.", 400

    try:
        print(f"\nUser question: {msg}")

        response = rag_chain.invoke(
            {"input": msg}
        )

        answer = response.get(
            "answer",
            "Sorry, I could not generate an answer.",
        )

        print("Answer generated successfully.")

        return str(answer)

    except Exception:
        app.logger.exception(
            "Error while generating the chatbot response"
        )

        return (
            "Sorry, an error occurred while generating the answer. "
            "Check the VS Code terminal for details.",
            500,
        )


# ==================================================
# 8. Start Flask
# ==================================================

if __name__ == "__main__":
    print("\nMedical Chatbot is starting...")
    print("Open http://127.0.0.1:8080 in your browser.")

    app.run(
        host="127.0.0.1",
        port=8080,
        debug=True,
        use_reloader=False,
    )

