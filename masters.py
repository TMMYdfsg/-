# -*- coding: utf-8 -*-
"""
Master data for the offline Android version of
「リアルお店屋さんごっこ」.
Amounts are in "万円" units.
"""

INITIAL_MONEY = 10  # 10万円

SEASONS = ["春", "夏", "秋", "冬"]
DAY = "昼"
NIGHT = "夜"

# 累進税率（万円ベース）
INCOME_TAX_RATES = {10: 0.05, 50: 0.10, 100: 0.20}
RESIDENCE_TAX = 1  # 万円
PROPERTY_TAX_RATE = 0.01
CONSUMPTION_TAX_RATE = 0.10  # 参考: 今回は消費時の外税計算に利用可能

# 納税周期（ターン）
TAX_PERIOD = 4

# ターン秒数(600秒)、昼夜切替（奇数=昼、偶数=夜）、季節3ターンで進む
TURN_SECONDS = 600
SEASON_ADVANCE_EVERY = 3

# 犯罪ランク閾値
CRIME_THRESHOLDS = [
    (100, "永久指名手配犯"),
    (70, "極悪犯罪者"),
    (50, "指名手配犯"),
    (20, "凶悪犯"),
    (10, "犯罪者"),
    (1, "軽犯罪者"),
]

# 職業
JOBS = {
    # 通常の職業
    "無職": {
        "description": "アルバイトや宝探しなど、自由な生き方ができる。",
        "requires_qualification": None,
        "type": "通常",
    },
    "ケーキ屋": {
        "description": "タイミングゲームで美味しいケーキを作る。",
        "requires_qualification": None,
        "type": "通常",
    },
    "警察官": {
        "description": "探し物ミニゲームで町の人々の困りごとを解決する。夜にパトロールができる。",
        "requires_qualification": None,
        "type": "通常",
    },
    "Youtuber": {
        "description": "記憶力ゲームで面白い動画を撮影する。",
        "requires_qualification": None,
        "type": "通常",
    },
    "農家": {
        "description": "毎ターン1万円の安定収入がある。",
        "requires_qualification": None,
        "type": "通常",
    },
    "投資家": {
        "description": "株の売買手数料が無料になる。(通常5%)",
        "requires_qualification": None,
        "type": "通常",
    },
    "アイドル": {
        "description": "『応援を求める』コマンドで臨時収入を得られることがある。",
        "requires_qualification": None,
        "type": "通常",
    },
    "公務員": {
        "description": "毎ターン3万円の安定収入があり、住民税が免除される。",
        "requires_qualification": None,
        "type": "通常",
    },
    "アニメーター": {
        "description": "パラパラ漫画を作るミニゲームで作品を制作する。",
        "requires_qualification": None,
        "type": "通常",
    },
    "小説家": {
        "description": "物語のアイデアを考えて、ベストセラーを目指す。",
        "requires_qualification": None,
        "type": "通常",
    },
    "ミュージシャン": {
        "description": "リズムゲームで作曲し、ファンを増やす。",
        "requires_qualification": None,
        "type": "通常",
    },
    "探偵": {
        "description": "証拠を集めて、簡単な事件を解決する。",
        "requires_qualification": None,
        "type": "通常",
    },
    "プログラマー": {
        "description": "コードの間違い探しゲームでアプリを開発する。",
        "requires_qualification": None,
        "type": "通常",
    },
    "花屋": {
        "description": "注文通りに花束を作るミニゲーム。",
        "requires_qualification": None,
        "type": "通常",
    },
    "タクシー運転手": {
        "description": "お客さんを目的地まで最短ルートで送り届ける。",
        "requires_qualification": None,
        "type": "通常",
    },
    "パン屋": {
        "description": "美味しいパンを焼いてお店に並べる。",
        "requires_qualification": None,
        "type": "通常",
    },
    "漫画家": {
        "description": "面白いオチを考えて4コマ漫画を完成させる。",
        "requires_qualification": None,
        "type": "通常",
    },
    "科学者": {
        "description": "フラスコを混ぜて新発見を目指す実験ゲーム。",
        "requires_qualification": None,
        "type": "通常",
    },
    "郵便配達員": {
        "description": "指定されたルートを覚えて正確に配達するミニゲーム。",
        "requires_qualification": None,
        "type": "通常",
    },
    "美容師": {
        "description": "髪型の注文に合わせてカットするスピード＆記憶ゲーム。",
        "requires_qualification": None,
        "type": "通常",
    },
    "ペットショップ店員": {
        "description": "動物たちの世話をしながら来客に対応する。",
        "requires_qualification": None,
        "type": "通常",
    },
    "カフェ店員": {
        "description": "ドリンクやスイーツを正確に提供する。接客力が問われる。",
        "requires_qualification": None,
        "type": "通常",
    },
    "家具職人": {
        "description": "部品を組み立てて家具を完成させるパズルゲーム。",
        "requires_qualification": None,
        "type": "通常",
    },
    "ガイド": {
        "description": "観光客に観光地を案内し、知識と対応力が求められる。",
        "requires_qualification": None,
        "type": "通常",
    },
    "引越し業者": {
        "description": "荷物を効率よく詰めるテトリス風ミニゲーム。",
        "requires_qualification": None,
        "type": "通常",
    },
    "レジ打ち": {
        "description": "スキャン速度＆金額の正確さが求められる。",
        "requires_qualification": None,
        "type": "通常",
    },
    "書店員": {
        "description": "客の要望に合わせた本を素早く探し出す。",
        "requires_qualification": None,
        "type": "通常",
    },
    "郵便局員": {
        "description": "書類の分類と処理をこなす地味だが重要な仕事。",
        "requires_qualification": None,
        "type": "通常",
    },
    "雑貨屋": {
        "description": "小物を売って利益を上げる。仕入れ選定のセンスが必要。",
        "requires_qualification": None,
        "type": "通常",
    },
    "水族館スタッフ": {
        "description": "魚たちの世話や水槽のメンテナンスを行う。",
        "requires_qualification": None,
        "type": "通常",
    },
    "バーテンダー": {
        "description": "注文通りのカクテルを作成。センスと記憶力勝負。",
        "requires_qualification": None,
        "type": "通常",
    },
    "DJ": {
        "description": "リズムに合わせて盛り上げる音楽系職。夜イベントにも強い。",
        "requires_qualification": None,
        "type": "通常",
    },
    "大道芸人": {
        "description": "技を決めて観客の注目を集める。失敗するとブーイング。",
        "requires_qualification": None,
        "type": "通常",
    },
    # 特殊職業
    "医者": {
        "description": "診断ミニゲームで人々を助ける。",
        "requires_qualification": "medical_license",
        "type": "特殊",
    },
    "エンジニア": {
        "description": "土地の購入費用が20%割引になる。夜に残業ができる。",
        "requires_qualification": "engineer_cert",
        "type": "特殊",
    },
    "料理人": {
        "description": "商品の売上が10%上乗せされ、新しいレシピをひらめきやすい。",
        "requires_qualification": "chef_license",
        "type": "特殊",
    },
    "検事": {
        "description": "プレイヤーを起訴する権限を持つ。",
        "requires_qualification": "law_license",
        "type": "特殊",
    },
    "弁護士": {
        "description": "被告人を弁護する。",
        "requires_qualification": "law_license",
        "type": "特殊",
    },
    "看守": {
        "description": "刑務所の受刑者を管理する。",
        "requires_qualification": None,
        "type": "特殊",
    },
    "建築家": {
        "description": "新しい物件を設計・建設できる。",
        "requires_qualification": "architect_cert",
        "type": "特殊",
    },
    "パイロット": {
        "description": "長距離移動ができる。飛行中に特殊イベントが起きることも。",
        "requires_qualification": "pilot_license",
        "type": "特殊",
    },
    "薬剤師": {
        "description": "処方された薬を正しく調合・提供する。",
        "requires_qualification": "pharmacist_cert",
        "type": "特殊",
    },
    "救急救命士": {
        "description": "一刻を争う対応を迫られる。緊急イベントで活躍。",
        "requires_qualification": "emergency_cert",
        "type": "特殊",
    },
    "プロゲーマー": {
        "description": "eスポーツ大会に参加でき、ランキング報酬がある。",
        "requires_qualification": "pro_license",
        "type": "特殊",
    },
    "ロボット技術者": {
        "description": "AIロボの開発ができる。新技術の研究が可能。",
        "requires_qualification": "engineer_cert",
        "type": "特殊",
    },
    "占い師": {
        "description": "他プレイヤーの運勢を操作できるミステリアス職。",
        "requires_qualification": None,
        "type": "特殊",
    },
    "宇宙飛行士": {
        "description": "宇宙ミッションイベントに参加できるレア職。",
        "requires_qualification": "astronaut_cert",
        "type": "特殊",
    },
    "記者": {
        "description": "社会の出来事を取材し、記事として発信。真実を暴ける。",
        "requires_qualification": None,
        "type": "特殊",
    },
    "通訳者": {
        "description": "外国イベントで活躍。多言語に対応可能。",
        "requires_qualification": "language_cert",
        "type": "特殊",
    },
    "考古学者": {
        "description": "遺跡を発掘してレアアイテムを見つけることがある。",
        "requires_qualification": None,
        "type": "特殊",
    },
    "ゲーム開発者": {
        "description": "他プレイヤーがプレイするミニゲームを設計可能。",
        "requires_qualification": "engineer_cert",
        "type": "特殊",
    },
    # 犯罪系の職業
    "クラッカー": {
        "description": "ハッキングや窃盗などの犯罪活動に特化している。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "軽犯罪者": {
        "description": "法を一度だけ破った者。まだ引き返せるかもしれない。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "犯罪者": {
        "description": "犯罪に手を染め、裏社会に足を踏み入れた者。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "凶悪犯": {
        "description": "もはやカタギの世界には戻れない重罪人。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "指名手配犯": {
        "description": "警察に追われる身となった危険人物。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "極悪犯罪者": {
        "description": "その名を聞けば誰もが震え上がる大悪党。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "永久指名手配犯": {
        "description": "国家を敵に回した、伝説の犯罪者。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "詐欺師": {
        "description": "他プレイヤーを騙して金品を得る。バレるとリスク大。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "密輸業者": {
        "description": "違法アイテムの流通に関与。成功すれば高報酬。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "裏社会の仲介人": {
        "description": "犯罪系プレイヤー間の交渉や取引を取り持つ。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "情報屋": {
        "description": "あらゆる情報を売買し、他人の秘密を握る。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "殺し屋": {
        "description": "任意のプレイヤーを一時的にゲームから排除できる。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "スパイ": {
        "description": "他プレイヤーの行動ログを覗き見できる能力を持つ。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "ダークウェブ管理者": {
        "description": "犯罪取引の仲介や拡散を行う謎多き存在。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "爆弾魔": {
        "description": "施設やイベントに干渉できるが、リスクも高い。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "黒幕": {
        "description": "犯罪者たちのボス。一度だけ巨大な計画を実行可能。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "裏切り者": {
        "description": "他プレイヤーの信頼を裏切り、資源を奪うことができる。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "密猟者": {
        "description": "動物を違法に捕獲し、希少アイテムを得る。",
        "requires_qualification": None,
        "type": "犯罪",
    },
    "麻薬製造者": {
        "description": "違法薬物を製造・販売し、高額な利益を得る。",
        "requires_qualification": None,
        "type": "犯罪",
    },
}

