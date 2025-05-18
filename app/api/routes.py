from fastapi import APIRouter, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import os
import shutil
from typing import Dict, Any
import json
from PIL import Image
import librosa
import soundfile as sf
import trimesh
import numpy as np

from ..core.config import current_data, FILE_TYPES, BASE_DIR
from ..services.processors import TextProcessor, ImageProcessor, AudioProcessor, ThreeDProcessor

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "ui" / "templates"))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = str(BASE_DIR / "data" / file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Copy to static directory for serving
        static_path = str(BASE_DIR / "ui" / "static" / file.filename)
        shutil.copy2(file_path, static_path)
        
        # Determine file type
        file_type = None
        for type_name, extensions in FILE_TYPES.items():
            if any(file.filename.lower().endswith(ext) for ext in extensions):
                file_type = type_name
                break
        
        if not file_type:
            return {"status": "error", "error": "Unsupported file type"}
        
        current_data["original"] = file_path
        current_data["file_type"] = file_type
        
        return {"status": "success", "file_type": file_type}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/preprocess")
async def preprocess_data_route(preprocessing: Dict[str, bool], augmentation: Dict[str, bool]):
    if not current_data.get("original") or not current_data.get("file_type"):
        return {"status": "error", "error": "No file uploaded"}
    
    try:
        file_type = current_data["file_type"]
        file_path = current_data["original"]
        
        if file_type == 'text':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            result = TextProcessor.process(text, preprocessing, augmentation)
            
            # Save results
            for stage in ['preprocessed', 'augmented']:
                output_path = str(BASE_DIR / "data" / f"{stage}_{os.path.basename(file_path)}")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result[stage])
                current_data[stage] = output_path
            
            return {
                "status": "success",
                "original": result["original"],
                "preprocessed": result["preprocessed"],
                "augmented": result["augmented"]
            }
            
        elif file_type == 'image':
            image = Image.open(file_path)
            result = ImageProcessor.process(image, preprocessing, augmentation)
            
            # Save results
            for stage in ['preprocessed', 'augmented']:
                output_path = str(BASE_DIR / "data" / f"{stage}_{os.path.basename(file_path)}")
                static_path = str(BASE_DIR / "ui" / "static" / f"{stage}_{os.path.basename(file_path)}")
                result[stage].save(output_path)
                result[stage].save(static_path)
                current_data[stage] = output_path
            
            return {
                "status": "success",
                "original": f"/static/{os.path.basename(file_path)}",
                "preprocessed": f"/static/preprocessed_{os.path.basename(file_path)}",
                "augmented": f"/static/augmented_{os.path.basename(file_path)}"
            }
            
        elif file_type == 'audio':
            audio_data, sr = librosa.load(file_path)
            result = AudioProcessor.process(audio_data, sr, preprocessing, augmentation)
            
            # Save results
            for stage in ['preprocessed', 'augmented']:
                output_path = str(BASE_DIR / "data" / f"{stage}_{os.path.basename(file_path)}")
                static_path = str(BASE_DIR / "ui" / "static" / f"{stage}_{os.path.basename(file_path)}")
                sf.write(output_path, result[stage][0], result[stage][1])
                sf.write(static_path, result[stage][0], result[stage][1])
                current_data[stage] = output_path
            
            return {
                "status": "success",
                "original": f"/static/{os.path.basename(file_path)}",
                "preprocessed": f"/static/preprocessed_{os.path.basename(file_path)}",
                "augmented": f"/static/augmented_{os.path.basename(file_path)}"
            }
            
        elif file_type == '3d':
            mesh = trimesh.load(file_path)
            result = ThreeDProcessor.process(mesh, preprocessing, augmentation)
            
            # Save results
            for stage in ['preprocessed', 'augmented']:
                output_path = str(BASE_DIR / "data" / f"{stage}_{os.path.basename(file_path)}")
                static_path = str(BASE_DIR / "ui" / "static" / f"{stage}_{os.path.basename(file_path)}")
                result[stage].export(output_path)
                result[stage].export(static_path)
                current_data[stage] = output_path
            
            return {
                "status": "success",
                "original": f"/static/{os.path.basename(file_path)}",
                "preprocessed": f"/static/preprocessed_{os.path.basename(file_path)}",
                "augmented": f"/static/augmented_{os.path.basename(file_path)}"
            }
            
    except Exception as e:
        return {"status": "error", "error": str(e)} 