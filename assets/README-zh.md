<h1 align="center">General README Skill</h1>
<p align="center">
  <strong>使用 AI 编程助手生成和更新有项目依据的 README 文件</strong>
  <br />
  <em>v2.0.0 · 偏好确认 · Git 增量更新 · 多平台 · 多语言</em>
</p>

<p align="center">
  <a href="#快速开始"><img src="https://img.shields.io/badge/快速开始-4CAF50?style=for-the-badge" alt="快速开始" /></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/许可证-MIT-yellow?style=for-the-badge" alt="许可证：MIT" /></a>
</p>

<p align="center">
  <a href="../install/claude-code.md"><img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white" alt="Claude Code 集成" /></a>
  <a href="../install/copilot.md"><img src="https://img.shields.io/badge/GitHub_Copilot-000000?style=flat&logo=github&logoColor=white" alt="GitHub Copilot 集成" /></a>
  <a href="../install/cursor.md"><img src="https://img.shields.io/badge/Cursor-000000?style=flat&logo=cursor&logoColor=white" alt="Cursor 集成" /></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · 中文 · <a href="README-ja.md">日本語</a> · <a href="README-ko.md">한국어</a> · <a href="README-ru.md">Русский</a>
</p>

<p align="center">
  <img src="intro.png" alt="General README Skill — README 生成与平台集成概览" width="800" />
</p>

## 快速开始

本仓库（目录名 `general-readme-skill`）提供两个 skill：**`readme-write`** 负责创建 README，**`readme-update`** 负责根据 Git 变更保持 README 最新。核心流程只依赖 agent 原生的读取、搜索和编辑工具。可选的离线检查器需要 **Python 3.9+**，不需要第三方包。

### 安装 readme-write

将 `SKILL.md`、`references/` 和 `scripts/` 一起放进名为 `readme-write` 的 skill 目录，保持相对路径不变；只复制 `SKILL.md` 会让流程不完整。

```bash
mkdir -p .claude/skills/readme-write
cp SKILL.md .claude/skills/readme-write/
cp -r references/ scripts/ .claude/skills/readme-write/
```

安装到其他项目时，把目标改为该项目的绝对 skill 目录，并且不要覆盖已有团队指令。参考安装指南：[Claude Code](../install/claude-code.md)、[GitHub Copilot](../install/copilot.md)、[Cursor](../install/cursor.md)。这些指南说明文件放置方式，实际加载仍需在对应宿主中验证。自然语言调用最通用；`/readme-write` 和 `/readme` 是触发文本，不保证是已注册的斜杠命令。

### 得到第一个结果

向 agent 发送：

> 帮我写 README

第一轮会集中询问未确定的偏好，并**停止等待你的回答**。回复具体选择或“用推荐配置”后，agent 才扫描静态项目依据、写入约定的 README，并报告检查结果。

如果希望明确交给 agent 决定：

> 生成 README，不用问，英文，面向开发者，均衡布局，其余你决定。

这类授权不等于允许删除手写内容，也不等于允许运行项目的安装或启动命令。

## 2.0 解决什么问题

| 用户痛点 | 本次升级 |
|---|---|
| agent 忘记询问偏好 | 入口门槛：必须有真实回答或明确授权，才能扫描或生成 |
| 内容好看，安装说明却跑不通 | 命令、工作目录和首个示例必须有项目依据 |
| 所有 README 长得一样 | 紧凑、均衡、展示型三种布局，只放相关徽章 |
| 没有图，或者图是编造的 | 每份 README 都有源码依据的流程图 |
| 各语言版本越改越不一致 | 所有语言版本除语言外保持完全一致 |
| 更新堆在开头或结尾 | 每处变更放到它自然所属的位置 |
| 更新覆盖维护者的文字 | 成对的生成区域标记，未标记文字视为手写内容 |

这些 skill 是指令型的，不是强制执行引擎。门槛和评测场景能降低遗漏风险，但实际遵循率仍需要在宿主 agent 上验证。

## 偏好配置

各项独立选择，而不是接受万能模板：