# 資格
QUALIFICATIONS = {
    "medical_license": {
        "name": "医師免許",
        "cost": 50,
        "maintenance": 2,
        "unlocks": ["医者"],
    },
    "law_license": {
        "name": "司法資格",
        "cost": 70,
        "maintenance": 3,
        "unlocks": ["検事", "弁護士"],
    },
    "accounting_cert": {
        "name": "会計士資格",
        "cost": 60,
        "maintenance": 2,
        "unlocks": ["会計士"],
    },
    "teaching_license": {
        "name": "教員免許",
        "cost": 45,
        "maintenance": 1,
        "unlocks": ["教師"],
    },
    "engineer_cert": {
        "name": "技術士資格",
        "cost": 65,
        "maintenance": 3,
        "unlocks": ["エンジニア"],
    },
    "chef_license": {
        "name": "料理師免許",
        "cost": 40,
        "maintenance": 1,
        "unlocks": ["シェフ"],
    },
    "driver_license": {
        "name": "運転免許",
        "cost": 10,
        "maintenance": 0,
        "unlocks": ["配達員"],
    },
    "pharmacist_cert": {
        "name": "薬剤師資格",
        "cost": 55,
        "maintenance": 2,
        "unlocks": ["薬剤師"],
    },
    "firefighter_cert": {
        "name": "消防士免許",
        "cost": 30,
        "maintenance": 1,
        "unlocks": ["消防士"],
    },
    "pilot_license": {
        "name": "パイロットライセンス",
        "cost": 100,
        "maintenance": 5,
        "unlocks": ["パイロット"],
    },
    "vet_license": {
        "name": "獣医師免許",
        "cost": 60,
        "maintenance": 3,
        "unlocks": ["獣医"],
    },
    "dentist_cert": {
        "name": "歯科医師資格",
        "cost": 65,
        "maintenance": 3,
        "unlocks": ["歯科医"],
    },
    "journalist_pass": {
        "name": "報道記者証",
        "cost": 25,
        "maintenance": 1,
        "unlocks": ["ジャーナリスト"],
    },
    "research_cert": {
        "name": "研究員資格",
        "cost": 55,
        "maintenance": 2,
        "unlocks": ["研究者"],
    },
    "architect_cert": {
        "name": "建築士資格",
        "cost": 70,
        "maintenance": 3,
        "unlocks": ["建築家"],
    },
    "artist_license": {
        "name": "アーティスト認定",
        "cost": 40,
        "maintenance": 1,
        "unlocks": ["アーティスト"],
    },
    "music_cert": {
        "name": "音楽講師免許",
        "cost": 35,
        "maintenance": 1,
        "unlocks": ["音楽家"],
    },
    "therapist_cert": {
        "name": "心理士資格",
        "cost": 50,
        "maintenance": 2,
        "unlocks": ["カウンセラー"],
    },
    "athletic_cert": {
        "name": "運動トレーナー資格",
        "cost": 45,
        "maintenance": 2,
        "unlocks": ["トレーナー"],
    },
    "security_cert": {
        "name": "警備員資格",
        "cost": 30,
        "maintenance": 1,
        "unlocks": ["警備員"],
    },
}

