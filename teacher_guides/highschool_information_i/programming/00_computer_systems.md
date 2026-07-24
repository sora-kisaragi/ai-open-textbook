# 教師用ガイド: コンピュータのしくみと情報処理

## レッスンのねらい

架空の印刷依頼を使い、コンピュータを部品名の暗記ではなく、入力、保存装置、主記憶、処理装置、出力、ソフトウェアの関係として捉えます。
アプリケーションの値と状態の流れを手作業で追跡した後、OSによる資源利用の仲介を別の層として重ね、主記憶と保存装置の違い、表現と資源の限界を説明できることを目指します。

## 授業時間（必修50分×2時限）

本時は**2時限とも必修**です。第1時で概念モデルとQ104の手作業トレース、第2時で誤解修正、限界の分類、異なる場面への転移を行います。Pythonなどの実行環境は使いません。

## 教材・準備

- 学習者用本文。図を提示する場合は `c1-computer-system-trace.svg`
- 1組につき「入力、アプリケーションの状態、保存装置、主記憶、処理装置、出力」の流れカードと、「OSによる資源利用の仲介」カード。OSカードは流れの一段階に置かず、各資源との関係を重ねる
- Q104の値カード: 6ページ、2部、残り12、残り11、残り0、受付済み、処理中、完了
- 個人用の空欄トレース表。列は「出来事、保存装置、主記憶の状態、処理、出力」
- 板書または投影の準備: 主記憶と保存装置の比較表、8ビットの値表

授業前に、図なしでも全内容を扱えるよう表を印刷または共有します。実機分解、特定OSの画面、Python、実在する印刷履歴は不要です。

## 前提確認と分岐

B2の「表現を細かくすると一般にデータ量が増える」を確認します。
準備チェックの1と2で迷う学習者には、マイク入力とスピーカー出力の二択を先に行います。
3で編集中データと保存済みデータを同一視する場合は、「保存後に一文字追加して、まだ保存していない」カードを重ね、二つの状態があり得ることを示します。

## 学習者用本文との対応

1. アプリケーションの状態・流れの層と、OSによる資源利用の仲介の層を分けて説明する。（C1.O1）
2. 保存装置と主記憶を、保持目的と処理時点から区別する。（C1.O1）
3. Q104のアプリケーション状態を出来事ごとに手作業で追い、OSが仲介する資源を別欄へ示す。（C1.O2）
4. 誤った説明を、役割と状態を使って修正する。（C1.O1、C1.O2）
5. 表現範囲、丸め、資源不足を分類する。（C1.O3）
6. 自動販売機で役割、状態、保存、表現範囲を独立して扱い、図書貸出端末は追加転移に使う。（C1.O1〜O3）

## 50分授業の到達点と判断

| 時限 | 学習者の到達点 | 50分の区切り | 続行条件 |
| --- | --- | --- | --- |
| 第1時 | アプリケーションの状態変化とOSの資源仲介を分け、保存装置、主記憶、処理装置、入出力の関係をQ104で追う。 | Q104の状態変化を一段階示し、同じ段階でOSが仲介する資源を別に説明する。 | 値の変化と資源仲介を混同せず説明できれば第2時へ進み、不足時は二層カードを並べ直す。 |
| 第2時 | 表現範囲、丸め、資源不足を区別し、別の装置場面へ転移する。 | 分類表と独立転移を提出し、続行、再学習、支援要請を選ぶ。 | 三種類の限界と状態を理由付きで示せれば次へ進み、不足時は該当する計算またはトレースへ戻る。 |

## 詳細進行

### 第1時: 役割、主記憶と保存装置、状態のトレース

| 時間 | 活動 | 期待する学習者の反応 | 教師のフィードバック |
| --- | --- | --- | --- |
| 0〜5分 | 大きな問いと準備チェック | 入力と出力を区別し、編集中と保存済みは同じとは限らないと気付く | 正誤だけで終えず、「どの時点のデータか」を尋ねる |
| 5〜15分 | 二層の役割カードを並べる | まず入力→アプリケーション状態→処理→出力を作り、保存装置との読み書きを足す。その後、OSカードを資源利用の仲介として重ねる | OSを値の流れの一段階に置いた場合は、アプリケーションの値が何によって変わるかと、資源利用を誰が仲介するかを別の問いにする |
| 15〜25分 | 主記憶と保存装置の比較 | 実行中の状態と保存済みファイルを別欄へ置く | 「速い・遅い」だけなら、処理時点と保存操作を分けた例へ戻す |
| 25〜42分 | Q104を一行ずつ手作業でトレース | 出来事の直後ごとに、状態と残り枚数を更新する | 答えを先に示さず、「前の行から変わった列はどれか」と促す |
| 42〜47分 | 説明になっていない例を修正 | 処理装置、主記憶、保存装置、OSの混同を二つ以上直す | 部品名だけの修正には、渡されるデータも言わせる |
| 47〜50分 | 出口確認 | 主記憶と保存装置の違い、Q104の一段階を説明する | 続行条件未達なら第2時冒頭の補習カードを指定する |

