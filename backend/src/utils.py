# utils.py
import aiofiles
import json

async def load_products(json_file):
    async with aiofiles.open(json_file, 'r') as f:
        contents = await f.read()
    products = json.loads(contents)
    return products
