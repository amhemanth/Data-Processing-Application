import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Create necessary directories
os.makedirs(BASE_DIR / "static", exist_ok=True)
os.makedirs(BASE_DIR / "templates", exist_ok=True)
os.makedirs(BASE_DIR / "data", exist_ok=True)

# File type configurations
FILE_TYPES = {
    'text': ['.txt', '.json'],
    'image': ['.jpg', '.jpeg', '.png'],
    'audio': ['.wav', '.mp3'],
    '3d': ['.obj', '.off']
}

# Processing configurations
IMAGE_CONFIG = {
    'resize_size': (224, 224),
    'normalize_range': (0, 1)
}

AUDIO_CONFIG = {
    'target_sr': 22050,
    'noise_level': 0.005,
    'stretch_range': (0.8, 1.2),
    'pitch_range': (-4, 4)
}

THREE_D_CONFIG = {
    'resolution': (400, 400),
    'fov': (60, 60),
    'noise_level': 0.01,
    'scale_range': (0.8, 1.2)
}

# Global state
current_data = {
    "original": None,
    "preprocessed": None,
    "augmented": None,
    "file_type": None
} 