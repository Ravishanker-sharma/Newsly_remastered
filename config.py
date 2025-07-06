from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json
import re


load_dotenv()
api = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key = api,
    temperature=0.7
)
def extract_json_from_llm_output(text):
    # Step 1: Remove markdown code fences and extra characters
    cleaned = re.sub(r"```(?:json|python)?", "", text, flags=re.IGNORECASE).strip("`\n ")

    # Step 2: Remove trailing commas before closing brackets
    cleaned = re.sub(r",\s*(\]|\})", r"\1", cleaned)

    # Step 3: Try parsing full JSON
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("[JSONDecodeError - Full Parse] Trying to fix...")
        print("Error:", e)

    # Step 4: Try trimming after the last closing bracket (for LLM junk after JSON)
    last_bracket = max(cleaned.rfind("]"), cleaned.rfind("}"))
    if last_bracket != -1:
        cleaned_trimmed = cleaned[:last_bracket + 1]
        try:
            return json.loads(cleaned_trimmed)
        except json.JSONDecodeError as e:
            print("[JSONDecodeError - Trimmed Parse] Still not valid JSON.")
            print("Error:", e)

    # Step 5: Try recovering by line
    lines = cleaned.splitlines()
    buffer = ""
    valid_json = ""
    for line in lines:
        buffer += line + "\n"
        try:
            json.loads(buffer)
            valid_json = buffer
        except:
            continue

    # Step 6: Final attempt
    try:
        return json.loads(valid_json)
    except json.JSONDecodeError as final_error:
        print("----- FINAL PARSE FAILED -----")
        print("Error parsing JSON after all recovery:", final_error)
        print("Original text:\n", text)
        return []