### 第2時: 限界の分類、誤解修正、別場面への転移

| 時間 | 活動 | 期待する学習者の反応 | 教師のフィードバック |
| --- | --- | --- | --- |
| 0〜5分 | 第1時の再生または補習 | 役割カードとQ104の状態を再構成する | OS、主記憶、保存装置を一文ずつ説明させる |
| 5〜12分 | 8ビットの表現範囲 | 256個の値と最大値255を区別する | 「0も一つ」と数直し、実在製品の仕様ではないと再確認する |
| 12〜20分 | 表現範囲・丸め・資源の比較 | 300、18.26、動画の例を三分類し、根拠を述べる | 「できない」で終えず、値の形式か利用資源かを問う |
| 20〜25分 | 自動販売機の初期状態と一つ目の出来事を全体で記入する | 入力と、出来事直後のアプリケーション状態を分ける | OS欄には資源利用の仲介だけを書き、状態値と混ぜないよう確認する |
| 25〜45分 | OS上で販売アプリケーションが動く学習用自動販売機を、役割、三つの出来事、保存判断、表現範囲の四欄で独立して追う | 投入金額、選択、在庫の状態を追い、OSの資源仲介を別欄にし、0〜255の欄へ300円を記録する限界を説明する | 制御ソフトウェアをOSと同義にした場合は、今回のOSモデルへ戻す。各行は一つの出来事とその直後の状態に絞る |
| 45〜50分 | 到達チェック、必要な一度の修正、学習経路決定 | 続行、再学習、支援要請のいずれかを表の行を根拠に選ぶ | 自己評価だけでなく表の具体的な行を証拠にする |

各表の時間は合計50分です。活動を早く終えた場合も、第2時の独立転移を省略して発展へ置き換えません。

## 期待する反応とフィードバックの要点

| 観察される反応 | 判断 | 次の働きかけ |
| --- | --- | --- |
| 「主記憶は一時、保存装置は後で使う」と例付きで言える | 概念を接続できている | この教材で主記憶を揮発性とする条件を確認し、電源断または大きなファイルの場面へ広げる |
| 「CPUが全部する」または「OSが全部する」と答える | 状態変化と資源仲介が未分化 | 入力値を受けるアプリケーション、命令を実行する処理装置、資源利用を仲介するOSへ分ける |
| 各行で残り枚数だけを更新できる | 状態追跡の基礎がある | 状態名と出力枚数も同時に記録させる |
| 最終結果12だけを書き、途中を省く | トレースと計算結果を混同 | 出来事カードを一枚ずつめくり、直後の値を書く |
| 300と動画の両方を「容量不足」とする | 表現と資源を混同 | 「300という値自体を欄に書けるか」「動画の値は書けるか」を分けて問う |

## アクセシビリティの代替

図は必須にせず、図の直後の順序表を完全な代替として使います。
色だけで役割を区別せず、カードへ番号と役割名を記します。
カード操作が難しい学習者は、番号を口頭で読み上げる、表へ記号を入れる、支援者へ配置を指示する方法を選べます。
状態表は列ごとに読み上げ可能な見出しを付け、視覚的な矢印だけを根拠に評価しません。

## 一人・静的教材での同等活動

対話や実機が使えない場合は、学習者用本文のQ104表で次の行を隠し、予想を書いてから開く方法を使います。役割カードは番号付きリストへ置き換えます。相互説明は、自分の表だけを読んだ第三者が再現できるよう、各行へ「何が起きたため」を一文追加する活動へ置き換えます。

## 形成的評価

