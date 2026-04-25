import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_batch_summaries(incidents):
    # Build prompt with numbered incidents
    prompt = "You are a road safety AI.\n\n"

    for i, inc in enumerate(incidents):
        prompt += f"""
Incident {i+1}:
Distance: {inc['distance_m']} m
Velocity: {inc['relative_velocity']} m/s
TTC: {inc['ttc_seconds']} s
Risk: {inc['risk_level']}
"""

    prompt += """
For each incident, return a short 1-line explanation.
Respond as a numbered list:
1. ...
2. ...
3. ...
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Split into lines safely
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    summaries = []
    for line in lines:
        if "." in line:
            summaries.append(line.split(".", 1)[1].strip())
        else:
            summaries.append(line)

    # Fallback if mismatch
    while len(summaries) < len(incidents):
        summaries.append("AI summary unavailable")

    return summaries[:len(incidents)]