import numpy as np
import json

with open('../backend/products.json', 'r') as f:
    products = json.load(f)


# Task 1: Create a dictionary mapping product id to the first image URL
id_to_image_mapping = dict()

for product in products:
    try:
        id_to_image_mapping[product['id']] = product["images"][0]
    except:
        id_to_image_mapping[product['id']] = "https://vipha.co/wp-content/themes/vipha/images/empty-img.png"

with open('assets/id_to_image_mapping.json', 'w') as f:
    json.dump(id_to_image_mapping, f)

# Task 2: Get ranges of product prices and get all product categories
product_prices = [product['current_price'] for product in products if product['current_price']]
# devide into 25 ranges
price_ranges = np.linspace(min(product_prices), max(product_prices), num=25, dtype=int)

product_categories = set()
for product in products:
    if not product['category_name']:
        continue
    product_categories.add(product['category_name'])

# save
with open('assets/product_prices.json', 'w') as f:
    json.dump(price_ranges.tolist(), f)

with open('assets/product_categories.json', 'w') as f:
    json.dump(list(product_categories), f)


