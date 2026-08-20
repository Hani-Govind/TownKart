from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("townkart-f5344-firebase-adminsdk-fbsvc-866e1045b4.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def search_inventory(product, budget_max=None):
    stores_ref = db.collection("stores")
    stores = stores_ref.stream()
    results = []

    for store in stores:
        store_data = store.to_dict()
        inventory_ref = (
            stores_ref.document(store.id).collection("inventory")
        )

        for item in inventory_ref.stream():
            item_data = item.to_dict()

            if item_data.get("product", "").lower() != product.lower():
                continue

            quantity = item_data.get("quantity", 0)
            price = item_data.get("price")

            if quantity <= 0 or price is None:
                continue

            if budget_max is not None and price > budget_max:
                continue

            results.append({
                "store_id": store.id,
                "store_name": store_data.get("name"),
                "latitude": store_data.get("latitude"),
                "longitude": store_data.get("longitude"),
                "product": item_data.get("product"),
                "price": price,
                "quantity": quantity,
                "unit": item_data.get("unit"),
            })

    return results

def update_inventory(store_id, product, price, quantity, unit):
    inventory_ref = (
        db.collection("stores")
        .document(store_id)
        .collection("inventory")
    )

    existing = (
        inventory_ref
        .where("product", "==", product)
        .limit(1)
        .stream()
    )
    existing_item = next(existing, None)

    data = {
        "product": product,
        "price": price,
        "quantity": quantity,
        "unit": unit,
        "updated_at": datetime.now(timezone.utc),
    }

    if existing_item:
        inventory_ref.document(existing_item.id).update(data)
        return existing_item.id

    _, new_ref = inventory_ref.add(data)
    return new_ref.id