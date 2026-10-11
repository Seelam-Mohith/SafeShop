import os
import time
from flask import Flask, request, render_template, redirect, url_for, jsonify, g, send_from_directory
from config import Config
from services.product_service import load_products, get_product_by_id, get_products_by_category
from services.access_logger import AccessLogger, get_source_ip

app = Flask(__name__)
app.config.from_object(Config)

logger = AccessLogger(log_file=app.config.get('LOG_FILE'))

# Load products once
ALL_PRODUCTS = load_products()


@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    try:
        duration_ms = (time.time() - getattr(g, 'start_time', time.time())) * 1000.0
        response_bytes = response.calculate_content_length()
        if response_bytes is None:
            response_bytes = 0
        logger.log_request(
            source_ip=get_source_ip(request),
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            referer=request.headers.get('Referer'),
            user_agent=request.headers.get('User-Agent'),
            response_bytes=response_bytes,
            duration_ms=round(duration_ms, 2)
        )
    except Exception:
        pass
    return response


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'ShopSafe is running'}), 200


@app.route('/')
def index():
    featured_products = [p for p in ALL_PRODUCTS if p.get('featured')]
    best_selling = sorted(ALL_PRODUCTS, key=lambda x: x.get('rating', 0), reverse=True)[:6]
    return render_template('index.html', featured_products=featured_products, best_selling=best_selling)


@app.route('/products')
def products():
    query = request.args.get('q', '').strip().lower()
    category = request.args.get('category', '').strip()
    sort = request.args.get('sort', 'default').strip()

    filtered = list(ALL_PRODUCTS)
    if query:
        filtered = [p for p in filtered if query in p.get('name', '').lower() or query in p.get('description', '').lower()]
    if category:
        filtered = [p for p in filtered if p.get('category', '') == category]

    if sort == 'price_asc':
        filtered.sort(key=lambda x: x.get('price', 0))
    elif sort == 'price_desc':
        filtered.sort(key=lambda x: x.get('price', 0), reverse=True)
    elif sort == 'rating_desc':
        filtered.sort(key=lambda x: x.get('rating', 0), reverse=True)

    return render_template('products.html', products=filtered, query=request.args.get('q', ''), category=category, sort=sort)


@app.route('/product/<product_id>')
def product_detail(product_id):
    product = get_product_by_id(ALL_PRODUCTS, product_id)
    if not product:
        return render_template('404.html'), 404
    return render_template('product_detail.html', product=product)


@app.route('/category/<category_name>')
def category(category_name):
    products = get_products_by_category(ALL_PRODUCTS, category_name)
    return render_template('category.html', category_name=category_name, products=products)


@app.route('/cart')
def cart():
    return render_template('cart.html', products=ALL_PRODUCTS)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Disable debug by default; can be enabled via env if needed
    debug_mode = os.environ.get('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
