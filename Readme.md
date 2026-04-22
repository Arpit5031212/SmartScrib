smartscribe/
│
├── backend/
│   ├── agents/
│   │   ├── intent_classifier.py       # Classifies user input into NEW/QUERY/FOLLOWUP/UPDATE
│   │   ├── clarification_agent.py     # Asks follow-up questions, fills required fields
│   │   ├── planner_agent.py           # Decides tool call sequence
│   │   └── response_builder.py        # Formats final response to user
│   │
│   ├── tools/
│   │   ├── create_doc.py              # Generates .docx using python-docx
│   │   ├── create_excel.py            # Generates .xlsx using openpyxl
│   │   ├── create_pdf.py              # Generates .pdf using reportlab
│   │   ├── update_artifact.py         # Appends or edits existing files
│   │   └── tool_registry.py           # Registers all tools for LangChain agent
│   │
│   ├── rag/
│   │   ├── indexer.py                 # Chunks + embeds + stores artifacts
│   │   ├── retriever.py               # Queries vector store, returns relevant chunks
│   │   └── vector_store.py            # ChromaDB setup and config
│   │
│   ├── memory/
│   │   ├── session_memory.py          # Tracks clarification state within a session
│   │   └── artifact_metadata.py       # SQLite index of all generated files + tags
│   │
│   ├── schemas/
│   │   ├── journal_schema.py          # Required fields for journal mode
│   │   ├── timesheet_schema.py        # Required fields for timesheet mode
│   │   ├── meeting_schema.py          # Required fields for meeting mode
│   │   └── rewrite_schema.py          # Required fields for general rewrite
│   │
│   ├── storage/
│   │   └── artifacts/                 # Generated files saved here, organized by date
│   │
│   ├── api/
│   │   ├── chat.py                    # POST /chat — main conversation endpoint
│   │   ├── artifacts.py               # GET /artifacts — list saved files
│   │   └── download.py                # GET /download/:id — download a file
│   │
│   └── main.py                        # FastAPI app entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx         # Main chat interface
│   │   │   ├── MessageBubble.jsx      # Individual message, supports file previews
│   │   │   ├── ArtifactSidebar.jsx    # Lists saved files with download buttons
│   │   │   ├── ModeSelector.jsx       # Optional: lets user pre-select a mode
│   │   │   └── FilePreview.jsx        # Preview doc/pdf/excel inline
│   │   │
│   │   ├── hooks/
│   │   │   ├── useChat.js             # Chat state and API calls
│   │   │   └── useArtifacts.js        # Artifact list fetching
│   │   │
│   │   ├── services/
│   │   │   └── api.js                 # Axios config, all API calls
│   │   │
│   │   └── App.jsx
│   │
│   └── package.json
│
├── docker-compose.yml
└── README.md