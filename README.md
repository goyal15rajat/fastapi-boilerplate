# Fastapi Boilerplate

Fastapi bolierplate with Python 3.11

## Installation

For dev -

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

For production -

```bash
pip install -r requirements.txt
```

## Creating Your First App

The boilerplate includes a build script to help you create new apps quickly. To create a new app:

```bash
python scripts/build_app.py
```

The script will prompt you for:
- App name (e.g., users, products)
- Route slug (e.g., user, product)

This will create a new app directory with the following structure:
```
your_app/
├── controllers/
│   └── your_route_controller.py
├── utils/
└── routes.py
```

## UI Templating

The boilerplate uses Jinja2 templating for the UI. Templates are located in the `templates` directory.

### Template Structure
- Base templates are in `templates/base/`
- Page templates are in `templates/`
- Static assets (CSS, JS) are in `static/`

### Using Templates

1. Create a new template:
```html
{% extends "base/base.html" %}

{% block content %}
    <!-- Your content here -->
{% endblock %}
```

2. Render templates in your routes:
```python
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {"request": request, "title": "Welcome"}
    )
```

### Styling
- The boilerplate uses Tailwind CSS for styling
- Custom CSS can be added in `static/css/styles.css`
- Add new stylesheets in your templates:
```html
<link href="{{ url_for('static', path='/css/your-styles.css') }}" rel="stylesheet">
```

## Usage

For dev -

```bash
uvicorn app:app --reload
```

For production -

```bash
uvicorn app:app --workers 3

```

## ENV

```bash
APP_NAME=bolierplate
ENV=dev
CUSTOMER_CODE=internal
ENV_CODE=pd
MONGO_HOST=127.0.0.1
MONGO_PORT=27017
MONGO_DBNAME=boilerplate
REDIS_DBNAME=2
```

## Docker Deployment

To run the application in production mode:

```bash
TBA

```

To run the application in development mode:

```bash
TBA
```

To run the application in test mode:

```bash
TBA

```

## Nomenclature rules

- Folder names will be **lowerCamel**
- File names will be **snake_case**
- Variables, Functions will be **snake_case**
- Class names will be **PascalCase**

## Dependencies

- Mongo
- Redis

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

[_Install pre-commit_](https://pre-commit.com/)

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type post-commit
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
