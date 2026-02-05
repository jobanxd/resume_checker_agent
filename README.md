# Resume Analyzer API

AI-powered resume analysis system that matches resumes against job descriptions using LangGraph and OpenAI.

## Overview

This application uses a multi-agent workflow to analyze resumes, extract keywords, and provide match scores with actionable recommendations. Built with FastAPI, LangGraph, and OpenAI's GPT models.

## How to Run

### Prerequisites

1. **Python 3.8+** installed
2. **OpenAI API Key** - Set up your environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Method 1: API Server with Swagger UI

1. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

2. **Access Swagger UI**: Open your browser to `http://localhost:8000/docs`

3. **Test the API**:
   - Navigate to the `POST /api/v1/resume-analyzer/analyze` endpoint
   - Click "Try it out"
   - Input your payload (see example below)
   - Click "Execute"

### Method 2: CLI Tool

The CLI automatically starts the server, sends the request, and displays results.

1. **Prepare your payload**: Edit `data/payload.json` with your resume and job description

2. **Run the CLI**:
   ```bash
   python cli.py
   ```

3. **Results**: Output is displayed in the terminal and saved to `data/results.json`

## Example Input and Output

### Input (`data/payload.json`)

```json
{
  "resume_text": "Seth Jovan Pacturanan... AI/ML Computational Science Analyst... LangChain, LangGraph, multi-agent systems...",
  "job_description": "Senior AI/ML Engineer - Agentic Systems... LangChain and LangGraph... multi-agent architectures..."
}
```

### Output (`data/results.json`)

```json
{
  "success": true,
  "match_score": 0.85,
  "matched_keywords": [
    "LangChain", "LangGraph", "multi-agent systems", "RAG solutions",
    "vector databases", "FastAPI", "OpenAI", "GCP", "AWS"
  ],
  "missing_keywords": [
    "enterprise applications", "scalable AI solutions",
    "cross-functional teams"
  ],
  "recommendations": [
    "Add explicit experience with production-grade agentic AI systems",
    "Highlight experience with scalable AI solutions",
    "Include section on cross-functional team collaboration"
  ],
  "confidence_notes": "Strong match (85%). Excellent alignment with agentic AI...",
  "final_summary": "Overall Assessment: Strong and highly relevant skillset..."
}
```

## Scoring Logic

### Algorithm

The match score is calculated using a simple keyword matching algorithm:

```
match_score = (matched_keywords_count / target_keywords_count)
```

**Process**:
1. **Extraction Agent** extracts keywords from both resume and job description
2. **Analysis Scoring Agent** compares the two sets:
   - **Matched keywords**: Keywords present in both resume and target
   - **Missing keywords**: Keywords in target but not in resume
3. **Score calculation**: Ratio of matched to total target keywords (0.0 to 1.0)

### Scoring Interpretation

- **0.7 - 1.0**: Strong match - Excellent alignment with job requirements
- **0.4 - 0.7**: Moderate match - Good foundation with some gaps
- **0.0 - 0.4**: Weak match - Significant skill gaps

### Recommendations

The system generates 3-5 actionable recommendations prioritized by:
- **Critical missing keywords** (frequently mentioned in job description)
- **Skill categories** (e.g., if multiple DevOps tools are missing)
- **Impact on match score** (most important gaps first)

## Known Limitations

### 1. **LLM Extraction Variability**
- Keyword extraction depends on the LLM model's interpretation and training data
- Results may vary between different models or runs
- No standardized approach—relies entirely on the model's understanding

### 2. **No Standardized Skill Taxonomy**
- Lacks a predefined skill classification system or curated skills database
- Related technologies may be treated as separate (e.g., React.js vs ReactJS vs React)

### 3. **No Keyword Weighting**
- All keywords weighted equally regardless of importance
- Critical "must-have" skills not distinguished from "nice-to-have"
- Experience levels and seniority not factored into scoring

### 4. **Limited Context Analysis**
- Doesn't evaluate quality, depth, or recency of experience
- Project impact and achievements reduced to keyword presence only

### 5. **Binary Matching with Limited Semantic Understanding**
- Keywords are either matched or not—no partial credit or fuzzy matching
- Related skills treated independently (e.g., "Python" and "Django")
- Limited semantic similarity beyond basic synonym handling

### 6. **No Soft Skills Assessment** *(Intentional Design Choice)*
- Soft skills deliberately excluded—focus is purely on technical skills
- Cultural fit and interpersonal abilities not evaluated

## Quality Improvements Implemented

To address common edge cases, the system includes:

✅ **Case-Insensitive Matching**: "Python", "python", "PYTHON" treated as same keyword
✅ **Synonym Recognition**: ML = Machine Learning, AWS = Amazon Web Services, K8s = Kubernetes
✅ **Special Character Preservation**: C++, C#, .NET, Node.js, Next.js properly handled
✅ **False Positive Prevention**: SQL not extracted from NoSQL/PostgreSQL/MySQL
✅ **No Hallucination**: Only skills explicitly mentioned in text are extracted
✅ **Messy Formatting Handling**: Extracts keywords from poorly formatted text, tables, bullet points
✅ **Version Number Normalization**: "Python 3.10" → "Python"
✅ **No ATS Jargon**: Avoids pass/fail language and ATS optimization terminology

## Project Structure

```
.
├── agents/              # Agent implementations
│   ├── extraction_agent.py
│   ├── analysis_scoring_agent.py
│   └── resume_analyzer_agent.py
├── graphs/              # LangGraph workflow
│   ├── state.py
│   └── workflow.py
├── data/                # Input/output examples
│   ├── payload.json
│   └── results.json
├── routers/             # FastAPI routes
├── services/            # Business logic
├── utils/               # Helpers (LLM, file parsing)
├── main.py              # FastAPI application
├── cli.py               # CLI tool
└── requirements.txt     # Dependencies
```

## API Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `POST /api/v1/resume-analyzer/analyze` - Analyze resume
- `GET /docs` - Interactive API documentation (Swagger UI)

## Future Improvements

- Semantic similarity matching using embeddings
- Keyword weighting based on job requirement priority
- Support for PDF/DOCX file uploads
- Experience level assessment (junior/mid/senior)
- Soft skills evaluation
- Industry-specific skill taxonomies