# 特性（例）
TRAITS = {
    "アクティブ": {
        "description": "よく働く → 収入が多くなる。運動系の店（スポーツジム店など）に向く。"
    },
    "ロマンチック": {
        "description": "おしゃれ屋・アクセサリー屋などで「魅力度」や人気度が上がる。恋愛系イベント追加可。"
    },
    "天才": {
        "description": "株や戦略要素に強くなる。株価を読む力があり、株式でボーナス。"
    },
    "完璧主義者": {
        "description": "商品品質が高くなり、売値が上がる。クラフト系職人向け。"
    },
    "芸術愛好家": {
        "description": "美術館、絵屋、手作り系店に有利。ひらめきボーナス付き。"
    },
    "きれい好き": {
        "description": "店が汚れていると売上が下がる or クレームになる。掃除イベント追加。"
    },
    "物質主義": {
        "description": "ブランド品や高額商品にこだわる。お金が貯まってもすぐ買ってしまう。"
    },
    "盗み癖": {
        "description": "ランダムイベントで他のプレイヤーの売上から盗む（要管理者承認）。"
    },
    "善人": {
        "description": "イベントで寄付・詐欺などに巻き込まれやすい性格設定。人気度に影響。"
    },
    "悪人": {
        "description": "イベントで寄付・詐欺などに巻き込まれやすい性格設定。人気度に影響。"
    },
    "嫉妬深い": {
        "description": "他人の売上に嫉妬 → ランダムでムードダウン or チャレンジモード。"
    },
    "外交的": {
        "description": "会話や売り込みが得意で、商品がよく売れる。交渉が上手くなる。"
    },
    "怠け者": {
        "description": "行動量が少ない → 昼の行動ターンが制限される。売上が出にくい。"
    },
    "野心家": {"description": "目標（売上額）達成に強い。昇格・褒賞に有利。"},
    "猫好き": {
        "description": "ペットショップが経営できる or 特定イベント（動物イベント）に好影響。"
    },
    "犬好き": {
        "description": "ペットショップが経営できる or 特定イベント（動物イベント）に好影響。"
    },
    "ベジタリアン": {"description": "飲食系の店での料理判定やクレーム要素に影響する。"},
    "美食家": {"description": "飲食系の店での料理判定やクレーム要素に影響する。"},
}
# スキル（レベル/XP制）
SKILLS = [
    "商才",
    "投資センス",
    "交渉術",
    "ハッキング",
    "ピッキング",
    "絵画",
    "ガーデニング",
    "プログラミング",
    "魅力",
    "いたずら",
    "探偵",
    "執筆",
    "ギター",
    "論理学",
    "器用さ",
    "コメディ",
    "医療知識",
    "料理",
    "音楽",
    "科学",
    "運転技術",
    "料理技術",
    "写真術",
    "演技力",
    "スポーツ",
    "デザイン",
    "マネジメント",
    "マーケティング",
    "分析力",
    "語学力",
    "耐久力",
    "集中力",
    "創造性",
    "リーダーシップ",
    "教育力",
    "忍耐力",
    "機械修理",
    "調査力",
    "交渉力",
    "釣り",
]

