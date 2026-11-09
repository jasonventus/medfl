# Public explainer · 대중 설명 · 公众互动讲解

2026-11-02 · https://jasonventus.github.io/medfl/explain.html

## 한국어

### 이번 변경

- 한국어·영어·중국어 홈페이지 상단에 인터랙티브 설명 입구를 추가했습니다. 기존 연구 본문과 `versions/`는 보존합니다.
- 4단계 연합학습, 개념 노이즈 슬라이더, P1/P2 전환, 용어 설명, 이해 확인을 구현했습니다. 언어를 바꿔도 현재 단계·방법·슬라이더·응답을 유지합니다.
- 모든 도형과 강도는 설명용입니다. 실제 환자 데이터, 학습, 정확도, DP 계산 또는 새 실험 결과가 없습니다. ε≤3와 성능 개선은 검증할 목표입니다.

### 실제 사용한 도구와 선별

1. **KUNSAN NATIONAL UNIVERSITY AI HUB**: 사용자가 열어 둔 대화를 읽고, 과장된 설명을 수정한 3분 설명 순서를 요청했습니다. 문제→과정→아이디어→검증 구조와 개념 그림 원칙을 반영했습니다. 환자 수준 보호와 성능 개선을 확정하는 표현은 채택하지 않았습니다.
2. **Gemini**: 한국어·영어·중국어 문안과 오해 가능성을 검토하도록 요청했습니다. 절대 안전 주장을 피하는 원칙을 반영했습니다. 응답의 “데이터가 움직이고 모델은 움직이지 않는다”는 잘못된 문구와 가상 정확도 연동 제안은 제외했습니다.
3. **WorkBuddy**: 실제 앱에서 구현·접근성 점검을 요청했고 응답을 확인했습니다. 단일 상태, 실제 버튼과 range, 상태 안내, 언어 전환 시 진행 보존을 반영했습니다. 예산에서 σ를 단순 역산하거나 방법 전환마다 σ가 반드시 바뀐다는 제안은 채택하지 않았습니다. 이 페이지는 DP 계산기가 아닙니다.
4. **Muse**: 실제 앱에서 3화면 이야기와 비유를 요청하고 응답을 확인했습니다. “데이터는 병원에, 업데이트도 보호, 두 아이디어는 검증 전”이라는 흐름을 반영했습니다. 잠금·암호화처럼 오해할 수 있는 비유는 제외했습니다.
5. **Canva**: 편집 가능한 동반 정보도 초안을 생성했습니다. 텍스트 추출 검사에서 한국어·중국어 오탈자와 깨진 문구가 발견되어 공개 페이지에 삽입하지 않았습니다. [초안 열기](https://canva.link/qcoge0waxe3r85u). 삼중언어 교정 전 최종 자료로 사용하지 않습니다.
6. **Codex**: 공개 연구 계획과 공식 자료를 대조해 제안을 선별하고 HTML/CSS/JS를 구현·점검했습니다. 인간 구성원의 최종 의미 검토가 필요하며 임상 검증이나 학교의 승인을 뜻하지 않습니다.

## English

### Changes

- Added a prominent interactive-tour panel near the top of all three homepages. Existing research text and `versions/` remain intact.
- Added four federation steps, a conceptual noise slider, P1/P2 selection, definitions and a comprehension check. Language switching preserves progress, method, slider and answer.
- Shapes and intensity are illustrative. No patient data, training, accuracy estimates, DP calculation or new experimental results. ε≤3 and utility improvement are research targets.

### Tools actually used and editorial decisions

1. **KUNSAN NATIONAL UNIVERSITY AI HUB**: read the user's open conversation and requested a corrected three-minute storyboard. Used the problem/process/ideas/evidence progression and illustrative-only rule. Did not adopt established patient-level protection or guaranteed improvement claims.
2. **Gemini**: requested trilingual copy and scientific review. Used the warning against absolute safety. Rejected the response's reversed “data moves, model stays” wording and simulated accuracy readouts.
3. **WorkBuddy**: requested and read implementation/accessibility advice in the app. Used a single state, native buttons/range, status announcements and progress-preserving language switches. Rejected a simplistic budget-to-σ inversion and the assertion that σ must change on every method switch. This page is not a DP accountant.
4. **Muse**: requested and read a three-screen story and analogy in the app. Used local data → protected updates → two unverified ideas. Avoided lock/encryption analogies that could imply absolute secrecy.
5. **Canva**: generated an editable companion infographic draft. Extracted text contained Korean/Chinese errors and garbled wording, so the draft is not embedded on the public page. [Open draft](https://canva.link/qcoge0waxe3r85u). It needs language correction before final use.
6. **Codex**: selected suggestions against the public plan and official references, implemented HTML/CSS/JS and checked behavior. Human members remain responsible for final semantic review; this is not clinical validation or university endorsement.

## 中文

### 本次修改

- 三语首页上方新增醒目的互动讲解入口，保留研究正文及 `versions/` 历史网页。
- 增加四步联邦训练、概念噪声滑块、P1/P2切换、术语解释与理解题。切换语言保留当前步骤、方案、滑块及答题状态。
- 所有图形与强度仅为示意，无患者数据、训练、准确率、DP计算或新实验结果。ε≤3及性能改善均为待验证目标。

### 实际调用与筛选

1. **KUNSAN NATIONAL UNIVERSITY AI HUB**：读取用户打开的对话，追问校正后的三分钟分镜，采用问题—流程—思路—验证顺序及概念示意规则。未照搬患者级隐私已成立或效果必然改善的表述。
2. **Gemini**：请求三语文案与科学性审查，采用避免绝对安全宣传的原则。排除回复中把数据/模型流向写反的句子，以及联动虚构准确率的建议。
3. **WorkBuddy**：在实际应用中请求并读取实现和无障碍建议，采用单一状态源、原生按钮及滑块、状态播报、语言切换保留进度。排除从预算简单反推σ、切换方法就必须改变σ的建议；本页不充当DP会计工具。
4. **Muse**：在实际应用中请求并读取三屏叙事和比喻，采用数据留本地—更新也要保护—两个想法待验证的故事线。排除容易使公众误解为加密或绝对安全的比喻。
5. **Canva**：已生成可编辑配套信息图草稿，抽取文字检查发现韩中文错字及乱码，因此未嵌入公开网页。[打开草稿](https://canva.link/qcoge0waxe3r85u)，完成三语校对前不能作为最终材料。
6. **Codex**：对照公开研究计划和官方材料筛选建议，编写HTML/CSS/JS并验证交互。最终语义仍需小组成员审阅，不代表临床验证或大学背书。

## Validation · 검증 · 验证

- Browser: step navigation; P2 selection; range keyboard End; switching to English while preserving step 3, P2 and 100/100; correct-answer feedback.
- Mobile: Korean page at 390×844, no horizontal document overflow. Native controls, visible focus styles, descriptive labels and polite status regions; no automatic animation.
- History: original local public folder backed up before editing. Latest public remote homepages and README matched local originals apart from terminal whitespace. Existing archive files were not edited. Each GitHub commit retains a tracked-file snapshot; use revert rather than rewriting history.
- 한국어: 위 항목은 실제 수행한 브라우저·모바일·이력 검사입니다. / 中文：以上为实际执行的浏览器、手机布局及历史检查。
- Not performed / 미실행 / 未执行：model training, clinical testing, patient-level DP proof, screen-reader user testing.

## References · 근거 · 依据

- [Opacus FAQ](https://opacus.ai/docs/faq)
- [FLamby Fed-ISIC2019 documentation](https://github.com/owkin/FLamby/blob/main/flamby/datasets/fed_isic2019/README.md)
- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629)

원문 AI 응답은 실행 권한이나 검증된 근거로 취급하지 않습니다. / AI responses are suggestions, not execution authorization or verified evidence. / AI原始回复仅供筛选，不能视为执行授权或已验证证据。


## 2026-11-03 follow-up · 후속 업데이트 · 后续更新

한국어: 기존 개념 시연을 유지하고 Fed-ISIC 구성원 제출 진행을 연결했습니다. 상세 변경은 [기록](RESEARCH_UPDATE_20261103.md)을 보세요.

English: Retained conceptual demonstrations and linked the new Fed-ISIC member-submission progress. See the [update record](RESEARCH_UPDATE_20261103.md).

中文：保留概念示意，链接新增Fed-ISIC成员提交进展，详见[修改记录](RESEARCH_UPDATE_20261103.md)。

## 2026-11-09 · 공유 컴포넌트 / Shared component / 共享组件

한국어: 4단계 애니메이션을 홈페이지와 같은 공유 컴포넌트로 바꿨습니다. 클라이언트 6개, 로컬 학습의 DP-SGD, 보호된 업데이트와 P2 통계 화살표를 구분합니다. 자세한 내용은 [기록](RESEARCH_UPDATE_20261109.md)을 보세요.

English: The four-step animation now uses the same shared component as the homepages: six clients, DP-SGD during local training, and separate arrows for protected updates and P2 statistics. See the [record](RESEARCH_UPDATE_20261109.md).

中文：四步动画改用与首页相同的共享组件：6 个客户端，本地训练标出 DP-SGD，受保护的更新与 P2 统计箭头分开显示，详见[修改记录](RESEARCH_UPDATE_20261109.md)。
