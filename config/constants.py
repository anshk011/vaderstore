"""
Constants for Valorant Store Checker
"""

# ── Riot Auth ─────────────────────────────────────────────────────────────────
AUTH_BASE        = "https://auth.riotgames.com"
ENTITLEMENT_URL  = "https://entitlements.auth.riotgames.com/api/token/v1"
USERINFO_URL     = "https://auth.riotgames.com/userinfo"
REGION_URL       = "https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant"
VERSION_URL      = "https://valorant-api.com/v1/version"

QR_AUTH_PARAMS = {
    "client_id":     "play-valorant-web-prod",
    "redirect_uri":  "https://playvalorant.com/opt_in",
    "response_type": "token id_token",
    "scope":         "account openid",
}

# ── Valorant PD servers ───────────────────────────────────────────────────────
PD_URLS = {
    "na":    "https://pd.na.a.pvp.net",
    "latam": "https://pd.na.a.pvp.net",
    "br":    "https://pd.na.a.pvp.net",
    "eu":    "https://pd.eu.a.pvp.net",
    "ap":    "https://pd.ap.a.pvp.net",
    "kr":    "https://pd.kr.a.pvp.net",
}

REGIONS = ["na", "eu", "ap", "kr", "latam", "br"]

# ── Currency UUIDs ────────────────────────────────────────────────────────────
VP_UUID  = "85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"
RAD_UUID = "e59aa87c-4cbf-517a-5983-6e81511be9b7"
KC_UUID  = "f08d4ae3-939c-4576-ab26-09ce1f23bb37"

# ── Client headers ────────────────────────────────────────────────────────────
CLIENT_PLATFORM = (
    "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0K"
    "CSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxh"
    "dGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
)
CLIENT_VERSION_FALLBACK = "release-09.01-shipping-16-2491987"

# ── QR session TTL (seconds) ──────────────────────────────────────────────────
QR_SESSION_TTL = 300  # 5 minutes