# 通常株（抜粋）
STOCKS = [
    {
        "name": "フルーツ会社(安定)",
        "price": 10,
        "volatility": 0.05,
        "category": "食品",
        "market_cap": 1000,
        "owner": None,
    },
    {
        "name": "おもちゃ産業(普通)",
        "price": 30,
        "volatility": 0.15,
        "category": "エンタメ",
        "market_cap": 3000,
        "owner": None,
    },
    {
        "name": "ITキングダム(成長)",
        "price": 80,
        "volatility": 0.3,
        "category": "テクノロジー",
        "market_cap": 8000,
        "owner": None,
    },
    {
        "name": "ドラゴンフーズ",
        "price": 45,
        "volatility": 0.5,
        "category": "食品",
        "market_cap": 4500,
        "owner": None,
    },
    {
        "name": "ほのお銀行",
        "price": 100,
        "volatility": 0.2,
        "category": "金融",
        "market_cap": 10000,
        "owner": None,
    },
    {
        "name": "ウィザード証券",
        "price": 65,
        "volatility": 0.4,
        "category": "金融",
        "market_cap": 6500,
        "owner": None,
    },
    {
        "name": "ねこのしっぽ製菓",
        "price": 50,
        "volatility": 0.6,
        "category": "食品",
        "market_cap": 5000,
        "owner": None,
    },
    {
        "name": "ホーリースター電気",
        "price": 70,
        "volatility": 0.3,
        "category": "エネルギー",
        "market_cap": 7000,
        "owner": None,
    },
    {
        "name": "スターライト製作所",
        "price": 90,
        "volatility": 0.35,
        "category": "工業",
        "market_cap": 9000,
        "owner": None,
    },
    {
        "name": "カゲネコ雑貨店",
        "price": 40,
        "volatility": 0.45,
        "category": "小売",
        "market_cap": 4000,
        "owner": None,
    },
    {
        "name": "フローズンミルク社",
        "price": 35,
        "volatility": 0.55,
        "category": "食品",
        "market_cap": 3500,
        "owner": None,
    },
    {
        "name": "たんぽぽ建設",
        "price": 95,
        "volatility": 0.25,
        "category": "建設",
        "market_cap": 9500,
        "owner": None,
    },
    {
        "name": "ソラニワ不動産",
        "price": 110,
        "volatility": 0.2,
        "category": "不動産",
        "market_cap": 11000,
        "owner": None,
    },
    {
        "name": "まじょまじょ医薬",
        "price": 88,
        "volatility": 0.4,
        "category": "医薬",
        "market_cap": 8800,
        "owner": None,
    },
    {
        "name": "シマエナガ出版",
        "price": 55,
        "volatility": 0.5,
        "category": "メディア",
        "market_cap": 5500,
        "owner": None,
    },
    {
        "name": "フクロウ放送",
        "price": 60,
        "volatility": 0.45,
        "category": "メディア",
        "market_cap": 6000,
        "owner": None,
    },
    {
        "name": "プラネットおもちゃ",
        "price": 30,
        "volatility": 0.6,
        "category": "玩具",
        "market_cap": 3000,
        "owner": None,
    },
    {
        "name": "ハピネス農園",
        "price": 42,
        "volatility": 0.35,
        "category": "農業",
        "market_cap": 4200,
        "owner": None,
    },
    {
        "name": "ギャラクシー家具",
        "price": 78,
        "volatility": 0.3,
        "category": "小売",
        "market_cap": 7800,
        "owner": None,
    },
    {
        "name": "雷鳴重工",
        "price": 125,
        "volatility": 0.15,
        "category": "工業",
        "market_cap": 12500,
        "owner": None,
    },
    {
        "name": "キャンディミント製薬",
        "price": 95,
        "volatility": 0.4,
        "category": "医薬",
        "market_cap": 9500,
        "owner": None,
    },
    {
        "name": "スマイル物流",
        "price": 62,
        "volatility": 0.5,
        "category": "運輸",
        "market_cap": 6200,
        "owner": None,
    },
    {
        "name": "夜空通信",
        "price": 100,
        "volatility": 0.3,
        "category": "テクノロジー",
        "market_cap": 10000,
        "owner": None,
    },
    {
        "name": "サクラコスメ",
        "price": 58,
        "volatility": 0.4,
        "category": "化粧品",
        "market_cap": 5800,
        "owner": None,
    },
    {
        "name": "オーロラ水産",
        "price": 47,
        "volatility": 0.5,
        "category": "水産",
        "market_cap": 4700,
        "owner": None,
    },
    {
        "name": "おはなITソリューション",
        "price": 83,
        "volatility": 0.35,
        "category": "テクノロジー",
        "market_cap": 8300,
        "owner": None,
    },
    {
        "name": "みどり製茶",
        "price": 38,
        "volatility": 0.45,
        "category": "食品",
        "market_cap": 3800,
        "owner": None,
    },
    {
        "name": "ワンダートラベル",
        "price": 73,
        "volatility": 0.4,
        "category": "旅行",
        "market_cap": 7300,
        "owner": None,
    },
    {
        "name": "にじいろ園芸",
        "price": 33,
        "volatility": 0.6,
        "category": "農業",
        "market_cap": 3300,
        "owner": None,
    },
    {
        "name": "おどろき証券",
        "price": 85,
        "volatility": 0.3,
        "category": "金融",
        "market_cap": 8500,
        "owner": None,
    },
    {
        "name": "もちもち不動産",
        "price": 92,
        "volatility": 0.35,
        "category": "不動産",
        "market_cap": 9200,
        "owner": None,
    },
    {
        "name": "未来都市電機",
        "price": 115,
        "volatility": 0.25,
        "category": "エネルギー",
        "market_cap": 11500,
        "owner": None,
    },
    {
        "name": "まほうITラボ",
        "price": 88,
        "volatility": 0.4,
        "category": "テクノロジー",
        "market_cap": 8800,
        "owner": None,
    },
    {
        "name": "わらい茸エンタメ",
        "price": 66,
        "volatility": 0.45,
        "category": "エンタメ",
        "market_cap": 6600,
        "owner": None,
    },
    {
        "name": "クマのパン屋",
        "price": 39,
        "volatility": 0.55,
        "category": "食品",
        "market_cap": 3900,
        "owner": None,
    },
    {
        "name": "まぼろし証券",
        "price": 103,
        "volatility": 0.3,
        "category": "金融",
        "market_cap": 10300,
        "owner": None,
    },
    {
        "name": "ルーン鉱業",
        "price": 120,
        "volatility": 0.25,
        "category": "素材",
        "market_cap": 12000,
        "owner": None,
    },
    {
        "name": "しあわせ製薬",
        "price": 99,
        "volatility": 0.35,
        "category": "医薬",
        "market_cap": 9900,
        "owner": None,
    },
    {
        "name": "エコヒカリ電力",
        "price": 84,
        "volatility": 0.4,
        "category": "エネルギー",
        "market_cap": 8400,
        "owner": None,
    },
    {
        "name": "ツバメ交通",
        "price": 71,
        "volatility": 0.5,
        "category": "運輸",
        "market_cap": 7100,
        "owner": None,
    },
    {
        "name": "ブルームホテルズ",
        "price": 60,
        "volatility": 0.45,
        "category": "宿泊",
        "market_cap": 6000,
        "owner": None,
    },
    {
        "name": "かがやき宇宙開発",
        "price": 140,
        "volatility": 0.2,
        "category": "テクノロジー",
        "market_cap": 14000,
        "owner": None,
    },
    {
        "name": "ミラクル農機",
        "price": 89,
        "volatility": 0.35,
        "category": "農業",
        "market_cap": 8900,
        "owner": None,
    },
    {
        "name": "こもれび森林開発",
        "price": 93,
        "volatility": 0.4,
        "category": "素材",
        "market_cap": 9300,
        "owner": None,
    },
    {
        "name": "チョコバナナ社",
        "price": 41,
        "volatility": 0.55,
        "category": "食品",
        "market_cap": 4100,
        "owner": None,
    },
    {
        "name": "まるっと警備保障",
        "price": 78,
        "volatility": 0.3,
        "category": "サービス",
        "market_cap": 7800,
        "owner": None,
    },
    {
        "name": "あさひカメラ",
        "price": 67,
        "volatility": 0.4,
        "category": "テクノロジー",
        "market_cap": 6700,
        "owner": None,
    },
    {
        "name": "やまね製鉄所",
        "price": 108,
        "volatility": 0.3,
        "category": "工業",
        "market_cap": 10800,
        "owner": None,
    },
    {
        "name": "はなまる保険",
        "price": 99,
        "volatility": 0.35,
        "category": "金融",
        "market_cap": 9900,
        "owner": None,
    },
    {
        "name": "デジタルねこ開発",
        "price": 105,
        "volatility": 0.25,
        "category": "テクノロジー",
        "market_cap": 10500,
        "owner": None,
    },
    {
        "name": "ホタルファーム",
        "price": 52,
        "volatility": 0.45,
        "category": "農業",
        "market_cap": 5200,
        "owner": None,
    },
    {
        "name": "つばさ航空",
        "price": 115,
        "volatility": 0.3,
        "category": "運輸",
        "market_cap": 11500,
        "owner": None,
    },
    {
        "name": "ふしぎなおもちゃ堂",
        "price": 44,
        "volatility": 0.5,
        "category": "玩具",
        "market_cap": 4400,
        "owner": None,
    },
    {
        "name": "トパーズ出版",
        "price": 68,
        "volatility": 0.4,
        "category": "メディア",
        "market_cap": 6800,
        "owner": None,
    },
    {
        "name": "スマート灯油",
        "price": 87,
        "volatility": 0.35,
        "category": "エネルギー",
        "market_cap": 8700,
        "owner": None,
    },
    {
        "name": "ラビットエンタープライズ",
        "price": 72,
        "volatility": 0.45,
        "category": "サービス",
        "market_cap": 7200,
        "owner": None,
    },
    {
        "name": "レモン交通",
        "price": 90,
        "volatility": 0.3,
        "category": "運輸",
        "market_cap": 9000,
        "owner": None,
    },
    {
        "name": "マジカル鉄道",
        "price": 110,
        "volatility": 0.25,
        "category": "運輸",
        "market_cap": 11000,
        "owner": None,
    },
    {
        "name": "もぐもぐ食堂",
        "price": 49,
        "volatility": 0.5,
        "category": "食品",
        "market_cap": 4900,
        "owner": None,
    },
    {
        "name": "ネコポスト",
        "price": 75,
        "volatility": 0.4,
        "category": "運輸",
        "market_cap": 7500,
        "owner": None,
    },
    {
        "name": "サイバーストリート",
        "price": 130,
        "volatility": 0.3,
        "category": "テクノロジー",
        "market_cap": 13000,
        "owner": None,
    },
    {
        "name": "まんてんソーラー",
        "price": 98,
        "volatility": 0.35,
        "category": "エネルギー",
        "market_cap": 9800,
        "owner": None,
    },
    {
        "name": "ゆめいろ温泉開発",
        "price": 83,
        "volatility": 0.4,
        "category": "宿泊",
        "market_cap": 8300,
        "owner": None,
    },
    {
        "name": "たぬきタクシー",
        "price": 58,
        "volatility": 0.45,
        "category": "運輸",
        "market_cap": 5800,
        "owner": None,
    },
    {
        "name": "しずく化粧品",
        "price": 77,
        "volatility": 0.35,
        "category": "化粧品",
        "market_cap": 7700,
        "owner": None,
    },
    {
        "name": "ドリームマート",
        "price": 70,
        "volatility": 0.5,
        "category": "小売",
        "market_cap": 7000,
        "owner": None,
    },
    {
        "name": "キラリ鉄道開発",
        "price": 102,
        "volatility": 0.3,
        "category": "工業",
        "market_cap": 10200,
        "owner": None,
    },
    {
        "name": "アイスピア社",
        "price": 39,
        "volatility": 0.6,
        "category": "食品",
        "market_cap": 3900,
        "owner": None,
    },
    {
        "name": "フラワー薬局",
        "price": 88,
        "volatility": 0.35,
        "category": "医薬",
        "market_cap": 8800,
        "owner": None,
    },
    {
        "name": "ミドリ物流",
        "price": 64,
        "volatility": 0.45,
        "category": "運輸",
        "market_cap": 6400,
        "owner": None,
    },
    {
        "name": "ムーンテック",
        "price": 121,
        "volatility": 0.2,
        "category": "テクノロジー",
        "market_cap": 12100,
        "owner": None,
    },
    {
        "name": "ブーケ不動産",
        "price": 96,
        "volatility": 0.35,
        "category": "不動産",
        "market_cap": 9600,
        "owner": None,
    },
]

