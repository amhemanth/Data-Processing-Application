# Data Processing Application

A modular web application for processing different types of data (text, images, audio, and 3D models) with preprocessing and augmentation capabilities.

## Project Structure

```
Data Processing Application/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API route definitions
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Core configuration and global data
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base/
│   │   │   └── __init__.py # Base models package (e.g., for common interfaces)
│   │   ├── data/
│   │   │   └── __init__.py # Data models package (currently placeholder)
│   │   └── config/
│   │       ├── __init__.py # Configuration models package
│   │       └── settings.py   # Application settings and configurations
│   ├── services/
│   │   ├── __init__.py # Services package
│   │   ├── audio_processor.py # Audio processing service logic
│   │   ├── image_processor.py # Image processing service logic
│   │   ├── text_processor.py  # Text processing service logic
│   │   └── three_d_processor.py # 3D model processing service logic
│   └── ui/          # User interface components and logic
│       ├── __init__.py # UI package
│       ├── components.py # Reusable UI components (currently unused)
│       ├── templates.py # Python functions for rendering HTML templates
│       ├── utils.py     # UI related utility functions
│       ├── static/      # Static assets served to the browser
│       │   ├── css/
│       │   │   └── style.css # Custom CSS styles
│       │   └── js/
│       │       └── main.js # Main JavaScript for UI interaction
│       └── templates/   # HTML template files
│           └── index.html
├── data/                    # Storage for uploaded and processed data files
├── .git/                    # Git version control data
├── README.md               # Project documentation
├── requirements.txt         # Python package dependencies
└── .gitignore       # Files and directories ignored by Git
```

## Features

-   **Modular Design**: Organized structure with clear separation of concerns.
-   **Supported Data Types**: Text, Image, Audio, and 3D Models.
-   **Preprocessing and Augmentation**: Various techniques available for each data type.
-   **Web Interface**: User-friendly UI for interacting with the processing capabilities.

## Supported Processing Options

### Text Processing
-   **Preprocessing**: Text Cleaning, Remove Stop Words, Downcase, Stemming, Lemmatization, Tokenization
-   **Augmentation**: Synonym Replacement, Random Insertion

### Image Processing
-   **Preprocessing**: Resizing, Normalization
-   **Augmentation**: Random Rotation, Random Horizontal Flip, Color Jitter

### Audio Processing
-   **Preprocessing**: Resampling
-   **Augmentation**: Adding Background Noise, Time Stretching, Pitch Shifting

### 3D Model Processing
-   **Preprocessing**: Normalize, Centering
-   **Augmentation**: Random Rotation, Scaling, Noise

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory_name> # e.g., cd data-processing-application
    ```
2.  Create and activate a virtual environment (recommended):
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Download necessary NLTK data (for text processing):
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    ```

## Usage

1.  Run the application from the root directory (e.g., `Data Processing Application/`):
    ```bash
    python -m app.main
    ```
2.  Open your web browser and navigate to `http://127.0.0.1:8000`
3.  Select the type of data you want to process using the tabs.
4.  Upload your data file using the file input.
5.  Choose the desired preprocessing and augmentation options by checking the boxes.
6.  Click the "Process [Data Type]" button.
7.  View the Original, Preprocessed, and Augmented data in the preview section.

## Dependencies

-   FastAPI: Web framework for building APIs
-   Uvicorn: ASGI server to run the FastAPI application
-   Python-Multipart: For handling form data, including file uploads
-   Jinja2: Templating engine for rendering HTML
-   NumPy: Fundamental package for scientific computing with Python
-   Pillow: Python Imaging Library (PIL) fork for image processing
-   Librosa: Python library for audio analysis
-   Soundfile: Library for reading and writing audio files
-   Trimesh: Library for loading and using triangular meshes
-   NLTK: Natural Language Toolkit for text processing
-   Scikit-learn: (Currently imported but may not be explicitly used in processing logic - review needed if errors arise)
-   Three.js (via CDN): JavaScript 3D library for rendering models
-   Wavesurfer.js (via CDN): JavaScript audio waveform and spectrogram visualizer

## Contributing

Feel free to contribute to the project by opening issues or pull requests on the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 