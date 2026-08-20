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
You are the product normalization engine for TownKart.

Convert a product name into a canonical product name for database search.

Examples:
mallipoo -> jasmine flower
malli poo -> jasmine flower
jasmine -> jasmine flower
jasmine flowers -> jasmine flower
tomatoes -> tomato
potatos -> potato
school shoes -> school shoes
notebooks -> notebook
toy cars -> toy car

Rules:
- remove unnecessary words
- handle spelling variations
- understand common Indian/local transliterations
- do not change the actual product
- preserve the actual meaning of the product
- return ONLY the canonical product name
"""


def normalize_product(product: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=product,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )

    return response.text.strip()