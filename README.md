<div align="center">

<img src="frontend/logo.svg" width="130" alt="Mind Compass" />

# 🧭 Mind Compass

**고민을 정리하는 가장 단순한 방법.**

정답을 내려주는 대신, 무엇이 당신의 결론을 흔드는지 보여주는 의사결정 도우미.

[🔗 Live Demo](https://decision-debugger.onrender.com) · [📐 설계서](decision_debugger_design_v3.md) · [🎨 디자인 가이드](DESIGN.md)

<sub>Python · FastAPI · numpy/scipy · OpenAI · Vanilla JS (Apple-style UI)</sub>

</div>

---

## 무엇인가요?

복잡한 고민을 입력하면 —
1. AI가 **판단 기준·중요도·선택지 점수를 알아서** 정하고,
2. 당신은 **"A vs B" 카드 둘 중 하나만** 고르면 (어려우면 더 쉬운 질문으로 쪼개줘요),
3. 그 선택으로 숨은 우선순위를 추정해서
4. **왜 이 결론인지 · 무엇이 바뀌면 뒤집히는지 · 뭘 더 알아보면 좋은지** 를 알려줍니다.

> 핵심 철학: *"정답"이 아니라 "내 결정의 구조"를 보여준다.*

## ✨ 특징

- 🤖 **AI 자율 분석** — 고민만 적으면 기준·점수를 알아서 잡음 (사용자는 컨펌·편집 불필요)
- 🃏 **고르기만 하면 됨** — 모든 질문이 카드 2장 비교로 통일, 답하기 쉬움
- 🪜 **"잘 모르겠어요" → 더 쉬운 질문으로 재귀 분해** 후 결론에 반영 (roll-up)
- 📊 **민감도 분석** — "무엇이 결론을 움직이나", 어떤 가정이 바뀌면 뒤집히는지 시각화
- 🧠 **LLM ↔ 계산 분리** — 물렁한 판단은 AI, 가중치·집계·민감도는 결정론적 수학(테스트됨)
- 🍎 **Apple 스타일 UI** — 군더더기 없는 깔끔한 화면

## ⚙️ 동작 원리 (요약)

```
[고민 입력]
  → AI: 선택지·판단기준·중요도·점수 결정 + 카드 질문 생성
  → 사용자: 카드 선택 (못 고르면 → 더 쉬운 카드로 분해 → roll-up)
  → 계산: 가중치 정교화(Bradley-Terry) + 집계(WSM) + 민감도(OAT)
  → AI: "왜 + 뭐가 뒤집나 + 뭘 더 알아야" 리포트
```
수학적 디테일(가중치 정교화·민감도 공식 등)은 [설계서 §8](decision_debugger_design_v3.md)을 참고하세요.

## 🛠 기술 스택

| 영역 | 사용 |
|---|---|
| 백엔드 | Python 3 · FastAPI · uvicorn |
| 계산 코어 | numpy · scipy (순수 함수, pytest로 검증) |
| AI | OpenAI (`gpt-4o`, 서버 전용 · 키는 `.env` 격리) |
| 프론트엔드 | Vanilla HTML/CSS/JS (빌드 불필요, Apple 디자인) |
| 저장 | 인메모리 세션 |

## 🚀 로컬 실행

```powershell
# Windows
.\run.ps1
```
```bash
# 또는 수동
python -m venv .venv
./.venv/Scripts/python -m pip install -r requirements.txt
./.venv/Scripts/python -m uvicorn backend.main:app --port 8000
```
브라우저에서 **http://localhost:8000** 접속.

> `.env.example`을 `.env`로 복사하고 본인 `OPENAI_API_KEY`를 넣으세요. 키는 절대 커밋되지 않습니다(`.gitignore`).

테스트:
```powershell
./.venv/Scripts/python -m pytest -q
```

## ☁️ 배포 (Render)

상시 서버가 필요하므로 Render에 배포합니다. `render.yaml` 블루프린트가 포함돼 있어요.

1. [render.com](https://render.com) → **New → Blueprint** (또는 **Web Service**) → 이 저장소 연결
2. **`OPENAI_API_KEY`** 를 Render 대시보드 환경변수로 입력 (저장소엔 없음)
3. 배포 → `git push` 할 때마다 자동 재배포

> 무료 티어는 15분 유휴 시 잠들었다가 다음 접속에 ~30–60초 콜드스타트가 있습니다.

## 📁 구조

```
backend/      FastAPI 앱 (main · orchestrator · llm · prompts · compute · models)
frontend/     Apple 스타일 SPA (index.html · styles.css · app.js · logo.svg)
tests/        계산 코어 단위테스트
scripts/      종단 스모크 테스트
render.yaml   Render 배포 블루프린트
```

## 🔒 보안

- API 키는 `.env`(git 제외)에만 — 코드/프론트/로그/응답 어디에도 없음
- 모든 AI 호출은 **서버에서만** (브라우저로 키 전송 안 함)
- `/api/health`는 키 설정 여부(불리언)만 노출

---

<div align="center"><sub>FORIF 해커톤 프로젝트 · Made with 🧭</sub></div>
