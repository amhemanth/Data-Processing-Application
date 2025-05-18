from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class ImageConfig:
    """Configuration for image processing.
    
    Attributes:
        resize_size: Target size for image resizing (width, height)
        normalize_range: Range for normalization [min, max]
        jitter_level: Standard deviation for jitter noise
    """
    resize_size: Tuple[int, int] = (224, 224)
    normalize_range: Tuple[float, float] = (0.0, 1.0)
    jitter_level: float = 25.0

@dataclass
class AudioConfig:
    """Configuration for audio processing.
    
    Attributes:
        target_sr: Target sample rate for resampling
        noise_level: Standard deviation for noise addition
        stretch_range: Range for time stretching [min, max]
        pitch_range: Range for pitch shifting [min, max]
    """
    target_sr: int = 22050
    noise_level: float = 0.005
    stretch_range: Tuple[float, float] = (0.8, 1.2)
    pitch_range: Tuple[int, int] = (-4, 5)

@dataclass
class ThreeDConfig:
    """Configuration for 3D model processing.
    
    Attributes:
        scale_range: Range for random scaling [min, max]
        noise_level: Standard deviation for vertex noise
    """
    scale_range: Tuple[float, float] = (0.8, 1.2)
    noise_level: float = 0.01

@dataclass
class ProcessingConfig:
    """Main configuration class for all data processing.
    
    Attributes:
        image: Image processing configuration
        audio: Audio processing configuration
        three_d: 3D model processing configuration
    """
    image: ImageConfig = ImageConfig()
    audio: AudioConfig = AudioConfig()
    three_d: ThreeDConfig = ThreeDConfig()
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ProcessingConfig':
        """Create a ProcessingConfig instance from a dictionary.
        
        Args:
            config_dict: Dictionary containing configuration values
            
        Returns:
            ProcessingConfig instance
        """
        return cls(
            image=ImageConfig(**config_dict.get('image', {})),
            audio=AudioConfig(**config_dict.get('audio', {})),
            three_d=ThreeDConfig(**config_dict.get('three_d', {}))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary.
        
        Returns:
            Dictionary containing all configuration values
        """
        return {
            'image': {
                'resize_size': self.image.resize_size,
                'normalize_range': self.image.normalize_range,
                'jitter_level': self.image.jitter_level
            },
            'audio': {
                'target_sr': self.audio.target_sr,
                'noise_level': self.audio.noise_level,
                'stretch_range': self.audio.stretch_range,
                'pitch_range': self.audio.pitch_range
            },
            'three_d': {
                'scale_range': self.three_d.scale_range,
                'noise_level': self.three_d.noise_level
            }
        } 