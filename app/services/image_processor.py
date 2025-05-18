import numpy as np
from PIL import Image
from typing import Dict, Any

from ..core.config import IMAGE_CONFIG

class ImageProcessor:
    @staticmethod
    def process(image: Image.Image, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, Image.Image]:
        result = {
            "original": image,
            "preprocessed": image.copy(),
            "augmented": image.copy()
        }
        
        # Preprocessing
        if preprocessing_options.get("resize"):
            result["preprocessed"] = result["preprocessed"].resize(IMAGE_CONFIG['resize_size'])
        
        if preprocessing_options.get("normalize"):
            img_array = np.array(result["preprocessed"])
            img_array = img_array / 255.0
            result["preprocessed"] = Image.fromarray((img_array * 255).astype(np.uint8))
        
        # Augmentation
        if augmentation_options.get("flip"):
            result["augmented"] = result["preprocessed"].transpose(Image.FLIP_LEFT_RIGHT)
        
        if augmentation_options.get("jitter"):
            img_array = np.array(result["preprocessed"])
            jitter = np.random.normal(0, 25, img_array.shape).astype(np.int16)
            img_array = np.clip(img_array + jitter, 0, 255).astype(np.uint8)
            result["augmented"] = Image.fromarray(img_array)
        
        return result 