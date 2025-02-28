# SOS! Career: An AI-Powered Career Pathfinder

## Installation

1. Create a virtual environment and activate it
2. Install the dependencies saved in `requirements.txt`

```bash
$ pip install -r requirements.txt
```

3. That's it!

## Preparing the environment

Make sure you have the following environment variables:

- `SECRET_KEY`: The secret key to generate password hashes
- `OPENAI_API_KEY`: The API key for OpenAI

If you save the environment variables in an `.env` file, modify the following line in `app/config.py` with the name of your file:

```python
model_config = SettingsConfigDict(env_file="[YOUR ENV FILE NAME HERE]")
```

I recommend using the names already included in `.gitignore`, or adding your own, so that your secrets stay secret.

## Running the server

```bash
$ fastapi dev app/main.py
```

## Documentation

The automatically created docs can be accessed in the following paths:

1. `/docs`: Swagger docs
2. `/redoc`: ReDoc docs
