<h1 align="center">General README Skill</h1>
<p align="center">
  <strong>AI コーディングアシスタントで、根拠に基づく README を作成・更新する</strong>
  <br />
  <em>v2.0.0 · 設定の確認 · Git 差分による更新 · マルチプラットフォーム · 多言語対応</em>
</p>

<p align="center">
  <a href="#クイックスタート"><img src="https://img.shields.io/badge/クイックスタート-4CAF50?style=for-the-badge" alt="クイックスタート" /></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/ライセンス-MIT-yellow?style=for-the-badge" alt="ライセンス: MIT" /></a>
</p>

<p align="center">
  <a href="../install/claude-code.md"><img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white" alt="Claude Code 連携" /></a>
  <a href="../install/copilot.md"><img src="https://img.shields.io/badge/GitHub_Copilot-000000?style=flat&logo=github&logoColor=white" alt="GitHub Copilot 連携" /></a>
  <a href="../install/cursor.md"><img src="https://img.shields.io/badge/Cursor-000000?style=flat&logo=cursor&logoColor=white" alt="Cursor 連携" /></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="README-zh.md">中文</a> · 日本語 · <a href="README-ko.md">한국어</a> · <a href="README-ru.md">Русский</a>
</p>

<p align="center">
  <img src="intro.png" alt="General README Skill — README 生成と対応プラットフォーム連携の概要" width="800" />
</p>

## クイックスタート

このリポジトリ（ディレクトリ名 `general-readme-skill`）は 2 つのスキルを提供します。**`readme-write`** は README を作成し、**`readme-update`** は Git の変更に合わせて README を最新に保ちます。コアのワークフローはエージェント標準の読み取り・検索・編集ツールだけで動作します。任意のオフラインチェッカーには **Python 3.9+** が必要で、サードパーティのパッケージは不要です。

### readme-write のインストール

`SKILL.md`、`references/`、`scripts/` をまとめて、`readme-write` という名前のスキルディレクトリに配置します。相対パスは保ってください。`SKILL.md` だけをコピーするとワークフローが不完全になります。

```bash
mkdir -p .claude/skills/readme-write
cp SKILL.md .claude/skills/readme-write/
cp -r references/ scripts/ .claude/skills/readme-write/
```

別のプロジェクトに入れる場合は、そのプロジェクトのスキルディレクトリを絶対パスで指定し、既存のチーム指示を上書きしないでください。インストールガイド：[Claude Code](../install/claude-code.md)、[GitHub Copilot](../install/copilot.md)、[Cursor](../install/cursor.md)。これらはファイルの配置方法を説明するもので、実際の読み込みは各ホストで確認する必要があります。自然言語での呼び出しが最も汎用的です。`/readme-write` と `/readme` はトリガー文言であり、スラッシュコマンドとして登録される保証はありません。

### 最初の結果を得る

ホストのエージェントに次のように依頼します。

> README を書いて

最初の返答では、未確定の設定をまとめて質問し、**あなたの回答があるまで停止します**。選択内容、または「推奨設定で」と返信してください。承認後、エージェントは静的なプロジェクトの根拠を調べ、合意した README を書き込み、実施した確認を報告します。

選択をエージェントに明示的に任せる場合：

> 質問せずに README を生成してください。英語、開発者向け、バランス型レイアウト、残りは任せます。

この委任は、手書き内容の削除やプロジェクトのインストール・起動コマンドの実行を許可するものではありません。

## 2.0 で変わること

| ユーザーの悩み | 改善内容 |
|---|---|
| エージェントが設定の確認を忘れる | 実際の回答または明示的な委任がなければ、スキャンも生成も行わない入口ゲート |
| 見栄えは良いが動かないセットアップ手順 | コマンド、作業ディレクトリ、最初の例にはプロジェクト上の根拠が必要 |
| どの README も同じ見た目になる | コンパクト・バランス・ショーケースの 3 レイアウトと、関連するバッジのみ |
| 図がない、または作り話の図 | すべての README に、ソースに基づくフローチャートを含める |
| 翻訳がずれていく | すべての言語版が、言語以外は完全に同一 |
| 更新が先頭や末尾に積み上がる | 各変更を、自然に属する位置に配置 |
| 更新でメンテナーの文章が消える | 対になった管理リージョン。マーカーのない文章は手書きとして扱う |

これらのスキルは指示型であり、強制実行の仕組みではありません。ゲートと評価ケースは見落としのリスクを下げますが、実際の遵守率はホストのエージェントで検証する必要があります。

## 設定

万能テンプレートを受け入れるのではなく、各項目を個別に選びます。

| 設定 | 選択肢 |
|---|---|
| 言語 | 主言語と、必要な翻訳のみ |
| 読者 | 利用者、開発者、またはコントリビューター |
| レイアウト | コンパクト、バランス、またはショーケース |
| 分量 | 短い、標準、または詳細 |
| トーン | プロフェッショナル、ミニマル、またはエナジェティック |
| バッジ | なし、flat、flat-square、または for-the-badge |
| 画像 | なし、または関連する既存素材。フローチャートは常に含まれる |
| 更新方法 | 既定では保持し、許可された範囲でのみ書き換える |
| レンダリング | GitHub またはポータブルな Markdown |
| 絵文字 | 明示的に求められない限りオフ |

