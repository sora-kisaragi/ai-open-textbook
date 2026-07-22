# AI Open Textbook

[English](README.md) | 日本語

このリポジトリでは、高等学校「情報I」の日本語オープン教材を制作しています。
教室での試行、自習、GitHub上での共同開発を想定し、教材本文、教員向け資料、
問題、解答、ルーブリックをレビュー可能なデータとして管理しています。

## 教材を読む

静的HTML教材を生成すると、Webサーバーやインターネット接続なしで閲覧できます。

```bash
uv sync --locked --extra dev
uv run python scripts/build_static_site.py
uv run python scripts/verify_static_site.py
```

生成後、`build/site/index.html` をブラウザで開いてください。目次から学習者向けの
各レッスンへ移動できます。教員向けページは学習者向けページと分けて表示されます。

印刷・PDF版は次のコマンドで生成できます。

```bash
uv run python -m playwright install chromium
uv run python scripts/build_pdf.py
```

出力先は `build/information-i-textbook.pdf` です。`build/` 以下は生成物であり、
直接編集したりGitへコミットしたりしません。

## 対象範囲

現在のv0.3最終レビュー候補は、高等学校「情報I」について暫定的に構成した
4単元・32レッスンを対象としています。

1. 情報社会と問題解決
2. コミュニケーションと情報デザイン
3. コンピュータ、アルゴリズム、プログラミング
4. ネットワーク、情報システム、データ

学習者向け教材に加えて、教員向け補足資料、練習問題、解答、ルーブリック、
オフラインHTML、再現可能な印刷・PDF生成手順を含みます。詳しい対象範囲と
確認状況は、`docs/MVP_SCOPE.md`、`docs/CURRICULUM_MAP.md`、
`docs/INFORMATION_I_COMPLETION_MATRIX.md` を参照してください。

この教材は、公式に承認された教科書であるとは主張していません。
また、学習指導要領への最終的な適合を主張するものでもありません。
人間による最終レビュー前のオープン教材、補助教材、自習用資料です。

## 教材設計の方針

Pythonを実行例の主な言語として使用しますが、Pythonの文法そのものを教材の
中心には置きません。問題解決、情報の表現、アルゴリズム、データ、モデル、
ネットワーク、情報倫理など、ほかの言語や状況にも移せる考え方を先に扱います。

プログラミング分野では、原則として次の順序で学びます。

1. 概念を理解する
2. 値や処理の流れを追跡する
3. Pythonの実行例で確かめる
4. Python固有の書き方を区別する
5. 別の状況に考え方を移す練習をする

## データとファイル構成

教材の正本データは `data/collections/*.ndjson` です。全体の暫定計画は
`curriculum/highschool_information_i.curriculum.json` で管理しています。
SQLiteは検索や検証に使う生成インデックスであり、正本ではありません。

- `lessons/`: 学習者向けレッスン
- `teacher_guides/`: 教員向け補足資料
- `data/collections/`: 問題、解答、ルーブリック、出典、改訂履歴
- `curriculum/`: 単元、目標、前提関係、対応表
- `schemas/`: JSON Schema
- `scripts/`: 検証、実行例確認、HTML・PDF生成
- `docs/`: 運用規則、設計資料、レビュー証拠

教材データを変更する場合は、安定したIDとスキーマを保ち、非自明な変更ごとに
`data/collections/revisions.ndjson` へ改訂記録を追加します。

## 開発と検証

開発環境を準備し、主要な検証を実行するには次のコマンドを使います。

```bash
uv sync --locked --extra dev
uv run python -m playwright install chromium
uv run python scripts/validate_ndjson.py
uv run python scripts/build_sqlite_index.py
uv run python scripts/check_examples.py
uv run python scripts/build_static_site.py
uv run python scripts/verify_static_site.py
uv run python scripts/build_pdf.py
uv run python -m pytest
```

ブランチやPull Requestでは、実際の比較元コミットを指定して改訂履歴も確認します。

```bash
uv run python scripts/check_revision_history.py --base-ref <base-commit>
```

Windowsでは、ロック済み環境を確実に使うため `uv run python` を使用してください。
GNU Makeを利用できる環境では、`make check` でも一連の検証を実行できます。

AIエージェントを使って変更する場合は、最初に `AGENTS.md` を読み、教材を
承認済み・公開可能とみなさず、小さくレビュー可能な変更として作業してください。

## ライセンス

- 教材コンテンツ: 特記がない限りCC BY 4.0
- コードとスクリプト: 特記がない限りMIT License

詳しくは `LICENSE-CONTENT-CC-BY-4.0.md` と `LICENSE-CODE-MIT.md` を
参照してください。
