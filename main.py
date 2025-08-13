# -*- coding: utf-8 -*-
from kivy.lang import Builder
Builder.load_file("ui.kv")
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from backup_manager import (export_backup,quick_export_backup,import_backup,import_latest_backup,)
from roulette import ROULETTE_TABLE
from animations import ReceiptOverlay, StampCardOverlay
from store import StateStore
from game_logic import Game
from masters import DAY, NIGHT, SEASONS, NEWS_EVENTS, FORBIDDEN_NEWS

KV = r"""
#:import dp kivy.metrics.dp
<Root@MDBoxLayout>:
    orientation: "vertical"
    MDToolbar:
        title: "リアルお店屋さんごっこ（Android/Offline）"
        elevation: 4
    MDTabs:
        id: tabs
        on_tab_switch: app.on_tab_switch(*args)
        Tab:
            title: "プレイヤー"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(10)
                MDLabel:
                    id: status_lbl
                    text: app.status_text
                    halign: "left"
                MDTextField:
                    id: target_player
                    hint_text: "プレイヤー名（例：たろう）"
                    text: "たろう"
                    helper_text: "対象プレイヤー"
                    helper_text_mode: "on_focus"
                MDGridLayout:
                    cols: 3
                    adaptive_height: True
                    spacing: dp(6)
                    MDRaisedButton:
                        text: "次のターン"
                        on_release: app.next_turn()
                    MDRaisedButton:
                        text: "昼"
                        on_release: app.set_time("昼")
                    MDRaisedButton:
                        text: "夜"
                        on_release: app.set_time("夜")
                MDGridLayout:
                    cols: 2
                    adaptive_height: True
                    spacing: dp(6)
                    MDRaisedButton:
                        text: "犯罪を実行(夜)"
                        on_release: app.commit_crime(target_player.text)
                    MDRaisedButton:
                        text: "自首する"
                        on_release: app.confess(target_player.text)
        Tab:
            title: "株式"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(10)
                MDTextField:
                    id: stock_name
                    hint_text: "銘柄名（例：ITキングダム）"
                MDTextField:
                    id: stock_amount
                    hint_text: "株数（+買い / -売り）"
                    text: "1"
                MDGridLayout:
                    cols: 2
                    adaptive_height: True
                    spacing: dp(6)
                    MDRaisedButton:
                        text: "取引(通常)"
                        on_release: app.trade(stock_name.text, stock_amount.text, False)
                    MDRaisedButton:
                        text: "取引(禁断)"
                        on_release: app.trade(stock_name.text, stock_amount.text, True)
                MDTextField:
                    id: code_field
                    hint_text: "秘密コードを入力（Zodiac77 など）"
                MDRaisedButton:
                    text: "コード適用"
                    on_release: app.apply_code(code_field.text)
        Tab:
            title: "銀行員(神)"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(10)
                MDTextField:
                    id: admin_user
                    hint_text: "ユーザー名（既定：admin）"
                    text: "admin"
                MDTextField:
                    id: admin_pass
                    hint_text: "パスワード（既定：1234）"
                    password: True
                MDRaisedButton:
                    text: "ログイン"
                    on_release: app.admin_login(admin_user.text, admin_pass.text)
                MDSeparator:
                MDLabel:
                    text: "ログイン後：各種介入"
                MDTextField:
                    id: tgt
                    hint_text: "対象プレイヤー名"
                    text: "たろう"
                MDGridLayout:
                    cols: 3
                    spacing: dp(6)
                    adaptive_height: True
                    MDTextField:
                        id: delta_money
                        hint_text: "所持金±"
                        text: "10"
                    MDRaisedButton:
                        text: "付与/徴収"
                        on_release: app.god_money(tgt.text, delta_money.text)
                    MDRaisedButton:
                        text: "人気+1"
                        on_release: app.god_popularity(tgt.text, "1")
                MDGridLayout:
                    cols: 3
                    spacing: dp(6)
                    adaptive_height: True
                    MDTextField:
                        id: title_field
                        hint_text: "称号を付与"
                    MDRaisedButton:
                        text: "称号付与"
                        on_release: app.god_title(tgt.text, title_field.text)
                    MDRaisedButton:
                        text: "釈放"
                        on_release: app.god_release(tgt.text)
                MDGridLayout:
                    cols: 3
                    spacing: dp(6)
                    adaptive_height: True
                    MDRaisedButton:
                        text: "投獄(1T)"
                        on_release: app.god_jail(tgt.text, "1")
                    MDRaisedButton:
                        text: "季節→夏"
                        on_release: app.god_set_season("夏")
                    MDRaisedButton:
                        text: "禁断 解禁"
                        on_release: app.god_toggle_forbidden(True)
                MDGridLayout:
                    cols: 2
                    spacing: dp(6)
                    adaptive_height: True
                    MDRaisedButton:
                        text: "ニュース強制(通常)"
                        on_release: app.god_news(False)
                    MDRaisedButton:
                        text: "ニュース強制(禁断)"
                        on_release: app.god_news(True)
                MDGridLayout:
                    cols: 2
                    spacing: dp(6)
                    adaptive_height: True
                    MDRaisedButton:
                        text: "世代交代"
                        on_release: app.god_generation()
                    MDRaisedButton:
                        text: "国庫+100"
                        on_release: app.god_treasury("100")

        Tab:
            title: "市場"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(8)
                MDTextField:
                    id: m_seller
                    hint_text: "出品者（プレイヤー名）"
                    text: "たろう"
                MDTextField:
                    id: m_name
                    hint_text: "商品名"
                MDTextField:
                    id: m_price
                    hint_text: "価格（万円）"
                    text: "5"
                MDGridLayout:
                    cols: 2
                    adaptive_height: True
                    MDRaisedButton:
                        text: "出品"
                        on_release: app.market_list(m_seller.text, m_name.text, m_price.text)
                    MDRaisedButton:
                        text: "更新"
                        on_release: app.refresh_status()
                MDLabel:
                    text: "購入"
                MDTextField:
                    id: m_item_id
                    hint_text: "商品ID"
                MDTextField:
                    id: m_buyer
                    hint_text: "購入者（プレイヤー名）"
                    text: "はなこ"
                MDRaisedButton:
                    text: "購入する"
                    on_release: app.market_buy(m_buyer.text, m_item_id.text)
                MDSeparator:
                MDLabel:
                    id: market_list_lbl
                    text: app.market_text
                    halign: "left"
                MDSeparator:
                MDLabel:
                    text: "スタンプ/満タンカード"
                MDTextField:
                    id: ex_player
                    hint_text: "交換するプレイヤー"
                    text: "はなこ"
                MDTextField:
                    id: ex_reward
                    hint_text: "景品名（例：50万円と交換）"
                MDRaisedButton:
                    text: "カード交換"
                    on_release: app.exchange_card(ex_player.text, ex_reward.text)
        Tab:
            title: "不動産"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(8)
                MDTextField:
                    id: rp_player
                    hint_text: "購入者"
                    text: "たろう"
                MDTextField:
                    id: rp_id
                    hint_text: "物件ID"
                MDRaisedButton:
                    text: "購入"
                    on_release: app.buy_property(rp_player.text, rp_id.text)
                MDSeparator:
                MDTextField:
                    id: rp_search
                    hint_text: "検索（名字/建物などの一部）"
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(6)
                    MDRaisedButton:
                        text: "前へ"
                        on_release: app.prop_prev()
                    MDRaisedButton:
                        text: "次へ"
                        on_release: app.prop_next()
                MDLabel:
                    id: prop_list_lbl
                    text: app.property_text
                    halign: "left"
        Tab:
            title: "料理"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(8)
                MDTextField:
                    id: c_player
                    hint_text: "料理する人"
                    text: "はなこ"
                MDTextField:
                    id: c_recipe
                    hint_text: "レシピ名（例：おにぎり）"
                MDRaisedButton:
                    text: "作る"
                    on_release: app.cook(c_player.text, c_recipe.text)
                MDSeparator:
                MDLabel:
                    text: "在庫: " + app.inventory_text(c_player.text)
                    halign: "left"
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(8)
                    MDRaisedButton:
                        text: "釣りで魚GET"
                        on_release: app.mg_fishing(c_player.text)
                    MDRaisedButton:
                        text: "畑で野菜GET"
                        on_release: app.mg_farming(c_player.text)
        Tab:
            title: "コレクション"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(8)
                MDTextField:
                    id: col_player
                    hint_text: "プレイヤー"
                    text: "はなこ"
                MDTextField:
                    id: col_cat
                    hint_text: "カテゴリ（昆虫/魚/化石）"
                MDRaisedButton:
                    text: "ランダムGET"
                    on_release: app.collect(col_player.text, col_cat.text)
        Tab:
            title: "ペット"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(8)
                MDTextField:
                    id: pet_player
                    hint_text: "購入者"
                    text: "はなこ"
                MDTextField:
                    id: pet_name
                    hint_text: "ペット名（例：いぬ）"
                MDRaisedButton:
                    text: "購入"
                    on_release: app.buy_pet(pet_player.text, pet_name.text)
        Tab:
            title: "NPC"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(8)
                MDTextField:
                    id: npc_player
                    hint_text: "プレイヤー"
                    text: "たろう"
                MDTextField:
                    id: npc_name
                    hint_text: "NPC名（例：熱血市長）"
                MDRaisedButton:
                    text: "話す"
                    on_release: app.npc_talk(npc_player.text, npc_name.text)
                MDRaisedButton:
                    text: "イベント受取"
                    on_release: app.npc_event(npc_player.text, npc_name.text)
        Tab:
            title: "世代交代"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(8)
                MDTextField:
                    id: g_player
                    hint_text: "親プレイヤー"
                    text: "たろう"
                MDTextField:
                    id: child_name
                    hint_text: "子の名前"
                MDTextField:
                    id: child_age
                    hint_text: "年齢"
                    text: "8"
                MDRaisedButton:
                    text: "子を追加"
                    on_release: app.add_child(g_player.text, child_name.text, child_age.text)
                MDSeparator:
                MDTextField:
                    id: ratios
                    hint_text: "配分カンマ（例：50,50）"
                MDRaisedButton:
                    text: "世代交代"
                    on_release: app.do_inherit(g_player.text, ratios.text)
        Tab:
            title: "ミニゲーム"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(10)
                MDRaisedButton:
                    text: "ケーキ屋：タイミング"
                    on_release: app.minigame_cake('はなこ')
                MDRaisedButton:
                    text: "農家：タップ連打"
                    on_release: app.minigame_farmer('たろう')
                MDRaisedButton:
                    text: "ケーキ屋：ストップバー"
                    on_release: app.ui_cake_stop('はなこ')
                MDRaisedButton:
                    text: "警察官：隠しアイコン"
                    on_release: app.ui_police_find('たろう')
                MDRaisedButton:
                    text: "DJ：ビートタップ"
                    on_release: app.ui_dj('はなこ')
                MDRaisedButton:
                    text: "料理人：手順記憶"
                    on_release: app.ui_chef_memory('はなこ')

        Tab:
            title: "ルーレット"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(10)
                MDTextField:
                    id: rp
                    hint_text: "対象プレイヤー"
                    text: "たろう"
                MDGridLayout:
                    cols: 3
                    adaptive_height: True
                    spacing: dp(6)
                    MDRaisedButton:
                        text: "宝くじ"
                        on_release: app.spin(rp.text, "lottery")
                    MDRaisedButton:
                        text: "病気"
                        on_release: app.spin(rp.text, "illness")
                    MDRaisedButton:
                        text: "転職"
                        on_release: app.spin(rp.text, "job_change")
"""

