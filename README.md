# AI Resume Analyzer

A Flask-based resume analysis application that reads a resume, compares it against a target job role, and uses Gemini to generate structured feedback such as skills, missing skills, roadmap, and interview questions.

## Features

- User signup and login
- Resume text input or PDF/DOCX upload
- AI-powered resume evaluation using Gemini
- Structured JSON output for analysis results
- Saved history of previous resume analyses per user
- Dashboard-style UI for review

## Tech Stack

- Python
- Flask
- SQLAlchemy
- SQLite
- Gemini API (Google Generative AI)
- PyPDF2 for PDF parsing
- python-docx for DOCX parsing

## Project Structure

```text
.
├── app.py                  # Root launcher for the Flask backend
├── backend/
│   ├── __init__.py
│   ├── app.py              # Main Flask app
│   ├── ai.py               # Gemini integration and resume analysis logic
│   ├── db.py               # Database setup
│   ├── models.py           # SQLAlchemy models
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── history.html
│       ├── login.html
│       └── signup.html
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (not committed)
├── .env.example            # Sample environment file
├── README.md
├── site.db                 # SQLite database file
└── .gitignore
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

Copy `.env.example` to `.env` and update the values:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
SECRET_KEY=your_secret_key_here
```

4. Run the application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## Usage

1. Sign up for a new account.
2. Log in.
3. Enter a target role or job goal.
4. Paste resume text or upload a PDF/DOCX resume.
5. Review the generated analysis.
6. View previous analyses in the history section.

## Gemini Model

The app is configured to use the active Gemini model:

```env
GEMINI_MODEL=gemini-3.6-flash
```

This avoids compatibility issues with older model names that are no longer available to new users.

## Notes

- The backend keeps the Gemini API key on the server side; it is not exposed to the frontend.
- The app stores the user data and previous resume reports in SQLite.
- `.env` should never be committed to version control.

## License

This project is for educational and personal use.
