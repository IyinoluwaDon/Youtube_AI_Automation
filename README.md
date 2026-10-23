# AI-Assisted Video Production Prototype

A FastAPI prototype that coordinates provider-dependent steps for generating video assets, rendering a short and optionally publishing through YouTube OAuth. It is not a one-click production service; integrations require credentials and explicit review.

## What is included

- FastAPI application and pipeline/service modules
- Optional Gemini, Pixabay/media, text-to-speech and YouTube integrations
- Offline import-safety tests; provider workflows are opt-in

## Run locally

```sh
python -m venv .venv
# Activate .venv, then:
python -m pip install -r requirements.txt
# Configure only the provider credentials needed in a private .env file
uvicorn app.main:app --reload
```

## Verify

Run offline-safe checks with `python -m pytest -q`. Read `TESTING.md` before provider integration tests; some actions can generate content or publish externally.

## Repository map

`app/api/` contains HTTP routes; `app/services/` contains provider and pipeline code; `app/core/` loads configuration. `artifacts/` and logs are runtime outputs and should not be committed. `TESTING.md` describes safe test boundaries.

## Evidence and limitations

Offline import-safety checks pass. Gemini generation, media retrieval, rendering with production assets, OAuth and YouTube uploads were not exercised.

Do not place API keys, OAuth client secrets or token files in Git. Review generated media, source licenses, privacy, quotas and consent before use. YouTube publication is an external side effect and must remain explicit. Treat provider failures and cost limits as part of any deployment design.

## License

No repository license file is included. Unless the project owner adds a license, do not assume the code, data or model artifacts may be redistributed or reused. Verify third-party data and model terms separately.
