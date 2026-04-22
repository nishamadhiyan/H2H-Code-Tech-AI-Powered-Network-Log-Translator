from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.dirname(__file__))
from log_parser import parse_logs
from translator import translate_logs
import uvicorn

app = FastAPI(title="AI Network Log Translator")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = os.path.join(BASE_DIR, "frontend", "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/analyze")
async def analyze(log_text: str = Form(...)):
    parsed = parse_logs(log_text)
    ai_result = translate_logs(parsed)
    return JSONResponse({"parsed": parsed, "ai_analysis": ai_result})

@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    log_text = content.decode("utf-8", errors="ignore")
    parsed = parse_logs(log_text)
    ai_result = translate_logs(parsed)
    return JSONResponse({
        "parsed": parsed,
        "ai_analysis": ai_result,
        "filename": file.filename
    })

@app.post("/explain-line")
async def explain_line(log_line: str = Form(...)):
    parsed = parse_logs(log_line)
    ai_result = translate_logs(parsed)
    return JSONResponse({"explanation": ai_result.get("plain_english_summary", "")})

@app.post("/chat")
async def chat_with_logs(
    question: str = Form(...),
    log_context: str = Form(...)
):
    from groq import Groq
    import os
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a network security expert. Answer questions about the network logs provided. Be concise and helpful."
            },
            {
                "role": "user",
                "content": f"Here are the network logs:\n\n{log_context}\n\nQuestion: {question}"
            }
        ],
        max_tokens=500,
        temperature=0.3
    )
    
    return JSONResponse({
        "answer": response.choices[0].message.content.strip()
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)