| 偏好 | 可选项 |
|---|---|
| 语言 | 主语言，以及真正需要的翻译 |
| 读者 | 使用者、开发者或贡献者 |
| 布局 | 紧凑、均衡或展示型 |
| 篇幅 | 简短、标准或详细 |
| 语气 | 专业、简约或活力 |
| 徽章 | 不放、flat、flat-square 或 for-the-badge |
| 图片 | 不放，或已有的相关素材；流程图始终包含 |
| 更新方式 | 默认保护手写内容，仅在授权范围内重写 |
| 渲染目标 | GitHub 或可移植 Markdown |
| Emoji | 除非明确要求，否则关闭 |

推荐起点是：当前请求的语言、使用者、均衡、标准、专业、flat、已有图片、保留手写内容和 GitHub。**推荐不等于用户已经同意。**“帮我做得美观”不能被解释成默认配置授权。`--no-beautify` 只确定紧凑布局；`--yes`、“用默认值”或“你决定”才表示授权剩余偏好。

## 美观，但先服务读者

| 布局 | 适用情况 | 展示方式 |
|---|---|---|
| **紧凑** | 小型库和 CLI | 左对齐 Markdown，尽早给代码，最多 2 个徽章 |
| **均衡** | 大多数仓库 | 清晰的标题和下一步，最多 4 个徽章，一张有用的图片 |
| **展示型** | 有真实演示的产品 | 可选居中 Hero、文字导航、一张真实截图 |

语气与布局相互独立：专业不等于居中 HTML，活力不等于 emoji。真实截图有帮助，虚构界面没有。每种布局都包含流程图，而且生成文档所用的助手不会自动成为支持的平台徽章。

## 工作流程

`readme-write` 遵循 **确认 → 检查 → 规划 → 撰写 → 校验 → 交付**：

```mermaid
flowchart LR
    A[确认偏好] --> B[检查项目依据]
    B --> C[规划读者路径]
    C --> D[撰写内容与设计]
    D --> E[检查事实、链接和一致性]
    E --> F[交付所有语言版本]
    classDef step fill:#1e40af,stroke:#1e3a8a,color:#fff
    class A,B,C,D,E,F step
```

1. **确认：** 集中询问一次并等待，然后复述已确定的偏好。
2. **检查：** 读取清单、入口、示例、测试和相关配置；绝不运行项目代码或读取真实凭据。
3. **规划：** 选择首次成功路径、流程图和真正有用的章节。
4. **撰写：** 基于同一份规范结构，同时写出各语言版本的内容和设计。
5. **校验：** 核对事实依据、链接、锚点、标记、流程图和一致性。
6. **交付：** 只编辑约定的文件，并报告实际执行过的检查。

入口是 [`SKILL.md`](../SKILL.md)；详细协议位于 [`references/`](../references/)。

## 更新 Skill

配套的 [`readme-update`](../side-skills/readme-update-skill/SKILL.md) skill（源码目录 `side-skills/readme-update-skill`）根据本地 Git 变更更新已有 README：

```mermaid
flowchart LR
    U1[询问目标版本] --> U2[检查 Git 变更层]
    U2 --> U3[把变更映射到章节]
    U3 --> U4[把每条事实放到自然位置]
    U4 --> U5[同步所有语言版本]
    U5 --> U6[更新流程图并校验]
    classDef step fill:#047857,stroke:#065f46,color:#fff
    class U1,U2,U3,U4,U5,U6 step
```

### 安装 readme-update

在本仓库根目录，以项目级 Claude Code 安装为例：

```bash
mkdir -p .claude/skills/readme-update
cp side-skills/readme-update-skill/SKILL.md .claude/skills/readme-update/
cp -r side-skills/readme-update-skill/references side-skills/readme-update-skill/scripts .claude/skills/readme-update/
```

发送“更新 README”或“update README”。agent 会先询问目标项目版本，并提供明确的**版本不变**选项，等待回答后才修改；“你决定”不能跳过这一步，你已经说明的版本也不会重复询问。随后用本地只读 Git 命令检查已提交、已暂存、未暂存和未跟踪的变更，并把对读者有影响的变化映射到受影响的章节。

每处变更都会**融入它所属的章节**，放在最相近的内容旁边并遵循该章节的既有顺序。不会因为方便就追加到开头或结尾，也不会添加更新日志。版本范围默认只改 README：不改清单、不打标签、不提交、不发布。备用的 Git 基线是主 README 最近一次变更，并明确标为启发式线索。详见 [Git 协议](../side-skills/readme-update-skill/references/git-delta.md)、[版本规则](../side-skills/readme-update-skill/references/version-and-language-sync.md)和[位置规则](../side-skills/readme-update-skill/references/placement-and-parity.md)。

