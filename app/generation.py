
import os

from dotenv import load_dotenv
from google import genai
import time
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

# Generation model
MODEL_NAME = "gemini-3.5-flash-lite"



def generate_answer(question, context):

    prompt = f"""
You are a friendly AI assistant representing Rudesh
on his personal portfolio website.

Answer the visitor's question using ONLY the
provided context.

Rules:
- Be friendly and professional.
- Give clear and concise answers.
- Do not invent information about Rudesh.
- If the answer is not available in the context,
  clearly say that you don't have that information.

Context:
{context}

Visitor's question:
{question}

Answer:
"""

    for attempt in range(3):

        try:
            print(f"Calling Gemini (attempt {attempt + 1}/3)...")

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            return response.text

        except errors.ServerError:
            if attempt == 2:
                raise

            wait_time = 2 ** (attempt + 1)

            print(f"Gemini unavailable. Retrying in {wait_time} seconds...")

            time.sleep(wait_time)

