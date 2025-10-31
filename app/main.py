from fastapi import FastAPI, HTTPException, UploadFile, File

app = FastAPI()

async def read_csv(file: UploadFile) -> list[str]:
    # Check if the uploaded file is a CSV
    if file.content_type not in {"text/csv", "application/vnd.ms-excel"}:
        raise HTTPException(status_code=422, detail="Expected a CSV file")
    
    content = await file.read()
    csv_text = content.decode('utf-8')
    return csv_text.strip().split('\n')

@app.post("/validate")
async def validate_csv(file: UploadFile = File(...)):
    
    lines = await read_csv(file)
    total_rows = len(lines) - 1
    return {"total_rows": total_rows}

@app.post("/typecheck")
async def typecheck_csv(file: UploadFile = File(...)):
    lines = await read_csv(file)
    total_rows = len(lines) - 1
    return {"total_rows": total_rows}