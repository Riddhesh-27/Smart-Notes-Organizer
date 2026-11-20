# Smart Notes Organizer 📝
> **Turn scattered notes into structured knowledge using Google Gemini.**

Final Year Mini-Project for Generative AI (Project 48).

---

## 📌 Problem Statement

Notes taken during lectures, study sessions, team meetings, or research are often fragmented, disorganized, and scattered across multiple topics. Manually reading, sorting, grouping, and formatting these unstructured notes is time-consuming and error-prone.

**Smart Notes Organizer** solves this problem by using Google's state-of-the-art Gemini Flash LLM to:
- Ingest raw, multi-topic, unorganized notes.
- Automatically identify semantic relationships and conceptual clusters.
- Generate meaningful, descriptive section headings.
- Cleanly convert points into readable Markdown bullet points.
- Remove duplicate information without losing important facts.
- Produce an exportable, presentation-ready study guide or summary.

---

## 🎯 Project Objectives

1. **Semantic Clustering**: Group notes by actual meaning rather than keyword matching.
2. **Visual Sticky Notes Board**: Render each clustered category inside its own distinct, vibrant sticky note card with soft shadows, pins, and custom accents.
3. **Dual View Options**: Provide both a colorful **Sticky Notes Board** and a standard **Document Preview** tab.
4. **Context Preservation**: Retain all factual information, definitions, and action items without hallucination.
5. **Clean Presentation**: Render structured Markdown directly in an intuitive, responsive Streamlit dashboard.
6. **Export & Portability**: Provide one-click downloading (`.md` file) and raw Markdown viewing/copying.
7. **Secure Configuration**: Strictly isolate secrets via `.env` and `.gitignore`.

---

## 🛠️ Technology Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **LLM / AI**: Google Gemini Flash (`gemini-2.5-flash`, `gemini-flash-latest`, `gemini-1.5-flash`)
- **SDK & API**: `google-genai` Python SDK with automated resilient fallback to Google Generative Language REST API
- **Environment Management**: `python-dotenv`
- **Language**: Python 3.10+

---

## 📂 Project Folder Structure

```
smart-notes-organizer/
│
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Project dependencies
├── .env                        # Private API configuration (ignored by Git)
├── .env.example                # Template for environment configuration
├── .gitignore                  # Git exclusions for secrets and venv
├── README.md                   # Comprehensive documentation
│
├── utils/
│   ├── __init__.py             # Package init
│   └── gemini_handler.py       # Gemini API client, fallbacks, & error handling
│
├── prompts/
│   └── system_prompt.py        # Carefully engineered system instructions
│
└── sample_data/
    └── sample_notes.txt        # Multi-topic sample test dataset
```

---

## 🚀 Setup and Installation

### 1. Clone or Open the Repository
```bash
cd smart-notes-organizer
```

### 2. (Optional) Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration

1. Get your free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
2. Duplicate `.env.example` to create your `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and paste your API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
4. **Security Notice**: Never commit `.env` to GitHub. It is protected by `.gitignore`.

---

## ▶️ Running the Application

Launch the Streamlit web dashboard:
```bash
streamlit run app.py
```

The application will automatically open in your default browser at:
`http://localhost:8501`

---

## 📋 Sample Input and Expected Output

### Sample Input (Mixed Unorganized Notes)
```text
Python is a high-level programming language.
Supervised learning uses labelled datasets.
SQL is used to manage relational databases.
Complete the project documentation.

Python supports object-oriented programming.
Regression predicts continuous values.
Primary keys uniquely identify records.
Prepare the final presentation.

Lists are mutable in Python.
Classification predicts categories.
Foreign keys establish relationships between tables.
Test the application before submission.
```

### Expected Output (Organized by Gemini)
```markdown
## Python Programming
* High-level programming language supporting object-oriented programming.
* Lists are mutable data structures.
* Dictionaries store information as key-value pairs.

## Machine Learning
* Supervised learning models train on labelled datasets.
* Regression algorithms predict continuous numerical values.
* Classification algorithms predict discrete categories.
* Decision trees can perform both classification and regression tasks.

## Database Management
* SQL is the standard language for relational databases.
* Primary keys uniquely identify every record in a table.
* Foreign keys establish relational links between distinct tables.
* Normalization minimizes data redundancy across schemas.

## Project Management & Next Steps
* Complete the project documentation.
* Prepare the final presentation slides.
* Thoroughly test the application before submission.
* Submit the final project deliverables prior to the deadline.
```

---

## 🧪 Testing Checklist

- [x] **Sample Dataset Loading**: Click `📂 Load Sample Notes` to populate diverse test topics.
- [x] **Gemini Semantic Clustering**: Successfully categorizes mixed notes into clean topic groups.
- [x] **Input Validation**: Displays a warning if organizing empty notes.
- [x] **Missing API Key Handling**: Prompts user with friendly banner if `.env` is unconfigured.
- [x] **Download Functionality**: Generates a downloadable `organized_notes.md` file.
- [x] **Reorganize Feature**: Re-runs the model with one click.
- [x] **Reset / Clear**: Clears all inputs and outputs for fresh use.

---

## 🎓 Viva & Demonstration Guide

1. **How does semantic clustering work in this project?**
   - The user's input notes and a specialized system prompt are sent to the Gemini Flash model. The LLM evaluates semantic embeddings and contextual relationships across lines, creates distinct topic boundaries, and structures output in Markdown bullet points.
2. **Why Gemini Flash?**
   - Gemini Flash offers sub-second latency, low token cost, high contextual accuracy, and built-in system instruction support.
3. **How is prompt injection or override prevented?**
   - System instructions and user notes are isolated in separate API request payloads (`system_instruction` vs `contents`), preventing user notes from altering organizational rules.
