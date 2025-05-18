import numpy as np
import librosa
import soundfile as sf
import random
from typing import Dict, Any, Tuple

from ..core.config import AUDIO_CONFIG

class AudioProcessor:
    @staticmethod
    def process(audio_data: np.ndarray, sr: int, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, Tuple[np.ndarray, int]]:
        result = {
            "original": (audio_data, sr),
            "preprocessed": (audio_data, sr),
            "augmented": (audio_data, sr)
        }
        
        # Preprocessing
        if preprocessing_options.get("resample"):
            result["preprocessed"] = (librosa.resample(audio_data, orig_sr=sr, target_sr=AUDIO_CONFIG['target_sr']), 
                                    AUDIO_CONFIG['target_sr'])
        
        # Augmentation
        if augmentation_options.get("noise"):
            noise = np.random.normal(0, AUDIO_CONFIG['noise_level'], audio_data.shape)
            result["augmented"] = (audio_data + noise, sr)
        
        if augmentation_options.get("stretch"):
            rate = random.uniform(*AUDIO_CONFIG['stretch_range'])
            result["augmented"] = (librosa.effects.time_stretch(audio_data, rate=rate), sr)
        
        if augmentation_options.get("pitch"):
            n_steps = random.randint(*AUDIO_CONFIG['pitch_range'])
            result["augmented"] = (librosa.effects.pitch_shift(audio_data, sr=sr, n_steps=n_steps), sr)
        
        return result 