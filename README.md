# Data Processing Application

A modular web application for processing different types of data (text, images, audio, and 3D models) with preprocessing and augmentation capabilities.

## Project Structure

```
assignment/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API route definitions
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Core configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base/
│   │   │   ├── __init__.py
│   │   │   └── processor.py # Base processor interface
│   │   ├── data/
│   │   │   ├── __init__.py
│   │   │   ├── text.py      # Text data model and processor
│   │   │   ├── image.py     # Image data model and processor
│   │   │   ├── audio.py     # Audio data model and processor
│   │   │   └── three_d.py   # 3D model data model and processor
│   │   └── config/
│   │       ├── __init__.py
│   │       └── settings.py   # Configuration models
│   ├── services/
│   │   ├── __init__.py
│   │   └── processors.py     # Processing service implementations
│   ├── static/              # Static files (CSS, JS, images)
│   └── templates/           # HTML templates
├── data/                    # Processed data storage
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Models

The application uses a modular model structure to handle different types of data processing:

### Base Models
- `BaseProcessor`: Abstract base class that defines the interface for all data processors

### Data Models
1. **Text Processing**
   - `TextData`: Data class for text content
   - `TextProcessor`: Processor for text data with features:
     - Preprocessing: cleaning, lowercase, stopwords, stemming, lemmatization
     - Augmentation: synonym replacement, word insertion

2. **Image Processing**
   - `ImageData`: Data class for image content
   - `ImageProcessor`: Processor for image data with features:
     - Preprocessing: resizing, normalization
     - Augmentation: flipping, jitter

3. **Audio Processing**
   - `AudioData`: Data class for audio content
   - `AudioProcessor`: Processor for audio data with features:
     - Preprocessing: resampling
     - Augmentation: noise, time stretching, pitch shifting

4. **3D Model Processing**
   - `ThreeDData`: Data class for 3D model content
   - `ThreeDProcessor`: Processor for 3D models with features:
     - Preprocessing: normalization, centering
     - Augmentation: scaling, noise

### Configuration Models
- `ProcessingConfig`: Main configuration class
- `ImageConfig`: Image processing parameters
- `AudioConfig`: Audio processing parameters
- `ThreeDConfig`: 3D model processing parameters

## Features

- **Modular Design**: Each data type has its own model and processor
- **Type Safety**: Uses Python type hints and dataclasses
- **Extensible**: Easy to add new data types and processing features
- **Configuration**: Flexible configuration system for processing parameters
- **Web Interface**: User-friendly web interface for data processing

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python -m assignment.app.main
   ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000`
2. Select the type of data you want to process
3. Upload your data file
4. Choose preprocessing and augmentation options
5. Click "Process" to see the results

## Dependencies

- FastAPI: Web framework
- Pydantic: Data validation
- Pillow: Image processing
- Librosa: Audio processing
- Trimesh: 3D model processing
- NLTK: Text processing
- NumPy: Numerical operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 