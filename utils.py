import os
from PIL import Image
import numpy as np
import librosa
import soundfile as sf
import trimesh
from typing import Union, Tuple, Any
import json

def detect_file_type(file_path: str) -> str:
    """Detect the type of file based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        return 'image'
    elif ext in ['.wav', '.mp3', '.ogg']:
        return 'audio'
    elif ext in ['.off', '.obj', '.stl']:
        return '3d'
    elif ext in ['.txt', '.json', '.csv']:
        return 'text'
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def load_data(file_path: str) -> Tuple[str, Any]:
    """Load data from file and return its type and content."""
    file_type = detect_file_type(file_path)
    
    if file_type == 'image':
        return file_type, Image.open(file_path)
    elif file_type == 'audio':
        # Load audio with a lower sample rate and shorter duration for faster processing
        audio, sr = librosa.load(file_path, sr=16000, duration=30)
        return file_type, (audio, sr)
    elif file_type == '3d':
        return file_type, trimesh.load(file_path)
    elif file_type == 'text':
        with open(file_path, 'r', encoding='utf-8') as f:
            return file_type, f.read()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def preprocess_data(file_type: str, data: Any) -> Any:
    """Preprocess data based on its type."""
    if file_type == 'image':
        # Convert to grayscale and resize
        img = data.convert('L')
        img = img.resize((224, 224))
        return img
    elif file_type == 'audio':
        # Simple normalization only
        audio, sr = data
        audio = librosa.util.normalize(audio)
        return audio, sr
    elif file_type == '3d':
        # Center and normalize mesh
        mesh = data
        mesh.vertices -= mesh.center_mass
        mesh.vertices /= np.max(np.abs(mesh.vertices))
        return mesh
    elif file_type == 'text':
        # Basic text preprocessing
        text = data.lower()
        text = ' '.join(text.split())  # Remove extra whitespace
        return text
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def augment_data(file_type: str, data: Any) -> Any:
    """Augment data based on its type."""
    if file_type == 'image':
        # Random rotation and flip
        angle = np.random.randint(-30, 30)
        img = data.rotate(angle)
        if np.random.random() > 0.5:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        return img
    elif file_type == 'audio':
        # Simple audio augmentation
        audio, sr = data
        
        # Add small amount of noise
        noise = np.random.normal(0, 0.005, len(audio))
        audio_augmented = audio + noise
        
        # Simple time stretching (just shift the audio)
        shift = np.random.randint(-1000, 1000)
        audio_augmented = np.roll(audio_augmented, shift)
        
        return audio_augmented, sr
    elif file_type == '3d':
        # Random rotation
        mesh = data.copy()
        angle = np.random.uniform(0, 2 * np.pi)
        rotation = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])
        mesh.apply_transform(rotation)
        return mesh
    elif file_type == 'text':
        # Simple word replacement
        replacements = {
            'the': 'a',
            'is': 'was',
            'are': 'were',
            'and': 'or'
        }
        words = data.split()
        augmented = [replacements.get(word, word) for word in words]
        return ' '.join(augmented)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def save_processed_data(file_type: str, data: Any, output_path: str) -> str:
    """Save processed data to file."""
    if file_type == 'image':
        data.save(output_path)
    elif file_type == 'audio':
        audio, sr = data
        # Save directly using soundfile
        sf.write(output_path, audio, sr)
    elif file_type == '3d':
        data.export(output_path)
    elif file_type == 'text':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(data)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    return output_path 