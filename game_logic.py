# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict, Any, List, Optional
from datetime import datetime
import random
import math

from masters import (
    INITIAL_MONEY,
    SEASONS,
    DAY,
    NIGHT,
    INCOME_TAX_RATES,
    RESIDENCE_TAX,
    PROPERTY_TAX_RATE,
    TAX_PERIOD,
    TURN_SECONDS,
    SEASON_ADVANCE_EVERY,
    CRIME_THRESHOLDS,
    JOBS,
    QUALIFICATIONS,
    TRAITS,
    SKILLS,
    STOCKS,
    FORBIDDEN_STOCKS,
    FORBIDDEN_NEWS,
    NEWS_EVENTS,
    FURNITURE,
    PETS,
    RECIPES,
    PREFECTURES,
    CITIES,
    DISTRICTS,
    BUILDING_NAMES,
    CARD_REWARDS,
    SECRET_CODES,
    ROULETTE_TABLE,
    STAMP_PER_PRICE,
    STAMP_TARGET,
    DEDUCTION_PER_DEPENDENT,
    RENT_RATE,
    NPCS,
    COLLECTIBLES,
)

def now_iso():
    return datetime.now().isoformat(timespec="seconds")

def crime_rank_from_count(total_crimes: int) -> Optional[str]:
    for thresh, rank in CRIME_THRESHOLDS:
        if total_crimes >= thresh:
            return rank
    return None

