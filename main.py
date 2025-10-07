from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
import json
from pathlib import Path
import html

# JSON Path
JSON_file = Path(__file__).parent / "products.json"

# Load data with error handling
try:
    with open(JSON_file, "r", encoding="utf-8") as f:
        products = json.load(f)
except FileNotFoundError:
    products = []
    print(f"Warning: {JSON_file} not found. Starting with an empty product list.")
except json.JSONDecodeError:
    products = []
    print(f"Warning: Failed to decode JSON from {JSON_file}. Starting with an empty product list.")

# Create API app with fastapi framework
app = FastAPI(title="Aggrega API")

# function for styling the API output
def render_products_html(items: List[dict]) -> str:
    # Convert the list of products to a styled HTML table.
    if not items:
        headers_list = ["Product"]
        headers = "<th>Product</th>"
        body = f"<tr><td colspan=\"{len(headers_list)}\">No products available.</td></tr>"
    else:
        headers_list = list(items[0].keys())
        headers = "".join(f"<th>{html.escape(str(key))}</th>" for key in headers_list)
        rows = []
        for product in items:
            cells = []
            for key in headers_list:
                value = product.get(key, "")
                cells.append(f"<td>{html.escape(str(value))}</td>")
            rows.append(f"<tr>{''.join(cells)}</tr>")
        body = "".join(rows)

    # Return the document with styling
    return f"""<!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\" />
        <title>Aggrega Products</title>
        <style>
            root {{
                color-scheme: light dark;
                font-family: system-ui, sans-serif;
            }}

            body {{
                margin: 2rem;
                background: #f5f5f5;
                color: #222;
            }}

            h1 {{
                margin-bottom: 1rem;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
                border-radius: 12px;
                overflow: hidden;
            }}

            thead {{
                background: #FFD400;
                color: black;
            }}

            th, td {{
                padding: 0.75rem 1rem;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                text-align: left;
            }}

            tbody tr:nth-child(even) {{
                background: rgba(75, 108, 183, 0.08);
            }}

            tbody tr:hover {{
                background: rgba(24, 40, 72, 0.1);
            }}

            @media (prefers-color-scheme: dark) {{
                body {{
                    background: #121212;
                    color: #eee;
                }}
                table {{
                    background: #1f1f1f;
                }}
                th, td {{
                    border-bottom-color: rgba(255, 255, 255, 0.08);
                }}
            }}
        </style>
    </head>
    <body>
        <h1>Aggrega Products</h1>
        <table>
            <thead>
                <tr>{headers}</tr>
            </thead>
            <tbody>
                {body}
            </tbody>
        </table>
    </body>
    </html>
    """

# Utility to keep responses sorted
def sort_products_by_id(items: List[dict]) -> List[dict]:
    return sorted(items, key=lambda product: product.get("Id", float("inf")))

def sort_products_by_price(items: List[dict]) -> List[dict]:
    return sorted(items, key=lambda product: product.get("Price", float("inf")))

# Show all products in a styled HTML table
@app.get("/products", response_class=HTMLResponse)
def get_products_styled() -> HTMLResponse:
    return HTMLResponse(content=render_products_html(sort_products_by_id(products)))

# Show products matching a specific ID using the same styled table
@app.get("/products/{product_id}", response_class=HTMLResponse)
def get_product(product_id: int) -> HTMLResponse:
    matched_products = [p for p in products if p.get("Id") == product_id]
    if not matched_products:
        raise HTTPException(status_code=404, detail={"error": "Product not found"})
    return HTMLResponse(content=render_products_html(sort_products_by_price(matched_products)))
