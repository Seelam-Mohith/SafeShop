import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from services.access_logger import AccessLogger


def test_homepage():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


def test_products_listing():
    client = app.test_client()
    response = client.get('/products')
    assert response.status_code == 200


def test_valid_product_details():
    client = app.test_client()
    response = client.get('/product/1')
    assert response.status_code == 200


def test_unknown_product():
    client = app.test_client()
    response = client.get('/product/9999')
    assert response.status_code == 404


def test_unknown_route():
    client = app.test_client()
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_health_endpoint():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert 'status' in data


def test_product_search():
    client = app.test_client()
    response = client.get('/products?q=headphones')
    assert response.status_code == 200


def test_category_filtering():
    client = app.test_client()
    response = client.get('/category/Electronics')
    assert response.status_code == 200
