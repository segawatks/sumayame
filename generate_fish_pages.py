#!/usr/bin/env python3
"""
魚ごとの個別LP（X カード用）を一括生成。
ファイル構成：
  lp/fish/{enumName}/index.html  ← 個別ページ
  lp/fish/{enumName}/og.png      ← その魚のOG画像
"""
import os
import shutil
from pathlib import Path

# ===== 設定 =====
BASE = Path(__file__).parent
LP_DIR = BASE / "lp"
FISH_DIR = LP_DIR / "fish"
TWEET_IMG = BASE / "TweetImg"
SITE_BASE = "https://segawatks.github.io/sumayame/lp/fish"

# 削除フラグ付きの魚（コメントで「削除」と書かれているもの）
DELETED = {"Kurione4", "AdeliaePen4", "HigePen4"}

# enum から「名前」だけ抽出
# (NONAME, MAXValue, _en, 削除 を除外)
FISH_LIST = [
    # C_rank=0
    "Oyabittya0", "KakureKumanomi0", "SomewakeYakko0",
    # B_rank=1
    "TogeTyou1", "HakoFugu1", "PFGoby1",
    # A_rank=2
    "CandyBasulet2", "ThinkerBF2", "Same2",
    # Ver1.1.0で追加
    "DebaSuzumedai0", "FueYakko0",
    "NanyoHagi1", "TatsunoOtoshigo1",
    "KuraionEnzelu2", "Manboo2",
    # Ver1.3.0で追加
    "MGKHagi1", "NDHaze1",
    "PMEnjenl2", "ItomakiEi2",
    # Ver1.5.0で追加
    "PQueen0", "Tsunodashi0",
    "OrangeFBF1", "ZinbeiSame2",
    # Ver1.7.0で追加
    "KuroyuriHaze1",
    "KaeruAnkoo2",
    # Ver5.0.0で追加
    "Dolphin4",
    # Ver5.1.0で追加
    "Syachi4",
    # Ver6.5.0で追加
    "Shironaga_Big5", "PenEmp_Big5",
    # Ver17.0.16で追加
    "HigePen0",
    # Ver18.0.0で追加 (画像が無いものはスキップ)
    "AdeliaePen1", "Kurione0",
]

# ===== HTMLテンプレート =====
TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>スマホをやめれば魚が育つ — スマホ依存防止アプリ</title>
  <meta name="description" content="スマホを置いて集中している間、水槽の魚たちが育っていく。やめたい気持ちを、かわいい魚を育てる楽しさに変えるiOSアプリ「スマやめ」。">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{fish_url}">
  <meta property="og:title" content="App Store">
  <meta property="og:description" content="集中時間がかわいい魚に変わる。スマホ依存を、魚を育てる楽しさへ。">
  <meta property="og:image" content="{img_url}">
  <meta property="og:image:width" content="{img_w}">
  <meta property="og:image:height" content="{img_h}">
  <meta property="og:image:alt" content="スマホをやめれば魚が育つ">
  <meta property="og:site_name" content="スマやめ">
  <meta property="og:locale" content="ja_JP">

  <!-- X (Twitter) Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@rikodesign">
  <meta name="twitter:title" content="App Store">
  <meta name="twitter:description" content="スマホをやめれば、魚が育つ。集中時間がかわいい魚に変わるiOSアプリ。">
  <meta name="twitter:image" content="{img_url}">

  <!-- Apple Smart App Banner -->
  <meta name="apple-itunes-app" content="app-id=1669133971">

  <!-- App Links -->
  <meta property="al:ios:app_store_id" content="1669133971">
  <meta property="al:ios:app_name" content="スマホをやめれば魚が育つ">
  <meta property="al:ios:url" content="https://apps.apple.com/jp/app/id1669133971">
  <meta property="al:web:url" content="{fish_url}">

  <link rel="canonical" href="{fish_url}">
  <link rel="icon" href="../../AppIcon.png" type="image/png">
  <link rel="apple-touch-icon" href="../../AppIcon.png">

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic UI", "Meiryo", sans-serif;
      background: #ffffff;
      -webkit-font-smoothing: antialiased;
      -webkit-tap-highlight-color: transparent;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    main {{
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }}
    .icon-link {{
      display: block;
      margin: -30px 0 32px;
      transition: transform .15s ease, opacity .15s ease;
    }}
    .icon-link:active {{ transform: scale(0.96); opacity: 0.85; }}
    .icon {{
      width: 35vw;
      height: 35vw;
      max-width: 160px;
      max-height: 160px;
      min-width: 96px;
      min-height: 96px;
      border-radius: 22%;
      box-shadow: 0 10px 30px rgba(44, 91, 184, 0.25);
      display: block;
    }}
    .store-badge {{
      display: block;
      transition: transform .15s ease, opacity .15s ease;
      margin: 0 0 12px;
    }}
    .store-badge:active {{ transform: scale(0.96); opacity: 0.85; }}
    .store-badge img {{
      display: block;
      width: 50vw;
      max-width: 220px;
      min-width: 140px;
      height: auto;
    }}
    .cta-note {{ font-size: 13px; color: #1a3d80; margin: 0; }}
  </style>
</head>
<body>
  <main>
    <a class="icon-link store-link" href="https://apps.apple.com/jp/app/id1669133971">
      <img class="icon" src="../../AppIcon.png" alt="スマホをやめれば魚が育つ">
    </a>
    <a class="store-badge store-link" href="https://apps.apple.com/jp/app/id1669133971">
      <img src="../../ToStoreBtn.png" alt="App Storeからダウンロード">
    </a>
    <p class="cta-note">タップで App Store が開きます</p>
  </main>
  <script>
    Array.prototype.forEach.call(document.querySelectorAll('.store-link'), function (el) {{
      el.addEventListener('click', function (e) {{
        var ua = navigator.userAgent || '';
        if (/iPhone|iPad|iPod/i.test(ua)) {{
          e.preventDefault();
          window.location.href = 'itms-apps://itunes.apple.com/jp/app/id1669133971';
          setTimeout(function () {{
            window.location.href = 'https://apps.apple.com/jp/app/id1669133971';
          }}, 600);
        }}
      }});
    }});
  </script>
</body>
</html>
"""


def main():
    from PIL import Image

    FISH_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    skipped = []

    for fish in FISH_LIST:
        if fish in DELETED:
            skipped.append((fish, "deleted in enum comment"))
            continue

        img_src = TWEET_IMG / f"{fish}.png"
        if not img_src.exists():
            skipped.append((fish, "image not found"))
            continue

        # 出力ディレクトリ
        out_dir = FISH_DIR / fish
        out_dir.mkdir(parents=True, exist_ok=True)

        # OG画像をコピー
        shutil.copy(img_src, out_dir / "og.png")

        # 画像サイズを取得
        with Image.open(img_src) as im:
            w, h = im.size

        # HTML生成
        fish_url = f"{SITE_BASE}/{fish}/"
        img_url = f"{fish_url}og.png"
        html = TEMPLATE.format(
            fish_url=fish_url,
            img_url=img_url,
            img_w=w,
            img_h=h,
        )
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        generated.append(fish)

    print(f"\n✅ 生成完了: {len(generated)} 種類")
    for f in generated:
        print(f"  - {SITE_BASE}/{f}/")

    if skipped:
        print(f"\n⏭  スキップ: {len(skipped)} 件")
        for f, reason in skipped:
            print(f"  - {f} ({reason})")


if __name__ == "__main__":
    main()
