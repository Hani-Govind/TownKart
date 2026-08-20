from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials, firestore


# =========================================================
# FIREBASE CONNECTION
# =========================================================

CREDENTIAL_FILE = "townkart-f5344-firebase-adminsdk-fbsvc-866e1045b4.json"

cred = credentials.Certificate(CREDENTIAL_FILE)

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

db = firestore.client()


# =========================================================
# PERAMBALUR DEMO STORES
# =========================================================

stores = [
    {
        "id": "store_001",
        "name": "Akshaya Super Market",
        "city": "Perambalur",
        "latitude": 11.2345,
        "longitude": 78.8800,
    },
    {
        "id": "store_002",
        "name": "Aadhirai Mart",
        "city": "Perambalur",
        "latitude": 11.2360,
        "longitude": 78.8820,
    },
    {
        "id": "store_003",
        "name": "GRAND SUPER MARKET",
        "city": "Perambalur",
        "latitude": 11.2325,
        "longitude": 78.8775,
    },
    {
        "id": "store_004",
        "name": "Mahalakshmi Super Market",
        "city": "Perambalur",
        "latitude": 11.2380,
        "longitude": 78.8850,
    },
    {
        "id": "store_005",
        "name": "Sri Namagal Stationery & Fancy Store",
        "city": "Perambalur",
        "latitude": 11.2315,
        "longitude": 78.8810,
    },
    {
        "id": "store_006",
        "name": "BAMA BOOK SHOP",
        "city": "Perambalur",
        "latitude": 11.2355,
        "longitude": 78.8785,
    },
    {
        "id": "store_007",
        "name": "SIMS Footwear and Apparel",
        "city": "Perambalur",
        "latitude": 11.2330,
        "longitude": 78.8840,
    },
    {
        "id": "store_008",
        "name": "SHOE WORLD",
        "city": "Perambalur",
        "latitude": 11.2370,
        "longitude": 78.8805,
    },
    {
        "id": "store_009",
        "name": "BABY'S WORLD AND GIFTS",
        "city": "Perambalur",
        "latitude": 11.2305,
        "longitude": 78.8830,
    },
    {
        "id": "store_010",
        "name": "KUMAR FANCY STORE",
        "city": "Perambalur",
        "latitude": 11.2340,
        "longitude": 78.8860,
    },
]


# =========================================================
# INVENTORY
#
# Format:
# product, category, price, quantity, unit
#
# Prices and quantities are SYNTHETIC DEMO DATA.
# =========================================================