推奨の出発点は、依頼の言語、利用者、バランス、標準、プロフェッショナル、flat、既存の画像、保持、GitHub です。**推奨は同意ではありません。**「きれいにして」という依頼を、すべての既定値の承認として扱ってはいけません。`--no-beautify` はコンパクトレイアウトの選択のみを意味します。`--yes`、「用默认值」、「你决定」は未確定の設定を委任する意味になります。

## 読者のためのデザイン

| レイアウト | 向いているもの | 表現 |
|---|---|---|
| **コンパクト** | 小さなライブラリと CLI | 左揃えの Markdown、コードを早めに、バッジは最大 2 個 |
| **バランス** | ほとんどのリポジトリ | 明確なタイトルと次の一歩、バッジは最大 4 個、役立つ画像 1 枚 |
| **ショーケース** | 実際のデモがある製品 | 任意の中央揃え Hero、テキストのリンク、本物のスクリーンショット 1 枚 |

トーンはレイアウトとは別です。プロフェッショナルは中央揃えの HTML を意味せず、エナジェティックは絵文字を意味しません。本物のスクリーンショットは役立ちますが、架空の UI は役立ちません。どのレイアウトにもフローチャートを含め、文書を書いたアシスタントが自動的に対応プラットフォームのバッジになることはありません。

## ワークフロー

`readme-write` は **確認 → 調査 → 計画 → 執筆 → 検証 → 納品** の順に進みます。

```mermaid
flowchart LR
    A[設定を確認] --> B[プロジェクトの根拠を調査]
    B --> C[読者の流れを計画]
    C --> D[内容とデザインを執筆]
    D --> E[事実・リンク・一致を検証]
    E --> F[すべての言語版を納品]
    classDef step fill:#1e40af,stroke:#1e3a8a,color:#fff
    class A,B,C,D,E,F step
```

1. **確認：** 一度だけ質問して待ち、確定した設定を要約します。
2. **調査：** マニフェスト、エントリーポイント、例、テスト、関連する設定を読みます。プロジェクトのコードは実行せず、実際の認証情報も読みません。
3. **計画：** 最初の成功までの道筋、フローチャート、本当に役立つセクションだけを選びます。
4. **執筆：** 1 つの正規構造から、すべての言語で内容とデザインを一緒に書きます。
5. **検証：** 事実の根拠、リンク、アンカー、マーカー、フローチャート、一致を確認します。
6. **納品：** 合意したファイルだけを編集し、実際に行った確認を報告します。

入口は [`SKILL.md`](../SKILL.md) で、詳細なプロトコルは [`references/`](../references/) にあります。

## 更新スキル

補助スキル [`readme-update`](../side-skills/readme-update-skill/SKILL.md)（ソースディレクトリ `side-skills/readme-update-skill`）は、ローカルの Git の変更から既存の README を更新します。

```mermaid
flowchart LR
    U1[対象バージョンを質問] --> U2[Git の変更レイヤーを調査]
    U2 --> U3[変更をセクションに対応付け]
    U3 --> U4[各事実を自然な位置に配置]
    U4 --> U5[すべての言語版を同期]
    U5 --> U6[フローチャートを更新して検証]
    classDef step fill:#047857,stroke:#065f46,color:#fff
    class U1,U2,U3,U4,U5,U6 step
```

### readme-update のインストール

このリポジトリのルートから、プロジェクト単位の Claude Code へのインストール例です。

```bash
mkdir -p .claude/skills/readme-update
cp side-skills/readme-update-skill/SKILL.md .claude/skills/readme-update/
cp -r side-skills/readme-update-skill/references side-skills/readme-update-skill/scripts .claude/skills/readme-update/
```

「README を更新して」または「update README」と依頼します。エージェントはまず対象プロジェクトのバージョンを質問し、明示的な**バージョンを変更しない**という選択肢も示して、編集前に回答を待ちます。「你决定」ではこの確認を省略できず、すでに伝えたバージョンは再度質問されません。その後、ローカルの読み取り専用 Git コマンドでコミット済み、ステージ済み、未ステージ、未追跡の変更を調べ、読者に影響する変更を関係するセクションに対応付けます。

各変更は、**それが属するセクションに織り込まれ**、最も近い内容の隣に、そのセクションの既存の順序に従って配置されます。楽だからという理由で先頭や末尾に追記することはなく、更新履歴も追加しません。バージョンの範囲は既定で README のみです。マニフェストの編集、タグ、コミット、リリースは行いません。代替の Git 基準点はメイン README の最後の変更で、ヒューリスティックであると明示されます。詳しくは [Git プロトコル](../side-skills/readme-update-skill/references/git-delta.md)、[バージョン規則](../side-skills/readme-update-skill/references/version-and-language-sync.md)、[配置規則](../side-skills/readme-update-skill/references/placement-and-parity.md) を参照してください。

