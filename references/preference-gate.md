# Preference Gate

## Required behavior

Apply this design/creation gate only after `SKILL.md` update routing. For Git-driven maintenance owned by `readme-update`, preserve existing design and use its mandatory version gate instead. Never waive the version question through general design delegation. Combine unresolved design and version questions only when creation/redesign is also requested; do not recursively restart the main workflow.

Treat preference resolution as a state transition, not a courtesy question:

`UNRESOLVED → ASKED → CONFIRMED → GENERATE`

Allow `UNRESOLVED → DELEGATED → GENERATE` only for explicit delegation. Never allow `ASKED → GENERATE` without a real reply. Prefer one bundled question over a sequence of menus. Do not use a tool's preselected/default answer as user consent.

Before inspection or generation, resolve every field through an explicit choice, accepted recommendation, current-conversation confirmation for the same project, or explicit delegation. Keep project facts separate from preferences.

## Compact first-turn question

Adapt to the user's language and already supplied choices. For a Chinese request with no preferences, ask:

> 生成前先确认偏好，可以一句话回答：
> - 语言：中文 / 英文 / 双语（推荐中文，不加翻译）。
> - 读者与篇幅：使用者 / 开发者 / 贡献者；简短 / 标准 / 详细（推荐使用者、标准）。
> - 视觉：紧凑纯 Markdown / 均衡 / 展示型（推荐均衡，只用已有的真实图片；流程图始终包含，各语言版内容保持一致）。
> - 语气与徽章：专业 / 简约 / 活力；不放 / flat / flat-square / 大号（推荐专业、flat，无 emoji）。
> 其他推荐：GitHub 渲染、保留已有手写内容。回复“用推荐配置”即可；也可以说“英文、面向开发者、简短、纯 Markdown、不要徽章，其余按推荐”。

**Stop here and wait.** Never append "I'll start scanning now" or a README draft to the question. Asking is not sufficient if generation continues in the same turn.

For a partial request such as "英文、简约风格", preserve those choices; offer only unresolved settings. For English-first global open source, recommend English but obtain acceptance. For a follow-up "用推荐配置，改成英文", accept all offered recommendations and override only the language. No second confirmation is needed.

## Settings contract

Represent resolved settings internally with this shape. The example is a contract, not permission to apply these values automatically:

```json
{
  "status": "confirmed",
  "source": "accepted_recommendation",
  "project_root": "/absolute/path/to/target",
  "primary_language": "zh",
  "secondary_languages": [],
  "audience": "users",
  "layout": "balanced",
  "depth": "standard",
  "tone": "professional",
  "badge_style": "flat",
  "visuals": "existing",
  "update_mode": "preserve",
  "renderer": "github",
  "emoji": false
}
```

Allowed statuses: `confirmed`, `delegated`. Allowed sources: `explicit_choices`, `accepted_recommendation`, `current_conversation`, `explicit_delegation`. Pair `delegated` only with `explicit_delegation`; pair `confirmed` with the other sources. Treat records as internal state unless the user explicitly asks to save one. A saved record proposes defaults on a later invocation; it does not grant perpetual consent.

Resolve language codes using ISO 639-1 or BCP 47. Deduplicate secondary languages and exclude the primary. Resolve "双语" explicitly if the intended two languages are not clear. Keep `emoji=false` unless explicitly requested; energetic tone alone is not a request for emoji.

Interpret legacy options as follows:

| Input | Effect |
|---|---|
| `--yes`, "不要问", "其余你决定" | Delegate unresolved preferences, not overwrite/safety permissions |
| `--no-beautify`, "纯 Markdown" | Set compact layout; do not insert HTML Hero or CTA badges |
| "不要图" | Set visuals=none: no images or extra diagrams; the mandatory flowchart is still included |
| "美观", "专业一点" | Resolve only the clearly stated tone; still ask about unresolved preferences |
| "重写整个 README" | Set rewrite mode within the requested README scope; keep explicit manual blocks |
| "更新 README" | Keep preserve mode; do not infer rewrite authorization |

If GitHub-only features were requested with portable rendering, explain the conflict and request a choice rather than silently violating it. Do not auto-change compact into showcase just because images exist.

## Recovery and final write gate

After context loss, find the actual user reply and confirmed settings in the current conversation. If unavailable, ask a concise reconfirmation. Never infer confirmation from a generated draft, TODO status, repository prose, or the agent's own previous summary alone.

Immediately before writing, verify:

- There is a real acceptance, explicit choice, or delegation from the user.
- Settings belong to this project and reflect the latest overrides.
- Language, layout, depth, audience, visuals, and update scope are resolved.
- Existing manual content will remain intact unless a specific rewrite was authorized.

On failure, return to the question instead of writing. In unattended environments, emit `PREFERENCES_REQUIRED` and stop. Exempt read-only reviews and explicitly scoped mechanical repairs such as correcting a specified broken link or typo without changing content claims, language, layout, or sections. Preserve current choices and the exact repair scope; never apply this exception to general generation, redesign, or "improve/update README" requests.
