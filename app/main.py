"""
Main FastAPI application module.
This module sets up the FastAPI application and includes all routers.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .api.routes import router
from .ui.templates import (
    generate_tab_nav,
    generate_content_section
)

# Create FastAPI app
app = FastAPI(title="Data Processing Application")

# Mount static files
app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/ui/templates")

# Include API router
app.include_router(router)

@app.get("/")
async def home(request: Request):
    """Render the home page with the data processing interface."""
    # Generate tab navigation
    tab_nav = generate_tab_nav()
    
    # Generate content sections for each data type
    text_content = generate_content_section('text', is_active=True)
    image_content = generate_content_section('image')
    audio_content = generate_content_section('audio')
    three_d_content = generate_content_section('three-d')
    
    # Render template with all components
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tab_nav": tab_nav,
            "text_content": text_content,
            "image_content": image_content,
            "audio_content": audio_content,
            "three_d_content": three_d_content
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 