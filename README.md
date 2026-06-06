# EduLens — Course Content Simplification Agent

> AI-powered educational content simplifier built with **IBM Granite** via **IBM Watsonx.ai**.

Paste any textbook excerpt, lecture note, or research paragraph and get a personalised explanation — from Beginner-friendly to Expert-grade — in seconds.

---

## Features

| Feature | Description |
|---|---|
| **Content Input** | Paste up to 8,000 characters of any educational material |
| **Proficiency Levels** | Beginner · Intermediate · Advanced · Expert |
| **Complexity Analysis** | Estimated reading difficulty, complexity descriptor |
| **Key Concept Extraction** | Up to 6 domain concepts identified |
| **Side-by-Side View** | Original vs Simplified content displayed together |
| **Copy Button** | One-click copy for both panels |

---

## Screenshots

> *(Add screenshots here after running the app)*

| Home / Hero | Simplification Interface | Results View |
|---|---|---|
| `screenshot-hero.png` | `screenshot-input.png` | `screenshot-results.png` |

---

## Project Structure

```
course-content-simplifier/
│
├── app.py                  # Flask application & routes
├── config.py               # IBM credentials (edit this file)
├── requirements.txt        # Python dependencies
├── README.md
│
├── static/
│   ├── style.css           # Dark editorial UI theme
│   └── script.js           # Frontend logic
│
├── templates/
│   └── index.html          # Single-page application template
│
└── services/
    ├── __init__.py
    └── granite_service.py  # IBM Watsonx.ai + Granite integration
```

---

## Prerequisites

- Python 3.9 or later
- An **IBM Cloud** account (free Lite tier works)
- A **Watsonx.ai** project with IBM Granite access

---

## IBM Cloud Setup

1. Sign up or log in at [https://cloud.ibm.com](https://cloud.ibm.com)
2. Navigate to **Watsonx.ai** and create a new project (or open an existing one).
3. Note your **Project ID** from *Manage → General → Project ID*.
4. Generate an **API Key** at *Manage → Access (IAM) → API Keys → Create*.
5. Note the **endpoint URL** for your region:

| Region | Endpoint |
|---|---|
| US South | `https://us-south.ml.cloud.ibm.com` |
| EU Germany | `https://eu-de.ml.cloud.ibm.com` |
| EU UK | `https://eu-gb.ml.cloud.ibm.com` |
| Tokyo | `https://jp-tok.ml.cloud.ibm.com` |

---

## Installation & Setup

### 1. Clone / Download the Project

```bash
# If cloning from Git
git clone <your-repo-url>
cd course-content-simplifier
```

### 2. Create a Virtual Environment

**Windows**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add IBM Credentials

Open **`config.py`** and replace the three placeholder values:

```python
PROJECT_ID   = "your-actual-project-id"
API_KEY      = "your-actual-api-key"
ENDPOINT_URL = "https://us-south.ml.cloud.ibm.com"   # or your region
```

> ⚠️  Never commit real credentials to version control. Add `config.py` to `.gitignore`.

### 5. Run the Flask Application

```bash
python app.py
```

Then open your browser at: **[http://localhost:5000](http://localhost:5000)**

---

## Usage

1. **Paste** your educational content into the large text area.
2. **Select** a proficiency level from the dropdown.
3. **Click** *Simplify with Granite* (or press `Ctrl + Enter`).
4. View the **complexity analysis** chips and **side-by-side** output.
5. **Copy** either panel with the copy button.

---

## API Endpoints

| Method | URL | Description |
|---|---|---|
| `GET` | `/` | Serve the web application |
| `POST` | `/api/simplify` | Simplify content via IBM Granite |
| `GET` | `/api/health` | Health check & credential status |

### POST `/api/simplify` — Request Body

```json
{
  "content": "Your educational text here...",
  "level": "beginner"
}
```

### POST `/api/simplify` — Response

```json
{
  "success": true,
  "data": {
    "difficulty": "Hard",
    "complexity_level": "Undergraduate academic text",
    "concepts": ["Photosynthesis", "Chlorophyll", "ATP", "Light reactions"],
    "simplified_text": "..."
  }
}
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `503 credentials not configured` | Open `config.py` and replace placeholder strings |
| `401 Unauthorized` | Check that `API_KEY` is correct and not expired |
| `404 model not found` | Verify `MODEL_ID` in `config.py` matches an enabled model in your project |
| `Connection timeout` | Check `ENDPOINT_URL` matches your IBM Cloud region |

---

## Future Enhancements

- 🌍 **Multi-language support** — Simplify and output in languages other than English
- 📄 **File upload** — Accept PDF and DOCX files directly
- 🔊 **Text-to-speech** — Read the simplified output aloud
- 💾 **History panel** — Save and revisit previous simplifications (browser localStorage)
- 📊 **Readability metrics** — Flesch-Kincaid score, word count delta
- 🤝 **Classroom mode** — Batch-simplify multiple paragraphs at once
- 🖼️ **Diagram generation** — Auto-generate concept diagrams via IBM Watson services
- 🔗 **LMS integration** — Export directly to Moodle / Canvas

---

## License

MIT — Free to use and modify for educational purposes.
