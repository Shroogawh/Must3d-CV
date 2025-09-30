import io
import json
import re
import os
import ollama
import docx2txt
import fitz
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:7b")
OLLAMA_URL = os.getenv("ollama_URL", "http://localhost:11434")

def extract_text(filename, data: io.BytesIO) -> str:
    if filename.lower().endswith(".pdf"):
        text = ""
        pdf = fitz.open(stream=data, filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text
    elif filename.lower().endswith((".docx", ".doc")):
        return docx2txt.process(data)
    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(data)
        return pytesseract.image_to_string(image, lang="eng+ara")
    return ""

def parse_cv_with_ai(text: str):
    system_prompt = (
        """
أنت مساعد ذكي يستخرج بيانات منظمة من السيرة الذاتية (CV).
يجب أن ترجع الرد بصيغة JSON فقط، بدون أي شرح أو كلام إضافي.
المفاتيح المطلوبة:
{
  "experience": [],
  "skills": [],
  "qualification": [],
  "certification_and_achievement": []
}
- إذا لم تجد أي قيمة ضع [].
- لا تضف أي نص آخر خارج JSON.
"""
    )
    assistant_text = ""
    try:
        client = ollama.Client(host=OLLAMA_URL)
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text[:4000]},
            ],
        )
      
        print("DEBUG Ollama Response:", response)
        assistant_text = response.get("message", {}).get("content", "").strip()
        if not assistant_text:
            return {"error": "Ollama returned empty response"}
       
        if assistant_text.startswith("{"):
            try:
                return json.loads(assistant_text)
            except json.JSONDecodeError:
                return {"raw": assistant_text, "error": "Invalid JSON"}
       
        m = re.search(r"(\{[\s\S]*\})", assistant_text)
        if m:
            try:
                return json.loads(m.group(1))
            except:
                return {"raw": assistant_text, "error": "Could not parse JSON"}
      
        return {"raw": assistant_text}
    except Exception as e:
        print("Error calling Ollama:", e)
        return {"error": str(e)}
