import os
import shutil
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.extraction import extract_text
from backend.preprocessing import clean_text
from backend.evaluate import evaluate_resume

app = FastAPI(title="ProITbridge Resume Screening AI")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DEFAULT_JD = """Title: Senior Data Engineer
Location: Bengaluru (Hybrid)
 
About the role:
We are looking for a Senior Data Engineer to design and operate large-scale batch and streaming data pipelines that power our analytics and ML platforms. You will own pipeline reliability, data warehousing, and real-time ingestion.
 
Responsibilities:
- Design, build, and maintain scalable ETL/ELT pipelines.
- Build real-time streaming ingestion and processing.
- Own and optimize the cloud data warehouse serving analysts and data scientists.
- Ensure pipeline reliability, data quality, and performance at scale.
 
Required skills (must-have):
- 5+ years of data engineering experience
- Strong SQL and Python
- Apache Spark
- Apache Airflow
- Apache Kafka (streaming)
- Cloud data platform (AWS strongly preferred)
- ETL/ELT and data warehousing
 
Nice to have:
- Snowflake, dbt, Databricks
- Terraform / infrastructure-as-code"""

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "default_jd": DEFAULT_JD})

@app.post("/screen")
async def screen_resumes(jd_text: str = Form(...), files: list[UploadFile] = File(...)):
    os.makedirs("temp_resumes", exist_ok=True)
    
    records = []
    for uploaded_file in files:
        temp_path = os.path.join("temp_resumes", uploaded_file.filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
        
        text = extract_text(temp_path)
        clean_res_text = clean_text(text)
        score = evaluate_resume(jd_text, clean_res_text)
        
        records.append({
            "file_name": uploaded_file.filename,
            "text": text,
            "fit_score": score
        })
        try:
            os.remove(temp_path)
        except:
            pass

    if not records:
        return JSONResponse({"error": "No valid resumes uploaded.", "results": []})

    resume_df = pd.DataFrame(records)
    resume_df = resume_df.sort_values(by="fit_score", ascending=False).reset_index(drop=True)
    resume_df["rank"] = resume_df.index + 1

    return JSONResponse({"results": resume_df.to_dict(orient="records")})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)