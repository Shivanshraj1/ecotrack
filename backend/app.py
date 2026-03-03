from dotenv import load_dotenv
import os
import random
import razorpay
import hmac
import hashlib

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Razorpay Client Setup
razorpay_client = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

# ✅ Test Route
@app.get("/")
def home():
    return {"message": "EcoTrack Backend Running"}

# ✅ Waste Prediction Route
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

# ✅ Create Razorpay Order
@app.post("/create-order")
async def create_order(request: Request):
    body = await request.json()
    amount = body.get("amount")

    order = razorpay_client.order.create({
        "amount": amount * 100,  # convert to paise
        "currency": "INR",
        "receipt": f"receipt_{amount}"
    })

    return order

# ✅ Verify Razorpay Payment
@app.post("/verify-payment")
async def verify_payment(request: Request):
    body = await request.json()

    razorpay_order_id = body.get("razorpay_order_id")
    razorpay_payment_id = body.get("razorpay_payment_id")
    razorpay_signature = body.get("razorpay_signature")

    generated_signature = hmac.new(
        os.getenv("RAZORPAY_KEY_SECRET").encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    if generated_signature == razorpay_signature:
        return {"success": True}
    else:
        return {"success": False}