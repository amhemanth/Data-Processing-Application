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
from ..services import TextProcessor, ImageProcessor, AudioProcessor, ThreeDProcessor

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
            return JSONResponse(status_code=400, content={'status': 'error', 'error': 'Unsupported file type'})
        
        current_data["original"] = file_path
        current_data["file_type"] = file_type
        
        return {"status": "success", "file_type": file_type}
    except Exception as e:
        return JSONResponse(status_code=500, content={'status': 'error', 'error': str(e)})

@router.post("/preprocess")
async def preprocess_data_route(preprocessing: Dict[str, bool], augmentation: Dict[str, bool]):
    if not current_data.get("original") or not current_data.get("file_type"):
        return JSONResponse(status_code=400, content={'status': 'error', 'error': 'No file uploaded'})
    
    try:
        file_type = current_data["file_type"]
        file_path = current_data["original"]
        
        result = {
            "original": None,
            "preprocessed": None,
            "augmented": None
        }

        if file_type == 'text':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            processed_data = TextProcessor.process(text, preprocessing, augmentation)
            result["original"] = processed_data["original"]
            result["preprocessed"] = processed_data["preprocessed"]
            result["augmented"] = processed_data["augmented"]
            
            # For text, return content directly
            return {"status": "success", **result}
            
        elif file_type == 'image':
            image = Image.open(file_path)
            processed_data = ImageProcessor.process(image, preprocessing, augmentation)
            
            # Save processed images to static for serving
            output_paths = {}
            for stage in ['original', 'preprocessed', 'augmented']:
                 # Ensure we have data for the stage
                if processed_data[stage] is not None:
                    # Create a unique filename for the processed image
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_filename = f'{stage}_{base_name}.png' # Save as PNG
                    output_path = str(BASE_DIR / "ui" / "static" / output_filename)
                    processed_data[stage].save(output_path)
                    output_paths[stage] = f'/static/{output_filename}'
            
            return {"status": "success", **output_paths}
            
        elif file_type == 'audio':
            audio_data, sr = sf.read(file_path)
            processed_data = AudioProcessor.process(audio_data, sr, preprocessing, augmentation)

            # Save processed audio to static for serving
            output_paths = {}
            for stage in ['original', 'preprocessed', 'augmented']:
                if processed_data[stage] is not None:
                     base_name = os.path.splitext(os.path.basename(file_path))[0]
                     output_filename = f'{stage}_{base_name}.wav' # Save as WAV
                     output_path = str(BASE_DIR / "ui" / "static" / output_filename)
                     sf.write(output_path, processed_data[stage][0], processed_data[stage][1])
                     output_paths[stage] = f'/static/{output_filename}'

            return {"status": "success", **output_paths}

        elif file_type == '3d':
            mesh = trimesh.load_mesh(file_path)
            processed_data = ThreeDProcessor.process(mesh, preprocessing, augmentation)

            # Save processed 3D models to static for serving (e.g., as OBJ)
            output_paths = {}
            for stage in ['original', 'preprocessed', 'augmented']:
                 if processed_data[stage] is not None:
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_filename = f'{stage}_{base_name}.obj' # Save as OBJ
                    output_path = str(BASE_DIR / "ui" / "static" / output_filename)
                    processed_data[stage].export(output_path)
                    output_paths[stage] = f'/static/{output_filename}'
            
            return {"status": "success", **output_paths}

        else:
            return JSONResponse(status_code=400, content={'status': 'error', 'error': 'Unsupported file type for processing'})

    except Exception as e:
        print(f"Error during processing: {e}")
        return JSONResponse(status_code=500, content={'status': 'error', 'error': str(e)}) 