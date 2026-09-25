# 🤖 AI Document QA

An AI-powered multi-document PDF question-answering application built using **Retrieval-Augmented Generation (RAG)**.

The application allows users to upload one or more PDF documents, process their content, ask questions about the documents, and receive answers generated from the relevant document context.

Each answer also displays the **PDF filename and page number** of the retrieved sources.

## 🚀 Live Application

**Live Demo:**
Add your Streamlit app URL here.

Example:

`https://your-app-name.streamlit.app`

## 📌 Project Overview

AI Document QA is designed to make it easier to interact with information stored inside PDF documents.

Instead of manually searching through long documents, users can:

1. Upload one or more PDF files.
2. Process the documents.
3. Ask questions using a chat interface.
4. Retrieve the most relevant document sections.
5. Generate an answer using an LLM.
6. View the source PDF filename and page number.

The project uses a **Retrieval-Augmented Generation (RAG)** pipeline so that the language model receives relevant information from the uploaded documents before generating an answer.

## ✨ Features

* 📄 Upload multiple PDF documents
* 🔍 Extract text from PDF pages
* ✂️ Split documents into overlapping text chunks
* 🧠 Generate text embeddings using Sentence Transformers
* ⚡ Store and search embeddings using FAISS
* 💬 Chat-based question answering
* 🤖 LLM-powered answer generation
* 🔄 Multiple LLM provider fallback architecture
* 📚 Display PDF filename and page number as sources
* 🔐 API keys stored securely outside the source code
* ☁️ Deployable using Streamlit Community Cloud

## 🏗️ System Architecture

```text
                PDF Documents
                      │
                      ▼
              PDF Text Extraction
                   PyMuPDF
                      │
                      ▼
                 Text Chunking
                1000 characters
                  150 overlap
                      │
                      ▼
            Sentence Transformers
             all-MiniLM-L6-v2
                      │
                      ▼
                FAISS Vector Index
                      │
                      │
User Question ────────┘
      │
      ▼
Question Embedding
      │
      ▼
Retrieve Top Relevant Chunks
      │
      ▼
Document Context
      │
      ▼
      LLM Manager
      │
      ├── Gemini
      ├── Groq
      ├── OpenAI
      └── xAI / Grok
      │
      ▼
Generated Answer
      │
      ▼
Source References
PDF filename + Page number
```

## 🧠 How RAG Works in This Project

RAG stands for **Retrieval-Augmented Generation**.

The application does not simply send the user's question directly to an LLM.

Instead, it follows these steps:

### 1. Document ingestion

The user uploads PDF files through the Streamlit interface.

### 2. Text extraction

PyMuPDF extracts text from each PDF page while keeping track of:

* PDF filename
* Page number
* Extracted text

### 3. Chunking

The extracted text is divided into smaller chunks.

The current implementation uses:

* Chunk size: **1000 characters**
* Chunk overlap: **150 characters**

The overlap helps preserve context between neighboring chunks.

### 4. Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

from Sentence Transformers.

### 5. Vector search

The embeddings are stored in a FAISS index.

When the user asks a question, the question is also converted into an embedding.

FAISS then retrieves the most relevant document chunks.

The current application retrieves the top **5** results.

### 6. Context construction

The retrieved chunks are combined into a document context containing:

* Source document
* Page number
* Relevant text

### 7. Answer generation

The context and user question are sent to the configured LLM provider.

The prompt instructs the model to answer using only the supplied document context and to avoid inventing information.

### 8. Source display

After generating the answer, the application displays the retrieved source references:

```text
📄 document.pdf — Page 3
📄 another-document.pdf — Page 7
```

## 🛠️ Technologies Used

| Technology                | Purpose                               |
| ------------------------- | ------------------------------------- |
| Python                    | Core programming language             |
| Streamlit                 | Web application and user interface    |
| PyMuPDF                   | PDF text extraction                   |
| Sentence Transformers     | Text embeddings                       |
| all-MiniLM-L6-v2          | Embedding model                       |
| FAISS                     | Vector similarity search              |
| NumPy                     | Numerical processing                  |
| Google GenAI              | Gemini LLM integration                |
| OpenAI SDK                | OpenAI-compatible LLM integrations    |
| Groq                      | LLM fallback provider                 |
| xAI                       | Grok fallback provider                |
| python-dotenv             | Local environment variable management |
| GitHub                    | Source code repository                |
| Streamlit Community Cloud | Public deployment                     |

