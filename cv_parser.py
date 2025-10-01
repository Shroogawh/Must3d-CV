import io
import json
import re
import os
import tempfile
import ollama
import docx2txt
import fitz
import pytesseract
from PIL import Image
from fastapi import HTTPException
from dotenv import load_dotenv

# تحميل القيم من ملف .env
load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# تعريف HOST لـ Ollama
os.environ["OLLAMA_HOST"] = OLLAMA_URL


def extract_text(filename: str, data: io.BytesIO) -> str:
    """
    استخراج النصوص من الملفات (PDF, DOCX, Images).
    """
    try:
        if filename.lower().endswith(".pdf"):
            text = ""
            pdf = fitz.open(stream=data, filetype="pdf")
            for page in pdf:
                text += page.get_text()
            return text

        elif filename.lower().endswith((".docx", ".doc")):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(data.read())
                tmp_path = tmp.name
            return docx2txt.process(tmp_path)

        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(data)
            return pytesseract.image_to_string(image, lang="eng+ara")

        return ""

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text: {str(e)}")


def parse_cv_with_ai(text: str) -> dict:
    """
    استدعاء Ollama لاستخراج بيانات منظمة من CV.
    """
    system_prompt = """
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

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text[:4000]},
            ],
        )

        print("DEBUG Ollama Response:", response)  # للتصحيح

        assistant_text = response["message"]["content"].strip()

        if not assistant_text:
            raise HTTPException(status_code=500, detail="Ollama returned empty response")

        # محاولة قراءة JSON مباشرة
        try:
            return json.loads(assistant_text)
        except json.JSONDecodeError:
            # fallback باستخدام regex
            match = re.search(r"(\{[\s\S]*\})", assistant_text)
            if match:
                return json.loads(match.group(1))

            raise HTTPException(
                status_code=500,
                detail=f"Invalid JSON from Ollama: {assistant_text}",
            )

    except Exception as e:
        print("Error calling Ollama:", e)  # للتصحيح
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ollama: {str(e)}")
