from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io
from cv_parser import extract_text, parse_cv_with_ai  

app = FastAPI(title="CV Parser with Ollama")


@app.post("/parse")
async def parse_cv(cvfile: UploadFile = File(...)):
    # التحقق من الامتداد
    if not cvfile.filename.lower().endswith((".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="امتداد الملف غير مسموح")

    # قراءة البيانات
    data = io.BytesIO(await cvfile.read())
    data.seek(0)

    # استخراج النص
    text = extract_text(cvfile.filename, data)
    if not text.strip():
        raise HTTPException(status_code=400, detail="لم أستطع استخراج نص من الملف")

    # تحليل النص بالذكاء الاصطناعي
    parsed = parse_cv_with_ai(text)

    # رجوع النتيجة كـ JSON
    return JSONResponse(content={
        "filename": cvfile.filename,
        "extracted_text": text,
        "parsed": parsed
    })
