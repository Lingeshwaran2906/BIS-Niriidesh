# \# 🇮🇳 BIS Nirdesh — AI-Powered BIS Standards Assistant

# 

# An AI-powered assistant designed to help users understand Indian Standards published by the \*\*Bureau of Indian Standards (BIS)\*\* through document-grounded question answering, source references, and product standards gap analysis.

# 

# \## 🚀 Overview

# 

# BIS Nirdesh aims to make standards-related information easier to understand and navigate. It combines a web interface, a Python backend, document retrieval, and Google's Gemini AI to answer questions based on the standards documents included in its knowledge base.

# 

# \## ✨ Features

# 

# \- \*\*AI-Powered Q\&A:\*\* Ask questions about the BIS documents available in the project.

# \- \*\*Document-Grounded Answers:\*\* Retrieve relevant passages from the prepared knowledge base to support responses.

# \- \*\*Source References:\*\* Help users trace answers back to relevant document content.

# \- \*\*Product Gap Analysis:\*\* Explore potential gaps between product information and applicable requirements represented in the available documents.

# \- \*\*Gemini API Integration:\*\* Uses Google Gemini for AI-powered responses and embeddings.

# \- \*\*Multi-API Key Management:\*\* Configure and test multiple Gemini API keys locally.

# \- \*\*Automatic API Failover:\*\* Attempts other configured keys when a request fails with a retryable API error.

# \- \*\*One-Click Startup:\*\* Use `START.bat` to prepare the environment and launch the application on Windows.

# \- \*\*Separate API Manager:\*\* Use `API\_MANAGER.bat` to manage API keys without editing source code.

# 

# \## 🛠️ Technology Stack

# 

# | Component | Technology |

# |---|---|

# | Frontend | React and Vite |

# | Backend | Python and FastAPI |

# | AI | Google Gemini API |

# | Document processing | Python-based ingestion and retrieval |

# | Local development | Windows batch scripts |

# 

# \## 📁 Project Structure

# 

# ```text

# bis-nirdesh-main/

# ├── START.bat

# ├── API\_MANAGER.bat

# ├── RUN\_BACKEND.bat

# ├── RUN\_FRONTEND.bat

# ├── backend/

# │   ├── main.py

# │   ├── requirements.txt

# │   ├── ingest/

# │   └── ...

# ├── frontend/

# │   ├── package.json

# │   └── ...

# ├── data/

# │   └── ...

# ├── .gitignore

# └── README.md

# ```

# 

# \*The exact files and folders may vary slightly by project version.\*

# 

# \## ⚙️ Prerequisites

# 

# Install the following before running the application:

# 

# \- Windows 10 or Windows 11

# \- Python 3.10 or newer

# \- Node.js LTS and npm

# \- Git (optional, for cloning the repository)

# \- A Google Gemini API key from \[Google AI Studio](https://aistudio.google.com/app/api-keys)

# 

# An internet connection is required for dependency installation and Gemini API requests.

# 

# \## ▶️ Installation and Setup

# 

# \### 1. Download the project

# 

# Clone the repository:

# 

# ```bash

# git clone https://github.com/YOUR-USERNAME/BIS-Nirdesh.git

# cd BIS-Nirdesh

# ```

# 

# Alternatively, download the ZIP from GitHub and extract it.

# 

# \### 2. Configure Gemini API keys

# 

# Run:

# 

# ```bat

# API\_MANAGER.bat

# ```

# 

# Follow the menu to add and test your API keys. Add more than one key if you want the application to have alternatives available during API failures.

# 

# \*\*Security:\*\* API keys must remain local. Never commit API keys, `.env` files, or local API-key storage files to GitHub.

# 

# \### 3. Start the application

# 

# Double-click:

# 

# ```text

# START.bat

# ```

# 

# The startup script is intended to prepare the local environment, install required dependencies, and launch the backend and frontend.

# 

# Keep the backend and frontend terminal windows open while using the application.

# 

# \### 4. Open the application

# 

# | Service | Local address |

# |---|---|

# | Web application | http://127.0.0.1:5173 |

# | Backend API | http://127.0.0.1:8000 |

# | Interactive API documentation | http://127.0.0.1:8000/docs |

# 

# If the application does not start, read the error displayed in the relevant terminal window.

# 

# \## 🔑 API Key Failover

# 

# BIS Nirdesh supports configuring multiple Gemini API keys through its local API manager.

# 

# The intended workflow is:

# 

# 1\. Add API keys locally.

# 2\. Test key and model access.

# 3\. Make API requests through the backend.

# 4\. Try another configured key when a request encounters a retryable failure.

# 

# Failover cannot guarantee success if every key is invalid, the service is unavailable, or all keys share the same exhausted quota. Multiple keys belonging to the same Google Cloud project may share quota limits.

# 

# \## 📚 Knowledge Base

# 

# The assistant uses the documents and prepared retrieval data bundled with the project. Its answers are limited by the coverage, accuracy, and version of those documents.

# 

# The bundled knowledge base should not be treated as a complete catalogue of all BIS standards.

# 

# For compliance-critical decisions, consult the applicable official BIS publication and verify the current edition, amendments, and requirements.

# 

# Official website: \[Bureau of Indian Standards](https://www.bis.gov.in/)

# 

# \## 🔒 Security

# 

# Before pushing this project to GitHub, verify that:

# 

# \- `.env` files are excluded from Git.

# \- API-key storage files are excluded from Git.

# \- Python virtual environments are excluded.

# \- `node\_modules` is excluded.

# \- Local databases and logs containing private information are excluded.

# \- No API keys or other credentials appear in source code, README files, screenshots, or commit history.

# 

# A `.gitignore` file helps prevent accidental commits but does not remove secrets that have already been committed.

# 

# \## 🧪 Testing

# 

# After startup, verify the following:

# 

# \- The frontend opens successfully.

# \- The backend API documentation is accessible.

# \- Gemini API requests return responses.

# \- The assistant answers questions using available document content.

# \- Source references are relevant to the answer.

# \- The API manager handles invalid keys and temporary API failures appropriately.

# \- The application displays useful errors when the backend or AI service is unavailable.

# 

# \## 🗺️ Future Improvements

# 

# \- Expand the knowledge base with additional official BIS standards.

# \- Improve clause-level retrieval and citation accuracy.

# \- Add standards edition and amendment tracking.

# \- Improve multilingual support.

# \- Add robust conversation history and document search.

# \- Add automated tests and production deployment configuration.

# \- Strengthen authentication, rate limiting, and access control before public deployment.

# 

# \## 🤝 Contributing

# 

# Contributions, bug reports, and feature suggestions are welcome.

# 

# 1\. Fork the repository.

# 2\. Create a feature branch.

# 3\. Make and test your changes.

# 4\. Submit a pull request with a clear description.

# 

# \## ⚠️ Disclaimer

# 

# BIS Nirdesh is an independent software project intended to assist users in exploring and understanding standards-related information. It is not an official BIS product and is not a substitute for the applicable official standards or professional compliance assessment.

# 

# \## 📄 License

# 

# No license has been specified yet. Add an appropriate open-source license before permitting others to reuse, modify, or redistribute the project.

# 

# \---

# 

# \*\*Built to make Indian Standards easier to explore, understand, and use.\*\*

