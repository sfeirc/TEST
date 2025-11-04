# Infotel RFP Summarizer Backend

FastAPI backend service for summarizing RFPs using AI.

## Features

- 📄 **File Upload Support**: PDF, DOCX, TXT
- 🔗 **SharePoint Integration**: Direct link support
- 🤖 **AI-Powered Summarization**: Azure OpenAI / OpenAI
- 📊 **Structured Output**: Executive summary, requirements, risks, timeline, next steps

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Model configuration (used across all services):**
```env
MODEL=gpt-5
```

**Minimum required configuration (Azure OpenAI):**
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-5
```

**OR using OpenAI:**
```env
OPENAI_API_KEY=sk-your-key-here
```

**Optional - SharePoint support:**
```env
SHAREPOINT_CLIENT_ID=your-app-id
SHAREPOINT_CLIENT_SECRET=your-secret
SHAREPOINT_TENANT_ID=your-tenant-id
```

### 3. Run the Server

```bash
python main.py
```

Server will start on `http://localhost:3001`

## Usage

### API Endpoint

**POST /summarizeRfp**

Accepts three input methods:

1. **File Upload**
```bash
curl -X POST http://localhost:3001/summarizeRfp \
  -F "file=@rfp_document.pdf"
```

2. **SharePoint Link**
```bash
curl -X POST http://localhost:3001/summarizeRfp \
  -F "rfpText=https://contoso.sharepoint.com/sites/MySite/Documents/RFP.pdf"
```

3. **Direct Text**
```bash
curl -X POST http://localhost:3001/summarizeRfp \
  -F "rfpText=Full RFP content here..."
```

### Response Format

```json
{
  "executive_summary": [
    "High-level point 1",
    "High-level point 2"
  ],
  "requirements": [
    "Customer requirement 1",
    "Customer requirement 2"
  ],
  "risks": [
    "Risk 1: SLA penalties",
    "Risk 2: IP transfer clause"
  ],
  "timeline": [
    "Proposal due: 2024-03-15",
    "Project start: 2024-04-01"
  ],
  "next_steps": [
    "Clarify licensing requirements",
    "Assess resource availability"
  ]
}
```

## Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── services/
│   ├── file_extractor.py   # File text extraction (PDF, DOCX, TXT)
│   ├── sharepoint_extractor.py  # SharePoint integration
│   └── ai_summarizer.py    # AI summarization logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md
```

## Development

### Auto-reload during development

```bash
uvicorn main:app --reload --port 3001
```

### API Documentation

Once running, visit:
- Swagger UI: http://localhost:3001/docs
- ReDoc: http://localhost:3001/redoc

## Troubleshooting

**SharePoint authentication errors:**
- Ensure your app registration has the correct permissions
- Verify client ID and secret are correct
- Check that the SharePoint site is accessible

**File parsing errors:**
- Ensure file is not password-protected
- Check file is not corrupted
- Verify file format is supported

**AI service errors:**
- Verify API key is valid
- Check Azure OpenAI deployment name matches
- Ensure you have sufficient quota/credits

