"""
 AI mechanic suggestion endpoint
"""
import json, time, requests
from app.core.config import settings
from app.utils.ai import extract_json

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
    "Content-Type": "application/json",
}


def suggest_mechanics_ai(issue_type: str, description: str, mechanics: list, retries: int = settings.AI_MAX_RETRIES):
    """
    Sends a request to Groq API to suggest suitable mechanics.
    Retries up to `retries` times on failure.
    """
    system_prompt = """
            You are an assistant that matches truck issues with mechanics.
            You MUST return **a JSON array**.
            Each element must have exactly these fields:
            - first_name
            - last_name
            - expertise
            - confidence_score (1.0 - 0.0)
            
            
            Sort the results by confidence_score from highest to lowest.            
            Do NOT nest mechanic inside another object. 
            Do NOT add explanations or text outside the JSON.
        """

    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (system_prompt),
            },
            {
                "role": "user",
                "content": json.dumps({
                    "issue_type": issue_type,
                    "description": description,
                    "mechanics": [
                        {
                            "fist_name": mechanic.first_name,
                            "last_name": mechanic.last_name,
                            "expertise": mechanic.expertise
                        }
                        for mechanic in mechanics
                    ]
                })
            }
        ],
        "temperature": 0.2
    }

    for attempt in range(retries):
        try:
            response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload, timeout=15)

            # Retry on rate limit or server errors
            if response.status_code in (429, 500, 502, 503, 504):
                if attempt < retries - 1:
                    time.sleep(settings.AI_RETRY_DELAY)
                    continue
                return []

            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            try:
                parsed = extract_json(content)
                if isinstance(parsed, list):
                    parsed.sort(key=lambda x: x["confidence_score"], reverse=True)
                    return parsed
                else:
                    if attempt < retries - 1:
                        time.sleep(settings.AI_RETRY_DELAY)
                        continue
                    return []
            except json.JSONDecodeError:
                if attempt < retries - 1:
                    time.sleep(settings.AI_RETRY_DELAY)
                    continue
                return []

        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(settings.AI_RETRY_DELAY)
                continue
            return []
    return []
