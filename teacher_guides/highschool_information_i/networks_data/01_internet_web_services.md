# 教師用ガイド: インターネット、Web、情報サービス

## レッスンのねらい

架空の図書検索URLを使い、DNSの問い合わせ・応答とWebサービスへの接続・要求・応答を二つのまとまりとして構成します。
どちらのやり取りにもローカルネットワーク、ルーター、IP経路制御、トランスポートが働くことを示し、DNSが通信経路を飛び越える誤解を防ぎます。
障害例では原因当てをさせず、観察から成功済み、候補、未確認を分け、次の安全な確認を選ばせます。

## 授業時間（必修50分×2時限）

本時は**2時限とも必修**です。第1時でURLの分解と正常経路、第2時で503の観察記録を使った障害局所化と別場面への転移を行います。実在サイトへの接続や診断コマンドの実行は必要ありません。

## 教材・準備

- 学習者用本文。図を提示する場合は `d2-web-service-path.svg`
- 二つの台紙: DNSのやり取り、Webサービスのやり取り
- 両方の台紙に置くカード2組: クライアントのアプリケーション、トランスポート、IP、ローカルネットワーク（スイッチなど）とルーター
- DNS用カード: DNS問い合わせ、DNS応答、DNSサーバー
- Webサービス用カード: 接続とTLS、HTTP要求、サービス内処理、HTTP応答、Webサービス
- URL分解カード: スキーム、ホスト名、パス、クエリ
- 観察A〜Eのカードと、「成功済み、候補、未確認、次の確認」の空欄表
- 図を使わない学習者向けに、番号付き経路表と要求・応答の段階表

授業前に `.test` と `192.0.2.24` が教材用であることを確認します。証明書警告を再現する実習、実在ネットワークへの調査、個人の閲覧履歴の収集は行いません。

## 前提確認と分岐

D1のクライアント、サーバー、LAN、ルーター、IPアドレスを確認します。
ローカルネットワークとインターネットを同じ範囲として描く学習者には、教室内の区間と校外へ出る境目を別枠にし、境目へルーターを置かせます。
サーバーを「大きなコンピュータ」とだけ答える場合は、機器の大きさではなく「要求へ応答する側」という関係へ戻します。

## 学習者用本文との対応

1. インターネット、Web、情報サービスを区別する。（D2.O1）
2. URIとURLの役割を限定して区別し、DNSが扱うホスト名とHTTP要求のパス・クエリを分ける。（D2.O1）
3. ローカルネットワークからWebサービスまでを役割カードで追う。（D2.O2）
4. DNSの通信とWebサービスへの通信を分け、両方をD1の通信経路へ入れた段階表にする。（D2.O2）
5. URLのホスト名と証明書のサービス名を照合する役割を説明し、暗号の詳細はD3へ分ける。（D2.O2）
6. 観察A〜Eから503障害の候補を絞り、サービス利用への影響を根拠付きで説明する。（D2.O3）
7. 災害情報確認サービスへ独立して転移する。（D2.O1〜O3）

## 50分授業の到達点と判断

| 時限 | 学習者の到達点 | 50分の区切り | 続行条件 |
| --- | --- | --- | --- |
| 第1時 | URI・URLの役割を分け、DNS通信とWeb通信をそれぞれD1の通信経路へ入れて説明する。 | 二つの通信と、URLから作る参照名と証明書の識別名を照合する役割を一文ずつ書く。 | DNSの問い合わせと応答、HTTP要求と応答、共通する通信経路、URLのホスト名と証明書識別名を照合する役割が該当欄に示されていれば第2時へ進み、不足時は該当する経路カードを並べ直す。 |
| 第2時 | 観察から成功済み、候補、未確認、次の安全な確認、利用者への影響を分け、別の情報サービスへ転移する。 | 到達チェックで続行、再学習、支援要請を成果物の具体的な記述に基づいて選ぶ。 | 観察と成功済み・候補・未確認・影響が対応すれば次へ進み、不足時は該当する観察へ戻る。 |

