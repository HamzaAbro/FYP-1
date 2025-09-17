import re
from urllib.parse import urlparse
import pandas as pd

# Load dataset header once to lock feature names
DATASET_PATH = "merged_lexical_clean_2.csv"  # update path if needed
df = pd.read_csv(DATASET_PATH, nrows=1)
LABEL_COLS = {"label", "class", "target", "result"}
FEATURE_NAMES = [c for c in df.columns if c.lower() not in LABEL_COLS and c.lower() != "url"]

def _safe_hostname(parsed):
    host = parsed.hostname or ""
    return host[:-1] if host.endswith(".") else host

def _is_ip(host: str) -> int:
    if not host:
        return 0
    ipv4 = re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", host)
    return 1 if ipv4 else 0

def _has_https(parsed) -> int:
    return 1 if (parsed.scheme or "").lower() == "https" else 0

def extract_url_features(url: str) -> dict:
    s = url or ""
    parsed = urlparse(s)
    host = _safe_hostname(parsed)

    feats = {
        "length_url": len(s),
        "length_hostname": len(host),
        "ip": _is_ip(host),
        "https": _has_https(parsed),
        "nb_dots": s.count("."),
        "nb_hyphens": s.count("-"),
        "nb_at": s.count("@"),
        "nb_and": s.count("&"),
        "nb_underscore": s.count("_"),
        "nb_percent": s.count("%"),
        # placeholders (dataset had them but cannot extract dynamically)
        "iframe": 0,
        "popup_window": 0,
        "submit_email": 0,
    }

    # Ensure output matches exactly the training dataset's features
    return {col: feats.get(col, 0) for col in FEATURE_NAMES}

def batch_extract(urls):
    return pd.DataFrame([extract_url_features(u) for u in urls])