## 语言一致与流程图

两个 skill 写入或更新的每份 README 都遵守两条规则：

1. **始终有流程图。** 每份 README 都包含有源码依据的真实主流程流程图。无法证实组件关系时，画已验证的安装、配置、运行和结果流程。选择不放图片只会去掉图片，不会去掉流程图。
2. **各版本完全一致。** 每个语言版本的章节、表格、代码块、流程图节点和连线、链接、图片和徽章都相同。只有语言不同，不保留某个版本独有的内容。

已经分叉的版本会被统一到同一份规范结构，并用下面的检查器验证结构。一致性检查只能证明结构相同，翻译是否准确仍需要人工阅读。

## 安全更新

通过 `readme-update` 维护时，真实的版本决定只授权对未标记章节做窄范围、有依据的修改，而不是重写。显式手写区和无关内容继续受保护。新生成的章节使用稳定的成对标记：

```markdown
<!-- readme-skill:begin usage -->
## 使用方法

基于项目实际内容的说明。
<!-- readme-skill:end usage -->
```

只更新标记范围，保留范围外文字以及 `MANUAL-START` / `MANUAL-END` 手写区。已有未标记章节视为手写内容，旧的 `AUTO-GENERATED` 或 `BEAUTIFIED` 注释不是整篇覆盖授权。详见[证据与更新规则](../references/evidence-and-updates.md)。

## 质量检查

在本仓库根目录检查目标项目，不执行其代码。先列主 README，再列所有翻译：

```bash
python3 scripts/check_readme.py --root /absolute/path/to/project --require-flowchart --parity /absolute/path/to/project/README.md /absolute/path/to/project/assets/README-zh.md
```

加 `--json` 可输出机器可读报告；只有用户授权保存过偏好记录时才使用 `--preferences /path/to/preferences.json`。检查器能发现缺失的流程图、语言版本之间的结构偏差、缺失的本地路径和锚点、图片缺少替代文字、未闭合的代码围栏、损坏的标记、模板残留、高可信的敏感值格式以及部分 Mermaid 错误。退出码：`0` 无错误，`1` 校验错误，`2` 参数或读取失败。

它**不能证明**用户真实同意、内容事实正确、示例可运行、远端链接可访问、翻译准确、Mermaid 语法完全正确或 GitHub 渲染成功。详见[检查范围与限制](../references/quality-checks.md)。

### 回归验证

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

自动测试覆盖检查器、Git 增量工具和 skill 契约。[`tests/behavior-cases.json`](../tests/behavior-cases.json) 和 [`side-skills/readme-update-skill/tests/behavior-cases.json`](../side-skills/readme-update-skill/tests/behavior-cases.json) 提供用于真实宿主 agent 评测的场景。它们是评测规范，不代表所有宿主均已通过。

## 后续开发路线

优先推进 **偏好可靠性 → 可信首次使用 → 安全维护 → 各版本一致**，下一轮不要主要增加徽章映射或更复杂的 HTML 模板。接下来应在真实宿主上运行行为场景，再按[设计验收标准](../references/quality-checks.md#design-acceptance-rubric)比较代表性应用、库、CLI 和 monorepo 的实际渲染效果。

## 仓库导航

| 路径 | 用途 |
|---|---|
| `SKILL.md` | `readme-write` 入口与强制工作流 |
| `references/` | 偏好门槛、证据、章节、设计、图表、语言和质量检查 |
| `scripts/check_readme.py` | 只读离线检查器 |
| `side-skills/readme-update-skill/` | `readme-update` skill、其参考文档和 Git 增量工具 |
| `tests/` | 自动测试和行为场景 |
| `examples/` | 历史展示示例，不是已验证的标准样例 |
| `install/` | 宿主集成指南 |
| `assets/` | 宣传图和翻译版 README |

## 贡献

修改流程规则时，同步更新相关参考文档并补一个行为场景。修改检查器时，添加通过和失败的样例并运行回归套件。没有实际宿主运行记录，不要宣称某个场景已通过宿主验证。

## 许可证

[MIT](../LICENSE)