inventory = {

    # =====================================================
    # SUPERMARKET 001
    # =====================================================

    "store_001": [
        ("mango", "fruits", 120, 18, "kg"),
        ("apple", "fruits", 180, 12, "kg"),
        ("banana", "fruits", 55, 30, "kg"),
        ("orange", "fruits", 100, 20, "kg"),
        ("grapes", "fruits", 140, 15, "kg"),

        ("tomato", "vegetables", 40, 25, "kg"),
        ("potato", "vegetables", 45, 35, "kg"),
        ("onion", "vegetables", 50, 30, "kg"),
        ("carrot", "vegetables", 70, 18, "kg"),
        ("beans", "vegetables", 80, 12, "kg"),

        ("rice", "groceries", 65, 40, "kg"),
        ("wheat", "groceries", 55, 25, "kg"),
        ("sugar", "groceries", 48, 35, "kg"),
        ("milk", "groceries", 60, 25, "litre"),
        ("eggs", "groceries", 7, 120, "piece"),

        ("jasmine flower", "flowers", 80, 20, "100g"),
        ("rose", "flowers", 100, 15, "100g"),
    ],


    # =====================================================
    # SUPERMARKET 002
    # =====================================================

    "store_002": [
        ("mango", "fruits", 105, 22, "kg"),
        ("apple", "fruits", 170, 15, "kg"),
        ("banana", "fruits", 50, 35, "kg"),
        ("orange", "fruits", 95, 18, "kg"),
        ("watermelon", "fruits", 35, 20, "kg"),

        ("tomato", "vegetables", 35, 40, "kg"),
        ("potato", "vegetables", 42, 30, "kg"),
        ("onion", "vegetables", 48, 35, "kg"),
        ("cabbage", "vegetables", 45, 18, "kg"),
        ("cauliflower", "vegetables", 70, 15, "kg"),

        ("rice", "groceries", 62, 50, "kg"),
        ("wheat", "groceries", 52, 30, "kg"),
        ("sugar", "groceries", 46, 40, "kg"),
        ("milk", "groceries", 58, 30, "litre"),
        ("eggs", "groceries", 6, 150, "piece"),

        ("rose", "flowers", 120, 15, "100g"),
        ("jasmine flower", "flowers", 75, 20, "100g"),
    ],


    # =====================================================
    # SUPERMARKET 003
    # =====================================================

    "store_003": [
        ("mango", "fruits", 130, 15, "kg"),
        ("apple", "fruits", 190, 10, "kg"),
        ("banana", "fruits", 60, 25, "kg"),
        ("orange", "fruits", 110, 16, "kg"),
        ("grapes", "fruits", 150, 12, "kg"),

        ("tomato", "vegetables", 42, 20, "kg"),
        ("potato", "vegetables", 48, 25, "kg"),
        ("onion", "vegetables", 52, 20, "kg"),
        ("carrot", "vegetables", 75, 15, "kg"),
        ("beans", "vegetables", 85, 10, "kg"),

        ("rice", "groceries", 68, 30, "kg"),
        ("sugar", "groceries", 50, 25, "kg"),
        ("milk", "groceries", 62, 20, "litre"),
        ("eggs", "groceries", 7, 100, "piece"),

        ("marigold", "flowers", 60, 25, "100g"),
        ("jasmine flower", "flowers", 85, 18, "100g"),
    ],


    # =====================================================
    # SUPERMARKET 004
    # =====================================================

    "store_004": [
        ("mango", "fruits", 115, 25, "kg"),
        ("apple", "fruits", 175, 15, "kg"),
        ("banana", "fruits", 52, 40, "kg"),
        ("orange", "fruits", 98, 20, "kg"),
        ("grapes", "fruits", 135, 18, "kg"),

        ("tomato", "vegetables", 38, 35, "kg"),
        ("potato", "vegetables", 40, 40, "kg"),
        ("onion", "vegetables", 45, 35, "kg"),
        ("carrot", "vegetables", 65, 20, "kg"),
        ("beans", "vegetables", 75, 15, "kg"),

        ("rice", "groceries", 60, 55, "kg"),
        ("wheat", "groceries", 50, 35, "kg"),
        ("sugar", "groceries", 45, 50, "kg"),
        ("milk", "groceries", 58, 35, "litre"),
        ("eggs", "groceries", 6, 180, "piece"),

        ("jasmine flower", "flowers", 75, 30, "100g"),
        ("rose", "flowers", 110, 20, "100g"),
    ],


    # =====================================================
    # STATIONERY 005
    # =====================================================

    "store_005": [
        ("notebook", "stationery", 45, 80, "piece"),
        ("pen", "stationery", 8, 200, "piece"),
        ("pencil", "stationery", 5, 250, "piece"),
        ("eraser", "stationery", 5, 150, "piece"),
        ("sharpener", "stationery", 8, 100, "piece"),
        ("geometry box", "stationery", 85, 40, "piece"),
        ("sketch pens", "stationery", 60, 35, "pack"),
        ("marker", "stationery", 30, 50, "piece"),
        ("school bag", "stationery", 500, 20, "piece"),
        ("drawing book", "stationery", 45, 50, "piece"),
        ("colour pencils", "stationery", 70, 40, "pack"),
        ("glue", "stationery", 25, 60, "piece"),
        ("file folder", "stationery", 35, 50, "piece"),
        ("stapler", "stationery", 55, 30, "piece"),
    ],


    # =====================================================
    # BOOK SHOP 006
    # =====================================================

    "store_006": [
        ("notebook", "stationery", 50, 100, "piece"),
        ("pen", "stationery", 9, 180, "piece"),
        ("pencil", "stationery", 5, 220, "piece"),
        ("eraser", "stationery", 5, 160, "piece"),
        ("sharpener", "stationery", 7, 120, "piece"),
        ("geometry box", "stationery", 90, 35, "piece"),
        ("sketch pens", "stationery", 65, 30, "pack"),
        ("marker", "stationery", 28, 55, "piece"),
        ("drawing book", "stationery", 40, 60, "piece"),
        ("colour pencils", "stationery", 75, 45, "pack"),
        ("glue", "stationery", 22, 70, "piece"),
        ("school bag", "stationery", 520, 15, "piece"),
        ("file folder", "stationery", 32, 60, "piece"),
        ("stapler", "stationery", 60, 25, "piece"),
    ],


    # =====================================================
    # FOOTWEAR 007
    # =====================================================

    "store_007": [
        ("school shoes", "footwear", 580, 20, "pair"),
        ("running shoes", "footwear", 900, 10, "pair"),
        ("sports shoes", "footwear", 1100, 8, "pair"),
        ("sandals", "footwear", 420, 25, "pair"),
        ("slippers", "footwear", 250, 30, "pair"),
        ("casual shoes", "footwear", 750, 12, "pair"),
        ("formal shoes", "footwear", 950, 7, "pair"),
        ("women sandals", "footwear", 550, 15, "pair"),
        ("kids shoes", "footwear", 480, 12, "pair"),
        ("flip flops", "footwear", 180, 25, "pair"),
        ("school belt", "accessories", 180, 20, "piece"),
        ("shoe polish", "shoe care", 90, 30, "piece"),
    ],


    # =====================================================
    # FOOTWEAR 008
    # =====================================================

    "store_008": [
        ("school shoes", "footwear", 550, 25, "pair"),
        ("running shoes", "footwear", 850, 12, "pair"),
        ("sports shoes", "footwear", 1050, 10, "pair"),
        ("sandals", "footwear", 390, 30, "pair"),
        ("slippers", "footwear", 220, 35, "pair"),
        ("casual shoes", "footwear", 700, 15, "pair"),
        ("formal shoes", "footwear", 900, 8, "pair"),
        ("women sandals", "footwear", 500, 18, "pair"),
        ("kids shoes", "footwear", 450, 15, "pair"),
        ("flip flops", "footwear", 160, 30, "pair"),
        ("school belt", "accessories", 160, 25, "piece"),
        ("shoe polish", "shoe care", 85, 35, "piece"),
    ],


    # =====================================================
    # TOY / GIFT STORE 009
    # =====================================================

    "store_009": [
        ("teddy bear", "toys", 400, 15, "piece"),
        ("doll", "toys", 300, 18, "piece"),
        ("toy car", "toys", 200, 20, "piece"),
        ("building blocks", "toys", 450, 12, "set"),
        ("puzzle", "toys", 250, 15, "piece"),
        ("remote control car", "toys", 850, 6, "piece"),
        ("toy train", "toys", 500, 8, "piece"),
        ("rubik's cube", "toys", 180, 15, "piece"),
        ("colour pencils", "stationery", 75, 30, "pack"),
        ("sketch pens", "stationery", 60, 25, "pack"),
        ("notebook", "stationery", 55, 40, "piece"),
        ("school bag", "stationery", 550, 15, "piece"),
    ],


    # =====================================================
    # FANCY / GIFT STORE 010
    # =====================================================

    "store_010": [
        ("doll", "toys", 280, 20, "piece"),
        ("teddy bear", "toys", 380, 15, "piece"),
        ("toy car", "toys", 190, 25, "piece"),
        ("building blocks", "toys", 400, 12, "set"),
        ("puzzle", "toys", 230, 15, "piece"),
        ("remote control car", "toys", 800, 7, "piece"),
        ("toy train", "toys", 480, 8, "piece"),
        ("rubik's cube", "toys", 170, 20, "piece"),
        ("notebook", "stationery", 48, 60, "piece"),
        ("pen", "stationery", 8, 150, "piece"),
        ("pencil", "stationery", 5, 180, "piece"),
        ("eraser", "stationery", 5, 120, "piece"),
        ("geometry box", "stationery", 80, 30, "piece"),
        ("school bag", "stationery", 500, 18, "piece"),
    ],
}


