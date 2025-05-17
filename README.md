# Data Processing Application

A FastAPI-based web application that allows users to upload, preprocess, and augment different types of data files (images, audio, 3D models, and text).

## Features

- Support for multiple file types:
  - Images (.jpg, .jpeg, .png, .bmp)
  - Audio (.wav, .mp3, .ogg)
  - 3D Models (.off, .obj, .stl)
  - Text (.txt, .json, .csv)
- Interactive web interface
- Real-time data preview
- Data preprocessing capabilities
- Data augmentation features

## Preprocessing Features

### Images
- Grayscale conversion
- Resize to 224x224 pixels

### Audio
- Audio normalization
- MFCC feature extraction

### 3D Models
- Center mass alignment
- Vertex normalization

### Text
- Lowercase conversion
- Whitespace normalization

## Augmentation Features

### Images
- Random rotation (-30° to 30°)
- Random horizontal flip

### Audio
- Random noise addition
- Time stretching

### 3D Models
- Random rotation around Y-axis

### Text
- Simple word replacement
  - "the" → "a"
  - "is" → "was"
  - "are" → "were"
  - "and" → "or"

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd assignment
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

3. Using the application:
   - Click "Choose File" to select a data file
   - Click "Upload" to upload the file
   - Use the "Preprocess" button to preprocess the data
   - Use the "Augment" button to augment the data
   - View the results in the preview section

## Project Structure

```
assignment/
├── main.py              # FastAPI application
├── utils.py            # Utility functions for data processing
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   └── index.html    # Main application template
├── static/           # Static files (CSS, JS)
└── data/            # Directory for uploaded and processed files
```

## Dependencies

- FastAPI
- Uvicorn
- Pillow (PIL)
- NumPy
- SciPy
- Librosa
- Trimesh
- Python-multipart
- Jinja2

## Notes

- The application creates a `data` directory to store uploaded and processed files
- All processed files are saved with appropriate prefixes (preprocessed_, augmented_)
- The application supports real-time preview of all supported file types
- For 3D files, a download link is provided instead of direct preview

## License

This project is open source and available under the MIT License. 