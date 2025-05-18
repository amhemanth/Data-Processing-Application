"""
UI Templates for the Data Processing Application.
This module contains functions for generating HTML templates.
"""

from typing import List, Dict, Any
from .utils import (
    get_active_tab,
    get_preview_container_id,
    get_file_input_id,
    get_processing_options,
    get_style,
    get_all_tabs,
    get_preview_image_id,
    get_model_viewer_id
)

def generate_tab_nav() -> str:
    """Generate the tab navigation HTML."""
    tabs = get_all_tabs()
    nav_items = []
    
    for i, tab in enumerate(tabs):
        active_class = 'active' if i == 0 else ''
        nav_items.append(f'''
            <li class="nav-item">
                <a class="nav-link {active_class}" id="{tab['id']}-tab" data-bs-toggle="tab" 
                   href="#{get_active_tab(tab['id'])}" role="tab" 
                   aria-controls="{get_active_tab(tab['id'])}" 
                   aria-selected="{str(i == 0).lower()}">
                    {tab['label']}
                </a>
            </li>
        ''')
    
    return f'''
        <ul class="nav nav-tabs" id="dataTypeTabs" role="tablist">
            {''.join(nav_items)}
        </ul>
    '''

def generate_content_section(data_type: str, is_active: bool = False) -> str:
    """Generate a content section for a specific data type."""
    active_class = 'active show' if is_active else ''
    style = get_style('content_section_active' if is_active else 'content_section')
    
    preprocessing_options = get_processing_options(data_type, 'preprocessing')
    augmentation_options = get_processing_options(data_type, 'augmentation')
    
    return f'''
        <div class="tab-pane fade {active_class}" id="{get_active_tab(data_type)}" 
             role="tabpanel" aria-labelledby="{data_type}-tab" style="{style}">
            <div class="container mt-4">
                <div class="row">
                    <div class="col-md-6">
                        <h5>Upload {data_type.capitalize()}</h5>
                        <input type="file" class="form-control" id="{get_file_input_id(data_type)}" 
                               accept="{get_file_accept_types(data_type)}">
                        
                        <div class="mt-3">
                            <h6>Preprocessing Options</h6>
                            {generate_checkboxes(preprocessing_options)}
                        </div>
                        
                        <div class="mt-3">
                            <h6>Augmentation Options</h6>
                            {generate_checkboxes(augmentation_options)}
                        </div>
                        
                        <button class="btn btn-primary mt-3" onclick="process{data_type.capitalize()}()">
                            Process
                        </button>
                    </div>
                    
                    <div class="col-md-6">
                        {generate_preview_section(data_type)}
                    </div>
                </div>
            </div>
        </div>
    '''

def generate_checkboxes(options: List[Dict[str, Any]]) -> str:
    """Generate checkboxes for processing options."""
    checkboxes = []
    for option in options:
        checkboxes.append(f'''
            <div class="form-check">
                <input class="form-check-input" type="checkbox" 
                       id="{option['id']}" value="{option['value']}">
                <label class="form-check-label" for="{option['id']}">
                    {option['label']}
                </label>
            </div>
        ''')
    return ''.join(checkboxes)

def generate_preview_section(data_type: str) -> str:
    """Generate the preview section for a specific data type."""
    if data_type == 'three-d':
        return generate_3d_preview_section()
    elif data_type == 'audio':
        return generate_audio_preview_section()
    else:
        return generate_basic_preview_section(data_type)

