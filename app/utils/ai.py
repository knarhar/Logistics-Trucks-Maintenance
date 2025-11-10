import json
import re

def extract_json(text: str):
    """Extracts JSON from AI response, removing markdown."""
    # Gets first valid array in text
    match = re.search(r"\[\s*(?:\{.*?\}\s*,?\s*)+\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return []
    return []
