import os
import json
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()


def identify_object(uploaded_image):
    """
    Identify an uploaded object using Gemini.
    If Gemini is unavailable, return a clearly labelled fallback result.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    # Read the image safely
    try:
        image = Image.open(uploaded_image).convert("RGB")
    except Exception:
        return {
            "error": "Unable to read this image. Please upload a valid image."
        }

    prompt = """
    You are the visual identification component of Second-Life Detective,
    a responsible material recovery assistant.

    Examine the image and return ONLY valid JSON with these fields:
    {
      "object": "likely object name",
      "visible_materials": ["materials that appear visible"],
      "category": "reusable, recyclable, biodegradable, hazardous, or uncertain",
      "confidence": "high, medium, or low",
      "reason": "brief explanation of the visual evidence",
      "safety_note": "appropriate safety guidance"
    }

    Rules:
    - Identify only what can reasonably be inferred from the image.
    - If the image is unclear, use uncertain and low confidence.
    - A photo cannot establish exact material composition.
    - Recommend authorised e-waste collection when appropriate.
    - Never recommend opening batteries or electronic components.
    - Do not assume an object is safe just because it looks harmless.
    - Explain uncertainty where necessary.
    """

    # Try AI identification when an API key is available
    if api_key:
        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=[prompt, image]
            )

            result_text = (response.text or "").strip()

            if result_text.startswith("```"):
                result_text = result_text.split("\n", 1)[1]
                result_text = result_text.rsplit("```", 1)[0].strip()

            result = json.loads(result_text)

            required_fields = [
                "object",
                "visible_materials",
                "category",
                "confidence",
                "reason",
                "safety_note"
            ]

            if not all(field in result for field in required_fields):
                raise ValueError("AI response is missing required fields.")

            result["identification_mode"] = "AI"
            return result

        except Exception as error:
            print(f"Gemini identification unavailable: {error}")

    # Fallback: do not pretend that an object was identified by AI.
    return {
        "object": "Identification unavailable",
        "visible_materials": ["Not verified"],
        "category": "uncertain",
        "confidence": "low",
        "reason": (
            "Live AI identification is currently unavailable. "
            "No material classification has been verified. "
            "Please inspect the item manually or try again later."
        ),
        "safety_note": (
            "Do not handle unknown hazardous materials. "
            "Use an authorised collection service for batteries "
            "and electronic waste."
        ),
        "identification_mode": "Fallback",
        "demo_mode": True
    }