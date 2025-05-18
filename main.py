from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import os
from pathlib import Path
import shutil
from typing import Optional, Dict, Any
import json
import numpy as np
from PIL import Image
import librosa
import soundfile as sf
import trimesh
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import random
import io

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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

def process_text(text: str, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, str]:
    result = {"original": text, "preprocessed": text, "augmented": text}
    
    # Preprocessing
    if preprocessing_options.get("cleaning"):
        # Basic text cleaning
        text = text.replace('\n', ' ').strip()
        text = ' '.join(text.split())
    
    if preprocessing_options.get("lowercase"):
        text = text.lower()
    
    if preprocessing_options.get("stopwords"):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        text = ' '.join([word for word in words if word.lower() not in stop_words])
    
    if preprocessing_options.get("stemming"):
        stemmer = PorterStemmer()
        words = word_tokenize(text)
        text = ' '.join([stemmer.stem(word) for word in words])
    
    if preprocessing_options.get("lemmatization"):
        lemmatizer = WordNetLemmatizer()
        words = word_tokenize(text)
        text = ' '.join([lemmatizer.lemmatize(word) for word in words])
    
    if preprocessing_options.get("tokenization"):
        text = ' '.join(word_tokenize(text))
    
    result["preprocessed"] = text
    
    # Augmentation
    if augmentation_options.get("synonym"):
        words = word_tokenize(text)
        augmented_words = []
        for word in words:
            synsets = wordnet.synsets(word)
            if synsets:
                synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas()]
                if synonyms:
                    augmented_words.append(random.choice(synonyms))
                else:
                    augmented_words.append(word)
            else:
                augmented_words.append(word)
        result["augmented"] = ' '.join(augmented_words)
    
    if augmentation_options.get("insertion"):
        words = word_tokenize(text)
        augmented_words = []
        for word in words:
            augmented_words.append(word)
            if random.random() < 0.3:  # 30% chance to insert a synonym
                synsets = wordnet.synsets(word)
                if synsets:
                    synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas()]
                    if synonyms:
                        augmented_words.append(random.choice(synonyms))
        result["augmented"] = ' '.join(augmented_words)
    
    return result

def process_image(image: Image.Image, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, Image.Image]:
    result = {
        "original": image,
        "preprocessed": image.copy(),
        "augmented": image.copy()
    }
    
    # Preprocessing
    if preprocessing_options.get("resize"):
        result["preprocessed"] = result["preprocessed"].resize((224, 224))
    
    if preprocessing_options.get("normalize"):
        img_array = np.array(result["preprocessed"])
        img_array = img_array / 255.0
        result["preprocessed"] = Image.fromarray((img_array * 255).astype(np.uint8))
    
    # Augmentation
    if augmentation_options.get("flip"):
        result["augmented"] = result["preprocessed"].transpose(Image.FLIP_LEFT_RIGHT)
    
    if augmentation_options.get("jitter"):
        img_array = np.array(result["preprocessed"])
        # Add random color jitter
        jitter = np.random.normal(0, 25, img_array.shape).astype(np.int16)
        img_array = np.clip(img_array + jitter, 0, 255).astype(np.uint8)
        result["augmented"] = Image.fromarray(img_array)
    
    return result

def process_audio(audio_data: np.ndarray, sr: int, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, Any]:
    result = {
        "original": (audio_data, sr),
        "preprocessed": (audio_data, sr),
        "augmented": (audio_data, sr)
    }
    
    # Preprocessing
    if preprocessing_options.get("resample"):
        target_sr = 22050
        result["preprocessed"] = (librosa.resample(audio_data, orig_sr=sr, target_sr=target_sr), target_sr)
    
    # Augmentation
    if augmentation_options.get("noise"):
        noise = np.random.normal(0, 0.005, audio_data.shape)
        result["augmented"] = (audio_data + noise, sr)
    
    if augmentation_options.get("stretch"):
        rate = random.uniform(0.8, 1.2)
        result["augmented"] = (librosa.effects.time_stretch(audio_data, rate=rate), sr)
    
    if augmentation_options.get("pitch"):
        n_steps = random.randint(-4, 4)
        result["augmented"] = (librosa.effects.pitch_shift(audio_data, sr=sr, n_steps=n_steps), sr)
    
    return result

def process_3d(mesh: trimesh.Trimesh, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, trimesh.Trimesh]:
    result = {
        "original": mesh,
        "preprocessed": mesh.copy(),
        "augmented": mesh.copy()
    }
    
    # Preprocessing
    if preprocessing_options.get("normalize"):
        result["preprocessed"].vertices = result["preprocessed"].vertices / np.max(np.abs(result["preprocessed"].vertices))
    
    if preprocessing_options.get("center"):
        centroid = result["preprocessed"].centroid
        result["preprocessed"].vertices = result["preprocessed"].vertices - centroid
    
    # Augmentation
    if augmentation_options.get("scale"):
        # Random scaling between 0.8 and 1.2
        scale_factor = np.random.uniform(0.8, 1.2)
        result["augmented"].vertices = result["preprocessed"].vertices * scale_factor
    
    if augmentation_options.get("noise"):
        # Add Gaussian noise to vertices
        noise = np.random.normal(0, 0.01, result["preprocessed"].vertices.shape)
        result["augmented"].vertices = result["preprocessed"].vertices + noise
    
    return result

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
    
    # Copy to static directory for serving
    static_path = f"static/{file.filename}"
    shutil.copy2(file_path, static_path)
    
    # Determine file type
    file_type = None
    if file.filename.lower().endswith(('.txt', '.json')):
        file_type = 'text'
    elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        file_type = 'image'
    elif file.filename.lower().endswith(('.wav', '.mp3')):
        file_type = 'audio'
    elif file.filename.lower().endswith(('.obj', '.off')):
        file_type = '3d'
    
    if not file_type:
        return {"error": "Unsupported file type"}
    
    current_data["original"] = file_path
    current_data["file_type"] = file_type
    
    return {"status": "success", "file_type": file_type}

