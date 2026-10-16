import os
import json
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()

def identify_object(uploaded_image):
    """
    Analyse an uploaded image with Gemini.
    Returns a structured description of the object and likely materials.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "error": "Gemini API key not found. Check your .env file."
        }

    try:
        client = genai.Client(api_key=api_key)

        image = Image.open(uploaded_image).convert("RGB")

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
        - A photo cannot establish the exact composition of an object.
        - Electronic waste may contain hazardous components; recommend
          authorised e-waste collection when appropriate.
        - Never recommend opening batteries or electronic components.
        - Do not assume an object is safe just because it looks harmless.
        - Use biodegradable only when the visible material supports that
          possibility; explain uncertainty where necessary.
        """

        response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[prompt, image]
)

        result_text = response.text.strip()

        if result_text.startswith("```"):
            result_text = result_text.split("\n", 1)[1]
            result_text = result_text.rsplit("```", 1)[0].strip()

        result = json.loads(result_text)
        return result

    except Exception as error:
        return {
            "error": f"Object identification failed: {error}"
        }