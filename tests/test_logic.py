"""
Unit testing for logic module.
"""

from mylib import logic
from PIL import Image
import io

def test_predict():
    """
    Test that the predict function returns a string and that the string
    is one of the expected class names. 
    """
    img = Image.new('RGB', (10, 10), color = 'black')
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    image_bytes = byte_io.getvalue()
    
    prediction = logic.predict(image_bytes)
    assert isinstance(prediction, str), "Prediction is not a string."
    assert prediction in ["cat", "dog", "bird", "snake", "bear"], "Prediction is not in expected classes."

def test_resize():
    """Test the resize function."""
    # Create a simple black square image for testing
    img = Image.new('RGB', (50, 50), color = 'black')
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    image_bytes = byte_io.getvalue()
    
    resized_bytes = logic.resize(image_bytes, 20, 20)
    resized_img = Image.open(io.BytesIO(resized_bytes))
    
    assert resized_img.size == (20, 20), "Image was not resized to the correct dimensions."
    assert resized_img.format == 'PNG', "Resized image is not in PNG format."

