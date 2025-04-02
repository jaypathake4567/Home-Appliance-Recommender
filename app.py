import streamlit as st
from api_fetch import fetch_products, get_available_brands

st.title("🏠 Home Appliance Recommender")

# Select appliance type
appliance_type = st.selectbox(
    "Select Appliance Type",
    ["Kitchen", "Smart Home", "Vacuum Cleaners", "Laundry"]
)

# Fetch available brands dynamically
available_brands = get_available_brands(appliance_type)
available_brands.insert(0, "Any")  # Add "Any" option at the beginning

# Select price range
min_price, max_price = st.slider("Select Price Range (INR)", 1000, 500000, (1000, 100000))

# Select brand from dropdown
brand = st.selectbox("Select Preferred Brand (Optional)", available_brands)

# Initialize session state for recommendations and pagination
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "page" not in st.session_state:
    st.session_state.page = 0

# Fetch recommendations only when button is clicked
if st.button("Get Recommendations"):
    st.session_state.recommendations = fetch_products(
        appliance_type, min_price, max_price, brand if brand != "Any" else None
    )
    st.session_state.page = 0  # Reset pagination when new recommendations are fetched

# Display recommendations only if available
if st.session_state.recommendations:
    recommendations = st.session_state.recommendations
    total_items = len(recommendations)

    if total_items > 0:
        start_idx = st.session_state.page * 3
        end_idx = start_idx + 3
        items_to_show = recommendations[start_idx:end_idx]

        for item in items_to_show:
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px;">
                    <h4>{item['name']}</h4>
                    <p><b>Price:</b> ₹{int(float(item['price'].replace('$', '')) * 83)}</p>
                    <p><b>Brand:</b> {item['brand']}</p>
                    <p><b>Rating:</b> {item['rating']}⭐</p>
                    <p><b>SKU:</b> {item['sku']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Pagination buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.session_state.page > 0:
                if st.button("Previous"):
                    st.session_state.page -= 1
        with col2:
            if end_idx < total_items:
                if st.button("Next"):
                    st.session_state.page += 1
    else:
        st.warning("No recommendations found. Try changing filters.")