## 詳細進行

### 第1時: URL、経路、要求と応答

| 時間 | 活動 | 期待する学習者の反応 | 教師のフィードバック |
| --- | --- | --- | --- |
| 0〜5分 | 大きな問いと準備チェック | LAN、ルーター、サーバーを関係として説明する | 装置名だけなら「誰から何を受け、どこへ渡すか」を尋ねる |
| 5〜12分 | インターネット・Web・サービスの分類 | 接続基盤、Webの仕組み、目的を満たす全体へ分ける | 画面だけをサービスとしたら、データ更新と障害対応を加える |
| 12〜20分 | URI・URLの役割を確認し、URLを四部分へ分解 | URIは識別、URLはアクセス方法・場所の手掛かりも示すと限定し、ホスト名をDNS、パスとクエリをHTTP要求へ対応付ける | URIがあれば取得できるとしたら、識別とアクセス成功を分ける |
| 20〜34分 | 二つの経路図と段階表を読む | DNS通信とWeb通信の両方へトランスポート、IP、ローカル区間とルーターを入れる | DNSを経路の外へ置いたら、問い合わせと応答もD1の通信だと補う |
| 34〜44分 | 二つの通信をカードで入れ子に構成 | DNS応答で得たIPを使い、Webサービスへの別の通信を始める | 同じ役割カードを二組使い、DNSだけが近道になっていないか確認する |
| 44〜48分 | TLSとHTTP要求・応答を説明 | URLのホスト名から作る参照名と証明書の識別名を照合し、ほかの認証確認はD3へ残す | IPやパスと照合したら元のURLのホスト名へ戻し、名前照合だけで認証完了とはしない |
| 48〜50分 | 出口確認 | 二つの通信と証明書名照合を一文ずつ書く | 未達項目を第2時冒頭の再学習へ振り分ける |

### 第2時: 観察から障害箇所を絞る

| 時間 | 活動 | 期待する学習者の反応 | 教師のフィードバック |
| --- | --- | --- | --- |
| 0〜5分 | 経路の再生または補習 | 名前解決とWeb要求を別のまとまりにし、両方をD1の通信経路へ入れる | 層の名称より、入力と出力を先に確認する |
| 5〜12分 | 観察A〜Eを順に分析 | 成功済みを一つずつ増やし、候補をサービス側へ狭める | 「正常」と一般化したら、「今回のどの観察についてか」と限定させる |
| 12〜17分 | 503の誤診を対比・修正 | DNS変更の根拠がなく、応答した構成要素と内部原因は未確定と説明する | オリジンサーバーと中継者を候補に残し、観察と主張の対応を評価する |
| 17〜25分 | 別の観察セットを、成功済み、候補、次の確認の三列で誘導診断する | 観察を一つずつ対応付け、次の記録を選ぶ | 候補が一つだけなら代替候補か未確認事項を求める |
| 25〜45分 | 災害情報サービスへ、URL、二つの通信、診断記録の三欄を使って独立転移する | URLを分解し、DNSとWebの通信を分け、古いデータの成功済み・候補・次の確認・影響を整理する | ネットワーク到達とデータ更新を混同せず、影響を可能性として根拠へ結び付ける |
| 45〜50分 | 到達チェック、必要な一度の修正、経路決定 | 続行、再学習、支援要請を根拠付きで選ぶ | 原因断定より、証拠の範囲とサービス利用への影響を守った説明を重視する |

各表の時間は合計50分です。第2時の独立転移は必修であり、早く終えた学習者の発展課題で置き換えません。

## 期待する反応とフィードバックの要点