# 禁断市場
FORBIDDEN_STOCKS = [
    {
        "name": "シャドウ・コーポレーション",
        "price": 666,
        "volatility": 0.8,
        "category": "禁断",
        "market_cap": 66600,
        "owner": None,
    },
    {
        "name": "古代文明の遺産ファンド",
        "price": 123,
        "volatility": 0.6,
        "category": "禁断",
        "market_cap": 12300,
        "owner": None,
    },
]

FORBIDDEN_NEWS = [
    {
        "headline": "宇宙からの謎の信号を受信！",
        "effect": "stock_up",
        "target": "シャドウ・コーポレーション",
        "bonus": 5.0,
        "description": "シャドウ・コーポレーションの株価が5倍に！",
    },
    {
        "headline": "古代遺跡で大発見！",
        "effect": "stock_up",
        "target": "古代文明の遺産ファンド",
        "bonus": 10.0,
        "description": "古代文明の遺産ファンドの価値が10倍に！",
    },
    {
        "headline": "次元の歪みが発生...",
        "effect": "stock_crash",
        "target": "all",
        "bonus": 0.1,
        "description": "禁断の市場の全銘柄が暴落！",
    },
]

# 通常ニュース（抜粋）
NEWS_EVENTS = [
    {
        "id": "NE001",
        "headline": "インフルエンザ大流行の兆し",
        "category": "社会",
        "effect": "job_bonus",
        "target": "医者",
        "bonus": 1.5,
        "duration": 3,
        "description": "医者の仕事の報酬が1.5倍になります！",
    },
    {
        "id": "NE002",
        "headline": "記録的な猛暑！",
        "category": "天気",
        "effect": "product_price",
        "target": "アイス",
        "bonus": 2.0,
        "duration": 2,
        "description": "「アイス」の価格が2倍に高騰！",
    },
    {
        "id": "NE003",
        "headline": "レトロゲームが大ブーム！",
        "category": "流行",
        "effect": "skill_bonus",
        "target": "プログラミング",
        "bonus": 1.5,
        "duration": 4,
        "description": "「プログラミング」スキルの経験値獲得量が1.5倍に！",
    },
    {
        "id": "NE004",
        "headline": "町の宝探し大会開催！",
        "category": "イベント",
        "effect": "special_quest",
        "target": "all",
        "bonus": 0,
        "duration": 5,
        "description": "町のどこかに隠された宝箱を探し出そう！",
    },
    {
        "id": "NE005",
        "headline": "株式市場が好調！",
        "category": "経済",
        "effect": "stock_up",
        "target": "all",
        "bonus": 1.2,
        "duration": 1,
        "description": "全ての株価が1.2倍に上昇！",
    },
    {
        "id": "NE006",
        "headline": "大地震発生！",
        "category": "災害",
        "effect": "property_damage",
        "target": "all",
        "bonus": -0.3,
        "duration": 2,
        "description": "地震により土地の価値が下落しています。",
    },
    {
        "id": "NE007",
        "headline": "新技術発表！",
        "category": "技術",
        "effect": "skill_bonus",
        "target": "技術者",
        "bonus": 1.4,
        "duration": 3,
        "description": "技術者のスキル獲得が1.4倍に！",
    },
    {
        "id": "NE008",
        "headline": "食品偽装問題発覚",
        "category": "社会",
        "effect": "popularity_down",
        "target": "飲食店",
        "bonus": -0.5,
        "duration": 4,
        "description": "飲食店の人気が大きく下落しました。",
    },
    {
        "id": "NE009",
        "headline": "観光シーズン到来",
        "category": "観光",
        "effect": "popularity_up",
        "target": "観光地",
        "bonus": 1.3,
        "duration": 5,
        "description": "観光地の人気が上昇しています。",
    },
    {
        "id": "NE010",
        "headline": "選挙結果発表",
        "category": "政治",
        "effect": "policy_change",
        "target": "all",
        "bonus": 0,
        "duration": 0,
        "description": "新しい政策が実施されます。",
    },
    {
        "id": "NE011",
        "headline": "新型ウイルス発生",
        "category": "社会",
        "effect": "job_penalty",
        "target": "医者",
        "bonus": 0.7,
        "duration": 4,
        "description": "医者の仕事効率が70%に低下。",
    },
    {
        "id": "NE012",
        "headline": "交通網の整備",
        "category": "都市開発",
        "effect": "popularity_up",
        "target": "都市",
        "bonus": 1.2,
        "duration": 3,
        "description": "都市の人気が上昇。",
    },
    {
        "id": "NE013",
        "headline": "新規商店街開業",
        "category": "経済",
        "effect": "job_bonus",
        "target": "商人",
        "bonus": 1.3,
        "duration": 3,
        "description": "商人の収入が増加！",
    },
    {
        "id": "NE014",
        "headline": "映画祭開催",
        "category": "文化",
        "effect": "popularity_up",
        "target": "映画館",
        "bonus": 1.5,
        "duration": 4,
        "description": "映画館の人気が急上昇！",
    },
    {
        "id": "NE015",
        "headline": "工場火災発生",
        "category": "災害",
        "effect": "job_penalty",
        "target": "工場労働者",
        "bonus": 0.5,
        "duration": 3,
        "description": "工場労働者の効率が低下。",
    },
    {
        "id": "NE016",
        "headline": "新しい教育方針導入",
        "category": "教育",
        "effect": "skill_bonus",
        "target": "教師",
        "bonus": 1.3,
        "duration": 5,
        "description": "教師のスキル成長率アップ。",
    },
    {
        "id": "NE017",
        "headline": "大規模セール開催",
        "category": "経済",
        "effect": "product_price_down",
        "target": "小売店",
        "bonus": 0.8,
        "duration": 2,
        "description": "小売店の商品の価格が下落。",
    },
    {
        "id": "NE018",
        "headline": "国際交流イベント",
        "category": "文化",
        "effect": "popularity_up",
        "target": "都市",
        "bonus": 1.4,
        "duration": 3,
        "description": "都市の文化的な人気が上昇しています。",
    },
]
# 家具/ペット/レシピ（抜粋）
FURNITURE = {
    "シンプルなベッド": {"price": 5, "happiness_boost": 1},
    "大きな本棚": {"price": 10, "happiness_boost": 2},
    "最新ゲーム機": {"price": 20, "happiness_boost": 5},
    "ふかふかのソファ": {"price": 15, "happiness_boost": 3},
    "おしゃれなランプ": {"price": 8, "happiness_boost": 2},
    "木製ダイニングテーブル": {"price": 25, "happiness_boost": 4},
    "クラシックチェア": {"price": 12, "happiness_boost": 2},
    "デジタルピアノ": {"price": 30, "happiness_boost": 6},
    "アートパネル": {"price": 18, "happiness_boost": 3},
    "モダンカーテン": {"price": 14, "happiness_boost": 2},
    "スマートテレビ": {"price": 28, "happiness_boost": 5},
    "コーヒーテーブル": {"price": 10, "happiness_boost": 2},
    "屋内プラント": {"price": 7, "happiness_boost": 1},
    "書斎用デスク": {"price": 22, "happiness_boost": 3},
    "マッサージチェア": {"price": 40, "happiness_boost": 7},
    "レトロラジオ": {"price": 15, "happiness_boost": 3},
    "大型ミラー": {"price": 12, "happiness_boost": 2},
    "収納キャビネット": {"price": 20, "happiness_boost": 3},
    "ウッドフロアマット": {"price": 8, "happiness_boost": 1},
    "ペット用ベッド": {"price": 9, "happiness_boost": 2},
    "電気暖炉": {"price": 25, "happiness_boost": 4},
}
PETS = {
    "いぬ": {"price": 10, "happiness_boost": 5},
    "ねこ": {"price": 10, "happiness_boost": 5},
    "うさぎ": {"price": 8, "happiness_boost": 4},
    "ハムスター": {"price": 5, "happiness_boost": 3},
    "フェレット": {"price": 12, "happiness_boost": 6},
    "オウム": {"price": 15, "happiness_boost": 5},
    "金魚": {"price": 3, "happiness_boost": 2},
    "カメ": {"price": 7, "happiness_boost": 4},
    "モルモット": {"price": 6, "happiness_boost": 3},
    "リス": {"price": 9, "happiness_boost": 4},
    "ヘビ": {"price": 11, "happiness_boost": 3},
    "カエル": {"price": 4, "happiness_boost": 2},
    "ハリネズミ": {"price": 10, "happiness_boost": 5},
    "フクロウ": {"price": 14, "happiness_boost": 5},
    "シマリス": {"price": 8, "happiness_boost": 3},
    "ミニブタ": {"price": 20, "happiness_boost": 6},
    "ポニー": {"price": 30, "happiness_boost": 8},
    "ネズミ": {"price": 3, "happiness_boost": 1},
    "ウーパールーパー": {"price": 7, "happiness_boost": 3},
    "イグアナ": {"price": 13, "happiness_boost": 4},
}
RECIPES = {
    "おにぎり": {
        "ingredients": {"お米": 1},
        "effect_description": "幸福度が少し回復する。",
    },
    "焼き魚": {"ingredients": {"アジ": 1}, "effect_description": "幸福度が回復する。"},
    "フルーツタルト": {
        "ingredients": {"フルーツ": 2, "小麦粉": 1},
        "effect_description": "幸福度が大きく回復する。",
    },
    "味噌汁": {
        "ingredients": {"味噌": 1, "豆腐": 1},
        "effect_description": "体力が回復し、満足度が上がる。",
    },
    "カレーライス": {
        "ingredients": {"お米": 1, "肉": 1, "野菜": 2},
        "effect_description": "幸福度とエネルギーが大幅に回復する。",
    },
    "焼きそば": {
        "ingredients": {"小麦粉": 1, "野菜": 1, "肉": 1},
        "effect_description": "満腹感が増し、幸福度が上がる。",
    },
    "卵焼き": {
        "ingredients": {"卵": 2, "砂糖": 1},
        "effect_description": "小休憩に最適、幸福度が少し回復する。",
    },
    "サラダ": {
        "ingredients": {"野菜": 3},
        "effect_description": "健康効果があり、人気度が上がる。",
    },
    "パンケーキ": {
        "ingredients": {"小麦粉": 1, "卵": 1, "牛乳": 1},
        "effect_description": "甘いおやつで幸福度が上がる。",
    },
    "寿司": {
        "ingredients": {"お米": 1, "魚": 1},
        "effect_description": "豪華な食事で幸福度が大幅アップ。",
    },
    "唐揚げ": {
        "ingredients": {"鶏肉": 1, "調味料": 1},
        "effect_description": "ボリューム満点で満腹感が持続。",
    },
    "みたらし団子": {
        "ingredients": {"もち": 3, "砂糖": 1},
        "effect_description": "甘くて満足度が増す。",
    },
    "スープ": {
        "ingredients": {"野菜": 2, "肉": 1},
        "effect_description": "体を温めて体力回復。",
    },
    "プリン": {
        "ingredients": {"卵": 2, "牛乳": 1, "砂糖": 1},
        "effect_description": "甘くて幸福度が上がる。",
    },
    "焼き芋": {
        "ingredients": {"さつまいも": 1},
        "effect_description": "ほっこりとした甘さで幸福度が回復。",
    },
    "おでん": {
        "ingredients": {"大根": 1, "卵": 1, "こんにゃく": 1},
        "effect_description": "寒い日にはぴったり。体力回復。",
    },
    "ピザ": {
        "ingredients": {"小麦粉": 1, "チーズ": 1, "トマト": 1},
        "effect_description": "パーティーに最適。人気度アップ。",
    },
    "餃子": {
        "ingredients": {"小麦粉": 1, "肉": 1, "野菜": 1},
        "effect_description": "ボリューム満点で満足度が増す。",
    },
    "アイスクリーム": {
        "ingredients": {"牛乳": 1, "砂糖": 1},
        "effect_description": "暑い日にぴったりで幸福度アップ。",
    },
    "チャーハン": {
        "ingredients": {"お米": 1, "卵": 1, "肉": 1},
        "effect_description": "手軽に作れて満腹感アップ。",
    },
}