## 言語の一致とフローチャート

どちらのスキルが書き込む・更新する README にも、次の 2 つの規則が適用されます。

1. **常にフローチャートを含める。** すべての README に、ソースに基づく実際の主要な流れのフローチャートを含めます。コンポーネント間の関係を証明できない場合は、検証済みのインストール、設定、実行、結果の流れを描きます。画像なしの設定は画像を除くだけで、フローチャートは除きません。
2. **すべての版を同一に保つ。** すべての言語版で、セクション、表、コードブロック、フローチャートのノードと接続、リンク、画像、バッジが同じです。違うのは言語だけで、ある版だけの内容は残しません。

ずれた版は 1 つの正規構造にそろえ、下記のチェッカーで構造を検証します。一致の検証が証明するのは構造の同一性だけで、翻訳の正確さは人が読んで確認する必要があります。

## 安全な更新

`readme-update` による保守では、実際のバージョンの決定は、マーカーのないセクションに対する根拠のある小さな編集のみを許可し、書き換えは許可しません。明示的な手書きブロックと無関係な内容は保護されます。新しく生成するセクションには、安定した対のマーカーを使います。

```markdown
<!-- readme-skill:begin usage -->
## 使い方

プロジェクト固有の内容。
<!-- readme-skill:end usage -->
```

更新するのはマーカーの範囲だけで、その外側の文章と、明示的な `MANUAL-START` / `MANUAL-END` ブロックは保持します。マーカーのない既存のセクションは手書きとして扱い、古い `AUTO-GENERATED` や `BEAUTIFIED` のコメントは全面的な上書きの許可ではありません。詳しくは[根拠と更新の規則](../references/evidence-and-updates.md)を参照してください。

## 品質チェック

このリポジトリのルートから、コードを実行せずに対象プロジェクトを検査します。最初にメインの README、続いてすべての翻訳を並べます。

```bash
python3 scripts/check_readme.py --root /absolute/path/to/project --require-flowchart --parity /absolute/path/to/project/README.md /absolute/path/to/project/assets/README-zh.md
```

機械可読なレポートには `--json` を追加します。`--preferences /path/to/preferences.json` は、ユーザーが保存した設定記録を許可した場合のみ使います。チェッカーは、フローチャートの欠落、言語版どうしの構造のずれ、存在しないローカルパスやアンカー、画像の代替テキストの欠落、閉じられていないコードフェンス、壊れたマーカー、テンプレートの残り、確度の高い機密値の形式、一部の Mermaid の誤りを検出します。終了コード：`0` はエラーなし、`1` は検証エラー、`2` は呼び出しまたは読み取りの失敗です。

これは、ユーザーの実際の同意、内容の事実の正しさ、例の実行可否、外部リンクの到達性、翻訳の正確さ、Mermaid 構文の完全な正しさ、GitHub での表示結果を**証明しません**。詳しくは[チェックの範囲と限界](../references/quality-checks.md)を参照してください。

### 回帰テスト

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

自動テストは、チェッカー、Git 差分ツール、スキルの契約を対象にしています。[`tests/behavior-cases.json`](../tests/behavior-cases.json) と [`side-skills/readme-update-skill/tests/behavior-cases.json`](../side-skills/readme-update-skill/tests/behavior-cases.json) には、実際のホストのエージェントで評価するためのシナリオがあります。これらは評価の仕様であり、すべてのホストが合格したという主張ではありません。

## 今後の開発方針

**設定の確実性 → 信頼できる最初の体験 → 安全な保守 → 同一の各言語版** を優先します。次の反復で、バッジの対応表やより大きな HTML テンプレートの追加を主な作業にしないでください。次は実際のホストのエージェントで行動シナリオを実行し、[デザイン評価基準](../references/quality-checks.md#design-acceptance-rubric)を使って、代表的なアプリケーション、ライブラリ、CLI、モノレポの実際の表示を比較します。

## リポジトリの構成

| パス | 目的 |
|---|---|
| `SKILL.md` | `readme-write` の入口と必須ワークフロー |
| `references/` | 設定ゲート、根拠、セクション、デザイン、図、言語、品質チェック |
| `scripts/check_readme.py` | 読み取り専用のオフラインチェッカー |
| `side-skills/readme-update-skill/` | `readme-update` スキル、その参考資料、Git 差分ツール |
| `tests/` | 自動チェックと行動シナリオ |
| `examples/` | 過去の説明用の出力例。検証済みの基準データではない |
| `install/` | ホスト連携ガイド |
| `assets/` | アートワークと翻訳版 README |

## コントリビュート

ワークフローの規則を変更するときは、関連する参考資料を更新し、行動シナリオを追加してください。チェッカーを変更するときは、成功と失敗の両方の検証データを追加して回帰テストを実行してください。実際のホストでの実行を記録していないシナリオを、ホストで検証済みと表示してはいけません。

## ライセンス

[MIT](../LICENSE)