| 観察される反応 | 判断 | 次の働きかけ |
| --- | --- | --- |
| DNSはホスト名、IPは経路、HTTPは要求の意味と分ける | 役割モデルを形成できている | 一つの観察がどの役割の成功を示すか問う |
| DNS問い合わせを端末とDNSの直結矢印で描く | DNSが下位の通信役割を飛び越えている | DNS行にもトランスポート、IP、ローカル区間とルーターのカードを置く |
| 「Wi-Fi→インターネット→Web」とだけ書く | 中間の役割が見えない | ローカル区間、ルーター、IP、トランスポート、HTTPのカードを補う |
| 証明書の名前をIPアドレスやパスと比べる | URLのホスト名の役割がつながっていない | URLのホスト名カードをDNS後も残し、参照名と提示された識別名の照合位置へ移す |
| 503から「データベース故障」と断定する | 応答状態と内部原因を混同 | 503から観察できたことと、まだ見えない内部処理を二列にする |
| トップページ成功から「サービス全体が正常」とする | サービス内の機能差を無視 | トップページ要求と検索要求を別行へ分ける |
| 候補を複数挙げ、次の記録を一つ選ぶ | 局所化の考え方ができている | その記録で候補がどう減るかまで説明させる |

## アクセシビリティの代替

図の直後にある二つの段階表を完全な代替として使います。DNSとWebサービスの両方について、メッセージ、トランスポート、IP、ローカルネットワークとルーターの包含関係と、要求・応答の方向を読み上げます。
色だけで要求と応答を区別せず、実線・破線、方向、番号、見出し、語句を併用します。
カード操作が難しい学習者は、番号を口頭で伝える、表へ番号を入力する、支援者に配置を指示する方法を選べます。
URLはスキーム、ホスト名、パス、クエリを別行でも提示し、記号を読み上げる必要がある場合は区切って確認します。

## 一人・静的教材での同等活動

通信環境や共同作業がない場合は、二つの段階表の「D1の役割モデルでの運ばれ方」列を隠し、DNSとWebサービスの各行へ同じ役割を補います。
次に観察A〜Eを一枚ずつ読み、各時点で「成功済み、候補、未確認」を書き換えます。
相互説明は、各判断の後ろに「観察○から」を付ける自己説明へ置き換えます。実在の通信確認は行いません。

## 形成的評価

- D2.O1: インターネット、Web、サービスを範囲と役割で区別し、URI・URLの限定した関係とURLの各部分を対応付ける。
- D2.O2: DNSとWebサービスの二つの通信を分け、どちらにもローカルネットワーク、ルーター、IP、トランスポートを置き、TLSの証明書名照合とHTTP要求の順序を示す。
- D2.O3: 観察から言える成功範囲を限定し、複数候補または未確認事項を残して次の確認を提案し、サービス利用への影響を可能性として説明する。

技術用語の数ではなく、「何を入力し、何を出力する役割か」「その観察がどこまでを示すか」で評価します。

## 停止点と次時限への条件

第1時は、DNSへの問い合わせとWebサービスへの要求を別のまとまりとして並べます。
両方がD1の通信経路を通ることと、URLから作る参照名を証明書で提示された識別名と照合することまでで停止します。
名前照合は必要な確認の一つです。証明書の信頼経路、署名、鍵交換、暗号方式など、認証と通信保護を成立させる残りの確認はD3へ送ります。

第2時へそのまま進む条件は、次の4点です。

1. ローカルネットワークとルーターを区別する。
2. DNSとWebサービスの両方をD1の通信経路へ置く。
3. DNSが扱うホスト名とHTTP要求のパスを区別する。
4. URLから作る参照名と証明書の識別名を照合し、それだけで認証全体が完了するとはしない。
1点未達なら第2時冒頭7分でカードを再構成します。
2点以上未達なら、通常の第2時経路をそのまま追加せず、次の短縮経路へ切り替えます。

