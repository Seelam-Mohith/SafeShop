# ShopSafe

ShopSafe is a legitimate, fully functional e-commerce website built as the baseline for a Watering-Hole Detection Laboratory. It provides a normal shopping experience to establish a baseline of legitimate web traffic for cybersecurity analysis.

## Purpose

This website serves as the legitimate baseline in a Watering-Hole Detection Laboratory. Later, a separate simulated compromised website and a Python-based detection engine will compare web-server logs from both websites.

## Technology Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Templates:** Jinja2
- **Logging:** Python's built-in logging module (JSON Lines format)
- **Data Storage:** Local JSON file (`data/products.json`)
- **Development Server:** Flask development server
- **Testing:** pytest

## Project Structure

```
shopsafe/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── products.json
├── logs/
│   └── .gitkeep
├── services/
│   ├── __init__.py
│   ├── product_service.py
│   └── access_logger.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_detail.html
│   ├── category.html
│   ├── cart.html
│   ├── about.html
│   ├── contact.html
│   ├── privacy.html
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── cart.js
│   └── images/
└── tests/
    ├── test_routes.py
    ├── test_products.py
    └── test_logging.py
```

## Setup Instructions (Windows PowerShell)

1. **Create a virtual environment**
```powershell
python -m venv .venv
```

2. **Activate the virtual environment**
```powershell
.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Run the website**
```powershell
python app.py
```

The website will be available at: `http://127.0.0.1:5000`

## Pages

- `/` - Home page with featured products and categories
- `/products` - Product listing with search, filters, and sorting
- `/product/<product_id>` - Product details
- `/category/<category_name>` - Products by category
- `/cart` - Shopping cart (client-side, localStorage)
- `/about` - About page
- `/contact` - Contact page (demo form)
- `/privacy` - Privacy policy
- `/health` - Health check endpoint
- Error pages (404, 500)

## Logging

- **Log file:** `logs/legitimate_access.jsonl`
- **Format:** JSON Lines (one JSON object per line)
- **Fields:** timestamp (UTC ISO 8601), source_ip, method, path, status_code, referer, user_agent, response_bytes, duration_ms
- All HTTP requests (including static assets) are logged
- No cookies, credentials, or authorization headers are logged

## Testing

Run all tests:
```powershell
pytest
```

Run specific test files:
```powershell
pytest tests/test_routes.py
pytest tests/test_products.py
pytest tests/test_logging.py
```

## Inspecting Logs

View generated logs:
```powershell
Get-Content .\logs\legitimate_access.jsonl -Tail 10
```

## Current Limitations

- Client-side shopping cart (localStorage only)
- Demo checkout (no real payment processing)
- Local development server only
- Sample product data
- Images are placeholder SVGs

## Notes

- Debug mode is disabled by default
- Uses `127.0.0.1` to avoid network exposure
- Logs are written only to `logs/legitimate_access.jsonl`
- No external resources, analytics, or tracking
- No malicious behavior or attack simulations
