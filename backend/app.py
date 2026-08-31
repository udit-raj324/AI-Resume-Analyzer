from pathlib import Path

from flask import Flask, render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

from backend.db import Base, engine, SessionLocal
import backend.models as models
from backend.ai import analyze_resume
import PyPDF2
import docx
import json
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# Flask app setup with explicit template folder
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))
app.secret_key = os.environ.get("SECRET_KEY", "development-secret")

# Create database tables
Base.metadata.create_all(bind=engine)

# HOME
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    with SessionLocal() as db:
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            if not email or not password:
                return render_template("signup.html", error="Email and password are required.")

            existing_user = db.query(models.User).filter_by(email=email).first()
            if existing_user:
                return render_template("signup.html", error="User already exists.")

            hashed_password = generate_password_hash(password)
            user = models.User(email=email)
            user.password = hashed_password
            db.add(user)
            db.commit()
            return redirect("/login")

        return render_template("signup.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    with SessionLocal() as db:
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            if not email or not password:
                return render_template("login.html", error="Email and password are required.")

            user = db.query(models.User).filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session["user"] = user.email
                return redirect("/dashboard")

            return render_template("login.html", error="Invalid credentials.")

        return render_template("login.html")


# DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    result = None
    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")
        file = request.files.get("file")

        if file and file.filename != "":
            filename = file.filename.lower()
            if filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    resume_text = text
                except Exception as e:
                    result = {"error": f"PDF error: {str(e)}"}

            elif filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text = text
                except Exception as e:
                    result = {"error": f"Docx error: {str(e)}"}
            else:
                result = {"error": "Unsupported file format. Please upload a PDF or DOCX file."}

        if resume_text and user_goal and not (isinstance(result, dict) and result.get("error")):
            try:
                result = analyze_resume(resume_text, user_goal)

                with SessionLocal() as db:
                    user = db.query(models.User).filter_by(email=session["user"]).first()
                    if user is None:
                        return redirect("/login")

                    report = models.Report(
                        user_id=user.id,
                        resume_text=resume_text,
                        result=json.dumps(result)
                    )
                    db.add(report)
                    db.commit()

            except Exception as e:
                result = {"error": f"AI error: {str(e)}"}

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )

# HISTORY
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    with SessionLocal() as db:
        user = db.query(models.User).filter_by(email=session["user"]).first()
        if user is None:
            return redirect("/login")

        reports = db.query(models.Report).filter_by(user_id=user.id).all()

        parsed_reports = []
        for r in reports:
            try:
                parsed_result = json.loads(r.result)
            except json.JSONDecodeError:
                parsed_result = []
            parsed_reports.append({
                "resume": r.resume_text,
                "result": parsed_result
            })

    return render_template("history.html", reports=parsed_reports)

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    print("Template folder path:", os.path.abspath(app.template_folder))
    app.run(debug=True)