| 時間 | 短縮活動 | 退出成果物 |
| --- | --- | --- |
| 0〜6分 | URLからホスト名とパスを抜き出す | ホスト名はDNS、パスはHTTP要求へ置いた二行表 |
| 6〜16分 | DNSの問い合わせ・応答、Web接続と要求、応答と表示の三段階を並べる | 各段階の入力、出力、通る通信基盤を示した短縮経路 |
| 16〜24分 | URLから作る参照名と証明書の識別名の照合を置く | 名前照合は認証確認の一部で、残りはD3とする一文 |
| 24〜36分 | 503の観察だけを分析する | 成功済み一つ、候補二つ、未確認一つ、次の安全な確認一つ |
| 36〜44分 | 図書検索が使えない場合の利用者への影響を限定して書く | 観察と可能性を区別した影響一つ |
| 44〜50分 | 続行、自己学習で再試行、支援要請を選ぶ | 成果物の具体的な行と次の行動 |

この短縮経路では、完全な段階1〜8、観察A〜Eすべての比較、災害情報サービスへの独立転移を自己学習へ送ります。
短縮経路の三段階と、503について成功済みの段階一つ、原因候補二つ、利用者への影響一つが対応していれば、補習状況を判断するための退出成果物として扱います。これはD2の習得証拠ではありません。
通常の進行または任意発展へ移る前に、保留した完全な経路比較と災害情報サービスへの独立転移を再提出し、本文の5項目すべてで到達を確認します。

第2時は、到達チェックで学習者が自分の学習経路を選んだところで停止します。実在環境で原因を確定することは到達条件にしません。

## 補習と任意発展

補習はURL、二つの通信、観察と候補の対応の不足箇所へ戻ります。任意発展は通常経路の習得証拠、または短縮経路後に保留分を再提出して5項目すべてを満たした習得証拠が成立した後に行います。

### 補習

- DNSとWeb検索の混同: ホスト名カードだけをDNSへ、パスとクエリをHTTP要求へ移す。
- DNSの経路飛ばし: DNSの台紙にもトランスポート、IP、ローカルネットワークとルーターを置き、問い合わせと応答の矢印を通す。
- 証明書名照合の混同: DNS後もURLのホスト名カードを残し、参照名と証明書の識別名を並べる。IPアドレスとパスは別の役割へ戻し、信頼経路など未学習の確認をD3欄へ残す。
- ルーターとサービスの混同: 「宛先IPを見る」「図書IDを見る」の二枚を分ける。
- 層の暗記で止まる: 各役割を「受け取るもの→返すもの」の形式で書く。
- 原因の断定: 観察文へ「この記録から分かるのは」を付け、未確認を最低一つ残す。

### 任意発展

- キャッシュが応答速度と最新性へ与える影響を、二つの評価指標で比較する。
- 同じホスト名のサービスが複数のサーバーで提供される場合、図のどこを詳しくする必要があるか提案する。
- TCPを例にした基本経路と、別のトランスポート方式を使う経路で、変わらない役割モデルを抽出する。方式の優劣や固定的な採用条件は断定しない。

## 想定される誤解

- インターネットとWebを同義とする。
- DNSがURL全体や検索結果を処理する。
- DNSの問い合わせと応答だけは、トランスポート、IP、ローカルネットワーク、ルーターを使わない。
- ルーターがURLのパスを読み、サービス内の資源を選ぶ。
- トランスポートとHTTPを同じ役割とする。
- サーバーが応答すれば、データや運用を含むサービス全体が正常である。
- HTTPSがページ内容や運営者の信頼性を保証する。
- 証明書の識別名を、元のURLから作る参照名ではなくDNS応答のIPアドレスやURLのパスと照合する。または、名前の照合だけで認証全体が完了すると考える。
- 503、証明書警告、検索結果なしを、すべて同じネットワーク障害とする。
- 一つの観察から内部原因を断定する。

## 安全性と範囲

`.test` の名前と `192.0.2.24` のアドレスは教材用です。実在サイトへの接続確認、証明書警告の回避、ネットワーク診断コマンドの実行は不要です。教師が追加実演を行う場合も、学校が許可した環境と公開可能な記録だけを使い、学習者の閲覧履歴や認証情報を収集しません。

## 合成データと出典上の注意

