# 🇮🇳 BIS Nirdesh — AI-Powered BIS Standards Assistant

**Making Indian Standards easier to discover, understand, and apply.**

BIS Nirdesh is an AI-powered web application designed to help users explore Indian Standards published by the **Bureau of Indian Standards (BIS)**. It combines document-based retrieval, AI-powered question answering, source references, and product standards gap analysis in a single interface.

> **Project status:** Prototype / active development  
> **Platform:** Windows local deployment  
> **AI provider:** Google Gemini API

## 🚀 Why BIS Nirdesh?

Understanding technical standards can be challenging for manufacturers, students, product developers, and other users. Finding the right requirements in lengthy technical documents can take time.

BIS Nirdesh aims to simplify this process by letting users ask questions in natural language and explore information from the documents included in its knowledge base.

## ✨ Key Features

### 🤖 AI-Powered Question Answering
Ask questions about the available BIS documents and receive AI-generated responses.

### 📚 Document-Grounded Retrieval
Retrieve relevant passages from the prepared document collection to support question answering.

### 🔎 Source References
Help users trace responses back to relevant document content for further verification.

### 🧩 Product Standards Gap Analysis
Explore potential gaps between supplied product information and requirements represented in the available knowledge base.

### 🔑 Multi-API Key Management
Configure and test multiple Gemini API keys locally through the API manager.

### 🔄 Automatic API Failover
Attempt another configured key when a request encounters a retryable API failure. Successful failover depends on key validity, model availability, and quota.

### ⚡ One-Click Windows Startup
Use the included batch files to prepare the local environment and launch the frontend and backend.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, JavaScript |
| Backend | Python, FastAPI |
| AI services | Google Gemini API |
| Knowledge retrieval | Document chunks and embeddings |
| Local deployment | Windows batch scripts |

## 🏗️ Architecture

```text
User
  |
  v
React Web Interface
  |
  v
FastAPI Backend
  |
  +---- Document Retrieval
  |       |
  |       v
  |   BIS Knowledge Base
  |   Documents, Chunks, Embeddings
  |
  +---- Gemini API Manager
          |
          +---- Configured API Key
          |
          +---- Alternative Key on Retryable Failure
  |
  v
Answer and Relevant Source Content
```

## 📂 Repository Structure

```text
BIS-Niriidesh/
├── START.bat
├── API_MANAGER.bat
├── README.md
├── .gitignore
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── api_key_manager.py
│   ├── ingest/
│   ├── retrieval/
│   └── services/
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   └── src/
└── data/
    ├── documents.json
    ├── chunks.json
    ├── embeddings.json
    └── BIS reference documents
```

*The exact files may differ slightly between versions.*

## 💻 Requirements

Before running the application, install:

- Windows 10 or Windows 11
- Python 3.10 or newer
- Node.js LTS with npm
- An internet connection for dependency installation and AI requests
- A Google Gemini API key for live AI functionality

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/api-keys).

## ⚙️ Installation and Setup

### 1. Download the project

Clone the repository:

```bash
git clone https://github.com/Lingeshwaran2906/BIS-Niriidesh.git
cd BIS-Niriidesh
```

Alternatively, download the repository ZIP and extract it.

### 2. Configure API keys

Run:

```bat
API_MANAGER.bat
```

Follow the on-screen instructions to add and test your Gemini API keys.

Keep API keys private. Never paste them into GitHub, screenshots, issue reports, or public discussions.

### 3. Start the application

Double-click:

```text
START.bat
```

The startup script is intended to prepare the environment and launch the frontend and backend.

Keep the server terminal windows open while using the application.

### 4. Open the application

| Service | Address |
|---|---|
| Web interface | http://127.0.0.1:5173 |
| Backend API | http://127.0.0.1:8000 |
| Interactive API documentation | http://127.0.0.1:8000/docs |

These addresses are available on the same computer while the corresponding services are running. They are not public demo links.

## 🧪 Evaluator Testing Guide

After launching the application, testers can try the following scenarios.

| Test | Example action | Expected behavior |
|---|---|---|
| Application startup | Run `START.bat` | Frontend and backend start, or an actionable error is shown |
| AI question answering | Ask a question about a bundled BIS document | A response is returned when the API and retrieval system are available |
| Source verification | Inspect references in an answer | Relevant document content can be checked |
| Gap analysis | Submit product information | The application analyzes it against available document content |
| API key validation | Test a configured key | The manager reports whether the tested API access works |
| API failover | Simulate a retryable failure with multiple keys configured | The backend attempts an alternative key when applicable |
| Error handling | Temporarily make the AI service unavailable | The application reports the failure instead of presenting it as a successful live answer |

Actual results depend on the current implementation, API access, quota, and available documents. Do not treat example or fallback responses as proof of a successful live Gemini request.

## 🔐 Security

- Do not commit `.env` files or API-key storage files.
- Exclude Python virtual environments and `node_modules`.
- Never embed private API keys in frontend source code.
- Review `.gitignore` before every commit.
- Revoke exposed keys immediately and replace them locally.
- Remember that multiple keys from the same Google Cloud project may share quota limits.

## 📚 Knowledge Base and Limitations

The application's answers depend on the documents and prepared retrieval data bundled with the repository.

The included documents do **not** represent the complete BIS standards catalogue. Retrieval may miss relevant clauses, and AI-generated responses may be incomplete or incorrect.

For compliance-critical decisions, consult the applicable official BIS publication and verify the current edition, amendments, and requirements.

Official website: [Bureau of Indian Standards](https://www.bis.gov.in/)

## 🛣️ Future Enhancements

- Expand the knowledge base with additional official BIS publications.
- Improve clause-level citations and retrieval accuracy.
- Track standards editions and amendments.
- Add multilingual assistance.
- Improve automated tests and evaluator demo workflows.
- Strengthen authentication, logging, and production deployment.
- Provide a hosted demo with clear separation between live AI and sample responses.

## 🤝 Contributing

Suggestions, bug reports, and contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Open a pull request describing the changes.

## ⚖️ Disclaimer

BIS Nirdesh is an independent prototype and is **not an official Bureau of Indian Standards product**. It is intended to assist users in exploring standards-related information and does not replace official publications, professional assessment, or formal certification procedures.

## 📄 License

A license has not yet been specified. Add an appropriate open-source license before authorizing public reuse, modification, or redistribution.

---

**BIS Nirdesh — Explore standards. Understand requirements. Build with confidence.**
