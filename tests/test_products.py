import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.product_service import load_products, get_product_by_id, get_products_by_category


def test_load_products():
    products = load_products()
    assert isinstance(products, list)
    assert len(products) >= 15


def test_get_product_by_id_valid():
    products = load_products()
    product = get_product_by_id(products, 1)
    assert product is not None
    assert product['id'] == 1


def test_get_product_by_id_invalid():
    products = load_products()
    product = get_product_by_id(products, 9999)
    assert product is None
    product = get_product_by_id(products, 'invalid')
    assert product is None


def test_get_products_by_category():
    products = load_products()
    electronics = get_products_by_category(products, 'Electronics')
    assert isinstance(electronics, list)
    for p in electronics:
        assert p['category'] == 'Electronics'


def test_get_products_by_category_unknown():
    products = load_products()
    result = get_products_by_category(products, 'UnknownCategory')
    assert isinstance(result, list)
    assert len(result) == 0
