import streamlit as st
import requests
import json

with open('assets/id_to_image_mapping.json', 'r') as f:
    id_to_image_mapping = json.load(f)

with open('assets/product_prices.json', 'r') as f:
    price_ranges = json.load(f)

with open('assets/product_categories.json', 'r') as f:
    product_categories = json.load(f)

base_search_url = "http://semantic-backend:8002/search/query?query="

st.set_page_config(layout="wide")
st.title("Visual Semantic Search")


@st.experimental_fragment
def show_results_fragment(retrieved_products):
    columns = st.columns(5)
    for idx, product in enumerate(retrieved_products):
        with columns[idx % 5]:
            st.image(id_to_image_mapping[str(product["id"])], width=200)
            st.write(product["payload"]["title"])
            st.write(product["payload"]["price"])

search_bar_column, search_button_column = st.columns((0.9, 0.1))

with search_bar_column:
    search_query = st.text_input("Search products")

    price_range = st.select_slider("Price range", options=price_ranges)
    category = st.selectbox("Category", product_categories, index=None)

with search_button_column:
    search_button = st.button("Search")

if search_button:
    st.write("Searching for products with query:", search_query)
    # Call the backend API to search for products with the query
    search_url = base_search_url + search_query
    if category:
        search_url += f"&category={category}"
    if price_range:
        search_url += f"&price={price_range}"
    
    response = requests.post(search_url)
    response.raise_for_status()
    products = response.json()
    show_results_fragment(products)
