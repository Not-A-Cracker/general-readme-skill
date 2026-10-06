<h1 align="center">General README Skill</h1>
<p align="center">
  <strong>AI 코딩 어시스턴트로 근거에 기반한 README를 작성하고 업데이트합니다</strong>
  <br />
  <em>v2.0.0 · 설정 확인 · Git 변경 기반 업데이트 · 멀티 플랫폼 · 다국어 지원</em>
</p>

<p align="center">
  <a href="#빠른-시작"><img src="https://img.shields.io/badge/빠른_시작-4CAF50?style=for-the-badge" alt="빠른 시작" /></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/라이선스-MIT-yellow?style=for-the-badge" alt="라이선스: MIT" /></a>
</p>

<p align="center">
  <a href="../install/claude-code.md"><img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white" alt="Claude Code 연동" /></a>
  <a href="../install/copilot.md"><img src="https://img.shields.io/badge/GitHub_Copilot-000000?style=flat&logo=github&logoColor=white" alt="GitHub Copilot 연동" /></a>
  <a href="../install/cursor.md"><img src="https://img.shields.io/badge/Cursor-000000?style=flat&logo=cursor&logoColor=white" alt="Cursor 연동" /></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="README-zh.md">中文</a> · <a href="README-ja.md">日本語</a> · 한국어 · <a href="README-ru.md">Русский</a>
</p>

<p align="center">
  <img src="intro.png" alt="General README Skill — README 생성과 지원 플랫폼 연동 개요" width="800" />
</p>

## 빠른 시작

이 저장소(디렉터리 이름 `general-readme-skill`)는 두 가지 스킬을 제공합니다. **`readme-write`**는 README를 작성하고, **`readme-update`**는 Git 변경 사항에 맞춰 README를 최신 상태로 유지합니다. 핵심 워크플로는 에이전트의 기본 읽기·검색·편집 도구만 사용합니다. 선택 사항인 오프라인 검사기에는 **Python 3.9+**가 필요하며 서드파티 패키지는 필요하지 않습니다.

### readme-write 설치

`SKILL.md`, `references/`, `scripts/`를 함께 `readme-write`라는 이름의 스킬 디렉터리에 복사하세요. 상대 경로는 그대로 유지해야 하며, `SKILL.md`만 복사하면 워크플로가 불완전해집니다.

```bash
mkdir -p .claude/skills/readme-write
cp SKILL.md .claude/skills/readme-write/
cp -r references/ scripts/ .claude/skills/readme-write/
```

다른 프로젝트에 설치할 때는 해당 프로젝트의 스킬 디렉터리를 절대 경로로 지정하고, 기존 팀 지침을 덮어쓰지 마세요. 연동 가이드: [Claude Code](../install/claude-code.md), [GitHub Copilot](../install/copilot.md), [Cursor](../install/cursor.md). 이 가이드는 파일 배치 방법을 설명하며, 실제 로딩은 설치된 호스트에서 확인해야 합니다. 자연어 호출이 가장 범용적입니다. `/readme-write`와 `/readme`는 트리거 문구이며 슬래시 명령으로 등록된다는 보장은 없습니다.

### 첫 결과 얻기

호스트 에이전트에게 다음과 같이 요청하세요.

> README 작성해 줘

첫 응답에서는 확정되지 않은 설정을 한 번에 묻고 **답변이 올 때까지 멈춥니다**. 선택 사항 또는 “추천 설정으로”라고 답하세요. 승인 후 에이전트는 정적인 프로젝트 근거를 조사하고, 합의한 README를 작성하며, 수행한 검사를 보고합니다.

선택을 에이전트에게 명시적으로 맡기려면 다음과 같이 말하세요.

> 묻지 말고 README를 생성해 줘. 영어, 개발자 대상, 균형 레이아웃, 나머지는 네가 정해.

이 위임은 수동 작성 내용을 삭제하거나 프로젝트의 설치·실행 명령을 실행하도록 허용하는 것이 아닙니다.

## 2.0의 변화

