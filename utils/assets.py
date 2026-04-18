"""
Asset helpers — weapon type detection, formatting
"""
from typing import Optional


WEAPON_KEYWORDS = [
    "Vandal", "Phantom", "Operator", "Sheriff", "Ghost", "Classic",
    "Frenzy", "Spectre", "Bulldog", "Guardian", "Marshal", "Outlaw",
    "Ares", "Odin", "Stinger", "Judge", "Bucky", "Shorty",
    "Knife", "Melee",
]

WEAPON_EMOJIS = {
    "knife":    "🗡️",
    "melee":    "🗡️",
    "operator": "🎯",
    "marshal":  "🎯",
    "outlaw":   "🎯",
    "judge":    "💥",
    "bucky":    "💥",
}


def weapon_emoji(skin_name: str) -> str:
    lower = skin_name.lower()
    for key, emoji in WEAPON_EMOJIS.items():
        if key in lower:
            return emoji
    return "🔫"


def weapon_type(skin_name: str) -> str:
    lower = skin_name.lower()
    for w in WEAPON_KEYWORDS:
        if w.lower() in lower:
            return w
    return "Weapon"


def fmt_number(n: int) -> str:
    return f"{n:,}"