@app.post("/preprocess")
async def preprocess_data_route(preprocessing: Dict[str, bool], augmentation: Dict[str, bool]):
    if not current_data["original"] or not current_data["file_type"]:
        return {"error": "No file uploaded"}
    
    try:
        file_type = current_data["file_type"]
        file_path = current_data["original"]
        
        if file_type == 'text':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            result = process_text(text, preprocessing, augmentation)
            
            # Save results
            for stage in ['preprocessed', 'augmented']:
                output_path = f"data/{stage}_{os.path.basename(file_path)}"
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
            result = process_image(image, preprocessing, augmentation)
            
            # Save results
            for stage in ['preprocessed', 'augmented']:
                output_path = f"data/{stage}_{os.path.basename(file_path)}"
                static_path = f"static/{stage}_{os.path.basename(file_path)}"
                result[stage].save(output_path)
                result[stage].save(static_path)  # Save to static directory
                current_data[stage] = output_path
            
            return {
                "status": "success",
                "original": f"/static/{os.path.basename(file_path)}",
                "preprocessed": f"/static/preprocessed_{os.path.basename(file_path)}",
                "augmented": f"/static/augmented_{os.path.basename(file_path)}"
            }
            
        elif file_type == 'audio':
            audio_data, sr = librosa.load(file_path)
            result = process_audio(audio_data, sr, preprocessing, augmentation)
            
            # Save results and generate spectrograms
            for stage in ['preprocessed', 'augmented']:
                output_path = f"data/{stage}_{os.path.basename(file_path)}"
                static_path = f"static/{stage}_{os.path.basename(file_path)}"
                sf.write(output_path, result[stage][0], result[stage][1])
                sf.write(static_path, result[stage][0], result[stage][1])  # Save to static directory
                current_data[stage] = output_path
                
                # Generate spectrogram
                spec = librosa.feature.melspectrogram(y=result[stage][0], sr=result[stage][1])
                spec_db = librosa.power_to_db(spec, ref=np.max)
                spec_img = Image.fromarray((spec_db * 255).astype(np.uint8))
                spec_path = f"static/{stage}_spec_{os.path.basename(file_path)}.png"
                spec_img.save(spec_path)
            
            return {
                "status": "success",
                "original": f"/static/{os.path.basename(file_path)}",
                "preprocessed": f"/static/preprocessed_{os.path.basename(file_path)}",
                "augmented": f"/static/augmented_{os.path.basename(file_path)}",
                "original_spectrogram": f"/static/original_spec_{os.path.basename(file_path)}.png",
                "preprocessed_spectrogram": f"/static/preprocessed_spec_{os.path.basename(file_path)}.png",
                "augmented_spectrogram": f"/static/augmented_spec_{os.path.basename(file_path)}.png"
            }
            
        elif file_type == '3d':
            mesh = trimesh.load(file_path)
            result = process_3d(mesh, preprocessing, augmentation)
            
            # Save results
            for stage in ['preprocessed', 'augmented']:
                output_path = f"data/{stage}_{os.path.basename(file_path)}"
                static_path = f"static/{stage}_{os.path.basename(file_path)}"
                result[stage].export(output_path)
                result[stage].export(static_path)  # Save to static directory
                current_data[stage] = output_path
            
            # Generate preview images for 3D models
            for stage in ['original', 'preprocessed', 'augmented']:
                # Create a scene with the mesh
                scene = trimesh.Scene(result[stage])
                # Render the scene from different angles
                angles = [(0, 0), (45, 0), (0, 45)]
                for i, (azimuth, elevation) in enumerate(angles):
                    # Set up the camera
                    camera = trimesh.scene.Camera(
                        resolution=(400, 400),
                        fov=(60, 60)
                    )
                    # Render the scene
                    png = scene.save_image(
                        resolution=(400, 400),
                        visible=True,
                        camera=camera
                    )
                    # Save the preview image
                    preview_path = f"static/{stage}_view_{i}_{os.path.basename(file_path)}.png"
                    with open(preview_path, 'wb') as f:
                        f.write(png)
            
            return {
                "status": "success",
                "original": f"/static/{os.path.basename(file_path)}",
                "preprocessed": f"/static/preprocessed_{os.path.basename(file_path)}",
                "augmented": f"/static/augmented_{os.path.basename(file_path)}",
                "original_views": [
                    f"/static/original_view_0_{os.path.basename(file_path)}.png",
                    f"/static/original_view_1_{os.path.basename(file_path)}.png",
                    f"/static/original_view_2_{os.path.basename(file_path)}.png"
                ],
                "preprocessed_views": [
                    f"/static/preprocessed_view_0_{os.path.basename(file_path)}.png",
                    f"/static/preprocessed_view_1_{os.path.basename(file_path)}.png",
                    f"/static/preprocessed_view_2_{os.path.basename(file_path)}.png"
                ],
                "augmented_views": [
                    f"/static/augmented_view_0_{os.path.basename(file_path)}.png",
                    f"/static/augmented_view_1_{os.path.basename(file_path)}.png",
                    f"/static/augmented_view_2_{os.path.basename(file_path)}.png"
                ]
            }
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 