- C1.O1: OSの仲介を含め、アプリケーション、主記憶、保存装置、処理装置、入出力の関係を説明できる。
- C1.O2: 各出来事の直後に変わるアプリケーション状態を少なくとも3段階記録し、OSが仲介する資源を別欄へ示せる。
- C1.O3: 表現範囲、丸め、資源不足を、原因と影響を含む文で区別できる。

単語の暗記ではなく、「どのデータが」「どの時点で」「どの役割にあり」「何によって変わったか」がつながっているかを確認します。

## 停止点と次時限への条件

第1時は、Q104について段階0〜4を表にし、主記憶と保存装置を別の列として説明したところで停止します。全員が完了していなくても、ここから表現限界へ進めません。

第2時へそのまま進む条件は、(1) OSを物理装置や値の流れの一段階としない、(2) 保存済み画像と実行中の状態を区別する、(3) 出来事の直後に残り枚数を更新する、の3点です。
1点未達なら第2時冒頭7分で該当カードを再実施します。

2点以上未達の学習者には、通常経路を圧縮して次の50分経路を使います。

| 時間 | 短縮活動 | 退出成果物 |
| --- | --- | --- |
| 0〜7分 | 入力、アプリケーション状態、処理、出力を並べ、OSを資源仲介の別層へ置く | 二層カード配置 |
| 7〜18分 | Q104の段階0、1、3、4だけを教師と再構成する | 入力値6と2、計算結果12、1枚出力後の残り11を含む短縮トレース |
| 18〜28分 | 0〜255へ300を入れる例と、主記憶12 MBで4 MBずつ扱う例を比較する | 表現範囲と資源不足を分けた二行表 |
| 28〜40分 | 3ページを2部印刷する新しい値で短縮トレースを作る | 初期、計算後、1枚出力後、完了の四状態 |
| 40〜46分 | 値の変化とOSの仲介を一文ずつ説明する | 根拠付きの二文 |
| 46〜50分 | 続行、自己学習で再試行、支援要請を選ぶ | 未達項目と次の行動 |

この短縮経路では、Q104の完全表、丸めを含む三分類、自動販売機の完全な独立転移を自己学習へ送ります。短縮トレース、二行分類、別の値による四状態は補習の退出証拠であり、C1.O1〜O3の習得判定ではありません。通常の到達チェックと独立転移を再提出してから次のレッスンへ進みます。

第2時は到達チェックと学習経路の決定で停止します。発展課題は必修活動の代わりにしません。

## 補習と任意発展

補習は二層モデル、状態トレース、限界分類の不足箇所へ戻ります。任意発展は、通常経路の到達チェックと独立転移による習得証拠が成立した後にだけ行います。短縮経路の退出証拠だけでは発展へ進めません。

### 補習

- 役割の混同: 「受け取る・置く・実行する・渡す」の四つの動詞へ戻り、装置名を後から対応付ける。
- 主記憶と保存装置の混同: 保存後に一文字追加した二枚のカードを使い、どちらが再起動後に残る想定かを説明する。
- トレースの省略: 出来事を一枚ずつ提示し、変わらない欄には「同じ」と明記させる。
- 限界の混同: 「値を書けるか」「書けたデータを処理できるか」の二問で分類し直す。

### 任意発展

- 主記憶へ全ページを置かず、3ページずつ処理する場合の状態を追加する。
- 複数の印刷依頼があるとき、待ち行列の状態をどのように表すか提案する。
- 同じ役割モデルを、センサー付き信号機や音楽再生端末へ適用し、モデルで説明しにくい点も一つ挙げる。

## 想定される誤解

- 処理装置が命令、データ、ファイルを永久に保存する。
- 主記憶と保存装置は速度だけが違う。
- OSが処理装置そのもの、または利用者向けアプリケーションである。
- 最終出力が合えば途中状態は記録しなくてよい。
- 256個の値を表せるため最大値も256である。
- 教材の8ビット欄を実在システムの仕様と受け取る。
- 「容量不足」「遅い」だけで、表現または資源のどれが制約かを特定しない。

## C2へ接続する際の注意

C1ではPythonを中心にしません。カード、表、装置場面、手作業トレースを完了してから、C2で状態に名前を付ける方法として変数へ接続します。C1の理解確認に代入構文や実行環境の知識を要求しません。

## 合成データと出典上の注意

