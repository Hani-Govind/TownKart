import json
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are the query understanding engine for TownKart.

Convert a customer's natural-language shopping request into JSON.

Extract:

- product
- quantity
- budget_max
- location_required
- intent

Possible intents:
- cheapest
- nearest
- best_match
- highest_availability

Rules:
- quantity must be a number or null
- budget_max must be a number or null
- location_required must be true if the user wants something nearby
- intent should be "best_match" unless a preference is clearly expressed
- do not invent missing information
- return ONLY valid JSON
"""

def parse_customer_query(query: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)
