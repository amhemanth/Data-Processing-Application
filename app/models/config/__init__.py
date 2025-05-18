"""Configuration models package.

This package contains configuration models for different types of data processing:
- Image processing configuration
- Audio processing configuration
- 3D model processing configuration
"""

from .settings import ProcessingConfig, ImageConfig, AudioConfig, ThreeDConfig

__all__ = [
    'ProcessingConfig',
    'ImageConfig',
    'AudioConfig',
    'ThreeDConfig'
] 