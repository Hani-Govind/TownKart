def generate_explanation(result, query):
    product = result["product"]
    price = result["price"]
    quantity = result["quantity"]
    distance = result["distance_km"]

    budget = query.get("budget_max")
    required_quantity = query.get("quantity")
    intent = query.get("intent", "best_match")

    reasons = []

    if budget is not None and price <= budget:
        reasons.append(f"within your ₹{budget} budget")

    if required_quantity is not None:
        if quantity >= required_quantity:
            reasons.append(
                f"has all {required_quantity} units available"
            )
        else:
            reasons.append(
                f"has {quantity} units currently available"
            )

    reasons.append(f"{distance} km away")

    if intent == "cheapest":
        reasons.append("offers a strong price match")
    elif intent == "nearest":
        reasons.append("is one of the closest available stores")
    elif intent == "highest_availability":
        reasons.append("has high stock availability")

    return (
        f"{result['store_name']} is a strong match for "
        f"{product} because it is " + ", ".join(reasons) + "."
    )
