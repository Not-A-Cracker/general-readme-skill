# General README Skill

让 AI 编程助手生成有源码依据、容易上手、视觉清晰的 README：先确认读者偏好，再写真实可用的说明，而不是堆模板和徽章。

![许可证：MIT](https://img.shields.io/badge/license-MIT-2563eb?style=flat)
![Skill 版本：2.0.0](https://img.shields.io/badge/skill-2.0.0-334155?style=flat)

[English](../README.md) · 中文

[快速开始](#快速开始) · [偏好配置](#偏好配置) · [质量检查](#质量检查)

## 快速开始

核心生成流程只依赖 agent 原生的读取、搜索和编辑工具，无需额外运行时、第三方 CLI 或网络服务。可选离线检查器需要 **Python 3.9+**，不需要第三方包。

### 完整安装

将 `SKILL.md`、`references/` 和 `scripts/` 一起放进宿主的 skill 目录，保持相对路径。只复制入口文件会缺少必要规则。

例如，在本仓库根目录安装到项目级 Claude Code 目录：

```bash
mkdir -p .claude/skills/general-readme
cp SKILL.md .claude/skills/general-readme/
cp -r references/ scripts/ .claude/skills/general-readme/
```

安装到另一个项目时，把目标改为那个项目的绝对 skill 目录。不要覆盖已有团队指令。

参考安装指南：[Claude Code](../install/claude-code.md)、[GitHub Copilot](../install/copilot.md)、[Cursor](../install/cursor.md)。这些指南说明文件放置方式，实际加载和工具可用性仍需在对应宿主验证。自然语言调用最通用；`/readme` 是触发文本，不代表每个宿主都注册了同名斜杠命令。

### 得到第一个结果

向 agent 发送：

> 帮我写 README

第一轮应集中询问未确定的偏好，并**停止等待你的回答**。回复具体选择或“用推荐配置”后，agent 才扫描静态项目文件、编辑约定的 README，并报告检查结果。

如果希望直接交给 agent 决定：

> 生成 README，不用问，英文，面向开发者，均衡布局，其余你决定。

这类授权只覆盖未确定的偏好，不等于允许删除手写内容或执行项目安装、启动命令。

## 2.0 解决什么问题

| 用户痛点 | 本次升级 |
|---|---|
| agent 忘记询问 preference | 入口门槛：真实确认或明确授权后才能扫描、生成 |
| 内容好看，快速开始却跑不通 | 命令、目录、前置条件和首次使用示例必须有项目依据 |
| 所有 README 都长得一样 | 紧凑、均衡、展示型布局，限制首屏徽章，图片和图表可选 |
| 更新覆盖维护者手写内容 | 成对生成区域标记，未标记内容视为手写，限定替换范围 |
| 小项目被塞入不必要的架构和 API | 按应用、库、CLI、monorepo、skill、文档项目选择读者路径 |
| 翻译版许可证、图片、锚点断链 | 每个文件独立计算相对路径和翻译后的标题锚点 |
| “生成成功”掩盖了未验证问题 | 离线检查，并区分静态检查、运行验证和实际渲染 |

这仍是一个指令型 skill，不是强制执行引擎。新门槛和回归案例降低遗漏风险，但实际遵循率需要在宿主 agent 上验证。

## 偏好配置

各项独立选择，不把“专业”自动等同于居中 HTML：

| 偏好 | 可选项 |
|---|---|
| 语言 | 主语言，以及真正需要的翻译 |
| 读者 | 使用者、开发者、贡献者 |
| 布局 | 紧凑、均衡、展示型 |
| 篇幅 | 简短、标准、详细 |
| 语气 | 专业、简约、活力 |
| 徽章 | 不放、flat、flat-square、for-the-badge |
| 视觉素材 | 不放、已有相关素材、有源码依据的图表 |
| 更新方式 | 默认保护手写内容，仅在授权范围重写 |
| 渲染目标 | GitHub、可移植 Markdown |
| Emoji | 除非明确要求，否则关闭 |

推荐起点：当前请求语言、使用者、均衡、标准、专业、flat、已有素材、保留手写内容、GitHub。**推荐不等于用户已经同意。**“帮我做得美观”不能被解释成默认配置授权。

一次回复即可：

> 英文，面向开发者，简短，纯 Markdown，不要徽章，不要图，其余按推荐。

`--no-beautify` 只确定紧凑布局；`--yes`、“用默认值”、“你决定”明确授权剩余偏好。同一项目的后续更新可以复用本会话真实确认的设置；跨会话或上下文丢失时，不应从已有 README 的样式推断用户同意。

## 美观，但先服务读者

| 布局 | 适用情况 | 展示方式 |
|---|---|---|
| **紧凑** | 小型库、CLI | 左对齐 Markdown，尽早给代码，最多 2 个徽章，无装饰性 Hero |
| **均衡** | 大多数仓库 | 清晰标题和下一步，最多 4 个徽章，可选一张有用的真实素材 |
| **展示型** | 有真实演示的产品 | 可选居中 Hero、文字导航、一张真实截图；正文保持 Markdown |

语气与布局独立：专业不等于居中，活力不等于 emoji；可移植模式保持纯 Markdown。

真实截图可以帮助理解产品，虚构 UI 不可以。架构图只有在能解释源码支持的关系时才加入，不要求每个项目都画图。不能把生成 README 所用的 AI 工具当成项目支持的平台。

## 工作流程

**确认 → 检查项目 → 规划 → 内容与设计合成 → 校验 → 交付**

1. **确认：** 集中询问并等待，收到回答后简要复述配置。
2. **检查项目：** 读取清单、入口、示例、测试和公开配置；不执行项目代码，不读取真实凭据。
3. **规划：** 选择首次成功路径与必要章节，识别安全更新边界。
4. **合成：** 内容和视觉同时生成，按需加载参考规则。
5. **校验：** 核对声明依据、链接、锚点、标记和偏好一致性。
6. **交付：** 只编辑约定文件，说明实际检查与未验证项。

入口：[`SKILL.md`](../SKILL.md)；具体协议：[`references/`](../references/)。

## 安全更新

新生成章节使用稳定的成对标记：

```markdown
<!-- readme-skill:begin usage -->
## 使用方法

基于项目实际内容的说明。
<!-- readme-skill:end usage -->
```

只更新标记范围，保留范围外文字以及 `MANUAL-START` / `MANUAL-END` 手写区。已有未标记章节视为手写内容，旧 `AUTO-GENERATED` 或 `BEAUTIFIED` 标记不是整篇覆盖授权。

遇到需要替换的未标记章节，确认具体范围，不直接重写整篇，也不追加重复章节。详见[证据与更新规则](../references/evidence-and-updates.md)。

## 质量检查

从本仓库根目录检查目标项目，不执行其代码：

```bash
python3 scripts/check_readme.py --root /项目绝对路径 /项目绝对路径/README.md
```

`--json` 输出机器可读报告。只有用户授权保存过偏好记录时才提供 `--preferences /路径/preferences.json`；默认不创建状态文件。

检查器覆盖本地路径与锚点、图片替代文字、代码围栏、生成/手写区域标记、已知模板残留、高可信敏感值格式、部分 Mermaid 错误以及偏好相关布局冲突；禁止链接越出项目根目录。退出码：`0` 无错误，`1` 校验错误，`2` 参数或读取失败，警告单独报告。

它**不能证明**用户真实同意、内容事实正确、示例能运行、远端链接可访问、Mermaid 完整语法正确或 GitHub 渲染成功。详见[检查范围与限制](../references/quality-checks.md)。

### 回归验证

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

自动测试覆盖检查器和 skill 契约。[`tests/behavior-cases.json`](../tests/behavior-cases.json) 提供 17 个实际宿主 agent 评测场景，包括裸调用、部分偏好、上下文丢失、monorepo 和手写保护。这些是评测规范，不代表所有宿主均已通过。

## 后续开发路线

优先推进 **偏好可靠性 → 可信首次使用 → 安全维护 → 自适应视觉设计**，而不是主要增加徽章映射或更复杂的 HTML。

下一步应在真实宿主上跑行为场景，再用代表性应用、库、CLI 和 monorepo 比较实际渲染效果。按[设计验收标准](../references/quality-checks.md#design-acceptance-rubric)评估清晰度、实用性、克制和可维护性，用实际结果替代审美承诺。

## 仓库导航

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 入口门槛与主工作流 |
| `references/preference-gate.md` | 提问、状态契约与恢复 |
| `references/evidence-and-updates.md` | 证据记录与安全更新 |
| `references/section-guidelines.md` | 各类项目的读者路径 |
| `references/beautification-rules.md` | 布局与视觉设计体系 |
| `references/quality-checks.md` | 校验边界和评测方法 |
| `references/badge-styles.md`、`references/badges.md` | 可选徽章规则和映射 |
| `references/diagram-templates.md`、`references/language-guide.md` | 可选图表与翻译 |
| `scripts/check_readme.py` | 只读离线检查器 |
| `tests/` | 自动测试和行为场景 |
| `examples/` | 历史展示示例，不是已验证源码的 golden fixture |
| `install/` | 宿主集成指南 |
| `assets/` | 已有宣传图和翻译文档 |

日文、韩文、俄文仍保留带历史提示的 1.x 指南；2.0 工作流以本页和英文主页为准。

## 贡献

修改流程时，同步相关参考规则并补行为场景；修改检查器时，添加正反测试并运行回归套件。没有实际宿主调用记录，不要宣称某场景通过了宿主验证。

## 许可证

[MIT](../LICENSE)
