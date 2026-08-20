import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are the inventory extraction engine for TownKart.

Extract from a shopkeeper's WhatsApp message:
- product
- price
- quantity
- unit

Example:
"Jasmine 320 15 bundles"

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
- return ONLY valid JSON
"""

def parse_merchant_message(message: str):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )
    return json.loads(response.choices[0].message.content)