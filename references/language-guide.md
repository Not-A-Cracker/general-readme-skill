# Language Guide

Use the language preferences confirmed through the entry gate. Never apply English automatically or ask again after generation. Treat requested translations as a coordinated set of documents.

## Naming and placement

Write the primary language to `README.md`, regardless of which language it is. Write requested secondary languages to `README-{code}.md` using ISO 639-1 / BCP 47 codes, for example `README-en.md`, `README-zh.md`, `README-zh-TW.md`, `README-ja.md`, `README-ko.md`, `README-fr.md`, `README-es.md`, `README-pt-BR.md`.

Keep existing translation paths and spelling when updating a repository. Do not move nested translations or rename `pt-br` solely to normalize casing. Deduplicate languages and omit the primary from the secondary list. Generate only requested languages; do not delete existing unrequested translations.

## Switcher

Omit the switcher for a single-language document unless other existing translations need navigation. Mark the current language as plain text. List the primary first, followed by requested/existing languages in a consistent order. Link only files that exist or will be created in the agreed output.

Use plain Markdown for compact, balanced, or portable output:

```markdown
English · [中文](README-zh.md)
```

For showcase on GitHub, optionally use simple HTML:

```html
<p align="center">English · <a href="README-zh.md">中文</a></p>
```

For nested Chinese translations linking to a root English README, calculate paths from the translation directory:

```markdown
[English](../README.md) · 中文

[MIT](../LICENSE)
```

Do not reuse root-relative image/license URLs blindly. Use the current file's parent as the base for images, docs, source paths and translations.

## Translation rules

- Keep equivalent facts, section order, code examples and managed-region IDs across translated generated sections. Do not reorder or translate preserved manual content without permission.
- Translate headings and prose naturally; do not translate commands, imports, filenames, options, variables, route paths or executable string literals.
- Keep community-standard technical terms where appropriate. Translate descriptive alt text when useful.
- Recalculate local heading fragments after translation. `#quick-start` does not target `## 快速开始`; use its actual fragment or a supported explicit anchor in GitHub-only layouts.
- For portable mode, prefer normal Markdown headings and generated fragment links over explicit HTML anchors.
- Validate each file separately and compare managed-section ID sets across the generated translation set.
- Avoid claiming translation quality was reviewed by native speakers unless it actually was.

## Common headings

| English | Chinese | Japanese | Korean | Spanish |
|---|---|---|---|---|
| Features | 功能特性 | 機能 | 기능 | Características |
| Quick Start | 快速开始 | クイックスタート | 빠른 시작 | Inicio rápido |
| Installation | 安装 | インストール | 설치 | Instalación |
| Usage | 使用方法 | 使い方 | 사용법 | Uso |
| Configuration | 配置 | 設定 | 설정 | Configuración |
| API | API | API | API | API |
| Architecture | 架构 | アーキテクチャ | 아키텍처 | Arquitectura |
| Contributing | 贡献 | コントリビュート | 기여 | Contribuir |
| License | 许可证 | ライセンス | 라이선스 | Licencia |
