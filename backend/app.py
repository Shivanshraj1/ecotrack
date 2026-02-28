from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "EcoTrack Backend Running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    label = random.choice(["Biodegradable", "Non-Biodegradable"])
    
    if label == "Biodegradable":
        details = {
            "recommended_bin": "Green",
            "eco_points": 10,
            "description": "Organic waste suitable for composting."
        }
    else:
        details = {
            "recommended_bin": "Blue",
            "eco_points": 5,
            "description": "Plastic or metal waste."
        }

    return {
        "label": label,
        "confidence": 92.5,
        "details": details
    }