# 不動産名生成用
PREFECTURES = ["さくら県", "もみじ県", "ほしぞら県", "にじいろ県", "ゆうやけ県"]
CITIES = ["ひなた市", "こかげ市", "ゆうなぎ市", "あさひ市", "つきみ市"]
DISTRICTS = ["わかば町", "あおば町", "さつき町", "かえで町", "ひまわり町"]
BUILDING_NAMES = [
    "サンシャイン",
    "グリーンヒル",
    "スカイビュー",
    "リバーサイド",
    "ロイヤル",
]

# カード景品
CARD_REWARDS = [
    {"name": "50万円と交換", "cost": 1, "type": "money", "value": 50},
    {"name": "幸福度MAXドリンク", "cost": 1, "type": "happiness", "value": 100},
    {
        "name": "【限定】金のトロフィー",
        "cost": 5,
        "type": "furniture",
        "value": "金のトロフィー",
    },
]

# 秘密コード（禁断市場の解禁など）
SECRET_CODES = {
    "Zodiac77": {"unlock": "forbidden_market"},
    "Angel999": {"grant": {"money": 100}},
}

# ルーレットテーブル（宝くじ/病気/転職）
ROULETTE_TABLE = {
    "lottery": [
        {"label": "大当たり(+100)", "delta_money": +100, "weight": 1},
        {"label": "当たり(+20)", "delta_money": +20, "weight": 5},
        {"label": "ハズレ(0)", "delta_money": 0, "weight": 10},
        {"label": "没収(-10)", "delta_money": -10, "weight": 2},
    ],
    "illness": [
        {"label": "軽症(-2幸福)", "delta_happiness": -2, "weight": 5},
        {
            "label": "入院(-5幸福/-5万円)",
            "delta_happiness": -5,
            "delta_money": -5,
            "weight": 2,
        },
        {"label": "無事(0)", "weight": 8},
    ],
    "job_change": [
        {"label": "良転職(ボーナス)", "job_bonus": True, "weight": 3},
        {"label": "普通(変化なし)", "weight": 8},
        {"label": "悪転職(幸福-3)", "delta_happiness": -3, "weight": 3},
    ],
}