| 사용자 불편 | 개선 내용 |
|---|---|
| 에이전트가 설정 확인을 잊는다 | 실제 답변이나 명시적 위임이 없으면 스캔도 생성도 하지 않는 진입 게이트 |
| 보기 좋지만 동작하지 않는 설치 안내 | 명령, 작업 디렉터리, 첫 예제에는 프로젝트의 근거가 있어야 함 |
| 모든 README가 똑같아 보인다 | 컴팩트·균형·쇼케이스 세 가지 레이아웃과 관련 배지만 사용 |
| 다이어그램이 없거나 지어낸 것이다 | 모든 README에 소스에 근거한 플로차트 포함 |
| 번역본이 서로 어긋난다 | 모든 언어판이 언어를 제외하고 완전히 동일 |
| 업데이트가 맨 위나 맨 아래에 쌓인다 | 각 변경을 자연스럽게 속하는 위치에 배치 |
| 업데이트가 관리자의 글을 지운다 | 짝을 이룬 관리 영역, 표시가 없는 글은 수동 작성으로 취급 |

이 스킬들은 지침형이며 강제 실행 엔진이 아닙니다. 게이트와 평가 사례는 누락 위험을 줄여 주지만, 실제 준수 여부는 호스트 에이전트에서 검증해야 합니다.

## 설정

만능 템플릿을 받아들이는 대신, 각 항목을 독립적으로 선택합니다.

| 설정 | 선택지 |
|---|---|
| 언어 | 주 언어와 실제로 필요한 번역만 |
| 독자 | 사용자, 개발자 또는 기여자 |
| 레이아웃 | 컴팩트, 균형 또는 쇼케이스 |
| 분량 | 짧게, 표준 또는 상세 |
| 톤 | 전문적, 미니멀 또는 에너제틱 |
| 배지 | 없음, flat, flat-square 또는 for-the-badge |
| 이미지 | 없음 또는 관련된 기존 자산, 플로차트는 항상 포함 |
| 업데이트 방식 | 기본은 보존하고, 승인된 범위에서만 다시 작성 |
| 렌더링 | GitHub 또는 이식 가능한 Markdown |
| 이모지 | 명시적으로 요청하지 않으면 끔 |

권장 출발점은 요청의 언어, 사용자, 균형, 표준, 전문적, flat, 기존 이미지, 보존, GitHub입니다. **권장은 동의가 아닙니다.** “예쁘게 만들어 줘”라는 요청을 모든 기본값에 대한 승인으로 해석해서는 안 됩니다. `--no-beautify`는 컴팩트 레이아웃만 선택하며, `--yes`, “用默认值”, “你决定”은 확정되지 않은 설정을 위임한다는 뜻입니다.

## 독자를 위한 디자인

| 레이아웃 | 적합한 대상 | 표현 방식 |
|---|---|---|
| **컴팩트** | 작은 라이브러리와 CLI | 왼쪽 정렬 Markdown, 코드를 일찍 제시, 배지는 최대 2개 |
| **균형** | 대부분의 저장소 | 명확한 제목과 다음 단계, 배지는 최대 4개, 유용한 이미지 1장 |
| **쇼케이스** | 실제 데모가 있는 제품 | 선택적인 가운데 정렬 Hero, 텍스트 링크, 실제 스크린샷 1장 |

톤은 레이아웃과 별개입니다. 전문적이라고 가운데 정렬 HTML을 뜻하지 않으며, 에너제틱하다고 이모지를 뜻하지 않습니다. 실제 스크린샷은 도움이 되지만 가짜 UI는 그렇지 않습니다. 모든 레이아웃에 플로차트가 포함되며, 문서를 작성한 어시스턴트가 자동으로 지원 플랫폼 배지가 되지는 않습니다.

## 워크플로

`readme-write`는 **확인 → 조사 → 계획 → 작성 → 검증 → 전달** 순서로 진행합니다.

```mermaid
flowchart LR
    A[설정 확인] --> B[프로젝트 근거 조사]
    B --> C[독자의 흐름 계획]
    C --> D[내용과 디자인 작성]
    D --> E[사실, 링크, 일치 검증]
    E --> F[모든 언어판 전달]
    classDef step fill:#1e40af,stroke:#1e3a8a,color:#fff
    class A,B,C,D,E,F step
```

1. **확인:** 한 번만 묻고 기다린 뒤, 확정된 설정을 요약합니다.
2. **조사:** 매니페스트, 진입점, 예제, 테스트, 관련 설정을 읽습니다. 프로젝트 코드는 실행하지 않으며 실제 자격 증명도 읽지 않습니다.
3. **계획:** 첫 성공까지의 경로, 플로차트, 정말 유용한 섹션만 고릅니다.
4. **작성:** 하나의 표준 구조에서 모든 언어의 내용과 디자인을 함께 작성합니다.
5. **검증:** 사실 근거, 링크, 앵커, 마커, 플로차트, 일치 여부를 확인합니다.
6. **전달:** 합의한 파일만 편집하고, 실제로 수행한 검사를 보고합니다.

