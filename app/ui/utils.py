"""
UI Utilities for the Data Processing Application.
This module contains helper functions for UI operations.
"""

from typing import Dict, List, Any
from .components import COMMON_UI_CONFIG

def get_active_tab(tab_id: str) -> str:
    """Get the active tab's content section ID."""
    return f"{tab_id}Content"

def get_preview_container_id(data_type: str, stage: str) -> str:
    """Get the preview container ID for a specific data type and stage."""
    return f"{data_type}{stage.capitalize()}Preview"

def get_file_input_id(data_type: str) -> str:
    """Get the file input ID for a specific data type."""
    return f"{data_type}FileInput"

def get_processing_options(data_type: str, option_type: str) -> List[Dict[str, Any]]:
    """Get processing options for a specific data type and option type."""
    from .components import (
        TEXT_UI_CONFIG,
        IMAGE_UI_CONFIG,
        AUDIO_UI_CONFIG,
        THREE_D_UI_CONFIG
    )
    
    configs = {
        'text': TEXT_UI_CONFIG,
        'image': IMAGE_UI_CONFIG,
        'audio': AUDIO_UI_CONFIG,
        'three-d': THREE_D_UI_CONFIG
    }
    
    return configs.get(data_type, {}).get(f'{option_type}_options', [])

def get_style(style_name: str) -> str:
    """Get a style from the common UI configuration."""
    return COMMON_UI_CONFIG['styles'].get(style_name, '')

def get_all_tabs() -> List[Dict[str, str]]:
    """Get all available tabs."""
    return COMMON_UI_CONFIG['tabs']

def get_preview_image_id(data_type: str, stage: str, view: str = '') -> str:
    """Get the preview image ID for a specific data type, stage, and view."""
    base_id = f"{data_type}{stage.capitalize()}"
    return f"{base_id}View{view}" if view else base_id

def get_model_viewer_id(data_type: str, stage: str) -> str:
    """Get the model viewer ID for a specific data type and stage."""
    return f"{data_type}{stage.capitalize()}Viewer" 