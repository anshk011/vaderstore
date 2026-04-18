"""
Utility helpers
"""
import time
import uuid
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs, unquote


def new_nonce() -> str:
    return uuid.uuid4().hex


def parse_token_from_uri(uri: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract access_token and id_token from a Riot redirect URI fragment."""
    for sep in ("#", "?"):
        if sep in uri:
            fragment = uri.split(sep, 1)[1]
            # URLSearchParams-style manual parse (handles + as space)
            params: dict = {}
            for part in fragment.split("&"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    params[k] = unquote(v.replace("+", " "))
            at = params.get("access_token")
            it = params.get("id_token")
            if at:
                return at, it
    return None, None


def now_ts() -> float:
    return time.time()
