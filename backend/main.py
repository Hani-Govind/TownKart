from fastapi import FastAPI
from pydantic import BaseModel

from ai.query_parser import parse_customer_query
from ai.product_normalizer import normalize_product
from ai.merchant_parser import parse_merchant_message
from firebase_service import search_inventory, update_inventory
from location_service import calculate_distance
from ml.ranker import predict_match
from recommendation_service import generate_explanation

app = FastAPI(title="TownKart AI API")


class SearchQuery(BaseModel):
    query: str
    latitude: float
    longitude: float


class MerchantMessage(BaseModel):
    store_id: str
    message: str


@app.get("/")
def root():
    return {"message": "TownKart AI API is running"}


@app.post("/ai/parse-query")
def parse_query(data: SearchQuery):
    parsed = parse_customer_query(data.query)

    if parsed.get("product"):
        parsed["canonical_product"] = normalize_product(
            parsed["product"]
        )

    return {"success": True, "data": parsed}


@app.post("/search")
def search(data: SearchQuery):
    parsed = parse_customer_query(data.query)

    product = parsed.get("product")
    if product:
        product = normalize_product(product)

    results = search_inventory(
        product=product,
        budget_max=parsed.get("budget_max"),
    )

    nearby_results = []

    for result in results:
        if result.get("latitude") is None or result.get("longitude") is None:
            continue

        distance = calculate_distance(
            data.latitude,
            data.longitude,
            result["latitude"],
            result["longitude"],
        )

        result["distance_km"] = round(distance, 2)

        if distance <= 5:
            nearby_results.append(result)

    for result in nearby_results:
        result["match_score"] = predict_match(
            distance_km=result["distance_km"],
            price=result["price"],
            budget=parsed.get("budget_max"),
            stock=result["quantity"],
            required_quantity=parsed.get("quantity"),
        )

        result["explanation"] = generate_explanation(
            result, parsed
        )

    nearby_results.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return {
        "success": True,
        "query": parsed,
        "results": nearby_results,
    }


@app.post("/merchant/update")
def merchant_update(data: MerchantMessage):
    parsed = parse_merchant_message(data.message)

    product = parsed.get("product")
    price = parsed.get("price")
    quantity = parsed.get("quantity")
    unit = parsed.get("unit")

    if product:
        product = normalize_product(product)

    if not product:
        return {
            "success": False,
            "message": "Could not identify the product.",
        }

    if price is None:
        return {
            "success": False,
            "message": "Please provide the price.",
        }

    if quantity is None:
        return {
            "success": False,
            "message": "Please provide the quantity.",
        }

    item_id = update_inventory(
        store_id=data.store_id,
        product=product,
        price=price,
        quantity=quantity,
        unit=unit,
    )

    return {
        "success": True,
        "message": "Inventory updated successfully.",
        "product": product,
        "price": price,
        "quantity": quantity,
        "unit": unit,
        "item_id": item_id,
    }
