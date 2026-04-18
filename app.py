"""
Valorant Store Checker — Flask app
"""
import os
import logging
from typing import Dict, Any

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "online", "service": "valorant-store-checker"})


# ── Auth: finalize tokens from redirect URL ──────────────────────────────────
@app.route("/auth/finalize", methods=["POST"])
def auth_finalize():
    from utils.auth import finalize_auth
    body = request.get_json() or {}
    try:
        at = body.get("access_token", "")
        it = body.get("id_token", "")
        if not at:
            return jsonify({"error": "Missing access_token"}), 400
        result = finalize_auth(at, it)
        return jsonify(result)
    except Exception as e:
        logger.error(f"[auth_finalize] {e}")
        return jsonify({"error": str(e)}), 500


# ── Store ─────────────────────────────────────────────────────────────────────
@app.route("/store", methods=["POST"])
def store():
    from utils.valorant_api import get_store
    body = request.get_json() or {}
    try:
        result = get_store(
            body["access_token"],
            body["entitlement_token"],
            body["puuid"],
            body.get("region", "na"),
        )
        return jsonify(result)
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        logger.error(f"[store] {e}")
        return jsonify({"error": str(e)}), 400


# ── Night Market ──────────────────────────────────────────────────────────────
@app.route("/nightmarket", methods=["POST"])
def nightmarket():
    from utils.valorant_api import get_night_market
    body = request.get_json() or {}
    try:
        result = get_night_market(
            body["access_token"],
            body["entitlement_token"],
            body["puuid"],
            body.get("region", "na"),
        )
        if result:
            return jsonify({"active": True, **result})
        return jsonify({"active": False})
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        logger.error(f"[nightmarket] {e}")
        return jsonify({"error": str(e)}), 400


# ── Balance ───────────────────────────────────────────────────────────────────
@app.route("/balance", methods=["POST"])
def balance():
    from utils.valorant_api import get_balance
    body = request.get_json() or {}
    try:
        result = get_balance(
            body["access_token"],
            body["entitlement_token"],
            body["puuid"],
            body.get("region", "na"),
        )
        return jsonify(result)
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        logger.error(f"[balance] {e}")
        return jsonify({"error": str(e)}), 400


# ── Startup ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from utils.auth import fetch_client_version
    from utils.valorant_api import set_client_version
    
    version = fetch_client_version()
    set_client_version(version)
    
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
