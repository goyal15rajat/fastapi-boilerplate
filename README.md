# Fastapi Boilerplate

Fastapi bolierplate

## Installation

For dev -

```bash
virtualenv -p python3.8 venv
source venv/bin/activate
pip install -r requirements.txt

```

For production -

```bash
pip install -r requirements.txt
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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

[_Install pre-commit_](https://pre-commit.com/)

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type post-commit
chmod +x auto_changelog.sh
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
