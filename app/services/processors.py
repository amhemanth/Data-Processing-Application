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
from typing import Dict, Any, Tuple

from ..core.config import IMAGE_CONFIG, AUDIO_CONFIG, THREE_D_CONFIG

class TextProcessor:
    @staticmethod
    def process(text: str, preprocessing_options: Dict[str, bool], augmentation_options: Dict[str, bool]) -> Dict[str, str]:
        result = {"original": text, "preprocessed": text, "augmented": text}
        
        # Preprocessing
        if preprocessing_options.get("cleaning"):
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
                if random.random() < 0.3:
                    synsets = wordnet.synsets(word)
                    if synsets:
                        synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas()]
                        if synonyms:
                            augmented_words.append(random.choice(synonyms))
            result["augmented"] = ' '.join(augmented_words)
        
        return result

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