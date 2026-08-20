import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
        "Add it to your backend/.env file."
    )

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_PROMPT = """
You are the inventory extraction engine for TownKart.

Extract information from a shopkeeper's WhatsApp message.

Extract:

- product
- price
- quantity
- unit

Example:

Input:
"Jasmine 320 15 bundles"

Output:
{
    "product": "jasmine",
    "price": 320,
    "quantity": 15,
    "unit": "bundle"
}

Rules:

- do not invent missing values
- price must be a number or null
- quantity must be a number or null
- unit must be a string or null
- return ONLY valid JSON
"""


def parse_merchant_message(message: str):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
        ),
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid JSON: {response.text}"
        ) from e