class Game:
    def __init__(self, store):
        self.store = store

    # ---------- init & time ----------
    def ensure_initialized(self):
        st = self.store.load()
        if st.get("initialized"):
            return st
        st = {
            "initialized": True,
            "created_at": now_iso(),
            "generation": 1,
            "turn": 1,
            "time_of_day": DAY,
            "season_index": 0,  # 0=春
            "treasury": 0,
            "players": {},
            "news_active": [],
            "stocks": STOCKS[:],
            "forbidden_stocks": FORBIDDEN_STOCKS[:],
            "forbidden_unlocked": False,
            "secret_codes": list(SECRET_CODES.keys()),
            "log": [],
            "banker": {
                "name": "銀行員",
                # デフォルトは admin / 1234（初回に変更推奨）
                "user": "admin",
                "pass_hash": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
            }
        }
        # デモ用プレイヤー
        for pn in ["たろう", "はなこ"]:
            st["players"][pn] = self._new_player(pn)
        self.store.save(st)
        return st

    def _new_player(self, name: str) -> Dict[str, Any]:
        return {
            "name": name,
            "money": INITIAL_MONEY,
            "debt": 0,
            "happiness": 50,
            "popularity": 0,
            "full_cards": 0,
            "job": "無職",
            "skills": {k: {"level": 1, "xp": 0, "next_level": 100} for k in SKILLS},
            "traits": [],
            "qualifications": [],
            "children": [],
            "sales_since_tax": 0,
            "notifications": [],
            "crime_count": 0,
            "jailed_until": 0,  # turn number until released
            "titles": [],
            "stocks": {},  # name->shares
            "properties": [],  # list of dicts
            "pets": [],
        }

    def advance_if_needed(self) -> Dict[str, Any]:
        """Call this regularly; advances turn by TURN_SECONDS model if needed.
        In Kivy app we will trigger this by a periodic clock (not real 600s)."""
        st = self.ensure_initialized()
        # モデル時間の簡易進行：UI側でボタンや擬似タイマーから呼び出す
        # ここでは1呼び出し=1ターン進行のフックを提供
        return st

    def next_turn(self):
        st = self.ensure_initialized()
        st["turn"] += 1
        # 昼夜
        st["time_of_day"] = DAY if st["turn"] % 2 == 1 else NIGHT
        # 季節
        if st["turn"] % SEASON_ADVANCE_EVERY == 1 and st["turn"] > 1:
            st["season_index"] = (st["season_index"] + 1) % len(SEASONS)
        self._log(st, f"ターン{st['turn']}（{st['time_of_day']}） / 季節: {SEASONS[st['season_index']]}")
        # ニュース抽選
        self._roll_news(st)
        # 株価変動＆配当
        self._update_stocks(st)
        # 職業パッシブ収入＆資格維持費
        self._apply_passives_and_fees(st)
        # 税（周期）
        if st["turn"] % TAX_PERIOD == 0:
            self._collect_taxes(st)
        self.store.save(st)

    # ---------- helpers ----------
    def _log(self, st, msg: str):
        st["log"].append(f"[{now_iso()}] {msg}")

    def _find_stock(self, st, name: str, forbidden=False):
        arr = st["forbidden_stocks"] if forbidden else st["stocks"]
        for s in arr:
            if s["name"] == name:
                return s
        return None

    # ---------- banker / auth ----------
    def verify_banker(self, user: str, password: str) -> bool:
        import hashlib
        st = self.ensure_initialized()
        h = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return user == st["banker"]["user"] and h == st["banker"]["pass_hash"]

    def set_banker_password(self, user: str, new_password: str):
        import hashlib
        st = self.ensure_initialized()
        st["banker"]["user"] = user
        st["banker"]["pass_hash"] = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
        self._log(st, f"銀行員パスワードを更新")
        self.store.save(st)

    # ---------- banker god mode actions ----------
    def banker_adjust_money(self, player: str, delta: int):
        st = self.ensure_initialized()
        p = st["players"][player]
        p["money"] += int(delta)
        self._log(st, f"[神] {player} の所持金を {delta:+d} 万円")
        self.store.save(st)

    def banker_adjust_debt(self, player: str, delta: int):
        st = self.ensure_initialized()
        p = st["players"][player]
        p["debt"] = max(0, p["debt"] + int(delta))
        self._log(st, f"[神] {player} の借金を {delta:+d} 万円")
        self.store.save(st)

    def banker_add_title(self, player: str, title: str):
        st = self.ensure_initialized()
        p = st["players"][player]
        if title not in p["titles"]:
            p["titles"].append(title)
            self._log(st, f"[神] {player} に称号「{title}」を付与")
            self.store.save(st)

    def banker_adjust_popularity(self, player: str, delta: int):
        st = self.ensure_initialized()
        p = st["players"][player]
        p["popularity"] += int(delta)
        self._log(st, f"[神] {player} の人気を {delta:+d}")
        self.store.save(st)

    def banker_set_time(self, tod: str):
        st = self.ensure_initialized()
        st["time_of_day"] = tod
        self._log(st, f"[神] 時間帯を {tod} に変更")
        self.store.save(st)

    def banker_set_season(self, season: str):
        st = self.ensure_initialized()
        idx = SEASONS.index(season) if season in SEASONS else 0
        st["season_index"] = idx
        self._log(st, f"[神] 季節を {season} に変更")
        self.store.save(st)

    def banker_set_treasury(self, amount: int):
        st = self.ensure_initialized()
        st["treasury"] = int(amount)
        self._log(st, "[神] 国庫残高を更新")
        self.store.save(st)

    def banker_toggle_forbidden(self, enable: bool):
        st = self.ensure_initialized()
        st["forbidden_unlocked"] = bool(enable)
        self._log(st, f"[神] 禁断市場を {'解禁' if enable else '封印'}")
        self.store.save(st)

    def banker_force_news(self, news: Dict[str, Any], forbidden=False):
        st = self.ensure_initialized()
        target_list = st["news_active"]
        n = dict(news)
        n["until_turn"] = st["turn"] + int(n.get("duration", 1))
        n["forbidden"] = bool(forbidden)
        target_list.append(n)
        self._log(st, f"[神] ニュース強制: {n.get('headline', n.get('id', 'NEWS'))}")
        self.store.save(st)

    def banker_force_job(self, player: str, job: str):
        st = self.ensure_initialized()
        p = st["players"][player]
        p["job"] = job
        self._log(st, f"[神] {player} の職業を {job} に変更")
        self.store.save(st)

    def banker_generation(self, new_generation: Optional[int] = None):
        st = self.ensure_initialized()
        st["generation"] = new_generation if new_generation else st["generation"] + 1
        st["turn"] = 1
        st["season_index"] = 0
        self._log(st, "[神] 世代交代を発動")
        self.store.save(st)

    def banker_imprison(self, player: str, turns: int):
        st = self.ensure_initialized()
        p = st["players"][player]
        p["jailed_until"] = max(p.get("jailed_until", 0), st["turn"] + int(turns))
        self._log(st, f"[神] {player} を {turns} ターン収監")
        self.store.save(st)

    def banker_release(self, player: str):
        st = self.ensure_initialized()
        p = st["players"][player]
        p["jailed_until"] = 0
        self._log(st, f"[神] {player} を釈放")
        self.store.save(st)

    def banker_marry(self, a: str, b: str):
        st = self.ensure_initialized()
        if a not in st["players"] or b not in st["players"]:
            return
        self._log(st, f"[神] {a} と {b} を強制的に結婚させました（演出のみ）")
        self.store.save(st)

    def banker_manage_codes(self, add_code: Optional[str] = None, remove_code: Optional[str] = None):
        st = self.ensure_initialized()
        if add_code and add_code not in st["secret_codes"]:
            st["secret_codes"].append(add_code)
            self._log(st, f"[神] 秘密コード追加: {add_code}")
        if remove_code and remove_code in st["secret_codes"]:
            st["secret_codes"].remove(remove_code)
            self._log(st, f"[神] 秘密コード削除: {remove_code}")
        self.store.save(st)

    # ---------- news & stocks ----------
    def _roll_news(self, st):
        # 0〜2件ランダム抽選
        k = random.randint(0, 2)
        pool = NEWS_EVENTS[:]
        if st["forbidden_unlocked"]:
            # 低確率で禁断ニュース
            if random.random() < 0.5:
                n = random.choice(FORBIDDEN_NEWS)
                n2 = dict(n)
                n2["until_turn"] = st["turn"] + n2.get("duration", 1)
                n2["forbidden"] = True
                st["news_active"].append(n2)
        for _ in range(k):
            n = random.choice(pool)
            n2 = dict(n)
            n2["until_turn"] = st["turn"] + n2.get("duration", 1)
            n2["forbidden"] = False
            st["news_active"].append(n2)
        # 期限切れを掃除
        st["news_active"] = [n for n in st["news_active"] if n.get("until_turn", st["turn"]) >= st["turn"]]

    def _apply_news_stock_effect(self, st, s: Dict[str, Any], forbidden=False):
        mul = 1.0
        for n in st["news_active"]:
            if n.get("forbidden", False) != forbidden:
                continue
            if n["effect"] == "stock_up":
                if n["target"] in ("all", s["name"]):
                    mul *= float(n.get("bonus", 1.0))
            elif n["effect"] == "stock_crash":
                if n["target"] in ("all", s["name"]):
                    mul *= float(n.get("bonus", 1.0))
        return mul

    def get_player(self, name: str):
        st = self.store.get_state()
        players = st.setdefault("players", {})
        pdata = players.get(name)
        if not pdata:
            pdata = players[name] = {
                "name": name,
                "money": 0,
                "happiness": 50,
                "popularity": 0,
                "debt": 0,
                "stamps": 0,
                "full_cards": 0,
            }
        # 既存データに不足キーがあったら埋める
        pdata.setdefault("stamps", 0)
        pdata.setdefault("full_cards", 0)
        return st, pdata

    def add_debt(self, name: str, delta: int):
        st, p = self.get_player(name)
        p["debt"] = int(p.get("debt", 0)) + int(delta)
        self._log(st, f"{name} の借金 {delta:+d} → {p['debt']}")
        self.store.update_state(st)

    def adjust_happiness(self, name: str, delta: int):
        st, p = self.get_player(name)
        p["happiness"] = max(0, min(100, int(p.get("happiness", 50)) + int(delta)))
        self._log(st, f"{name} の幸福度 {delta:+d} → {p['happiness']}")
        self.store.update_state(st)

    def adjust_popularity(self, name: str, delta: int):
        st, p = self.get_player(name)
        p["popularity"] = int(p.get("popularity", 0)) + int(delta)
        self._log(st, f"{name} の人気 {delta:+d} → {p['popularity']}")
        self.store.update_state(st)

    def random_change_job(self, name: str):
        from random import choice

        st, p = self.get_player(name)
        jobs = ["無職", "農家", "投資家", "公務員", "料理人", "警察官", "Youtuber"]
        before = p.get("job", "無職")
        p["job"] = choice(jobs)
        self._log(st, f"{name} の職業: {before} → {p['job']}（ルーレット）")
        self.store.update_state(st)

    # ---- スタンプ連動：購入時に呼び出す -------------------------------

    def add_stamp(self, name: str, count: int = 1, threshold: int = 10) -> dict:
        """
        購入ごとにスタンプを加算。
        threshold 到達ごとに full_cards を+1し、stamps は閾値でロールオーバー。
        戻り値: {"stamps": 現在値, "full_cards": 合計, "completed": 直近で満タンになった枚数}
        """
        st, p = self.get_player(name)
        before = int(p.get("stamps", 0))
        total = before + int(count)
        completed = total // threshold
        remainder = total % threshold

        p["stamps"] = remainder
        if completed:
            p["full_cards"] = int(p.get("full_cards", 0)) + completed
            self._log(
                st,
                f"🟡 {name} のスタンプが満タン ×{completed}（満タンカード {p['full_cards']}）",
            )
        else:
            self._log(st, f"🟢 {name} のスタンプ +{count} → {p['stamps']}/{threshold}")

        self.store.update_state(st)
        return {
            "stamps": p["stamps"],
            "full_cards": p["full_cards"],
            "completed": completed,
        }

    def get_stamp_progress(
        self, name: str, threshold: int = 10
    ) -> tuple[int, int, int]:
        """
        現在のスタンプ・満タンカード・しきい値を返す。
        """
        _, p = self.get_player(name)
        return int(p.get("stamps", 0)), int(p.get("full_cards", 0)), threshold

    def _update_stocks(self, st):
        # 通常
        for s in st["stocks"]:
            base = s["price"]
            drift = random.uniform(-s["volatility"], s["volatility"])
            price = max(1, int(round(base * (1 + drift))))
            price = max(1, int(round(price * self._apply_news_stock_effect(st, s, forbidden=False))))
            s["price"] = price
        # 禁断
        for s in st["forbidden_stocks"]:
            base = s["price"]
            drift = random.uniform(-s["volatility"], s["volatility"])
            price = max(1, int(round(base * (1 + drift))))
            price = max(1, int(round(price * self._apply_news_stock_effect(st, s, forbidden=True))))
            s["price"] = price
        # 配当：オーナーに等比で（簡易）
        for p in st["players"].values():
            gain = 0
            for name, shares in p["stocks"].items():
                s = self._find_stock(st, name) or self._find_stock(st, name, forbidden=True)
                if not s: 
                    continue
                gain += int(shares * s["price"] * 0.01)  # 1%/ターン（簡易）
            if gain:
                p["money"] += gain
                self._log(st, f"{p['name']} は配当 {gain} 万円を受け取り")

    # ---------- stocks trade ----------
    def trade_stock(self, player: str, name: str, shares: int, forbidden=False):
        st = self.ensure_initialized()
        s = self._find_stock(st, name, forbidden=forbidden)
        if not s: 
            return False, "銘柄がありません"
        p = st["players"][player]
        price = int(s["price"]) * int(abs(shares))
        fee_rate = JOBS.get(p["job"], {}).get("passives", {}).get("stock_fee", 0.05)
        fee = 0 if fee_rate == 0.0 else int(round(price * fee_rate))
        if shares > 0:
            # buy
            need = price + fee
            if p["money"] < need:
                return False, "所持金が足りません"
            p["money"] -= need
            p["stocks"][name] = p["stocks"].get(name, 0) + shares
            self._log(st, f"{player} が {name} を {shares} 株購入（手数料{fee}）")
        else:
            # sell
            cur = p["stocks"].get(name, 0)
            if cur < abs(shares):
                return False, "保有株が不足"
            p["stocks"][name] = cur - abs(shares)
            p["money"] += price - fee
            self._log(st, f"{player} が {name} を {abs(shares)} 株売却（手数料{fee}）")
        self.store.save(st)
        return True, "OK"

    # ---------- forbidden unlock by code ----------
    def input_secret_code(self, code: str) -> bool:
        st = self.ensure_initialized()
        if code in st["secret_codes"]:
            eff = SECRET_CODES.get(code, {})
            if eff.get("unlock") == "forbidden_market":
                st["forbidden_unlocked"] = True
                self._log(st, f"禁断市場が解禁されました（{code}）")
            if "grant" in eff:
                g = eff["grant"]
                # 全員に適用（例）
                for p in st["players"].values():
                    p["money"] += int(g.get("money", 0))
                self._log(st, f"秘密コード {code} の効果を適用（grant）")
            self.store.save(st)
            return True
        return False

    # ---------- crime system ----------
    def commit_crime(self, player: str) -> str:
        st = self.ensure_initialized()
        if st["time_of_day"] != NIGHT:
            return "犯罪は夜のみ実行可能です"
        p = st["players"][player]
        if st["turn"] < p.get("jailed_until", 0):
            return "服役中は行動できません"
        # 簡易：成功50%
        if random.random() < 0.5:
            earn = random.randint(1, 10)
            p["money"] += earn
            result = f"成功！ +{earn} 万円"
        else:
            fine = random.randint(1, 5)
            p["debt"] += fine
            # 逮捕リスク：20%
            if random.random() < 0.2:
                jail = random.randint(1, 3)
                p["jailed_until"] = st["turn"] + jail
                result = f"逮捕… 懲役{jail}ターン・罰金{fine}万円"
            else:
                result = f"失敗… 罰金{fine}万円"
        p["crime_count"] = int(p.get("crime_count", 0)) + 1
        rank = crime_rank_from_count(p["crime_count"])
        if rank and rank not in p["titles"]:
            p["titles"].append(rank)
            self._log(st, f"{player} の犯罪ランクが {rank} に昇格")
        self._log(st, f"{player} が犯罪行為を実行：{result}")
        self.store.save(st)
        return result

    def confess(self, player: str) -> str:
        st = self.ensure_initialized()
        p = st["players"][player]
        # ランクを一段階下げる処理（簡易：titlesから犯罪系で最大のものを削除）
        order = [r for _, r in sorted(CRIME_THRESHOLDS, key=lambda x:-x[0])]
        for r in order:
            if r in p["titles"]:
                p["titles"].remove(r)
                p["crime_count"] = max(0, p["crime_count"] - 1)
                self._log(st, f"{player} が自首。犯罪ランク {r} を返上")
                self.store.save(st)
                return f"自首しました。{r} を返上"
        return "返上できる犯罪ランクはありません"

    # ---------- roulette (banker) ----------
    def spin_roulette(self, player: str, kind: str) -> str:
        st = self.ensure_initialized()
        table = ROULETTE_TABLE.get(kind, [])
        if not table:
            return "未設定"
        weights = [int(x.get("weight", 1)) for x in table]
        choice = random.choices(table, weights=weights, k=1)[0]
        p = st["players"][player]
        msg = choice.get("label", "結果")
        if "delta_money" in choice:
            p["money"] += int(choice["delta_money"])
        if "delta_happiness" in choice:
            p["happiness"] += int(choice["delta_happiness"])
        if choice.get("job_bonus"):
            p["popularity"] += 1
            msg += "（人気+1）"
        self._log(st, f"[ルーレット] {player}: {msg}")
        self.store.save(st)
        return msg

    def _ensure_catalog(self, st):
        if "market" not in st:
            st["market"] = []  # {id, seller, name, price}
        if "property_catalog" not in st:
            # 簡易生成
            st["property_catalog"] = []
            idx = 1
            for pf in PREFECTURES:
                for ct in CITIES:
                    for dt in DISTRICTS:
                        b = random.choice(BUILDING_NAMES)
                        price = random.randint(30, 120)
                        st["property_catalog"].append({
                            "id": idx,
                            "name": f"{pf}{ct}{dt}・{b}",
                            "price": price,
                            "rent": int(price * RENT_RATE),
                        })
                        idx += 1

    # ---------- market ----------
    def market_list(self, seller: str, item_name: str, price: int):
        st = self.ensure_initialized()
        self._ensure_catalog(st)
        iid = (st["market"][-1]["id"] + 1) if st["market"] else 1
        st["market"].append({"id": iid, "seller": seller, "name": item_name, "price": int(price)})
        self._log(st, f"{seller} が市場に『{item_name}』({price}万)を出品")
        self.store.save(st)
        return iid

    def market_buy(self, buyer: str, item_id: int):
        st = self.ensure_initialized()
        self._ensure_catalog(st)
        item = next((x for x in st["market"] if x["id"] == int(item_id)), None)
        if not item:
            return False, "該当商品がありません"
        p_buyer = st["players"][buyer]
        if p_buyer["money"] < item["price"]:
            return False, "所持金不足"
        p_buyer["money"] -= item["price"]
        # 売上を売り手に
        seller = item["seller"]
        if seller in st["players"]:
            st["players"][seller]["money"] += int(item["price"])
            st["players"][seller]["sales_since_tax"] += int(item["price"])
        # スタンプ付与
        stamps = item["price"] // STAMP_PER_PRICE
        p_buyer["stamps"] = int(p_buyer.get("stamps", 0)) + int(stamps)
        while p_buyer["stamps"] >= STAMP_TARGET:
            p_buyer["stamps"] -= STAMP_TARGET
            p_buyer["full_cards"] += 1
            self._log(st, f"{buyer} のスタンプが満タンになりました → 満タンカード+1")
        # ログ
        self._log(st, f"{buyer} が『{item['name']}』を {item['price']} 万で購入（スタンプ+{stamps}）")
        # 市場から削除
        st["market"] = [x for x in st["market"] if x["id"] != item["id"]]
        self.store.save(st)
        return True, "購入完了"

    def exchange_card(self, player: str, reward_name: str) -> str:
        st = self.ensure_initialized()
        p = st["players"][player]
        rw = next((r for r in CARD_REWARDS if r["name"] == reward_name), None)
        if not rw:
            return "景品がありません"
        if p["full_cards"] < rw["cost"]:
            return "カード不足"
        p["full_cards"] -= rw["cost"]
        if rw["type"] == "money":
            p["money"] += int(rw["value"])
        elif rw["type"] == "happiness":
            p["happiness"] = min(100, p["happiness"] + int(rw["value"]))
        elif rw["type"] == "furniture":
            # マイルーム用に保持
            p.setdefault("furniture", []).append(rw["value"])
        self._log(st, f"{player} が『{reward_name}』と交換")
        self.store.save(st)
        return "交換しました"

    # ---------- real estate ----------
    def buy_property(self, player: str, prop_id: int) -> str:
        st = self.ensure_initialized()
        self._ensure_catalog(st)
        pr = next((x for x in st["property_catalog"] if x["id"] == int(prop_id)), None)
        if not pr:
            return "物件がありません"
        p = st["players"][player]
        if p["money"] < pr["price"]:
            return "所持金不足"
        p["money"] -= int(pr["price"])
        p["properties"].append({"name": pr["name"], "price": pr["price"], "rent": pr["rent"]})
        self._log(st, f"{player} が不動産『{pr['name']}』を購入（{pr['price']}万）")
        self.store.save(st)
        return "購入しました"

    # ---------- cooking ----------
    def cook(self, player: str, recipe_name: str) -> str:
        st = self.ensure_initialized()
        rc = RECIPES.get(recipe_name)
        if not rc:
            return "レシピがありません"
        cost = sum(rc["ingredients"].values())  # 1素材=1万円として簡易コスト
        p = st["players"][player]
        if p["money"] < cost:
            return "所持金不足"
        p["money"] -= int(cost)
        # 効果：幸福度+材料数*2
        delta = min(100 - p["happiness"], len(rc["ingredients"]) * 2)
        p["happiness"] += delta
        self._log(st, f"{player} が料理『{recipe_name}』を作成（幸福+{delta}）")
        self.store.save(st)
        return f"美味しくできた！（幸福+{delta}）"

    # ---------- collection ----------
    def collect_random(self, player: str, category: str) -> str:
        st = self.ensure_initialized()
        pool = COLLECTIBLES.get(category, [])
        if not pool:
            return "カテゴリがありません"
        item = random.choice(pool)
        p = st["players"][player]
        coll = p.setdefault("collection", {}).setdefault(category, [])
        if item in coll:
            return f"既に『{item}』は集めました"
        coll.append(item)
        p["happiness"] = min(100, p["happiness"] + 1)
        self._log(st, f"{player} がコレクション『{category}:{item}』を入手（幸福+1）")
        self.store.save(st)
        return f"『{item}』をコレクション！"

    # ---------- pets ----------
    def buy_pet(self, player: str, pet_name: str) -> str:
        st = self.ensure_initialized()
        pd = PETS.get(pet_name)
        if not pd:
            return "ペットが見つかりません"
        p = st["players"][player]
        if p["money"] < pd["price"]:
            return "所持金不足"
        p["money"] -= int(pd["price"])
        p["pets"].append(pet_name)
        p["happiness"] = min(100, p["happiness"] + int(pd["happiness_boost"]))
        self._log(st, f"{player} が『{pet_name}』を飼い始めました（幸福+{pd['happiness_boost']}）")
        self.store.save(st)
        return "購入しました"

    # ---------- npc ----------
    def npc_talk(self, player: str, npc_name: str) -> str:
        st = self.ensure_initialized()
        st.setdefault("npcs", {k: dict(v) for k, v in NPCS.items()})
        if npc_name not in st["npcs"]:
            return "NPCがいません"
        st["npcs"][npc_name]["affinity"] += 1
        self._log(st, f"{player} が {npc_name} と交流（親交+1）")
        self.store.save(st)
        return "仲良くなった！"

    # ---------- generation (inherit) ----------
    def add_child(self, player: str, child_name: str, age: int):
        st = self.ensure_initialized()
        p = st["players"][player]
        p["children"].append({"name": child_name, "age": int(age)})
        self._log(st, f"{player} に子『{child_name}』が追加")
        self.store.save(st)

    def do_generation_inherit(self, player: str, ratios: List[int]):
        st = self.ensure_initialized()
        p = st["players"][player]
        kids = p.get("children", [])
        if not kids:
            return "子どもがいません"
        s = sum(ratios) if ratios else 0
        if s <= 0:
            return "配分が無効です"
        # 新プレイヤー作成
        for kid, r in zip(kids, ratios):
            share = int(p["money"] * (r / s))
            name = kid["name"]
            if name in st["players"]:  # 既存なら加算
                st["players"][name]["money"] += share
            else:
                st["players"][name] = self._new_player(name)
                st["players"][name]["money"] = share
        self._log(st, f"{player} は資産を子へ分配し世代交代")
        # 元プレイヤーは引退（演出のみ・所持金0化）
        p["money"] = 0
        self.banker_generation()
        self.store.save(st)
        return "世代交代完了"

    # ---- override: apply passives extended with rent ----
    def _apply_passives_and_fees(self, st):
        for p in st["players"].values():
            job = JOBS.get(p["job"], {})
            # 職業収入
            if "income_per_turn" in job.get("passives", {}):
                inc = int(job["passives"]["income_per_turn"])
                p["money"] += inc
                self._log(st, f"{p['name']}（{p['job']}）毎ターン収入 +{inc} 万円")
            # 家賃収入
            rent = sum(int(x.get("rent", 0)) for x in p.get("properties", []))
            if rent:
                p["money"] += rent
                self._log(st, f"{p['name']} 不動産家賃 +{rent} 万円")
            # 資格維持費
            fee_total = 0
            for q in p.get("qualifications", []):
                qd = QUALIFICATIONS.get(q, {})
                fee_total += int(qd.get("maintenance", 0))
            if fee_total:
                p["money"] -= fee_total
                self._log(st, f"{p['name']} 資格維持費 -{fee_total} 万円")

    # ---- override: taxes add dependent deduction ----
    def _collect_taxes(self, st):
        total_to_treasury = 0
        for p in st["players"].values():
            # 住民税
            job = JOBS.get(p["job"], {})
            residence_tax = 0 if job.get("passives", {}).get("residence_tax_free") else RESIDENCE_TAX
            # 扶養控除（子ども + ペット）
            dependents = len(p.get("children", [])) + len(p.get("pets", []))
            deduction = dependents * DEDUCTION_PER_DEPENDENT
            # 課税所得（簡易）：sales_since_tax - 扶養控除
            taxable = max(0, int(p.get("sales_since_tax", 0)) - deduction)
            income_tax = 0
            last_threshold = 0
            for threshold, rate in sorted(INCOME_TAX_RATES.items()):
                if taxable > threshold:
                    income_tax = int(threshold * rate)  # 簡易
                    last_threshold = threshold
            if taxable > last_threshold:
                income_tax = int(taxable * INCOME_TAX_RATES[max(INCOME_TAX_RATES.keys())])
            # 固定資産税
            prop_base = sum([int(x.get("price", 0)) for x in p.get("properties", [])])
            property_tax = int(round(prop_base * PROPERTY_TAX_RATE))
            total = residence_tax + income_tax + property_tax
            if total:
                p["money"] -= total
                total_to_treasury += total
                self._log(
                    st,
                    f"{p['name']} 納税 -{total}（住{residence_tax}・所{income_tax}・固{property_tax}・扶養控除{deduction}）",
                )
                p["sales_since_tax"] = 0
        st["treasury"] += total_to_treasury
        if total_to_treasury:
            self._log(st, f"国庫に +{total_to_treasury} 万円")
    # ---------- inventory ----------
    def add_inventory(self, player: str, item: str, qty: int = 1):
        st = self.ensure_initialized()
        p = st["players"][player]
        inv = p.setdefault("inventory", {})
        inv[item] = int(inv.get(item, 0)) + int(qty)
        self._log(st, f"{player} の在庫『{item}』+{qty}")
        self.store.save(st)

    def consume_inventory(self, player: str, needed: dict) -> bool:
        """必要材料を在庫から消費。足りなければFalse"""
        st = self.ensure_initialized()
        p = st["players"][player]
        inv = p.setdefault("inventory", {})
        # チェック
        for k, v in needed.items():
            if inv.get(k, 0) < int(v):
                return False
        # 消費
        for k, v in needed.items():
            inv[k] -= int(v)
        self.store.save(st)
        return True

    def inventory_text(self, player: str) -> str:
        st = self.ensure_initialized()
        inv = st["players"][player].get("inventory", {})
        if not inv:
            return "（在庫なし）"
        return ", ".join([f"{k}×{v}" for k, v in inv.items() if v > 0]) or "（在庫なし）"

    def npc_special_event(self, player: str, npc_name: str) -> str:
        st = self.ensure_initialized()
        from masters import NPC_EVENTS

        st.setdefault("npcs", {k: dict(v) for k, v in NPCS.items()})
        if npc_name not in st["npcs"]:
            return "NPCがいません"
        ev = NPC_EVENTS.get(npc_name)
        if not ev:
            return "イベントなし"
        if st["npcs"][npc_name]["affinity"] < ev["threshold"]:
            return "まだ親交が足りません"
        p = st["players"][player]
        done = p.setdefault("npc_events_done", [])
        key = f"{npc_name}"
        if key in done:
            return "もう受け取り済みです"
        # 付与
        rwd = ev["reward"]
        if "money" in rwd:
            p["money"] += int(rwd["money"])
        if "popularity" in rwd:
            p["popularity"] = int(p.get("popularity", 0)) + int(rwd["popularity"])
        if "item" in rwd:
            name, q = rwd["item"]
            self.add_inventory(player, name, int(q))
        done.append(key)
        self._log(st, f"{player} が {npc_name} イベント報酬を獲得")
        self.store.save(st)
        return ev.get("text", "報酬GET")
