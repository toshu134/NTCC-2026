import os
from app.llm_agent import faiss_index, metadata 
import json
import fitz  
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import AutoTokenizer, AutoProcessor, AutoModel
from sentence_transformers import SentenceTransformer
import faiss
from PIL import Image
import numpy as np
from io import BytesIO

PDF_DIR = "./data"
INDEX_PATH = "./vector_store/faiss_store.index"
METADATA_PATH = "./vector_store/metadata.json"


embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def generate_image_caption_blip(img: Image.Image) -> str:
    inputs = blip_processor(images=img, return_tensors="pt")
   
    with torch.no_grad():
        out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption

def process_pdf(file_path):
    print(f"\n🚀 Processing: {file_path}")
    doc = fitz.open(file_path)
    chunks = []

    for i, page in enumerate(doc):
        text = page.get_text()

        images = page.get_images(full=True)
        image_captions = []

        for img_index, img in enumerate(images):
            try:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(BytesIO(image_bytes)).convert("RGB")

                # 🔍 Use BLIP to caption image
                caption = generate_image_caption_blip(image)
                image_captions.append(f"[Figure {img_index+1}] {caption}")

            except Exception as e:
                print(f"Error processing image on page {i+1}: {e}")
                continue

        # Combine
        full_text = text + "\n\nImage Captions:\n" + "\n".join(image_captions)

        if len(full_text.strip()) > 50:
            chunks.append({
                "page": i + 1,
                "content": full_text
            })

    # Embed and index
    for chunk in chunks:
        embedding = embedding_model.encode(chunk["content"]).astype("float32")
        faiss_index.add(np.array([embedding]))
        metadata.append({
            "file": os.path.basename(file_path),
            "page": chunk["page"],
            "content": chunk["content"]
        })

    # Save index + metadata
    faiss.write_index(faiss_index, INDEX_PATH)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Done: {file_path}, Pages processed: {len(chunks)}")
    print(f"🧠 Sample embedding: {embedding[:5]}...")