# 追加定数（スタンプ/満タンカード、不動産、扶養控除）
STAMP_PER_PRICE = 10  # 10万円購入でスタンプ1
STAMP_TARGET = 10  # 10スタンプで満タンカード1枚
DEDUCTION_PER_DEPENDENT = 1  # 扶養控除（1人/匹あたり1万円）
RENT_RATE = 0.02  # 家賃収入（物件価格×2%/ターン）

# NPC 初期値
NPCS = {
    "熱血市長": {"description": "街の発展を願う熱い男。", "affinity": 0},
    "冷静な銀行頭取": {"description": "数字が全ての冷徹な頭取。", "affinity": 0},
    "謎の大富豪": {"description": "素性不明の大富豪。", "affinity": 0},
    "優しい薬剤師": {"description": "地域の健康を支える優しい薬剤師。", "affinity": 0},
    "頑固な鍛冶屋": {"description": "古い伝統を守る頑固な鍛冶屋。", "affinity": 0},
    "陽気な商人": {"description": "いつも笑顔の陽気な商人。", "affinity": 0},
    "冷静な警察署長": {
        "description": "街の安全を見守る冷静な警察署長。",
        "affinity": 0,
    },
    "謎めいた占い師": {"description": "未来を読み解く謎めいた占い師。", "affinity": 0},
    "若き教師": {"description": "未来を担う子供達を導く若き教師。", "affinity": 0},
    "厳格な神父": {"description": "街の精神的支柱となる厳格な神父。", "affinity": 0},
    "落ち着いた司書": {
        "description": "知識の宝庫、図書館の落ち着いた司書。",
        "affinity": 0,
    },
    "気さくな農夫": {"description": "自然と共に生きる気さくな農夫。", "affinity": 0},
    "勤勉な技術者": {"description": "街の未来を作る勤勉な技術者。", "affinity": 0},
    "陽気なバーテンダー": {
        "description": "誰とでも仲良くなれる陽気なバーテンダー。",
        "affinity": 0,
    },
    "自由奔放な画家": {"description": "街角で自由に絵を描く画家。", "affinity": 0},
    "勇敢な消防士": {"description": "街の安全を守る勇敢な消防士。", "affinity": 0},
    "社交的な記者": {"description": "真実を伝える社交的な記者。", "affinity": 0},
    "神秘的な魔法使い": {
        "description": "謎に包まれた神秘的な魔法使い。",
        "affinity": 0,
    },
    "寡黙な鍛冶職人": {"description": "黙々と作業する寡黙な鍛冶職人。", "affinity": 0},
    "人情味あふれるパン屋": {
        "description": "心温まるパンを焼く人情味あふれるパン屋。",
        "affinity": 0,
    },
}

