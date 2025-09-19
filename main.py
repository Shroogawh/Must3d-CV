from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import io
from cv_parser import extract_text, parse_cv_with_ai  

app = FastAPI(title="CV Parser with Ollama")


@app.post("/api/parse")
async def parse_cv(cvfile: UploadFile = File(...)):
    if not cvfile.filename.lower().endswith((".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="امتداد الملف غير مسموح")

    data = io.BytesIO(await cvfile.read())
    data.seek(0)
    text = extract_text(cvfile.filename, data)

    if not text.strip():
        raise HTTPException(status_code=400, detail="لم أستطع استخراج نص من الملف")

    parsed = parse_cv_with_ai(text)
    return JSONResponse(content=parsed)


@app.get("/")
def upload_form():
    html = """
    <html>
    <head>
        <title>CV Parser</title>
        <style>
            #progress-container { width: 100%; background: #eee; margin-top: 10px; }
            #progress-bar { width: 0%; height: 20px; background: #4caf50; text-align: center; color: white; }
            pre { background: #f5f5f5; padding: 10px; }
        </style>
    </head>
    <body>
        <h2>Upload CV</h2>
        <input id="fileInput" type="file" />
        <button onclick="uploadFile()">Upload</button>

        <div id="progress-container">
            <div id="progress-bar">0%</div>
        </div>

        <h3>Response:</h3>
        <pre id="response"></pre>

        <script>
            function uploadFile() {
                var fileInput = document.getElementById("fileInput");
                if (!fileInput.files.length) {
                    alert("Please select a file!");
                    return;
                }
                var file = fileInput.files[0];

                var formData = new FormData();
                formData.append("cvfile", file);

                var xhr = new XMLHttpRequest();
                xhr.open("POST", "/api/parse", true);

                // تحديث شريط التقدم
                xhr.upload.onprogress = function (e) {
                    if (e.lengthComputable) {
                        var percent = Math.round((e.loaded / e.total) * 100);
                        var bar = document.getElementById("progress-bar");
                        bar.style.width = percent + "%";
                        bar.innerText = percent + "%";
                    }
                };

                xhr.onload = function () {
                    if (xhr.status === 200) {
                        document.getElementById("response").innerText = JSON.stringify(JSON.parse(xhr.responseText), null, 2);
                    } else {
                        document.getElementById("response").innerText = "Error: " + xhr.status + " " + xhr.statusText;
                    }
                };

                xhr.send(formData);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
