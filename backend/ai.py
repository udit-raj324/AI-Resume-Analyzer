import json
import os
import re

import google.generativeai as genai

client = None


def get_gemini_model():
    global client
    if client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Set it in the backend environment before running the app.")

        model_name = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
        genai.configure(api_key=api_key)
        client = genai.GenerativeModel(model_name)
    return client


def analyze_resume(resume_text, user_goal):
    prompt = f"""
    You are an experienced hiring manager reviewing resumes for a technical role.
    Evaluate the resume based on the user's goal.
    user goal: "{user_goal}"

    Return only valid JSON with the following structure:
    {{
      "skills": [],
      "missing_skills": [],
      "roadmap": [],
      "interview_question": []
    }}

    Resume:
    {resume_text}
    """
    try:
        model = get_gemini_model()
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.0}
        )

        content = getattr(response, "text", "")
        if not content:
            raise ValueError("Empty response from Gemini API")

        content = content.strip()
        content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"\s*```$", "", content, flags=re.IGNORECASE)

        start = content.find("{")
        end = content.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("Unable to parse JSON from model response")

        return json.loads(content[start:end])

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_question": [],
            "error": str(e)
        }