星見高校、メディアラボ、依頼番号、ファイル名、機器条件は架空です。
8ビットのページ数欄と12 MBの主記憶例は、有限性を考えるための単純化したモデルであり、実在製品の仕様ではありません。
図とトレース表は本教材のために作成したオリジナルです。
外部の機器図や仕様表を追加する場合は、出典と利用条件を確認してください。

## Claim Review Ledger

| Claim locator | Exact claim | Claim type | Evidence | Check | Scope note |
| --- | --- | --- | --- | --- | --- |
| `lesson.info1.programming.computer.systems.v1` / `コンピュータを役割で捉える` / paragraph beginning `OS（オペレーティングシステム）は` | The lesson models an operating system as software that mediates an application's use of processing time, main-memory space, files, and input/output devices. | technical | `src.nist.csrc.operating.system.glossary.v1`; NIST SP 800-152 supports hardware-resource management and common services, NIST SP 800-82r3 supports the possible functions of input/output control, resource scheduling, and data management, and NISTIR 7695 supports the general intermediary relationship between users and computer hardware. | 2026-07-23, AI source review, `supported` | The sources support the OS category and these general functions. The application-to-OS request, listed resources, and sequence in the lesson are a simplified conceptual model, not a universal OS architecture, scheduling method, or execution order. |
| `lesson.info1.programming.computer.systems.v1` / "保存装置と主記憶" | Storage retains retrievable data; the lesson separately models current working state in main memory. | technical | `src.nist.csrc.storage.glossary.v1`, source locator NIST SP 800-88 Rev. 2 Appendix A, PDF p.42 / printed p.34; the main-memory split is explicitly a project-authored classroom model. | 2026-07-22, AI source review, `supported` | No power-loss, device-performance, or implementation claim is inferred from the storage glossary. |
| `lesson.info1.programming.computer.systems.v1` / "保存装置と主記憶は、なぜ分けるのか" / paragraph beginning "このレッスンでは、主記憶を" | The lesson models main memory as volatile memory, whose content is lost when power is turned off or lost. | technical | `src.nist.csrc.volatile.memory.glossary.v1`; NIST CSRC Glossary term "Volatile Memory," definition sourced to NIST SP 800-101 Rev. 1 and NIST SP 800-72, https://csrc.nist.gov/glossary/term/volatile_memory. | 2026-07-23, AI source review, `supported` | The NIST definition supports only the stated power-loss property of volatile memory. Treating main memory as volatile is this lesson's bounded model; it does not assert that every memory technology, file, storage device, or system state is lost when power is off. |
| `lesson.info1.programming.computer.systems.v1` / "表現と資源の限界" | An unsigned 8-bit classroom field has 256 combinations, representing 0 through 255; the displayed memory and rounding results follow from the stated model. | technical | Deterministic calculations in the lesson: `2^8 = 256`, `12 / 4 = 3`, and `23.5 - 23.47 = 0.03`. | 2026-07-22, AI calculation review, `supported` | The field width, memory sizes, and print system are synthetic and do not describe a real product or language runtime. |

## Figure Provenance

| Figure | Authoring record | Clean-room check | Review status |
| --- | --- | --- | --- |
| `c1-computer-system-trace.svg` | Project-original editable SVG revised in-repository on 2026-07-23 with AI-assisted drafting from the lesson's two-layer state-flow and resource-mediation model, using SVG text and vector primitives. SHA-256: `63d967dfc656d9e59a7e927c95e2470d05897402df740a197bd442c7bbb6d558`. | No imported or traced hardware diagram, textbook figure, sample page, or third-party asset was used. The adjacent two-layer table is the complete nonvisual equivalent. | `needs_human_review` |

## 練習問題

- **印刷依頼を役割別に整理する**（`prob.info1.programming.computer.systems.001.v1`）: C1.O1
- **命令とデータの流れをたどる**（`prob.info1.programming.computer.systems.002.v1`）: C1.O2
- **表現範囲と資源の限界を説明する**（`prob.info1.programming.computer.systems.003.v1`）: C1.O3
- **印刷システムの処理限界を分析する**（`prob.info1.programming.computer.systems.004.v1`）: C1.O1〜O3

## レビュー上の注意

このガイドと学習者用本文はドラフトです。機械検査は、人間による教科内容、年齢適合性、アクセシビリティ、出典・著作権、教育課程との対応の確認を代替しません。承認済み、公開済み、公開可能、安定版、または最終的に教育課程へ整合した教材として扱いません。
