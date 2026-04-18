"""
Valorant PD API — store, night market, balance
Uses synchronous requests (simpler than async httpx)
"""
import logging
import requests
from typing import Dict, Any, Optional

from config.constants import VP_UUID, RAD_UUID, KC_UUID, CLIENT_PLATFORM

logger = logging.getLogger(__name__)

# Region URL mapping
REGION_BASE = {
    "ap":    "pd.ap.a.pvp.net",
    "na":    "pd.na.a.pvp.net",
    "eu":    "pd.eu.a.pvp.net",
    "kr":    "pd.kr.a.pvp.net",
    "br":    "pd.na.a.pvp.net",      # BR uses NA shard
    "latam": "pd.na.a.pvp.net",      # LATAM uses NA shard
}

_client_version = "release-09.01-shipping-16-2491987"


def set_client_version(version: str):
    global _client_version
    _client_version = version


def get_client_version() -> str:
    return _client_version


def _pd_url(region: str) -> str:
    base = REGION_BASE.get(region.lower(), REGION_BASE["ap"])
    return f"https://{base}"


def _headers(access_token: str, entitlement_token: str) -> Dict[str, str]:
    return {
        "Authorization":           f"Bearer {access_token}",
        "X-Riot-Entitlements-JWT": entitlement_token,
        "X-Riot-ClientVersion":    get_client_version(),
        "X-Riot-ClientPlatform":   CLIENT_PLATFORM,
        "Content-Type":            "application/json",
    }


def get_store(access_token: str, entitlement_token: str,
              puuid: str, region: str) -> Dict[str, Any]:
    base = _pd_url(region)
    url  = f"{base}/store/v3/storefront/{puuid}"
    hdrs = _headers(access_token, entitlement_token)

    logger.info(f"[store] POST {url}")
    r = requests.post(url, json={}, headers=hdrs, timeout=15)
    
    logger.info(f"[store] status={r.status_code}")
    if not r.ok:
        logger.error(f"[store] error: {r.text[:400]}")
        raise Exception(f"Riot API {r.status_code}: {r.text[:400]}")

    raw   = r.json()
    panel = raw.get("SkinsPanelLayout", {})
    
    # Build price map from SingleItemStoreOffers
    price_map = {
        o["OfferID"]: o.get("Cost", {}).get(VP_UUID, 0)
        for o in panel.get("SingleItemStoreOffers", [])
    }
    
    skins = []
    for uid in panel.get("SingleItemOffers", []):
        info = _skin_info(uid)
        info["price"] = price_map.get(uid, 0)
        skins.append(info)

    return {
        "skins":      skins,
        "expires_in": panel.get("SingleItemOffersRemainingDurationInSeconds", 0),
    }


def get_night_market(access_token: str, entitlement_token: str,
                     puuid: str, region: str) -> Optional[Dict[str, Any]]:
    base = _pd_url(region)
    url  = f"{base}/store/v3/storefront/{puuid}"
    hdrs = _headers(access_token, entitlement_token)

    r = requests.post(url, json={}, headers=hdrs, timeout=15)
    
    if not r.ok:
        raise Exception(f"Riot API {r.status_code}: {r.text[:400]}")

    bonus = r.json().get("BonusStore")
    if not bonus:
        return None

    offers = []
    for item in bonus.get("BonusStoreOffers", []):
        # BonusStore structure: Offer.Rewards[0].ItemID
        offer_data = item.get("Offer", {})
        rewards = offer_data.get("Rewards", [])
        if not rewards:
            continue
        uid  = rewards[0].get("ItemID", "")
        info = _skin_info(uid)
        info["original_price"]   = offer_data.get("Cost", {}).get(VP_UUID, 0)
        info["discounted_price"] = item.get("DiscountCosts", {}).get(VP_UUID, 0)
        info["discount_pct"]     = item.get("DiscountPercent", 0)
        offers.append(info)

    return {"offers": offers}


def get_balance(access_token: str, entitlement_token: str,
                puuid: str, region: str) -> Dict[str, int]:
    base = _pd_url(region)
    url  = f"{base}/store/v1/wallet/{puuid}"
    hdrs = _headers(access_token, entitlement_token)

    r = requests.get(url, headers=hdrs, timeout=10)
    
    if not r.ok:
        raise Exception(f"Riot API {r.status_code}: {r.text[:400]}")

    bal = r.json().get("Balances", {})
    return {
        "vp":         bal.get(VP_UUID, 0),
        "radianite":  bal.get(RAD_UUID, 0),
        "freeagents": bal.get(KC_UUID, 0),
    }


def _skin_info(uuid: str) -> Dict[str, Any]:
    """Fetch skin metadata from valorant-api.com"""
    try:
        r = requests.get(
            f"https://valorant-api.com/v1/weapons/skinlevels/{uuid}",
            timeout=8
        )
        if r.status_code == 200:
            d = r.json().get("data", {})
            return {
                "uuid": uuid,
                "name": d.get("displayName", "Unknown Skin"),
                "icon": d.get("displayIcon", ""),
            }
    except Exception:
        pass
    return {"uuid": uuid, "name": "Unknown Skin", "icon": ""}