진입점은 [`SKILL.md`](../SKILL.md)이며, 상세 프로토콜은 [`references/`](../references/)에 있습니다.

## 업데이트 스킬

보조 스킬 [`readme-update`](../side-skills/readme-update-skill/SKILL.md)(소스 디렉터리 `side-skills/readme-update-skill`)는 로컬 Git 변경 사항으로 기존 README를 업데이트합니다.

```mermaid
flowchart LR
    U1[대상 버전 질문] --> U2[Git 변경 계층 조사]
    U2 --> U3[변경을 섹션에 대응]
    U3 --> U4[각 사실을 자연스러운 위치에 배치]
    U4 --> U5[모든 언어판 동기화]
    U5 --> U6[플로차트 갱신 및 검증]
    classDef step fill:#047857,stroke:#065f46,color:#fff
    class U1,U2,U3,U4,U5,U6 step
```

### readme-update 설치

이 저장소의 루트에서, 프로젝트 수준 Claude Code 설치 예시입니다.

```bash
mkdir -p .claude/skills/readme-update
cp side-skills/readme-update-skill/SKILL.md .claude/skills/readme-update/
cp -r side-skills/readme-update-skill/references side-skills/readme-update-skill/scripts .claude/skills/readme-update/
```

“README 업데이트해 줘” 또는 “update README”라고 요청하세요. 에이전트는 먼저 대상 프로젝트 버전을 묻고, 명시적인 **버전 유지** 선택지도 제시하며, 편집 전에 답변을 기다립니다. “你决定”으로는 이 확인을 건너뛸 수 없고, 이미 알려 준 버전은 다시 묻지 않습니다. 이후 로컬 읽기 전용 Git 명령으로 커밋된 변경, 스테이징된 변경, 스테이징되지 않은 변경, 추적되지 않는 변경을 조사하고, 독자에게 영향을 주는 변경을 해당 섹션에 대응시킵니다.

각 변경은 **그것이 속한 섹션에 녹아들어**, 가장 가까운 항목 옆에 그 섹션의 기존 순서를 따라 배치됩니다. 쉽다는 이유로 맨 위나 맨 아래에 덧붙이지 않으며, 업데이트 로그도 추가하지 않습니다. 버전 범위는 기본적으로 README에 한정됩니다. 매니페스트 수정, 태그, 커밋, 릴리스는 하지 않습니다. 대체 Git 기준점은 주 README의 마지막 변경이며 휴리스틱임을 명시합니다. 자세한 내용은 [Git 프로토콜](../side-skills/readme-update-skill/references/git-delta.md), [버전 규칙](../side-skills/readme-update-skill/references/version-and-language-sync.md), [배치 규칙](../side-skills/readme-update-skill/references/placement-and-parity.md)을 참고하세요.

## 언어 일치와 플로차트

두 스킬이 작성하거나 업데이트하는 모든 README에는 다음 두 규칙이 적용됩니다.

1. **항상 플로차트를 포함합니다.** 모든 README에는 소스에 근거한 실제 주요 흐름의 플로차트가 있습니다. 구성 요소 간 관계를 입증할 수 없으면, 검증된 설치, 설정, 실행, 결과 흐름을 그립니다. 이미지 없음 설정은 이미지만 제거하며 플로차트는 제거하지 않습니다.
2. **모든 판이 동일합니다.** 모든 언어판의 섹션, 표, 코드 블록, 플로차트 노드와 연결, 링크, 이미지, 배지가 같습니다. 다른 것은 언어뿐이며, 특정 판에만 있는 내용은 남기지 않습니다.

어긋난 판은 하나의 표준 구조로 맞추고, 아래의 검사기로 구조를 검증합니다. 일치 검사가 증명하는 것은 구조의 동일성뿐이며, 번역의 정확성은 사람이 읽고 확인해야 합니다.

## 안전한 업데이트

`readme-update`를 통한 유지보수에서, 실제 버전 결정은 표시가 없는 섹션에 대한 근거 있는 좁은 범위의 수정만 허용하며 다시 쓰기는 허용하지 않습니다. 명시적인 수동 블록과 관련 없는 내용은 계속 보호됩니다. 새로 생성하는 섹션에는 안정적인 짝 마커를 사용합니다.

