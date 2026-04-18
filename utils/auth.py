"""
Riot authentication — Direct login (window.open) + manual paste fallback
Uses synchronous requests (simpler than async)
"""
import logging
import requests
import base64
import json
from typing import Dict, Any

from config.constants import (
    ENTITLEMENT_URL, USERINFO_URL, REGION_URL,
    VERSION_URL, CLIENT_PLATFORM, CLIENT_VERSION_FALLBACK,
)

logger = logging.getLogger(__name__)

_client_version = CLIENT_VERSION_FALLBACK


def fetch_client_version() -> str:
    """Fetch current Riot client version from valorant-api.com"""
    global _client_version
    for attempt in range(3):
        try:
            r = requests.get(VERSION_URL, timeout=8)
            v = r.json().get("data", {}).get("riotClientVersion", "")
            if v:
                _client_version = v
                logger.info(f"[version] {v}")
                return _client_version
        except Exception as e:
            logger.warning(f"[version] attempt {attempt+1}: {e}")
    return _client_version


def get_client_version() -> str:
    return _client_version


def decode_jwt_payload(token: str) -> dict:
    """Decode JWT payload without verification (for extracting user_id)"""
    try:
        payload = token.split(".")[1]
        # Add padding if needed
        payload += "=" * ((4 - len(payload) % 4) % 4)
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except Exception:
        return {}


def finalize_auth(access_token: str, id_token: str) -> Dict[str, Any]:
    """Exchange access_token for entitlement, userinfo, region"""
    hdrs = {
        "Authorization":  f"Bearer {access_token}",
        "Content-Type":   "application/json",
    }

    # Entitlement token
    r   = requests.post(ENTITLEMENT_URL, json={}, headers=hdrs, timeout=10)
    r.raise_for_status()
    ent = r.json().get("entitlements_token", "")

    # User info
    r    = requests.get(USERINFO_URL, headers=hdrs, timeout=10)
    r.raise_for_status()
    user = r.json()

    puuid     = user.get("sub", "")
    game_name = user.get("acct", {}).get("game_name", "Agent")
    tag_line  = user.get("acct", {}).get("tag_line", "")

    region  = detect_region(access_token, ent, id_token)
    version = get_client_version()

    logger.info(f"[auth] puuid={puuid} region={region} name={game_name}#{tag_line}")

    return {
        "access_token":      access_token,
        "entitlement_token": ent,
        "puuid":             puuid,
        "username":          game_name,
        "tag":               tag_line,
        "region":            region,
        "client_version":    version,
    }


def detect_region(access_token: str, ent: str, id_token: str) -> str:
    """Detect player region from Riot geo API"""
    try:
        r = requests.put(
            REGION_URL,
            json={"id_token": id_token},
            headers={
                "Authorization":           f"Bearer {access_token}",
                "X-Riot-Entitlements-JWT": ent,
                "X-Riot-ClientPlatform":   CLIENT_PLATFORM,
                "X-Riot-ClientVersion":    get_client_version(),
                "Content-Type":            "application/json",
            },
            timeout=8
        )
        body = r.json()
        logger.info(f"[region] status={r.status_code} body={body}")
        live = body.get("affinities", {}).get("live", "")
        mapped = {"na":"na","latam":"na","br":"na","eu":"eu","ap":"ap","kr":"kr"}.get(live, "")
        if mapped:
            logger.info(f"[region] {live} → {mapped}")
            return mapped
        logger.warning(f"[region] unknown affinity '{live}', defaulting na")
    except Exception as e:
        logger.error(f"[region] {e}")
    return "na"