`.test`、文書用IPアドレス、URI、DNS、TCP、HTTP、TLS、サービス名照合に関する技術的な記述は、対応する一次資料の範囲を限定して確認する想定です。
特定方式が常に使われる、単一の観察で原因を確定できる、HTTPSが内容の真実性を保証する、という主張はしません。
図、二つのやり取りを含む九段階の経路、観察A〜E、障害局所化表、サービス評価活動は本教材のために作成したオリジナルです。
具体的な技術標準との対応は人間による出典レビューを必要とします。

## Claim-level evidence ledger

| Claim locator | Exact claim | Claim type | Evidence | Check | Scope note |
| --- | --- | --- | --- | --- | --- |
| `lesson.info1.networks.internet.web.v1` / “URI and URL roles” | A URI identifies a resource; this lesson uses URL for an HTTPS URI that also gives a primary access mechanism and location cues; having a URI does not guarantee access. | technical | `src.ietf.rfc3986.v1`, Sections 1.1.3, 1.2.2, and 3 | 2026-07-23, lesson-writer source review, supported | Classroom-bounded terminology; not a complete account of browser URL parsing or terminology history. |
| `lesson.info1.networks.internet.web.v1` / “Exchange 1” and `figure:d2-web-service-path.svg` | A DNS query and response are an application exchange; the lesson models both directions as carried by transport, IP, and local-network/router roles. | technical | `src.ietf.rfc9499.v1`, Sections 4 and 6; `src.ietf.rfc1122.v1`, Sections 1.1.2 and 1.1.3 | 2026-07-23, lesson-writer source review, supported | Simplified role model; resolver recursion, caching, DNSSEC, and transport selection are omitted. |
| `lesson.info1.networks.internet.web.v1` / “Exchange 2” | An HTTPS client establishes a secured connection and exchanges HTTP request and response messages with a server. | technical | `src.ietf.rfc9110.v1`, Sections 3.3, 3.4, 4.2.2, and 4.3.3 | 2026-07-23, lesson-writer source review, supported | The lesson uses a TCP-based base path while noting that Web traffic is not universally TCP-only. |
| `lesson.info1.networks.internet.web.v1` / `HTTPSでURLのホスト名をもう一度使う` | For this named HTTPS URL, the client constructs a reference identifier from the URL host and compares it with an identifier presented in the server certificate. Name matching is one required check; proper authentication also requires certificate-path validation. | technical | `src.ietf.rfc9525.v1`, Sections 1.2, 2, 6.1, and 6.3; `src.ietf.rfc9110.v1`, Section 4.3.4 | 2026-07-23, copyright-reviewer and lesson-writer source review, supported after scope correction | D2 teaches the role of name matching and explicitly defers certificate paths, signatures, key exchange, and algorithms to D3; it does not claim that name matching alone authenticates the service. |
| `lesson.info1.networks.internet.web.v1` / `HTTPSでURLのホスト名をもう一度使う` | TLS supports server authentication, confidentiality, and integrity for the channel; those properties do not establish the truth of page content or the conduct of an operator. | technical | `src.ietf.rfc9846.v1`, Section 1; `src.ietf.rfc9525.v1`, Sections 1 and 2 | 2026-07-23, lesson-writer source review, supported | Security goals are stated at role level only; cryptographic construction and certificate-path validation are deferred to D3. |
| `lesson.info1.networks.internet.web.v1` / `考え方を追う例: 「検索だけ使えない」を診断する` | A 503 response indicates temporary inability to handle a request, but the status alone does not identify the failing internal component. HTTP can include proxies and gateways, so the responding participant, origin application, upstream dependencies, and intermediaries remain candidates until additional records are checked. | technical | `src.ietf.rfc9110.v1`, Sections 3.7 and 15.6.4 | 2026-07-23, copyright-reviewer and lesson-writer source review, supported after scope correction | Synthetic diagnosis only. The lesson does not infer a database failure or prove that origin search logic ran from the 503 status alone. |
| `lesson.info1.networks.internet.web.v1` / synthetic URL note | `.test` is reserved for testing, and `192.0.2.0/24` is provided for documentation. | standard | `src.ietf.rfc2606.v1`, Section 2; `src.ietf.rfc5737.v1`, Section 3 | 2026-07-23, lesson-writer source review, supported | Synthetic classroom identifiers; no live reachability or certificate validity is implied. |
| `lesson.info1.networks.internet.web.v1` / router, IP, and transport role paragraphs | The lesson separates local-link/router forwarding and IP delivery from transport behavior; TCP is one bounded example of a reliable in-order byte stream rather than a property attributed to every transport protocol. | technical | `src.ietf.rfc1122.v1`, Sections 1.1.2 and 1.1.3; `src.ietf.rfc9293.v1`, Sections 1 and 3.1 | 2026-07-23, AI source review, `supported` | The path, device order, and classroom labels are simplified. The lesson does not teach routing-table algorithms, port administration, packet capture, or TCP implementation. |
| `lesson.info1.networks.internet.web.v1` / paragraph beginning `ただし、実際のWeb通信にはQUIC` | Web communication is not universally TCP-only because QUIC is a general-purpose transport protocol and QUIC packets can be carried in UDP datagrams. | technical | `src.ietf.rfc9000.v1`, Sections 1 and 1.2 | 2026-07-23, AI source review, `supported` | This row establishes only that QUIC is a transport alternative. It does not claim that a particular browser request used QUIC or teach QUIC security, performance, deployment, or version negotiation. |
| `lesson.info1.networks.internet.web.v1` / `情報サービスとして評価する` / cache paragraph and integrated assessment | Reusing a cached HTTP response can reduce latency and network use, while freshness and validation determine whether a stored response can be reused without contacting the origin. | technical | `src.ietf.rfc9111.v1`, Sections 1, 2, 4.2, and 4.3 | 2026-07-23, AI source review, `supported` | The fictional service cache duration, availability field, update policy, and user impact are project-authored. The lesson does not prescribe a universal cache duration or configuration. |
| `lesson.info1.networks.internet.web.v1` / `情報サービスとして評価する` | Effectiveness, availability, performance, accessibility, operability, and safety are a project-authored review frame for this fictional service. | artifact observation | The project-authored six-dimension worksheet and synthetic service observations in this lesson. | 2026-07-23, AI scope review, `supported` | The list is not asserted to be exhaustive and does not establish standards conformance, security assurance, accessibility conformance, or service quality. |

