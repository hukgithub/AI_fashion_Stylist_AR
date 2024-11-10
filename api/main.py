# api/main.py
# The backend code processes the user’s text input, generates an image based on it using VQGAN+CLIP, and returns the image as a base64 string.

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import VQGanProcessor, VQGanModel
import torch
from PIL import Image
import io
import base64

app = FastAPI()

# Load the model and processor from Hugging Face
model_name = "huggingface/VQGAN-CLIP"
processor = VQGanProcessor.from_pretrained(model_name)
model = VQGanModel.from_pretrained(model_name)

# Define the request body model
class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_outfit(prompt: Prompt):
    # Process the text input for the model
    inputs = processor(text=prompt.prompt, return_tensors="pt")

    # Generate image from the model
    with torch.no_grad():
        image_tensor = model.generate(**inputs)

    # Convert tensor to a PIL image and resize for AR
    image = Image.fromarray(image_tensor.squeeze().cpu().numpy())
    image = image.resize((512, 512))  # Resize for optimized AR
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Return the image as a base64 string
    return {"image_url": f"data:image/png;base64,{img_str}"}
