from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sys
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(__file__))

from log_parser import parse_logs
from translator import translate_logs
from database import init_db, save_analysis, get_history

try:
    from ip_checker import check_all_ips
    IP_CHECK_ENABLED = True
except:
    IP_CHECK_ENABLED = False

import uvicorn

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="AI Network Log Translator",
    description="Secure AI-powered network log analysis",
    version="1.0.0"
)

# Rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Init database
init_db()

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static")

# Input validation
def validate_log_input(text: str) -> str:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Log input cannot be empty")
    if len(text) > 100000:
        raise HTTPException(status_code=400, detail="Log input too large. Max 100,000 characters")
    # Remove null bytes
    text = text.replace('\x00', '')
    return text.strip()

@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = os.path.join(BASE_DIR, "frontend", "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze(request: Request, log_text: str = Form(...)):
    log_text = validate_log_input(log_text)
    parsed = parse_logs(log_text)
    ai_result = translate_logs(parsed)
    save_analysis(parsed, ai_result)
    ip_results = check_all_ips(log_text) if IP_CHECK_ENABLED else []
    return JSONResponse({
        "parsed": parsed,
        "ai_analysis": ai_result,
        "ip_reputation": ip_results
    })

@app.post("/analyze-file")
@limiter.limit("5/minute")
async def analyze_file(request: Request, file: UploadFile = File(...)):
    # File type validation
    allowed_types = ["text/plain", "application/octet-stream"]
    allowed_extensions = [".log", ".txt"]
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .log and .txt files allowed"
        )
    
    # File size validation (5MB max)
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 5MB"
        )
    
    log_text = content.decode("utf-8", errors="ignore")
    log_text = validate_log_input(log_text)
    
    parsed = parse_logs(log_text)
    ai_result = translate_logs(parsed)
    save_analysis(parsed, ai_result)
    ip_results = check_all_ips(log_text) if IP_CHECK_ENABLED else []
    
    return JSONResponse({
        "parsed": parsed,
        "ai_analysis": ai_result,
        "ip_reputation": ip_results,
        "filename": file.filename
    })

@app.post("/explain-line")
@limiter.limit("20/minute")
async def explain_line(request: Request, log_line: str = Form(...)):
    log_line = validate_log_input(log_line)
    if len(log_line) > 1000:
        raise HTTPException(status_code=400, detail="Log line too long")
    parsed = parse_logs(log_line)
    ai_result = translate_logs(parsed)
    return JSONResponse({
        "explanation": ai_result.get("plain_english_summary", "")
    })

@app.post("/chat")
@limiter.limit("15/minute")
async def chat_with_logs(
    request: Request,
    question: str = Form(...),
    log_context: str = Form(...)
):
    if len(question) > 500:
        raise HTTPException(status_code=400, detail="Question too long. Max 500 characters")
    
    question = question.strip()
    log_context = log_context[:4000]
    
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a network security expert. Answer questions about the network logs provided. Be concise and helpful. Do not reveal sensitive system information."
            },
            {
                "role": "user",
                "content": f"Logs:\n{log_context}\n\nQuestion: {question}"
            }
        ],
        max_tokens=500,
        temperature=0.3
    )
    
    return JSONResponse({
        "answer": response.choices[0].message.content.strip()
    })

@app.get("/history")
@limiter.limit("10/minute")
async def history(request: Request):
    return JSONResponse({"history": get_history()})

@app.get("/health")
async def health():
    return JSONResponse({
        "status": "healthy",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)