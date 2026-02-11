

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load processor and model (pretrained weights)
model_name = "Salesforce/blip-image-captioning-base"
processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

# Load your image
image = Image.open("C://Users//Arnav Singh//OneDrive//Desktop//stocastic//Screenshot 2024-05-11 141528.png").convert("RGB")

# Prepare inputs
inputs = processor(image, return_tensors="pt")

# Generate caption (use model.generate for text generation)
out = model.generate(**inputs)

# Decode generated tokens to text
caption = processor.decode(out[0], skip_special_tokens=True)

print("Caption:", caption)
