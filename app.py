from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- AI FUNCTION ---------------- #
def get_ai_recommendations(student_data):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        subjects = student_data.get("subjects", [])

        # Convert subjects into text
        subject_text = "\n".join([
            f"- {sub['name']}: {sub['pct']}%"
            for sub in subjects
        ])

        prompt = f"""
You are an academic advisor.

Student performance:
{subject_text}

Give ONLY 3–5 short improvement tips.

IMPORTANT:
- Return ONLY clean HTML
- Use <ul> and <li>
- No markdown, no **, no ###, no numbering
- Keep it short and practical

Example:
<ul>
<li>Revise basics daily</li>
<li>Practice coding problems</li>
<li>Focus on weak subjects</li>
</ul>
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text or fallback(student_data)

    except Exception as e:
        print("Gemini error:", e)
        return fallback(student_data)

# ---------------- FALLBACK ---------------- #
def fallback(student_data):
    subjects = student_data.get("subjects", [])

    tips = "<ul>"

    for sub in subjects:
        if sub["pct"] < 40:
            tips += f"<li><strong>{sub['name']}:</strong> Focus on basics and practice regularly.</li>"

    tips += """
    <li><strong>Daily Practice:</strong> Study at least 2 hours consistently.</li>
    <li><strong>Revision:</strong> Revise weak topics every day.</li>
    <li><strong>Mock Tests:</strong> Practice previous questions.</li>
    </ul>
    """

    return tips

# ---------------- ROUTE ---------------- #
@app.route('/generate-tips', methods=['POST'])
def generate_tips():
    data = request.json
    print("Incoming data:", data)

    try:
        recommendations = get_ai_recommendations(data)
        print("AI response:", recommendations)

        return jsonify({
            "success": True,
            "recommendations": recommendations
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        })

# ---------------- RUN ---------------- #
if __name__ == '__main__':
    app.run(debug=True)