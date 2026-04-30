# sumayame — App Card 用 Landing Page

「スマホをやめれば魚が育つ（スマやめ）」のX(Twitter)投稿で
App Card を表示させるための、軽量ランディングページ。

## URL（GitHub Pages 公開後）

```
https://segawatks.github.io/sumayame/
```

`segawatks` を自分のGitHubユーザー名に置換してください。
`index.html` 内の同プレースホルダも合わせて置換が必要です。

## 仕込んでいるメタタグ

- X (Twitter) App Card (`twitter:card=app`)
- Open Graph (Facebook / Discord / Slack 等)
- Apple Smart App Banner (Safari iOS で App Store 誘導バナー)
- App Links / Universal Links ヒント (`al:ios:*`)

## ファイル構成

```
.
├── index.html   # メタタグ込みのLP
├── og.png       # OG画像（1200x630px）※あとでアップロード
├── .nojekyll    # GitHub Pages の Jekyll 処理を無効化
└── README.md
```

## デプロイ手順（GitHub Pages）

1. GitHub で新規リポジトリ `sumayame` を **Public** で作成
2. このフォルダの中身をコミット & プッシュ
3. リポジトリ Settings → Pages
4. Source を **Deploy from a branch** にし、Branch を `main` / root に設定
5. 数分待つと `https://<user>.github.io/sumayame/` で公開

## カード表示の確認

- X: <https://cards-dev.twitter.com/validator>（廃止された場合は実投稿でテスト）
- OG: <https://www.opengraph.xyz/> や Discord/Slack に貼って確認
