from datetime import datetime, timezone
import re

import firebase_admin
from firebase_admin import credentials, firestore


# ---------------------------------------------------------
# FIREBASE INITIALIZATION
# ---------------------------------------------------------

cred = credentials.Certificate(
    "townkart-f5344-firebase-adminsdk-fbsvc-866e1045b4.json"
)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ---------------------------------------------------------
# PRODUCT MATCHING HELPERS
# ---------------------------------------------------------

def clean_text(text):
    """
    Normalize text for comparison.

    Example:
    "Black Shoes" -> "black shoes"
    "Toy Cars"    -> "toy cars"
    """
    if not text:
        return ""

    text = str(text).lower().strip()

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


def singularize_word(word):
    """
    Very small English singularization helper.

    This is intentionally simple because Gemini already handles
    most linguistic normalization.
    """

    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"

    if word.endswith("ses") and len(word) > 4:
        return word[:-2]

    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]

    return word


def tokenize(text):
    """
    Convert text into normalized individual words.

    Example:
    "black shoes" -> {"black", "shoe"}
    """

    words = clean_text(text).split()

    return {
        singularize_word(word)
        for word in words
    }


def product_matches(query_product, inventory_product):
    """
    Determine whether a customer's requested product matches
    an inventory product.

    Examples:

    "shoes" + "school shoes"       -> True
    "shoes" + "sports shoes"       -> True
    "black shoes" + "school shoes" -> True
    "toy car" + "toy car"          -> True
    "mango" + "mango"              -> True
    "mango" + "banana"             -> False
    """

    query = clean_text(query_product)
    inventory = clean_text(inventory_product)

    if not query or not inventory:
        return False

    # Exact match
    if query == inventory:
        return True

    query_words = tokenize(query)
    inventory_words = tokenize(inventory)

    if not query_words or not inventory_words:
        return False

    # -----------------------------------------------------
    # CATEGORY MATCHING
    # -----------------------------------------------------
    #
    # If the user searches for a broad category such as
    # "shoes", match products such as:
    #
    # school shoes
    # sports shoes
    # running shoes
    # casual shoes
    #
    # But don't match unrelated products.
    #

    if query_words.issubset(inventory_words):
        return True

    # -----------------------------------------------------
    # IMPORTANT CATEGORY WORDS
    # -----------------------------------------------------

    category_words = {
        "shoe",
        "shoes",
        "toy",
        "toys",
        "stationery",
        "notebook",
        "pen",
        "pencil",
        "bag",
        "flower",
        "flowers",
    }

    # If the query contains a category word that is also
    # present in the inventory product, consider it a match.
    #
    # Example:
    # "black shoes" -> "school shoes"
    #
    # Both contain "shoe".
    #

    common_words = query_words.intersection(inventory_words)

    if common_words.intersection(category_words):
        return True

    return False


# ---------------------------------------------------------
# SEARCH INVENTORY
# ---------------------------------------------------------

def search_inventory(product, budget_max=None):
    """
    Search all stores and their inventory.

    Product matching is semantic-ish rather than requiring
    an exact string match.
    """

    stores_ref = db.collection("stores")
    stores = stores_ref.stream()

    results = []

    for store in stores:
        store_data = store.to_dict()

        inventory_ref = (
            stores_ref
            .document(store.id)
            .collection("inventory")
        )

        for item in inventory_ref.stream():

            item_data = item.to_dict()

            inventory_product = item_data.get("product", "")

            # -------------------------------------------------
            # PRODUCT MATCH
            # -------------------------------------------------

            if not product_matches(
                product,
                inventory_product
            ):
                continue

            quantity = item_data.get("quantity", 0)
            price = item_data.get("price")

            # Ignore unavailable products
            if quantity <= 0:
                continue

            # Ignore invalid prices
            if price is None:
                continue

            # -------------------------------------------------
            # BUDGET FILTER
            # -------------------------------------------------

            if budget_max is not None and price > budget_max:
                continue

            # -------------------------------------------------
            # ADD RESULT
            # -------------------------------------------------

            results.append({
                "store_id": store.id,
                "store_name": store_data.get("name"),
                "latitude": store_data.get("latitude"),
                "longitude": store_data.get("longitude"),
                "product": inventory_product,
                "price": price,
                "quantity": quantity,
                "unit": item_data.get("unit"),
            })

    return results


# ---------------------------------------------------------
# UPDATE INVENTORY
# ---------------------------------------------------------

def update_inventory(
    store_id,
    product,
    price,
    quantity,
    unit
):
    """
    Add or update a store's inventory item.
    """

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

    # Existing product -> update
    if existing_item:
        inventory_ref.document(
            existing_item.id
        ).update(data)

        return existing_item.id

    # New product -> create
    _, new_ref = inventory_ref.add(data)

    return new_ref.id