## 📁 Project Structure

```text
AI-Document-QA/
│
├── app.py
│   └── Streamlit application and user interface
│
├── pdf_processor.py
│   └── PDF text extraction and document chunking
│
├── rag_engine.py
│   └── Embedding generation and FAISS similarity search
│
├── llm_manager.py
│   └── LLM provider management and fallback logic
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
├── .gitignore
│   └── Files excluded from Git
│
└── .env
    └── Local API keys
    └── Not committed to GitHub
```

## 🔑 API Key Configuration

API keys should **never be hard-coded into the source code or committed to GitHub**.

### Local Development

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=
XAI_API_KEY=
```

The `.env` file should remain local and should be excluded using `.gitignore`.

### Streamlit Community Cloud

For deployment, add the required API keys through:

```text
Streamlit Community Cloud
        ↓
App Settings
        ↓
Secrets
```

Example:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
GROQ_API_KEY = "your_groq_api_key"
OPENAI_API_KEY = ""
XAI_API_KEY = ""
```

**Never publish actual API keys in this README or on GitHub.**

## 💻 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/puli-anil/AI-Document-QA.git
```

Move into the project directory:

```bash
cd AI-Document-QA
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file and add your API keys.

### 5. Run the application

```powershell
streamlit run app.py
```

The application will open in your browser.

## ▶️ How to Use

### Step 1

Open the application.

### Step 2

Use the sidebar:

```text
📚 Upload Documents
```

### Step 3

Select one or more PDF files.

### Step 4

Click:

```text
Process Documents
```

The application extracts the text, creates chunks, generates embeddings, and builds the FAISS vector index.

### Step 5

Ask a question in:

```text
Ask a question about your documents...
```

### Step 6

Review the generated answer.

The application also displays:

* AI provider used
* PDF source
* Page number

## 🔄 LLM Fallback Architecture

The project uses a provider fallback design.

The current order is:

```text
Gemini
   ↓
Groq
   ↓
OpenAI
   ↓
xAI / Grok
```

If a configured provider fails, the application attempts the next available provider.

This architecture is intended to improve resilience when a provider is temporarily unavailable or a configured API cannot respond.

## 📚 Source Citations

The application keeps source metadata during document processing.

Each retrieved chunk contains:

```text
text
source
page
```

This allows the final interface to show the origin of the retrieved information.

Example:

```text
📄 internship_report.pdf — Page 12
```

## 🔒 Security

The project follows these basic security practices:

* API keys are stored in environment variables or Streamlit Secrets.
* `.env` is excluded from Git.
* API keys are not included in source code.
* Local vector-store artifacts are excluded from Git.
* Private documents should not be committed to a public repository.

## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

Deployment flow:

```text
GitHub Repository
       ↓
Streamlit Community Cloud
       ↓
Configure Secrets
       ↓
Deploy app.py
       ↓
Public Streamlit Application
```

## ⚠️ Current Limitations

The current version is designed as a lightweight RAG application and has some limitations:

* Vector indexes are created during document processing rather than stored permanently.
* Uploaded documents are processed for the current application session.
* Scanned/image-only PDFs may require OCR support.
* Retrieval quality depends on chunking and embedding quality.
* The application currently uses a basic FAISS similarity search.
* LLM availability depends on the configured provider and its API limits.

## 🔮 Future Improvements

Possible future improvements include:

* OCR support for scanned PDFs
* Better semantic chunking
* Metadata filtering
* Similarity score thresholds
* Reranking retrieved chunks
* Persistent vector databases
* Conversation memory
* Improved citation formatting
* Document management and deletion
* Authentication and user accounts
* Streaming LLM responses
* More advanced evaluation and RAG quality metrics
* Improved UI and document preview

## 🎯 Project Goal

The goal of this project is to build a practical AI-powered document assistant that combines:

* Document processing
* Natural language processing
* Vector search
* Retrieval-Augmented Generation
* LLM integration
* Source attribution
* Web application development
* Cloud deployment

The project demonstrates how a complete RAG pipeline can be integrated into an interactive application.

## 👨‍💻 Author

**Puli Anil**

GitHub:
https://github.com/puli-anil

## 📄 License

This project is intended for educational and demonstration purposes.

A formal open-source license can be added later if the project is intended for broader redistribution.
