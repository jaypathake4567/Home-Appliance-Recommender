import requests

BEST_BUY_API_KEY = "HkHmLGCPdwynPXp83mWYODoH"  # Replace with your actual API key
BEST_BUY_API_URL = "https://api.bestbuy.com/v1/products"

# Mapping categories to API filters
CATEGORY_MAPPING = {
    "Kitchen": "categoryPath.id=abcat0912000",
    "Smart Home": "categoryPath.id=pcmcat254000050002",
    "Vacuum Cleaners": "categoryPath.id=abcat0910000",
    "Laundry": "categoryPath.id=abcat0910001",
}

def fetch_products(appliance_type, min_price=1000, max_price=500000, brand=None):
    """
    Fetches appliance recommendations based on selected type, price range, and brand.
    """
    category_filter = CATEGORY_MAPPING.get(appliance_type, None)
    if not category_filter:
        return []

    url = f"{BEST_BUY_API_URL}({category_filter})?apiKey={BEST_BUY_API_KEY}&format=json&show=sku,name,salePrice,manufacturer,customerReviewAverage"

    try:
        response = requests.get(url)
        data = response.json()
        products = data.get("products", [])

        # Convert USD to INR (assuming 1 USD = 83 INR)
        USD_TO_INR = 83  

        recommendations = [
            {
                "name": item["name"],
                "price": int(item["salePrice"] * USD_TO_INR),  # Convert price to INR
                "brand": item.get("manufacturer", "Unknown"),
                "rating": item.get("customerReviewAverage", "No rating"),
                "sku": item.get("sku", "N/A"),
            }
            for item in products
        ]

        # Apply price filtering AFTER fetching data
        recommendations = [item for item in recommendations if min_price <= item["price"] <= max_price]

        # Apply brand filtering (if brand is selected and not "Any")
        if brand and brand.lower() != "any":
            recommendations = [item for item in recommendations if item["brand"].lower() == brand.lower()]

        return recommendations

    except Exception as e:
        print(f"Error fetching API data: {e}")
        return []


def get_available_brands(appliance_type):
    """
    Fetch unique brands available for the selected appliance type.
    """
    category_filter = CATEGORY_MAPPING.get(appliance_type, None)
    if not category_filter:
        return []

    url = f"{BEST_BUY_API_URL}({category_filter})?apiKey={BEST_BUY_API_KEY}&format=json&show=manufacturer"

    try:
        response = requests.get(url)
        data = response.json()
        products = data.get("products", [])

        # Extract and return unique brand names
        brands = list(set([item["manufacturer"] for item in products if "manufacturer" in item]))
        return sorted(brands)

    except Exception as e:
        print(f"Error fetching available brands: {e}")
        return []
