import requests

BEST_BUY_API_KEY = "HkHmLGCPdwynPXp83mWYODoH"
BEST_BUY_API_URL = "https://api.bestbuy.com/v1/products"

CATEGORY_MAPPING = {
    "Kitchen": "categoryPath.id=abcat0912000",
    "Smart Home": "categoryPath.id=pcmcat254000050002",
    "Vacuum Cleaners": "categoryPath.id=abcat0910000",
    "Laundry": "categoryPath.id=abcat0910001",
}

def fetch_products(appliance_type, min_price=1000, max_price=500000, brand=None):
    category_filter = CATEGORY_MAPPING.get(appliance_type, None)
    if not category_filter:
        return []

    min_price_usd = round(min_price / 83, 2)
    max_price_usd = round(max_price / 83, 2)

    filter_query = f"({category_filter}&salePrice>{min_price_usd}&salePrice<{max_price_usd})"

    if brand and brand != "Any":
        filter_query += f"&manufacturer={brand.replace(' ', '%20')}"  # Encode brand name properly

    url = f"{BEST_BUY_API_URL}{filter_query}?apiKey={BEST_BUY_API_KEY}&format=json&show=sku,name,salePrice,manufacturer,customerReviewAverage&pageSize=20"

    try:
        response = requests.get(url)
        data = response.json()
        products = data.get("products", [])

        recommendations = [
            {
                "name": item["name"],
                "price": f"${item['salePrice']}",
                "brand": item.get("manufacturer", "Unknown"),
                "rating": item.get("customerReviewAverage", "No rating"),
                "sku": item.get("sku", "N/A"),
            }
            for item in products
        ]

        return recommendations

    except Exception as e:
        print(f"Error fetching API data: {e}")
        return []

def get_available_brands(appliance_type):
    """Fetch available brands for the selected appliance type."""
    category_filter = CATEGORY_MAPPING.get(appliance_type, None)
    if not category_filter:
        return []

    url = f"{BEST_BUY_API_URL}({category_filter})?apiKey={BEST_BUY_API_KEY}&format=json&show=manufacturer&pageSize=100"

    try:
        response = requests.get(url)
        data = response.json()
        brands = {item["manufacturer"] for item in data.get("products", []) if "manufacturer" in item}
        return sorted(brands)  # Return sorted list of unique brands
    except Exception as e:
        print(f"Error fetching brand data: {e}")
        return []
