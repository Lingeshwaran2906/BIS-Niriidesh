"""Interactive, local-only Gemini API key manager."""
import argparse
import getpass
import os
import secrets
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from api_key_manager import (
    BACKEND_DIR, ENV_PATH, KEYS_PATH, add_key, list_keys, remove_key,
    set_active, validate_key, _read_store,
)

DEFAULT_MODEL = "gemini-3.8-flash"
DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


def ensure_config():
    existing = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8-sig").splitlines():
            item = line.strip()
            if item and not item.startswith("#") and "=" in item:
                k, v = item.split("=", 1)
                existing[k.strip()] = v.strip().strip('"').strip("'")
    existing.setdefault("JWT_SECRET", secrets.token_urlsafe(48))
    existing.setdefault("GEMINI_MODEL", DEFAULT_MODEL)
    existing.setdefault("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    lines = [
        "# Local settings for BIS Nirdesh. Do not share or commit this file.",
        f"JWT_SECRET={existing['JWT_SECRET']}",
        f"GEMINI_MODEL={existing['GEMINI_MODEL']}",
        f"GEMINI_EMBEDDING_MODEL={existing['GEMINI_EMBEDDING_MODEL']}",
    ]
    # Keep any pre-existing single-key configuration usable as a migration fallback.
    if existing.get("GEMINI_API_KEY"):
        lines.append(f"GEMINI_API_KEY={existing['GEMINI_API_KEY']}")
    if existing.get("GOOGLE_API_KEY"):
        lines.append(f"GOOGLE_API_KEY={existing['GOOGLE_API_KEY']}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    load_dotenv(ENV_PATH, override=True, encoding="utf-8-sig")


def safe_error(exc, key):
    return str(exc).replace(key, "[REDACTED]")[:500]


def validate_with_retries(key):
    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    embedding_model = os.getenv("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    last = None
    for attempt in range(1, 4):
        try:
            validate_key(key, model=model, embedding_model=embedding_model)
            return True, ""
        except Exception as exc:
            last = exc
            if attempt < 3:
                # Small backoff for temporary service/network errors.
                time.sleep(attempt * 2)
    return False, safe_error(last, key)


def show_keys():
    keys = list_keys()
    if not keys:
        print("\nNo keys saved yet.")
        return
    print("\nSaved keys (only last 4 characters are shown):")
    for item in keys:
        active = "  < ACTIVE" if item["active"] else ""
        print(f"  {item['index'] + 1}. {item['masked']}{active}")
    print(f"Total: {len(keys)}")


def add_flow():
    key = getpass.getpass("Paste Gemini API key (input hidden): ").strip()
    if not key:
        print("No key entered.")
        return
    current = [item["masked"] for item in list_keys()]
    # Duplicate detection is handled by add_key without printing the secret.
    print("Checking text-generation and embedding access (up to 3 attempts)...")
    ok, error = validate_with_retries(key)
    if ok:
        added, index = add_key(key)
        print("SUCCESS: Key passed both API tests.")
        print("Added." if added else "This key is already saved.")
        if added and not list_keys():
            set_active(index)
    else:
        print("Validation could not complete:")
        print(error or "Unknown API error")
        print("A temporary 503/network error can happen even for a valid key.")
        answer = input("Save this key anyway so runtime failover can try it? [y/N]: ").strip().lower()
        if answer == "y":
            added, _ = add_key(key)
            print("Key saved locally." if added else "This key is already saved.")
        else:
            print("Key not saved.")
    key = ""


def remove_flow():
    show_keys()
    entries = list_keys()
    if not entries:
        return
    try:
        number = int(input("Enter the key number to remove (0 to cancel): ").strip())
        if number == 0:
            return
        remove_key(number - 1)
        print("Key removed.")
    except (ValueError, IndexError) as exc:
        print(f"Could not remove key: {exc}")


def test_flow():
    entries = list_keys()
    if not entries:
        print("No keys saved.")
        return
    for item in entries:
        print(f"\nTesting key {item['index'] + 1} ({item['masked']})...")
        # Recover the raw key only internally; never print it.
        keys, _ = _read_store()
        key = keys[item["index"]]
        ok, error = validate_with_retries(key)
        if ok:
            print("VALID: text generation and embeddings work.")
        else:
            print("FAILED: " + (error or "Unknown error"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ensure-config", action="store_true")
    parser.add_argument("--has-keys", action="store_true")
    args = parser.parse_args()
    ensure_config()
    keys, _ = _read_store()
    if args.ensure_config:
        return 0
    if args.has_keys:
        return 0 if keys else 1

    while True:
        print("\n" + "=" * 52)
        print("             BIS NIRDESH API MANAGER")
        print("=" * 52)
        print("1. Add Gemini API key")
        print("2. List saved keys")
        print("3. Test all saved keys")
        print("4. Set active key")
        print("5. Remove a key")
        print("6. Exit")
        choice = input("Choose an option [1-6]: ").strip()
        if choice == "1":
            add_flow()
        elif choice == "2":
            show_keys()
        elif choice == "3":
            test_flow()
        elif choice == "4":
            show_keys()
            try:
                number = int(input("Enter key number to make active: ").strip())
                set_active(number - 1)
                print("Active key updated.")
            except (ValueError, IndexError) as exc:
                print(f"Could not set active key: {exc}")
        elif choice == "5":
            remove_flow()
        elif choice == "6":
            print("API Manager closed.")
            return 0
        else:
            print("Choose a number from 1 to 6.")


if __name__ == "__main__":
    raise SystemExit(main())
