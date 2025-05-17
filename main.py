from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os
from pathlib import Path
import shutil
from typing import Optional
import json
from utils import load_data, preprocess_data, augment_data, save_processed_data

# Create necessary directories
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("data", exist_ok=True)

app = FastAPI(title="Data Processing Application")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Global variable to store current data
current_data = {
    "original": None,
    "preprocessed": None,
    "augmented": None,
    "file_type": None
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Load and store the data
    try:
        file_type, data = load_data(file_path)
        current_data["original"] = file_path
        current_data["file_type"] = file_type
        return {"filename": file.filename, "status": "success", "file_type": file_type}
    except Exception as e:
        return {"error": str(e)}

@app.post("/preprocess")
async def preprocess_data_route():
    if not current_data["original"] or not current_data["file_type"]:
        return {"error": "No file uploaded"}
    
    try:
        # Load the original data
        _, data = load_data(current_data["original"])
        
        # Preprocess the data
        processed_data = preprocess_data(current_data["file_type"], data)
        
        # Save the preprocessed data
        output_path = f"data/preprocessed_{os.path.basename(current_data['original'])}"
        save_processed_data(current_data["file_type"], processed_data, output_path)
        
        current_data["preprocessed"] = output_path
        return {"status": "success", "file_path": output_path}
    except Exception as e:
        return {"error": str(e)}

@app.post("/augment")
async def augment_data_route():
    if not current_data["preprocessed"] or not current_data["file_type"]:
        return {"error": "No preprocessed data available"}
    
    try:
        # Load the preprocessed data
        _, data = load_data(current_data["preprocessed"])
        
        # Augment the data
        augmented_data = augment_data(current_data["file_type"], data)
        
        # Save the augmented data
        output_path = f"data/augmented_{os.path.basename(current_data['preprocessed'])}"
        save_processed_data(current_data["file_type"], augmented_data, output_path)
        
        current_data["augmented"] = output_path
        return {"status": "success", "file_path": output_path}
    except Exception as e:
        return {"error": str(e)}

@app.get("/sample/{stage}")
async def get_sample(stage: str):
    if stage not in ["original", "preprocessed", "augmented"]:
        return {"error": "Invalid stage"}
    
    if not current_data[stage]:
        return {"error": f"No {stage} data available"}
    
    try:
        return FileResponse(
            current_data[stage],
            media_type="application/octet-stream",
            filename=os.path.basename(current_data[stage])
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 