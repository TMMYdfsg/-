
# -*- coding: utf-8 -*-
import math
from typing import Dict

JAPANESE_LARGE_UNITS = [
    (10**68, "無量大数"),
    (10**64, "不可思議"),
    (10**60, "那由他"),
    (10**56, "阿僧祇"),
    (10**52, "恒河沙"),
    (10**48, "極"),
    (10**44, "載"),
    (10**40, "正"),
    (10**36, "澗"),
    (10**32, "溝"),
    (10**28, "穣"),
    (10**24, "秭"),
    (10**20, "垓"),
    (10**16, "京"),
    (10**12, "兆"),
    (10**8, "億"),
    (10**4, "万"),
]

def format_money_manjp(value: int) -> str:
    """万円単位の整数を日本語大数で整形。"""
    n = int(value)
    if n == 0:
        return "0円相当(万円基準)"
    parts = []
    remaining = n * 10000  # 万円→円換算の参考表記（あくまで装飾）
    for unit, name in JAPANESE_LARGE_UNITS:
        if remaining >= unit:
            count = remaining // unit
            remaining = remaining % unit
            parts.append(f"{count}{name}")
    if not parts:
        return f"{n}万円"
    return f"{n}万円（≈{''.join(parts)}）"
