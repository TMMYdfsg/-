# features/roulette.py
from __future__ import annotations
import random

PRESETS = {
    "lottery": [
        ("ハズレ", 0, 40),
        ("+10万", 10, 25),
        ("+30万", 30, 15),
        ("+100万", 100, 5),
        ("-10万", -10, 10),
        ("-50万", -50, 5),
    ],
    "illness": [
        ("軽い風邪: 幸福-5", ("happiness", -5), 40),
        ("胃痛: 幸福-10", ("happiness", -10), 25),
        ("休養: 幸福+8", ("happiness", +8), 20),
        ("健康診断で絶好調: 幸福+20", ("happiness", +20), 5),
        ("入院費: 借金+20", ("debt", +20), 10),
    ],
    "career": [
        ("昇進: 人気+5", ("popularity", +5), 30),
        ("配置転換: 職業ランダム変更", ("job", "random"), 20),
        ("資格試験合格: 幸福+15", ("happiness", +15), 15),
        ("左遷: 人気-5", ("popularity", -5), 20),
        ("ヘッドハント: 所持金+30", ("money", +30), 15),
    ],
}


def _weighted_choice(items):
    total = sum(w for *_, w in items)
    r = random.uniform(0, total)
    upto = 0.0
    for label, val, w in items:
        if upto + w >= r:
            return label, val
        upto += w
    return items[0][0], items[0][1]


def spin_and_apply(game, kind: str, player_name: str) -> str:
    label, val = _weighted_choice(PRESETS[kind])
    if kind == "lottery":
        game.add_money(player_name, int(val))
        game._log(
            game.store.get_state(), f"🎡 ルーレット(宝くじ): {player_name} → {label}"
        )
    elif kind == "illness":
        target, delta = val
        if target == "happiness":
            game.adjust_happiness(player_name, int(delta))
        elif target == "debt":
            game.add_debt(player_name, int(delta))
        game._log(
            game.store.get_state(), f"🎡 ルーレット(病気): {player_name} → {label}"
        )
    elif kind == "career":
        target, payload = val
        if target == "popularity":
            game.adjust_popularity(player_name, int(payload))
        elif target == "happiness":
            game.adjust_happiness(player_name, int(payload))
        elif target == "money":
            game.add_money(player_name, int(payload))
        elif target == "job":
            game.random_change_job(player_name)
        game._log(
            game.store.get_state(), f"🎡 ルーレット(転職): {player_name} → {label}"
        )
    game.store.update_state(game.store.get_state())
    return label
