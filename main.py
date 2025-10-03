from fastapi import FastAPI, HTTPException
from typing import List
import json
from pathlib import Path

# Pad naar je JSON
DATA_PATH = Path(__file__).parent / "products.json"

# Data inladen
with open(DATA_PATH, "r", encoding="utf-8") as f:
    products = json.load(f)

# API aanmaken
app = FastAPI(title="Aggrega API")

@app.get("/products")
def get_products() -> List[dict]:
    """Alle producten ophalen"""
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    """Eén product ophalen via ID"""
    for p in products:
        if p["Id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

