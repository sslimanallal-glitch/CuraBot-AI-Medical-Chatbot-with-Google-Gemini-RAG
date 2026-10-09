# MediGuide AI — Intelligent Medical Chatbot

**An AI-powered medical chatbot built with Python, Flask, LangChain, Google Gemini, and Pinecone.**

## About the Project

MediGuide AI is an intelligent medical information chatbot designed to answer user questions using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

I developed and customized this application by working on its frontend, backend, AI integration, and knowledge retrieval workflow. The project combines modern web development technologies with generative AI to create an interactive medical information assistant.

My objective was to build an end-to-end AI application that connects a user-friendly web interface to an LLM-powered backend and a vector database.

## Key Features

* **AI-Powered Chatbot:** Generate contextual responses using Google Gemini.
* **RAG Architecture:** Retrieve relevant information from a configured medical knowledge base before generating responses.
* **Semantic Search:** Use Pinecone to search for relevant document content.
* **Custom Frontend:** Customize the chatbot interface using HTML and CSS.
* **Python Backend:** Connect the user interface, AI model, and retrieval pipeline using Flask.
* **LLM Integration:** Integrate Google Gemini into the chatbot workflow.
* **Document Processing:** Prepare medical documents for information retrieval.
* **Environment Configuration:** Manage API credentials through environment variables.

## Technologies Used

| Technology    | Purpose                                |
| ------------- | -------------------------------------- |
| Python        | Backend development                    |
| Flask         | Web application and API routes         |
| Google Gemini | Language model and response generation |
| LangChain     | LLM application and RAG orchestration  |
| Pinecone      | Vector database and semantic retrieval |
| HTML5         | Web page structure                     |
| CSS3          | Interface design and styling           |
| Git & GitHub  | Version control                        |
| Docker        | Containerization, when configured      |
| AWS           | Cloud deployment, when configured      |

## System Architecture

```text
             USER
               |
               v
       HTML / CSS INTERFACE
               |
               v
         FLASK BACKEND
               |
               v
        LANGCHAIN PIPELINE
               |
          +----+----+
          |         |
          v         v
       PINECONE   GOOGLE GEMINI
       Retrieval   Generation
          |
          v
   Relevant Medical Context
          |
          v
    Contextual AI Response
          |
          v
       CHAT INTERFACE
```

## How It Works

1. The user submits a medical information question through the web interface.
2. Flask receives the request and passes it to the chatbot logic.
3. The retrieval pipeline searches the configured medical knowledge base.
4. Pinecone returns relevant document information when retrieval is configured correctly.
5. The retrieved context is combined with the user's question.
6. Google Gemini generates a response using the available context.
7. The application returns the response to the user.

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root and add the environment variables required by the application.

```ini
GOOGLE_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

Use the exact variable names expected by your Python files. Never publish real API keys.

### 5. Prepare the Knowledge Base

If the project includes the indexing script, configure the document directory and vector database, then run:

```bash
python store_index.py
```

### 6. Start the Application

```bash
python app.py
```

Open the local address displayed in the terminal. For example:

```text
http://localhost:8080
```

The port depends on the Flask configuration.

## Development Highlights

This project combines several important areas of AI engineering and web development:

* Designing and customizing a web-based chatbot interface.
* Connecting a Python backend to a generative AI model.
* Integrating external APIs and managing configuration.
* Working with vector databases and semantic retrieval.
* Organizing a Retrieval-Augmented Generation workflow.
* Preparing an application for testing and potential cloud deployment.

## Project Goals

The project demonstrates how generative AI, document retrieval, and web development can be combined into a practical application.

It also provides a foundation for further improvements, including source citations, conversation history, automated tests, Docker deployment, and a CI/CD pipeline.

## Medical Disclaimer

MediGuide AI is an educational project for medical information retrieval. It is not a medical professional and must not be used as a replacement for professional diagnosis, treatment, or emergency medical advice. AI-generated information may be incomplete or inaccurate.

## Author

**YOUR NAME**

* GitHub: YOUR_GITHUB_PROFILE
* LinkedIn: YOUR_LINKEDIN_PROFILE
* Portfolio: YOUR_PORTFOLIO_URL
* Email: YOUR_EMAIL

---

*AI Engineering | Large Language Models | Retrieval-Augmented Generation | Web Development*
