from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io
from cv_parser import extract_text, parse_cv_with_ai

app = FastAPI(title="CV Parser with Ollama")

@app.get("/")
async def root():
    return {"message": "مرحبًا بك في CV Parser API. استخدم المسار /parse لتحليل السير الذاتية."}

@app.post("/parse")
async def parse_cv(cvfile: UploadFile = File(...)):
    if not cvfile.filename.lower().endswith((".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="امتداد الملف غير مسموح")
    data = io.BytesIO(await cvfile.read())
    data.seek(0)
    text = extract_text(cvfile.filename, data)
    if not text.strip():
        raise HTTPException(status_code=400, detail="لم أستطع استخراج نص من الملف")
 
    parsed = parse_cv_with_ai(text)
   
    return JSONResponse(content={
        "filename": cvfile.filename,
        "extracted_text": text,
        "parsed": parsed
    })
