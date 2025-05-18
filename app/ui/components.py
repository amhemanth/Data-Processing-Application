"""
UI Components for the Data Processing Application.
This module contains reusable UI components and their configurations.
"""

# Text Processing UI Configuration
TEXT_UI_CONFIG = {
    'preprocessing_options': [
        {'id': 'textCleaning', 'label': 'Text Cleaning', 'value': 'cleaning'},
        {'id': 'textStopwords', 'label': 'Remove Stop Words', 'value': 'stopwords'},
        {'id': 'textLowercase', 'label': 'Lowercase', 'value': 'lowercase'},
        {'id': 'textStemming', 'label': 'Stemming', 'value': 'stemming'},
        {'id': 'textLemmatization', 'label': 'Lemmatization', 'value': 'lemmatization'},
        {'id': 'textTokenization', 'label': 'Tokenization', 'value': 'tokenization'}
    ],
    'augmentation_options': [
        {'id': 'textSynonym', 'label': 'Synonym Replacement', 'value': 'synonym'},
        {'id': 'textInsertion', 'label': 'Random Insertion', 'value': 'insertion'}
    ]
}

# Image Processing UI Configuration
IMAGE_UI_CONFIG = {
    'preprocessing_options': [
        {'id': 'imageResize', 'label': 'Resizing', 'value': 'resize'},
        {'id': 'imageNormalize', 'label': 'Normalization', 'value': 'normalize'}
    ],
    'augmentation_options': [
        {'id': 'imageFlip', 'label': 'Random Horizontal Flip', 'value': 'flip'},
        {'id': 'imageJitter', 'label': 'Color Jitter', 'value': 'jitter'}
    ]
}

# Audio Processing UI Configuration
AUDIO_UI_CONFIG = {
    'preprocessing_options': [
        {'id': 'audioResample', 'label': 'Resampling', 'value': 'resample'}
    ],
    'augmentation_options': [
        {'id': 'audioNoise', 'label': 'Add Background Noise', 'value': 'noise'},
        {'id': 'audioStretch', 'label': 'Time Stretching', 'value': 'stretch'},
        {'id': 'audioPitch', 'label': 'Pitch Shifting', 'value': 'pitch'}
    ]
}

# 3D Processing UI Configuration
THREE_D_UI_CONFIG = {
    'preprocessing_options': [
        {'id': '3dNormalize', 'label': 'Normalize', 'value': 'normalize'},
        {'id': '3dCenter', 'label': 'Centering', 'value': 'center'}
    ],
    'augmentation_options': [
        {'id': '3dScale', 'label': 'Scaling', 'value': 'scale'},
        {'id': '3dNoise', 'label': 'Noise', 'value': 'noise'}
    ]
}

# Common UI Configuration
COMMON_UI_CONFIG = {
    'styles': {
        'content_section': 'display: none;',
        'content_section_active': 'display: block;',
        'preview_container': 'border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;',
        'preview_image': 'max-width: 100%; height: auto;',
        'waveform': 'width: 100%; height: 200px; background: #f5f5f5; margin: 10px 0;',
        'model_viewer': 'width: 100%; height: 300px; background: #f5f5f5; margin: 10px 0;'
    },
    'tabs': [
        {'id': 'text', 'label': 'Text'},
        {'id': 'image', 'label': 'Image'},
        {'id': 'audio', 'label': 'Audio'},
        {'id': 'three-d', 'label': '3D'}
    ]
} 