# =========================================================
# DELETE OLD INVENTORY
# =========================================================

def clear_inventory(inventory_ref):
    """
    Delete all existing inventory documents for a store.

    This is important because the old dataset contained
    incorrect cross-category products.
    """

    docs = list(inventory_ref.stream())

    if not docs:
        return 0

    deleted = 0

    # Firestore supports batched writes.
    # Keep batches below the Firestore 500-operation limit.
    batch = db.batch()
    batch_count = 0

    for doc in docs:
        batch.delete(doc.reference)
        batch_count += 1
        deleted += 1

        if batch_count >= 450:
            batch.commit()
            batch = db.batch()
            batch_count = 0

    if batch_count > 0:
        batch.commit()

    return deleted


# =========================================================
# SEED DATABASE
# =========================================================

def seed_database():

    print("\n======================================")
    print("      TOWNKART FIREBASE SEEDER")
    print("======================================\n")

    stores_ref = db.collection("stores")

    total_items = 0
    total_deleted = 0

    for store in stores:

        store_id = store["id"]

        print(f"Processing store: {store['name']}")

        # -------------------------------------------------
        # CREATE / UPDATE STORE
        # -------------------------------------------------

        store_data = {
            "name": store["name"],
            "city": store["city"],
            "latitude": store["latitude"],
            "longitude": store["longitude"],
            "updated_at": datetime.now(timezone.utc),
        }

        stores_ref.document(store_id).set(
            store_data,
            merge=True
        )

        # -------------------------------------------------
        # INVENTORY REFERENCE
        # -------------------------------------------------

        inventory_ref = (
            stores_ref
            .document(store_id)
            .collection("inventory")
        )

        # -------------------------------------------------
        # DELETE OLD INVENTORY
        # -------------------------------------------------

        deleted = clear_inventory(inventory_ref)

        total_deleted += deleted

        if deleted > 0:
            print(f"  -> Removed {deleted} old inventory items")

        # -------------------------------------------------
        # ADD CLEAN INVENTORY
        # -------------------------------------------------

        items = inventory.get(store_id, [])

        for index, item in enumerate(items, start=1):

            product, category, price, quantity, unit = item

            item_data = {
                "product": product,
                "category": category,
                "price": price,
                "quantity": quantity,
                "unit": unit,
                "updated_at": datetime.now(timezone.utc),
            }

            document_id = f"item_{index:03d}"

            inventory_ref.document(document_id).set(
                item_data
            )

            total_items += 1

        print(f"  -> Added {len(items)} clean inventory items")

    # =====================================================
    # SUMMARY
    # =====================================================

    print("\n======================================")
    print("DATABASE SEEDING COMPLETE")
    print("======================================")

    print(f"Stores updated: {len(stores)}")
    print(f"Old inventory items removed: {total_deleted}")
    print(f"New inventory items added: {total_items}")

    print("\nInventory categories:")

    print("  Supermarkets -> fruits, vegetables, groceries, flowers")
    print("  Stationery   -> stationery")
    print("  Footwear     -> footwear + shoe care")
    print("  Gift stores  -> toys + selected stationery")

    print("\nFirestore structure:")
    print("stores/{store_id}/inventory/{item_id}")

    print("======================================\n")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    seed_database()