```markdown
<!-- readme-skill:begin usage -->
## 사용법

프로젝트별 내용.
<!-- readme-skill:end usage -->
```

마커 범위만 업데이트하고, 그 밖의 글과 명시적인 `MANUAL-START` / `MANUAL-END` 블록은 보존합니다. 표시가 없는 기존 섹션은 수동 작성으로 취급하며, 이전의 `AUTO-GENERATED`나 `BEAUTIFIED` 주석은 전체 덮어쓰기 허가가 아닙니다. 자세한 내용은 [근거와 업데이트 규칙](../references/evidence-and-updates.md)을 참고하세요.

## 품질 검사

이 저장소의 루트에서 코드를 실행하지 않고 대상 프로젝트를 검사합니다. 주 README를 먼저, 그다음 모든 번역을 나열하세요.

```bash
python3 scripts/check_readme.py --root /absolute/path/to/project --require-flowchart --parity /absolute/path/to/project/README.md /absolute/path/to/project/assets/README-zh.md
```

기계가 읽을 수 있는 보고서가 필요하면 `--json`을 추가하세요. `--preferences /path/to/preferences.json`은 사용자가 저장된 설정 기록을 허용한 경우에만 사용합니다. 검사기는 누락된 플로차트, 언어판 사이의 구조 차이, 존재하지 않는 로컬 경로와 앵커, 이미지 대체 텍스트 누락, 닫히지 않은 코드 펜스, 손상된 마커, 템플릿 잔여물, 신뢰도 높은 민감 값 형식, 일부 Mermaid 오류를 찾아냅니다. 종료 코드: `0`은 오류 없음, `1`은 검증 오류, `2`는 호출 또는 읽기 실패입니다.

이것은 사용자의 실제 동의, 내용의 사실 정확성, 예제의 실행 가능성, 외부 링크의 접근성, 번역의 정확성, Mermaid 문법의 완전한 정확성, GitHub 렌더링 결과를 **증명하지 않습니다**. 자세한 내용은 [검사 범위와 한계](../references/quality-checks.md)를 참고하세요.

### 회귀 테스트

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

자동 테스트는 검사기, Git 변경 도구, 스킬 계약을 다룹니다. [`tests/behavior-cases.json`](../tests/behavior-cases.json)과 [`side-skills/readme-update-skill/tests/behavior-cases.json`](../side-skills/readme-update-skill/tests/behavior-cases.json)에는 실제 호스트 에이전트 평가를 위한 시나리오가 있습니다. 이는 평가 명세이며 모든 호스트가 통과했다는 주장이 아닙니다.

## 개발 방향

**설정의 신뢰성 → 믿을 수 있는 첫 경험 → 안전한 유지보수 → 동일한 언어판**을 우선합니다. 다음 반복에서 배지 매핑이나 더 큰 HTML 템플릿 추가를 주된 작업으로 삼지 마세요. 다음으로는 실제 호스트 에이전트에서 행동 시나리오를 실행하고, [디자인 평가 기준](../references/quality-checks.md#design-acceptance-rubric)을 사용해 대표적인 애플리케이션, 라이브러리, CLI, 모노레포의 실제 렌더링을 비교합니다.

## 저장소 구성

| 경로 | 용도 |
|---|---|
| `SKILL.md` | `readme-write` 진입점과 필수 워크플로 |
| `references/` | 설정 게이트, 근거, 섹션, 디자인, 다이어그램, 언어, 품질 검사 |
| `scripts/check_readme.py` | 읽기 전용 오프라인 검사기 |
| `side-skills/readme-update-skill/` | `readme-update` 스킬, 참고 문서, Git 변경 도구 |
| `tests/` | 자동 검사와 행동 시나리오 |
| `examples/` | 과거의 설명용 출력 예시이며 검증된 기준 데이터가 아님 |
| `install/` | 호스트 연동 가이드 |
| `assets/` | 아트워크와 번역된 README |

## 기여

워크플로 규칙을 바꿀 때는 관련 참고 문서를 업데이트하고 행동 시나리오를 추가하세요. 검사기를 바꿀 때는 통과와 실패 사례를 모두 추가하고 회귀 테스트를 실행하세요. 실제 호스트 실행 기록이 없는 시나리오를 호스트에서 검증되었다고 표시해서는 안 됩니다.

## 라이선스

[MIT](../LICENSE)
