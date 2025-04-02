import streamlit as st
from api_fetch import fetch_products, get_available_brands

st.title("🏠 Home Appliance Recommender")

# Select appliance type
appliance_type = st.selectbox(
    "Select Appliance Type",
    ["Kitchen", "Smart Home", "Vacuum Cleaners", "Laundry"]
)

# Select price range
min_price, max_price = st.slider("Select Price Range (INR)", 1000, 500000, (1000, 50000))

# Get brands related to the selected appliance type
available_brands = ["Any"] + get_available_brands(appliance_type)

# Select brand from dropdown
brand = st.selectbox("Select Preferred Brand (Optional)", available_brands)

# Get recommendations only when the button is clicked
if st.button("Get Recommendations"):
    recommendations = fetch_products(appliance_type, min_price, max_price, brand)

    if recommendations:
        # Pagination: Show 3 items per page
        page_number = st.session_state.get("page_number", 0)
        items_per_page = 3

        start_idx = page_number * items_per_page
        end_idx = start_idx + items_per_page
        paginated_recommendations = recommendations[start_idx:end_idx]

        for item in paginated_recommendations:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                <b>{item['name']}</b><br>
                <b>Price:</b> ₹{item['price']}<br>
                <b>Brand:</b> {item['brand']}<br>
                <b>Rating:</b> {item['rating']}⭐<br>
                <b>SKU:</b> {item['sku']}<br>
            </div>
            """, unsafe_allow_html=True)

        # Pagination buttons
        col1, col2 = st.columns([0.5, 0.5])
        if col1.button("Previous") and page_number > 0:
            st.session_state.page_number = page_number - 1
        if col2.button("Next") and end_idx < len(recommendations):
            st.session_state.page_number = page_number + 1
    else:
        st.warning("No recommendations found. Try changing filters.")