def generate_basic_preview_section(data_type: str) -> str:
    """Generate a basic preview section for text and image data types."""
    return f'''
        <h5>Preview</h5>
        <div class="row">
            <div class="col-md-4">
                <h6>Original</h6>
                <div id="{get_preview_container_id(data_type, 'original')}" 
                     class="preview-container" style="{get_style('preview_container')}">
                    <img id="{get_preview_image_id(data_type, 'original')}" 
                         class="img-fluid" alt="Original {data_type}">
                </div>
            </div>
            <div class="col-md-4">
                <h6>Preprocessed</h6>
                <div id="{get_preview_container_id(data_type, 'preprocessed')}" 
                     class="preview-container" style="{get_style('preview_container')}">
                    <img id="{get_preview_image_id(data_type, 'preprocessed')}" 
                         class="img-fluid" alt="Preprocessed {data_type}">
                </div>
            </div>
            <div class="col-md-4">
                <h6>Augmented</h6>
                <div id="{get_preview_container_id(data_type, 'augmented')}" 
                     class="preview-container" style="{get_style('preview_container')}">
                    <img id="{get_preview_image_id(data_type, 'augmented')}" 
                         class="img-fluid" alt="Augmented {data_type}">
                </div>
            </div>
        </div>
    '''

def generate_audio_preview_section() -> str:
    """Generate the preview section for audio data type."""
    return '''
        <h5>Preview</h5>
        <div class="row">
            <div class="col-md-4">
                <h6>Original</h6>
                <div id="audioOriginalPreview" class="preview-container" style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div id="audioOriginalWaveform" class="waveform"></div>
                    <div id="audioOriginalSpectrogram" class="waveform"></div>
                </div>
            </div>
            <div class="col-md-4">
                <h6>Preprocessed</h6>
                <div id="audioPreprocessedPreview" class="preview-container" style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div id="audioPreprocessedWaveform" class="waveform"></div>
                    <div id="audioPreprocessedSpectrogram" class="waveform"></div>
                </div>
            </div>
            <div class="col-md-4">
                <h6>Augmented</h6>
                <div id="audioAugmentedPreview" class="preview-container" style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div id="audioAugmentedWaveform" class="waveform"></div>
                    <div id="audioAugmentedSpectrogram" class="waveform"></div>
                </div>
            </div>
        </div>
    '''

def generate_3d_preview_section() -> str:
    """Generate the preview section for 3D data type."""
    return '''
        <h5>Preview</h5>
        <div class="row">
            <div class="col-md-4">
                <h6>Original 3D Model</h6>
                <div id="three-dOriginalPreview" class="preview-container" style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div id="three-dOriginalViewer" class="model-viewer"></div>
                    <div class="row mt-2">
                        <div class="col-4">
                            <img id="three-dOriginalView0" class="img-fluid" alt="Front view">
                        </div>
                        <div class="col-4">
                            <img id="three-dOriginalView1" class="img-fluid" alt="Side view">
                        </div>
                        <div class="col-4">
                            <img id="three-dOriginalView2" class="img-fluid" alt="Top view">
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <h6>Preprocessed 3D Model</h6>
                <div id="three-dPreprocessedPreview" class="preview-container" style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div id="three-dPreprocessedViewer" class="model-viewer"></div>
                    <div class="row mt-2">
                        <div class="col-4">
                            <img id="three-dPreprocessedView0" class="img-fluid" alt="Front view">
                        </div>
                        <div class="col-4">
                            <img id="three-dPreprocessedView1" class="img-fluid" alt="Side view">
                        </div>
                        <div class="col-4">
                            <img id="three-dPreprocessedView2" class="img-fluid" alt="Top view">
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <h6>Augmented 3D Model</h6>
                <div id="three-dAugmentedPreview" class="preview-container" style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div id="three-dAugmentedViewer" class="model-viewer"></div>
                    <div class="row mt-2">
                        <div class="col-4">
                            <img id="three-dAugmentedView0" class="img-fluid" alt="Front view">
                        </div>
                        <div class="col-4">
                            <img id="three-dAugmentedView1" class="img-fluid" alt="Side view">
                        </div>
                        <div class="col-4">
                            <img id="three-dAugmentedView2" class="img-fluid" alt="Top view">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    '''

def get_file_accept_types(data_type: str) -> str:
    """Get the accepted file types for a specific data type."""
    accept_types = {
        'text': '.txt,.csv,.json',
        'image': '.jpg,.jpeg,.png,.gif',
        'audio': '.wav,.mp3,.ogg',
        'three-d': '.obj,.stl,.ply,.off'
    }
    return accept_types.get(data_type, '') 