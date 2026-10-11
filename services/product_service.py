import json
import os


def load_products():
    data_path = os.path.join('data', 'products.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        return products
    except Exception:
        return []


def get_product_by_id(products, product_id):
    try:
        pid = int(product_id)
    except (ValueError, TypeError):
        return None
    for p in products:
        if p.get('id') == pid:
            return p
    return None


def get_products_by_category(products, category_name):
    category = (category_name or '').strip()
    if not category:
        return []
    result = []
    for p in products:
        if p.get('category', '').lower() == category.lower():
            result.append(p)
    return result
