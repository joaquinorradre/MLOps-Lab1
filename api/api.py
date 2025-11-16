"""
api.py
----------------
API for image processing and prediction using FastAPI.
"""

import io
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from mylib import logic

app = FastAPI(
    title="API for Image Processing (MLOps Lab 1)",
    description="API to predict image classes and resize images.",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR.parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serves the home.html page."""
    return templates.TemplateResponse(request, "home.html")


@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to predict the class of a given image.
    Receives an image file and returns a JSON prediction.
    """
    try:
        image_bytes = await file.read()

        prediction = logic.predict(image_bytes)

        return {
            "filename": file.filename,
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}") from e

@app.post("/resize")
async def resize_endpoint(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...)
):
    """
    Endpoint to resize an image.
    Receives an image file, width, and height.
    Returns the resized image file.
    """
    try:
        image_bytes = await file.read()

        resized_bytes = logic.resize(image_bytes, width, height)

        return StreamingResponse(io.BytesIO(resized_bytes), media_type="image/png")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resizing image: {e}") from e


if __name__ == "__main__":
    uvicorn.run("api.api:app", host="0.0.0.0", port=8000, reload=True) # pragma: no cover
