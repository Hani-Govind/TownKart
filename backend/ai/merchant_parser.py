import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """
You are the inventory extraction engine for TownKart.

Extract from a shopkeeper's WhatsApp message:

- product
- price
- quantity
- unit

Example:
"Jasmine 320 15 bundles"

Return:
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
        model="gemini-2.5-flash",
        contents=message,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
        },
    )

    return json.loads(response.text)