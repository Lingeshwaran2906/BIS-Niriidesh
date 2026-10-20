# BIS Nirdesh

A local AI assistant for exploring the included BIS product manuals.

## Current architecture
- Frontend: React + Vite (`frontend/`)
- Backend: FastAPI + Uvicorn (`backend/`)
- AI: Google Gemini API (`GEMINI_API_KEY` in `backend/.env`)
- Retrieval: precomputed JSON chunks and embeddings (`data/`)
- Accounts: local SQLite database created at `data/users.db`

## Safety and answer quality
- Answers must be grounded only in supplied BIS document chunks.
- Show the IS number, page, clause reference when available, and supporting quote.
- If the available documents do not support an answer, say so rather than guessing.
- Keep API keys and JWT secrets in `backend/.env`; never commit secrets.
- Treat the bundled manuals as the limited current knowledge base, not the complete BIS catalogue.
- This is guidance software, not an official BIS certification decision.

## Windows startup
1. Run `START.bat`.
2. On first launch, follow the Gemini API setup prompt.
3. Keep the backend and frontend terminal windows open while using the app.