# コレクション（抜粋）
COLLECTIBLES = {
    "昆虫": [
        "モンシロチョウ",
        "カブトムシ",
        "ナナホシテントウ",
        "オニヤンマ",
        "アゲハチョウ",
        "クワガタ",
        "カミキリムシ",
        "トンボ",
        "ミヤマクワガタ",
        "ヤンマ",
        "カゲロウ",
        "カブトムシの幼虫",
        "オオクワガタ",
        "ヒラタクワガタ",
        "オオムラサキ",
        "セミ",
        "カマキリ",
        "ハチ",
        "テントウムシ",
        "コガネムシ",
    ],
    "魚": [
        "アジ",
        "サバ",
        "タイ",
        "ヒラメ",
        "マグロ",
        "シーラカンス",
        "カレイ",
        "イカ",
        "タコ",
        "ウナギ",
        "フグ",
        "サンマ",
        "ブリ",
        "カツオ",
        "サケ",
        "スズキ",
        "メダカ",
        "コイ",
        "フナ",
        "ドジョウ",
        "ニジマス",
        "ヤマメ",
        "イワナ",
        "カジキ",
        "アユ",
        "ウグイ",
        "カワムツ",
        "オイカワ",
        "モロコ",
        "タナゴ",
        "ギンポ",
        "ハゼ",
        "カワハギ",
        "キス",
        "ホッケ",
        "イシモチ",
        "メバル",
        "アイナメ",
        "カサゴ",
        "ソイ",
        "ウツボ",
        "アオリイカ",
        "ヤリイカ",
        "コウイカ",
        "タチウオ",
        "サヨリ",
        "シラス",
        "イワシ",
        "キンメダイ",
        "アカムツ",
        "ホウボウ",
        "ウミタナゴ",
        "アオダイ",
        "キジハタ",
        "マトウダイ",
        "アブラボウズ",
        "イシダイ",
        "クエ",
        "ハタハタ",
        "サクラマス",
        "シロギス",
        "マコガレイ",
        "マダイ",
    ],
    "キラキラカード": [
        "伝説の勇者",
        "魔法使い見習い",
        "鋼鉄のゴーレム",
        "キングドラゴン",
        "森のエルフ",
        "闇の騎士",
        "天空の守護者",
        "大地の精霊",
        "深海の魔女",
        "火の悪魔",
        "氷の女王",
        "風の精霊",
        "光の聖騎士",
        "影の暗殺者",
        "雷鳴の戦士",
        "聖なる巫女",
        "獣の王",
        "海賊船長",
        "幻の幻獣",
        "時空の旅人",
    ],
    "化石": [
        "アンモナイト",
        "三葉虫",
        "恐竜の足跡",
        "古代の植物",
        "始祖鳥の化石",
        "マンモスの牙",
        "サメの歯化石",
        "シーラカンスの骨",
        "巨大トリケラトプス",
        "古代哺乳類の骨",
        "化石魚",
        "翼竜の骨",
        "古代昆虫の化石",
        "氷河期の牙",
        "深海生物の化石",
        "珊瑚の化石",
        "珪化木",
        "古代哺乳類の足跡",
        "三葉虫の巣",
        "古代ウミユリ",
    ],
}


# NPC個別イベントしきい値（例）
NPC_EVENTS = {
    "熱血市長": {
        "threshold": 3,
        "reward": {"popularity": 2},
        "text": "市長から表彰状！人気+2",
    },
    "謎の大富豪": {
        "threshold": 5,
        "reward": {"money": 10},
        "text": "大富豪から寄付金！+10万",
    },
    "優しい薬剤師": {
        "threshold": 4,
        "reward": {"item": ("薬", 1)},
        "text": "回復薬をもらった！",
    },
    "冷静な銀行頭取": {
        "threshold": 4,
        "reward": {"money": 5},
        "text": "銀行頭取から投資アドバイス！+5万",
    },
    "頑固な鍛冶屋": {
        "threshold": 3,
        "reward": {"item": ("武器", 1)},
        "text": "鍛冶屋から特製武器をもらった！",
    },
    "陽気な商人": {
        "threshold": 2,
        "reward": {"popularity": 1},
        "text": "商人から特別割引券！人気+1",
    },
    "冷静な警察署長": {
        "threshold": 4,
        "reward": {"security": 1},
        "text": "警察署長から感謝状！治安+1",
    },
    "謎めいた占い師": {
        "threshold": 5,
        "reward": {"luck": 1},
        "text": "占い師から未来のヒント！運+1",
    },
    "若き教師": {
        "threshold": 3,
        "reward": {"knowledge": 1},
        "text": "教師から特別授業！知識+1",
    },
    "厳格な神父": {
        "threshold": 4,
        "reward": {"faith": 1},
        "text": "神父から祝福を受けた！信仰+1",
    },
    "落ち着いた司書": {
        "threshold": 3,
        "reward": {"knowledge": 1},
        "text": "司書から貴重な本をもらった！知識+1",
    },
    "気さくな農夫": {
        "threshold": 2,
        "reward": {"item": ("野菜", 3)},
        "text": "農夫から新鮮な野菜をもらった！",
    },
    "勤勉な技術者": {
        "threshold": 4,
        "reward": {"item": ("工具", 1)},
        "text": "技術者から特製工具をもらった！",
    },
    "陽気なバーテンダー": {
        "threshold": 3,
        "reward": {"popularity": 1},
        "text": "バーテンダーから特製ドリンク！人気+1",
    },
    "自由奔放な画家": {
        "threshold": 3,
        "reward": {"item": ("絵画", 1)},
        "text": "画家から特製絵画をもらった！",
    },
    "勇敢な消防士": {
        "threshold": 4,
        "reward": {"security": 1},
        "text": "消防士から感謝状！治安+1",
    },
    "社交的な記者": {
        "threshold": 3,
        "reward": {"popularity": 1},
        "text": "記者から特別記事！人気+1",
    },
    "神秘的な魔法使い": {
        "threshold": 5,
        "reward": {"magic": 1},
        "text": "魔法使いから特別な魔法を教わった！",
    },
    "寡黙な鍛冶職人": {
        "threshold": 3,
        "reward": {"item": ("防具", 1)},
        "text": "鍛冶職人から特製防具をもらった！",
    },
    "人情味あふれるパン屋": {
        "threshold": 2,
        "reward": {"item": ("パン", 2)},
        "text": "パン屋から焼きたてのパンをもらった！",
    },
}

# ミニゲーム設定
MINIGAME = {
    "cake_stop": {"center": [0.45, 0.55], "reward": 5},
    "police_find": {"grid": 16, "time_sec": 10, "reward": 5},
    "dj_beat": {"beats": 5, "interval": 0.9, "window": 0.15, "reward_per_good": 1},
    "chef_memory": {"length": 4, "reward": 4},
}
