import numpy as np
import trimesh
import random
from typing import Dict, Any

from ..core.config import THREE_D_CONFIG

class ThreeDProcessor:
    @staticmethod
    def process(mesh: trimesh.Trimesh, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, trimesh.Trimesh]:
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
            scale_factor = np.random.uniform(*THREE_D_CONFIG['scale_range'])
            result["augmented"].vertices = result["preprocessed"].vertices * scale_factor
        
        if augmentation_options.get("noise"):
            noise = np.random.normal(0, THREE_D_CONFIG['noise_level'], result["preprocessed"].vertices.shape)
            result["augmented"].vertices = result["preprocessed"].vertices + noise
        
        return result 