## Figure provenance

| Date | Asset | Provenance | Review state |
| --- | --- | --- | --- |
| 2026-07-23 | `site/assets/figures/d2-web-service-path.svg` | Project-original editable SVG created in-repository with AI-assisted drafting from D2's two-exchange role model; no imported or traced asset. SHA-256: `309d806c3945eccfbbe8cb27a6edc6824714f1ebe61b68c15702c03f2a62e283`. Labels and relationships are bounded by the claim-level ledger above. | `needs_human_review` for technical accuracy, pedagogy, accessibility, and copyright/source review. |

## 練習問題

- **インターネット、Web、URI・URL、サービスを区別する**（`prob.info1.networks.internet.web.001.v1`）: D2.O1
- **図書検索URLの経路をたどる**（`prob.info1.networks.internet.web.002.v1`）: D2.O2
- **観察から失敗した層を診断する**（`prob.info1.networks.internet.web.003.v1`）: D2.O3
- **サービスの性能と運用上の限界を評価する**（`prob.info1.networks.internet.web.004.v1`）: D2.O1〜O3

## レビュー上の注意

このガイドと学習者用本文はドラフトです。機械検査は、人間による技術内容、年齢適合性、アクセシビリティ、出典・著作権、安全性、教育課程との対応の確認を代替しません。承認済み、公開済み、公開可能、安定版、または最終的に教育課程へ整合した教材として扱いません。
