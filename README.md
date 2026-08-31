# AI Resume Analyzer

A Flask-based resume analysis application that reads a resume, compares it against a target job role, and uses Gemini to generate structured feedback such as skills, missing skills, roadmap, and interview questions.

## Features

- User signup and login with secure password hashing (`scrypt`)
- Resume text input or PDF/DOCX upload
- AI-powered resume evaluation using Gemini
- Structured JSON output for analysis results
- Saved history of previous resume analyses per user
- Dashboard-style UI for review
- **Cloud-ready:** Pre-configured for deployment on Vercel with PostgreSQL.

## Screenshots

### Dashboard Input
![Dashboard Input](assets/img_1.png)

### AI Analysis Result
![Analysis Result](assets/img_2.png)

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL (via Neon) & SQLAlchemy ORM
- **AI Integration:** Gemini API (Google Generative AI)
- **Document Parsing:** PyPDF2 (PDF), python-docx (DOCX)
- **Deployment:** Vercel

## Project Structure

```text
.
├── app.py                  # Root launcher for the Flask backend
├── backend/
│   ├── __init__.py
│   ├── app.py              # Main Flask app
│   ├── ai.py               # Gemini integration and resume analysis logic
│   ├── db.py               # Database setup and PostgreSQL connection
│   ├── models.py           # SQLAlchemy models (User, Report)
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── history.html
│       ├── login.html
│       └── signup.html
├── requirements.txt        # Python dependencies (includes psycopg for Postgres)
├── vercel.json             # Vercel deployment configuration (if applicable)
├── .env                    # Local environment variables (not committed)
├── .env.example            # Sample environment file
├── README.md
└── .gitignore
```

## Setup & Local Development

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

Copy `.env.example` to `.env` and update the values. You will need a PostgreSQL connection string (you can get a free one from [Neon.tech](https://neon.tech/)):

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@endpoint.neon.tech/dbname?sslmode=require
```

4. Run the application:

```bash
python app.py
```

Then open: `http://127.0.0.1:5000/`

## Deployment (Vercel)

This app is optimized for serverless deployment on Vercel. 
1. Push your code to a GitHub repository.
2. Import the project into Vercel.
3. In the Vercel Dashboard, go to **Settings > Environment Variables** and add your `GEMINI_API_KEY`, `GEMINI_MODEL`, `SECRET_KEY`, and `DATABASE_URL`.
4. Ensure **Vercel Authentication / Deployment Protection** is turned OFF if you want the app to be publicly accessible on any device.

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

This avoids compatibility issues with older model names that are no longer available to new users. If you encounter rate limits on the free tier, wait ~60 seconds for the quota to reset.

## Notes

- The backend keeps the Gemini API key on the server side; it is not exposed to the frontend.
- The app stores user data and previous resume reports in a PostgreSQL database using the `psycopg` driver.
- `.env` should never be committed to version control.

## License

This project is for educational and personal use.