class ShopGameApp(App):
    # --- Visual state ---
    prop_page = 0
    prop_per_page = 30

    def _toast(self, msg):
        try:
            from kivymd.toast import toast
            toast(str(msg))
        except Exception:
            print(msg)

    # ----- Receipt & Stamp Dialog -----
    def show_receipt(self, buyer, msg):
        from kivymd.uix.dialog import MDDialog
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        w = BoxLayout(orientation="vertical", padding=10, spacing=8, size_hint_y=None)
        w.bind(minimum_height=w.setter("height"))
        w.add_widget(Label(text=f"[レシート]\\n{buyer} : {msg}", halign="center"))
        # スタンプ可視化
        st = self.game.ensure_initialized()
        p = st["players"].get(buyer, {})
        stamps = int(p.get("stamps", 0))
        filled = "●"*stamps + "○"*(10-stamps if stamps<=10 else 0)
        w.add_widget(Label(text=f"スタンプ: {filled}  / 満タンカード: {int(p.get('full_cards',0))}"))
        self._receipt_dialog = MDDialog(title="購入レシート", type="custom", content_cls=w)
        self._receipt_dialog.open()
        # 紙が落ちるような演出（高さを変える）
        from kivy.animation import Animation
        if hasattr(self._receipt_dialog, 'children') and self._receipt_dialog.children:
            try:
                anim = Animation(opacity=0, d=0) + Animation(opacity=1, d=0.2)
                anim.start(self._receipt_dialog)
            except Exception:
                pass

    # ----- Property catalog paging/search -----
    def _prop_filtered(self):
        st = self.game.ensure_initialized()
        self.game._ensure_catalog(st)
        q = ""
        try:
            q = self.root.ids.rp_search.text or ""
        except Exception:
            pass
        items = st["property_catalog"]
        if q:
            ql = q.lower()
            items = [x for x in items if ql in x["name"].lower()]
        return items

    def _render_prop_page(self):
        items = self._prop_filtered()
        n = self.prop_per_page
        page = max(0, self.prop_page)
        start = page*n
        page_items = items[start:start+n]
        lines = [f"[不動産] page {page+1} / {max(1,(len(items)+n-1)//n)}"]
        for pr in page_items:
            lines.append(f"ID={pr['id']} / {pr['name']} / 価格{pr['price']}万 / 家賃{pr['rent']}万")
        self.property_text = "\n".join(lines)

    def prop_prev(self):
        if self.prop_page>0:
            self.prop_page -= 1
            self._render_prop_page()
    def prop_next(self):
        self.prop_page += 1
        self._render_prop_page()

    def refresh_lists(self):
        super(ShopGameApp, self).refresh_lists()
        # 上書き: 物件ページ再描画
        try:
            self._render_prop_page()
        except Exception:
            pass

    # ----- Inventory actions -----
    def inventory_text(self, player):
        try:
            return self.game.inventory_text(player)
        except Exception:
            return "（在庫なし）"

    def mg_fishing(self, player):
        # 成功で魚ランダム1～2
        q = __import__("random").randint(1,2)
        fish = __import__("random").choice(["アジ","タイ","マグロ"])
        self.game.add_inventory(player, fish, q)
        self._toast(f"釣れた！{fish}×{q}")
        self.refresh_status()

    def mg_farming(self, player):
        q = __import__("random").randint(1,3)
        veg = __import__("random").choice(["野菜","お米"])
        self.game.add_inventory(player, veg, q)
        self._toast(f"収穫！{veg}×{q}")
        self.refresh_status()

    # ----- NPC special event -----
    def npc_event(self, player, npc):
        self._toast(self.game.npc_special_event(player, npc))
        self.refresh_status()

    # ----- Market overrides to call receipt dialog -----
    def market_buy(self, buyer, item_id):
        try:
            iid = int(item_id)
        except:
            return self._toast("IDは数値で")
        ok, msg = self.game.market_buy(buyer, iid)
        self._toast(msg)
        if ok:
            self.show_receipt(buyer, msg)
        self.refresh_lists()

    # ----- Advanced Minigames UI -----
    def ui_cake_stop(self, player):
        # 動くスライダーを止める
        from kivymd.uix.dialog import MDDialog
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.slider import Slider
        from kivy.uix.button import Button
        from kivy.clock import Clock
        lay = BoxLayout(orientation="vertical", spacing=10, padding=10)
        sld = Slider(min=0, max=1, value=0)
        lay.add_widget(sld)
        b = Button(text="止める")
        lay.add_widget(b)
        dlg = MDDialog(title="ケーキ屋：ストップバー", type="custom", content_cls=lay, auto_dismiss=False)
        self._cake_dir = 1
        def tick(dt):
            v = sld.value + self._cake_dir*0.02
            if v>=1: v, self._cake_dir = 1, -1
            if v<=0: v, self._cake_dir = 0, 1
            sld.value = v
        ev = Clock.schedule_interval(tick, 0.02)
        center = (0.45, 0.55)
        def on_stop(instance):
            ev.cancel()
            v = sld.value
            if center[0]<=v<=center[1]:
                self.game.banker_adjust_money(player, 5)
                self._toast("大成功！+5万")
            else:
                self._toast(f"惜しい… v={v:.2f}")
            dlg.dismiss()
            self.refresh_status()
        b.bind(on_release=on_stop)
        dlg.open()

    def ui_police_find(self, player):
        # 16マスの中から⭐を制限時間で探す
        from kivymd.uix.dialog import MDDialog
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.button import Button
        from kivy.clock import Clock
        N = 16
        star = __import__("random").randint(0, N-1)
        grid = GridLayout(cols=4, spacing=6, padding=6)
        btns = []
        for i in range(N):
            btn = Button(text="?", size_hint_y=None, height=50)
            btns.append(btn); grid.add_widget(btn)
        dlg = MDDialog(title="警察官：隠しアイコン", type="custom", content_cls=grid, auto_dismiss=False)
        found = {"ok": False}
        def on_btn(idx):
            def cb(_):
                if idx==star:
                    found["ok"] = True
                    self.game.banker_adjust_money(player, 5)
                    self._toast("発見！+5万")
                    dlg.dismiss()
                    self.refresh_status()
                else:
                    btns[idx].text = "×"
            return cb
        for i,b in enumerate(btns):
            b.bind(on_release=on_btn(i))
        def timeout(dt):
            if not found["ok"]:
                self._toast("時間切れ…")
                dlg.dismiss()
        Clock.schedule_once(timeout, 10)
        dlg.open()

    def ui_dj(self, player):
        # 一定間隔のビートに合わせてタップ
        from kivymd.uix.dialog import MDDialog
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.clock import Clock
        interval = 0.9
        beats = 5
        window = 0.15
        lay = BoxLayout(orientation="vertical", spacing=8, padding=10)
        lbl = Label(text="♪ タップでビートに合わせよう")
        btn = Button(text="今！")
        lay.add_widget(lbl); lay.add_widget(btn)
        dlg = MDDialog(title="DJ：ビートタップ", type="custom", content_cls=lay, auto_dismiss=False)
        state = {"t0": None, "i": 0, "good": 0, "next": None}
        def start(dt):
            state["t0"] = __import__("time").time()
            state["i"] = 0; state["good"]=0
            def schedule_next():
                state["next"] = __import__("time").time() + interval
            schedule_next()
            def beat(dt2):
                if state["i"]>=beats:
                    dlg.dismiss()
                    gain = state["good"]
                    if gain>0:
                        self.game.banker_adjust_money(player, gain)
                    self._toast(f"Good {state['good']}/{beats}（+{gain}万）")
                    self.refresh_status()
                    return False
                # flash text
                lbl.text = f"Beat {state['i']+1}/{beats}"
                state["i"] += 1
                schedule_next()
            Clock.schedule_interval(beat, interval)
        def on_tap(_):
            now = __import__("time").time()
            if state["next"] is None: return
            if abs(now - state["next"]) <= window:
                state["good"] += 1
                lbl.text = "Good!"
            else:
                lbl.text = "Miss…"
        btn.bind(on_release=on_tap)
        dlg.open()
        Clock.schedule_once(start, 0.3)

    def ui_chef_memory(self, player):
        # 絵文字の手順記憶
        from kivymd.uix.dialog import MDDialog
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.clock import Clock
        steps = ["🥚","🥛","🍞","🔥","🍓","🧀"]
        import random
        seq = [random.choice(steps) for _ in range(4)]
        lay = BoxLayout(orientation="vertical", spacing=8, padding=10)
        lbl = Label(text="覚えてね: " + " ".join(seq))
        lay.add_widget(lbl)
        ans = []
        btns = BoxLayout(spacing=6, size_hint_y=None, height=48)
        for s in steps:
            b = Button(text=s)
            def mk(sx):
                def cb(_):
                    ans.append(sx)
                    lbl.text = "入力: " + " ".join(ans)
                    if len(ans)==len(seq):
                        ok = 1 if ans==seq else 0
                        if ok:
                            self.game.banker_adjust_money(player, 4)
                            self._toast("正解！+4万")
                        else:
                            self._toast("残念…")
                        dlg.dismiss()
                        self.refresh_status()
                return cb
            b.bind(on_release=mk(s))
            btns.add_widget(b)
        lay.add_widget(btns)
        dlg = MDDialog(title="料理人：手順記憶", type="custom", content_cls=lay, auto_dismiss=False)
        def hide(dt):
            lbl.text = "順番を再現してね！"
        Clock.schedule_once(hide, 2.5)
        dlg.open()

    market_text = StringProperty("")
    property_text = StringProperty("")

    def on_start(self):
        self.refresh_lists()

    def refresh_lists(self):
        st = self.game.ensure_initialized()
        self.game._ensure_catalog(st)
        # 市場
        lines = ["[市場]"]
        for it in st["market"]:
            lines.append(f"ID={it['id']} / {it['name']} {it['price']}万 / 出品:{it['seller']}")
        self.market_text = "\n".join(lines) if len(lines)>1 else "[市場] 出品なし"
        # 不動産
        lines = ["[不動産]"]
        for pr in st["property_catalog"][:80]:
            lines.append(f"ID={pr['id']} / {pr['name']} / 価格{pr['price']}万 / 家賃{pr['rent']}万")
        self.property_text = "\n".join(lines)

    def market_list(self, seller, name, price):
        try:
            p = int(price)
        except:
            return self._toast("価格は整数万円で")
        self.game.market_list(seller, name, p)
        self.refresh_lists()

    def market_buy(self, buyer, item_id):
        try:
            iid = int(item_id)
        except:
            return self._toast("IDは数値で")
        ok, msg = self.game.market_buy(buyer, iid)
        self._toast(msg)
        self.refresh_lists()

    def exchange_card(self, player, reward):
        msg = self.game.exchange_card(player, reward)
        self._toast(msg)
        self.refresh_status()

    def buy_property(self, player, pid):
        try:
            pid = int(pid)
        except:
            return self._toast("IDは数値で")
        msg = self.game.buy_property(player, pid)
        self._toast(msg)
        self.refresh_lists()
        self.refresh_status()

    def cook(self, player, recipe):
        self._toast(self.game.cook(player, recipe))
        self.refresh_status()

    def collect(self, player, cat):
        self._toast(self.game.collect_random(player, cat))
        self.refresh_status()

    def buy_pet(self, player, name):
        self._toast(self.game.buy_pet(player, name))
        self.refresh_status()

    def npc_talk(self, player, name):
        self._toast(self.game.npc_talk(player, name))
        self.refresh_status()

    def add_child(self, player, child_name, child_age):
        try:
            a = int(child_age)
        except:
            return self._toast("年齢は数値")
        self._toast(self.game.add_child(player, child_name, a) or "追加")
        self.refresh_status()

    def do_inherit(self, player, ratios_text):
        try:
            ratios = [int(x.strip()) for x in ratios_text.split(",") if x.strip()]
        except:
            return self._toast("配分は 50,50 のように入力")
        self._toast(self.game.do_generation_inherit(player, ratios))

    # ---- ミニゲーム ----
    def minigame_cake(self, player):
        # 簡易タイミング：ランプが光る（乱数1-100）、50±10で成功
        import random
        val = random.randint(1, 100)
        if 40 <= val <= 60:
            self.game.banker_adjust_money(player, 5)
            self._toast(f"大成功！（+5万） val={val}")
        else:
            self._toast(f"うーん… val={val}")

    def minigame_farmer(self, player):
        # 簡易：固定ボーナス
        self.game.banker_adjust_money(player, 3)
        self._toast("たくさん収穫！（+3万）")

    status_text = StringProperty("")
    admin_ok = BooleanProperty(False)

    def build(self):
        # lazy import KivyMD（requirementsで導入される想定）
        from kivymd.app import MDApp  # noqa: F401

        self.store = StateStore(self.user_data_dir)
        self.game = Game(self.store)
        self.state = self.game.ensure_initialized()
        self._load_sounds()
        root = Builder.load_string(KV)
        Clock.schedule_once(lambda *_: self.refresh_status())
        return root

    def _load_sounds(self):
        self.sounds = {
            "morning": self._load("assets/audio/ニワトリ.mp3"),
            "night": self._load("assets/audio/いびき.mp3"),
        }

    def _load(self, rel):
        p = resource_find(rel)
        return SoundLoader.load(p) if p else None

    # ---- UI actions ----
    def refresh_status(self):
        st = self.game.ensure_initialized()
        tod = st["time_of_day"]
        season = SEASONS[st["season_index"]]
        self.status_text = f"第{st['generation']}世代 / ターン{st['turn']}（{tod}）/ 季節: {season} / 国庫: {st['treasury']}万"
        # sound cue
        if tod == "昼" and self.sounds["morning"]:
            self.sounds["morning"].play()
        if tod == "夜" and self.sounds["night"]:
            self.sounds["night"].play()

    def next_turn(self):
        self.game.next_turn()
        self.refresh_status()

    def set_time(self, tod: str):
        if tod not in (DAY, NIGHT):
            return
        self.game.banker_set_time(tod)
        self.refresh_status()

    def commit_crime(self, player):
        res = self.game.commit_crime(player)
        self._toast(res)
        self.refresh_status()

    def confess(self, player):
        res = self.game.confess(player)
        self._toast(res)
        self.refresh_status()

    def trade(self, name, amount, forbidden):
        try:
            shares = int(amount)
        except Exception:
            self._toast("数値を入れてください")
            return
        ok, msg = self.game.trade_stock("たろう", name, shares, forbidden)
        self._toast(msg)
        self.refresh_status()

    def apply_code(self, code):
        if not code:
            return
        ok = self.game.input_secret_code(code.strip())
        self._toast("OK" if ok else "無効なコード")
        self.refresh_status()

    # ---- Admin (God) ----
    def admin_login(self, user, password):
        self.admin_ok = self.game.verify_banker(user, password)
        self._toast("ログイン成功" if self.admin_ok else "認証失敗")

    def _ensure_admin(self):
        if not self.admin_ok:
            self._toast("神モードは要ログイン")
            return False
        return True

    def god_money(self, player, delta):
        if not self._ensure_admin(): return
        try:
            d = int(delta)
        except Exception:
            return self._toast("数値を入れてください")
        self.game.banker_adjust_money(player, d)
        self.refresh_status()

    def god_popularity(self, player, delta):
        if not self._ensure_admin(): return
        try:
            d = int(delta)
        except Exception:
            return self._toast("数値を入れてください")
        self.game.banker_adjust_popularity(player, d)
        self.refresh_status()

    def god_title(self, player, title):
        if not self._ensure_admin(): return
        if not title: return
        self.game.banker_add_title(player, title)
        self.refresh_status()

    def god_jail(self, player, turns):
        if not self._ensure_admin(): return
        try:
            t = int(turns)
        except Exception:
            return self._toast("数値を入れてください")
        self.game.banker_imprison(player, t)
        self.refresh_status()

    def god_release(self, player):
        if not self._ensure_admin(): return
        self.game.banker_release(player)
        self.refresh_status()

    def god_set_season(self, season):
        if not self._ensure_admin(): return
        self.game.banker_set_season(season)
        self.refresh_status()

    def god_toggle_forbidden(self, enable):
        if not self._ensure_admin(): return
        self.game.banker_toggle_forbidden(bool(enable))
        self.refresh_status()

    def god_news(self, forbidden):
        if not self._ensure_admin(): return
        n = (FORBIDDEN_NEWS if forbidden else NEWS_EVENTS)[0]
        self.game.banker_force_news(n, forbidden=forbidden)
        self.refresh_status()

    def god_generation(self):
        if not self._ensure_admin(): return
        self.game.banker_generation()
        self.refresh_status()

    def god_treasury(self, amount):
        if not self._ensure_admin(): return
        try:
            v = int(amount)
        except Exception:
            return self._toast("数値を入れてください")
        self.game.banker_set_treasury(v)
        self.refresh_status()

    # ---- misc ----
    def _toast(self, msg):
        try:
            from kivymd.toast import toast
            toast(msg)
        except Exception:
            print(msg)

    def backup_export(self, *_):
        try:
            path = export_backup(self.store)
            self.toast(f"保存: {path}")
        except Exception as e:
            self.toast(f"保存失敗: {e}")

    def backup_import(self, *_):
        try:
            path = import_backup(self.store)
            if path:
                self.refresh_ui()
                self.toast(f"読み込み: {path}")
        except Exception as e:
            self.toast(f"読み込み失敗: {e}")

    # ===== 銀行員用：一括バックアップ／即時復元 =====
    def quick_backup(self, *_):
        try:
            path = quick_export_backup(self.store)
            self.toast(f"一括バックアップ完了: {path}")
        except Exception as e:
            self.toast(f"失敗: {e}")

    def restore_latest(self, *_):
        try:
            path = import_latest_backup(self.store)
            self.refresh_ui()
            self.toast(f"最新バックアップを復元: {path}")
        except Exception as e:
            self.toast(f"復元失敗: {e}")

    # ===== ルーレット（銀行員） =====
    def show_roulette_dialog(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.spinner import Spinner

        st = self.store.get_state()
        players = list(st.get("players", {}).keys()) or []

        box = BoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="8dp",
            size_hint_y=None,
            height="160dp",
        )
        sp_player = Spinner(
            text=players[0] if players else "プレイヤー未登録",
            values=players,
            size_hint_y=None,
            height="48dp",
        )
        sp_kind = Spinner(
            text="宝くじ",
            values=["宝くじ", "病気", "転職"],
            size_hint_y=None,
            height="48dp",
        )
        box.add_widget(sp_player)
        box.add_widget(sp_kind)

        def _run(*_a):
            if not players:
                self.toast("プレイヤーがいません")
                return
            kind_map = {"宝くじ": "lottery", "病気": "illness", "転職": "career"}
            label = spin_and_apply(self.game, kind_map[sp_kind.text], sp_player.text)
            self.show_receipt(
                [f"🎡 ルーレット({sp_kind.text})", f"{sp_player.text}: {label}"]
            )
            self.refresh_ui()
            dlg.dismiss()

        dlg = MDDialog(
            title="銀行員ルーレット",
            type="custom",
            content_cls=box,
            buttons=[
                MDFlatButton(text="回す", on_release=_run),
                MDFlatButton(text="閉じる", on_release=lambda *_: dlg.dismiss()),
            ],
        )
        dlg.open()

    # ===== レシート & スタンプ演出 =====
    def show_receipt(self, lines: list[str]):
        ReceiptOverlay(lines).open()

    def show_stampcard(self, stamps: int, total: int = 10):
        StampCardOverlay(stamps, total).open()

    # ===== 購入成功フック：購入フローから呼ぶだけで演出＋スタンプ加算 =====
    def on_purchase_succeeded(
        self,
        buyer: str,
        seller: str,
        item_name: str,
        price_man: int,
        stamp_inc: int = 1,
    ):
        """
        例）市場の購入処理が完了したら最後に呼び出す。
        - レシート紙アニメ
        - スタンプ加算 → 9/10, 10/10でポップ演出
        """
        # レシート
        self.show_receipt(
            [
                "🧾 レシート",
                f"買い手: {buyer}",
                f"売り手: {seller}",
                f"商品: {item_name}",
                f"支払い: {price_man} 万円",
            ]
        )
        # スタンプ
        result = self.game.add_stamp(buyer, count=stamp_inc, threshold=10)
        stamps, full_cards, total = result["stamps"], result["full_cards"], 10
        # 今回のスタンプ位置（9 or 10で輝く）
        self.show_stampcard(stamps if stamps != 0 else total, total)
        # 画面更新
        self.refresh_ui()
    
    def refresh_ui(self):
        st = self.store.get_state()
        turn = int(st.get('turn', 1))
        tod = st.get('time_of_day', '昼')
        season = st.get('season', '春')

        if self.root and 'turn_label' in self.root.ids:
            self.root.ids.turn_label.text = f"ターン: {turn}"
        if self.root and 'time_label' in self.root.ids:
            self.root.ids.time_label.text = f"時間帯: {tod} / 季節: {season}"

if __name__ == "__main__":
    ShopGameApp().run()
