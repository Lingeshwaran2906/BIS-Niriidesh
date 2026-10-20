"""Local multi-key Gemini failover manager for BIS Nirdesh."""
import json
import os
import threading
from pathlib import Path
from typing import Callable, TypeVar

from dotenv import load_dotenv
from google import genai

BACKEND_DIR = Path(__file__).resolve().parent
KEYS_PATH = BACKEND_DIR / "api_keys.json"
ENV_PATH = BACKEND_DIR / ".env"
_lock = threading.RLock()
T = TypeVar("T")


def _read_store():
    if KEYS_PATH.exists():
        try:
            data = json.loads(KEYS_PATH.read_text(encoding="utf-8-sig"))
            keys = data.get("keys", [])
            keys = [str(item).strip() for item in keys if str(item).strip()]
            active = int(data.get("active_index", 0))
            return keys, max(0, min(active, max(0, len(keys) - 1)))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
    load_dotenv(ENV_PATH, override=True, encoding="utf-8-sig")
    legacy = os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("GOOGLE_API_KEY", "").strip()
    return ([legacy] if legacy else []), 0


def _write_store(keys, active_index=0):
    KEYS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"keys": list(keys), "active_index": int(active_index)}
    temp_path = KEYS_PATH.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temp_path.replace(KEYS_PATH)


def list_keys():
    with _lock:
        keys, active = _read_store()
        return [{"index": i, "active": i == active, "masked": f"...{key[-4:]}" if len(key) >= 4 else "****"}
                for i, key in enumerate(keys)]


def add_key(key):
    key = key.strip()
    if not key:
        raise ValueError("Empty API key.")
    with _lock:
        keys, active = _read_store()
        if key in keys:
            return False, active
        keys.append(key)
        _write_store(keys, active if len(keys) > 1 else 0)
        return True, len(keys) - 1


def remove_key(index):
    with _lock:
        keys, active = _read_store()
        if index < 0 or index >= len(keys):
            raise IndexError("No key exists at that number.")
        removed = keys.pop(index)
        if not keys:
            active = 0
        elif index < active:
            active -= 1
        elif active >= len(keys):
            active = 0
        _write_store(keys, active)
        return removed


def set_active(index):
    with _lock:
        keys, _ = _read_store()
        if index < 0 or index >= len(keys):
            raise IndexError("No key exists at that number.")
        _write_store(keys, index)


def _ordered_keys():
    with _lock:
        keys, active = _read_store()
        if not keys:
            raise RuntimeError(
                "No Gemini API keys are configured. Run API_MANAGER.bat and add at least one key."
            )
        return [(idx, keys[idx]) for idx in list(range(active, len(keys))) + list(range(0, active))]


def _set_active(index):
    with _lock:
        keys, _ = _read_store()
        if 0 <= index < len(keys):
            _write_store(keys, index)


def call_with_failover(operation: Callable, *, operation_name="Gemini API request"):
    """Run operation(client) with the active key, switching and persisting on failure."""
    errors = []
    for index, key in _ordered_keys():
        try:
            client = genai.Client(api_key=key)
            result = operation(client)
            _set_active(index)
            return result
        except Exception as exc:
            # Do not include API key values in logs or propagated messages.
            message = str(exc).replace(key, "[REDACTED]")
            errors.append(f"key {index + 1} (...{key[-4:]}): {message[:220]}")
    details = " | ".join(errors)
    raise RuntimeError(
        f"{operation_name} failed with all configured Gemini API keys. "
        f"Add/check keys using API_MANAGER.bat. Details: {details}"
    )


def generate_content_with_failover(model, contents):
    return call_with_failover(
        lambda client: client.models.generate_content(model=model, contents=contents),
        operation_name="Text generation",
    )


def embed_content_with_failover(model, contents):
    return call_with_failover(
        lambda client: client.models.embed_content(model=model, contents=contents),
        operation_name="Embeddings",
    )


def validate_key(key, model="gemini-3.8-flash", embedding_model="gemini-embedding-001"):
    client = genai.Client(api_key=key)
    emb = client.models.embed_content(
        model=embedding_model, contents="BIS Nirdesh API validation test"
    )
    if not emb.embeddings or not emb.embeddings[0].values:
        raise RuntimeError("Embedding API returned no vector.")
    generated = client.models.generate_content(
        model=model, contents="Reply with only the word OK."
    )
    if not (generated.text or "").strip():
        raise RuntimeError("Text-generation API returned an empty response.")
    return True
