# 流入分析 実装サマリ — スマやめ X投稿キャンペーン

## 全体ファネル

```
[App内シェアボタン表示]    ← Firebase Analytics（未実装・予定）
        ↓
[シェアボタン押下]          ← Firebase Analytics（未実装・予定）
        ↓
[X投稿でカード表示]         ← X側の数値（Posts Analytics）
        ↓
[LPカードタップ]            ← GA4: PV
        ↓
[App Storeボタン押下]       ← GA4: click_store
        ↓
[App Store ページ閲覧]      ← Apple App Analytics: impressions
        ↓
[インストール]               ← Apple App Analytics: downloads
```

---

## 1. GA4（Web側計測）

| 項目 | 値 |
|---|---|
| 測定ID | `G-CFDC0LDR85` |
| 仕込みページ | メインLP `/lp/` ＋ 魚別30ページ `/lp/fish/{enum}/` |
| ダッシュボード | https://analytics.google.com/ |

**計測内容：**

- **ページビュー（PV）** — 自動。URLごとに集計
- **カスタムイベント `click_store`** — アイコンorボタン押下時に発火（魚種は記録しない）

**実装位置：**

- `<head>` に gtag.js
- 各 `.store-link` の click ハンドラで `gtag('event', 'click_store')`

---

## 2. Apple App Analytics（App Store側計測）

| 項目 | 値 |
|---|---|
| Campaign Token (ct) | `lp_x_fish` |
| 仕込みパラメータ | `?ct=lp_x_fish&mt=8` |
| 適用先 | 全アンカー / al:ios:url / itms-apps:// / https:// JS遷移 |
| ダッシュボード | https://appstoreconnect.apple.com/ → App Analytics → ソース |
| 反映遅延 | 24〜48時間 |

**計測内容：**

- **App Store ページ閲覧数（impressions）**
- **ダウンロード数**
- **コンバージョン率**（閲覧→DL）
- 日次集計

---

## 3. URL構造による間接的な魚種別計測

各魚に固有URL を発行（30種類）:
```
https://segawatks.github.io/sumayame/lp/fish/{enumName}/
例: /FueYakko0/, /Manboo2/, /Syachi4/ ...
```

GA4で URL別 PV が自動集計されるので、**「どの魚が一番シェアされてバズったか」** が後追いで分かる（明示的に魚種パラメータを送ってないが、URL自体が識別子になっている）。

---

## 計算可能な指標

| 指標 | 計算方法 | 用途 |
|---|---|---|
| LP流入経路 | GA4「集客」レポート | X / Discord / Slack 等の比較 |
| LPクリック率 | GA4: click_store ÷ PV | LP内動線の効果検証 |
| ストア閲覧→DL率 | App Analytics: DL ÷ impressions | App Store ページの説得力 |
| シェア→DL率 | Firebase share + App DL（実装後） | シェア機能のROI |
| 魚種別人気度 | GA4: URLごとPV | アプリ内シェア優先度の最適化 |

---

## 残タスク（追加予定）

### Firebase Analytics（iOS App側）

スマやめ本体に追加で：

```swift
import FirebaseAnalytics

// 1. シェアボタン表示時
.onAppear {
    Analytics.logEvent("share_button_impression", parameters: [
        "fish": fish.rawValue
    ])
}

// 2. シェアボタン押下時
Analytics.logEvent("share_button_tap", parameters: [
    "fish": fish.rawValue
])

// 3. シェア完了時
Analytics.logEvent("share_completed", parameters: [
    "fish": fish.rawValue,
    "destination": activityType?.rawValue ?? "unknown"
])
```

### 将来：BigQuery エクスポート

GA4 と Firebase Analytics を同じ BigQuery プロジェクトにエクスポートすれば、SQL でファネル全段を1クエリで結合可能。設定はFirebase Console → プロジェクト設定 → 統合 → BigQuery、で1クリック。

---

## 関連リソース

- **リポジトリ**: https://github.com/segawatks/sumayame
- **公開URL（メイン）**: https://segawatks.github.io/sumayame/lp/
- **魚別URL パターン**: `https://segawatks.github.io/sumayame/lp/fish/{enumName}/`
- **生成スクリプト**: `generate_fish_pages.py`
- **デプロイコマンド**: `sumayame_push.command`

---

## 制約 / 注意

- Apple App Analytics の計測は **24〜48時間遅延**
- Apple は **個人特定不可**（プライバシー仕様）
- X カードは URL 単位でキャッシュされるため、メタタグ更新時は新URL（クエリ追加）で投稿
- 魚別URLが増えるとリポジトリ容量が増えるが、現状4.2MB程度で問題なし
