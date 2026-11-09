# 2026-11-09 · 홈페이지 개편 / Homepage redesign / 首页改版

[한국어](https://jasonventus.github.io/medfl/index.html) · [English](https://jasonventus.github.io/medfl/en.html) · [中文](https://jasonventus.github.io/medfl/zh.html)

## 한국어

- 세 홈페이지를 6개 모듈로 다시 만들었습니다: 무엇을 연구하나 → 데이터 → 공개 데이터 연합 → 방법 → 진행 → 요약. 모듈마다 질문 1개, 한 문장 답, 설명 그림 1개, 기술 세부 펼치기 1개입니다.
- 사실·상태·결과를 `tools/site_content.py` 한 곳에 두고, `python tools/build_site.py`가 `index.html`·`en.html`·`zh.html`과 `data/medfl-data.json`·`data/medfl-data.js`를 함께 만듭니다. `explain.html`과 `progress.html`도 같은 데이터 파일에서 날짜·상태를 읽습니다.
- 상태 표기는 제출됨·검토 대기·검토 완료·시작 전 네 가지만 씁니다. 11-03 공개 기록 이후 비공개 저장소에 제출된 4차(B1·B5·P1-block·멤버십 추론 공격·흉부 영상)와 10–12차(PathMNIST 과목 설정)를 ‘제출됨·검토 대기’로 반영했습니다. LoRA 버전 P1, K=10, ISIC 분포 변화 검증은 ‘시작 전’입니다.
- 상세 수치는 계속 비공개입니다. 결과 객체의 지표·실제 ε·δ·시드 수는 `null`이며 화면에 ‘추후 보완’으로 표시하고, 근거는 비공개 저장소의 고정 commit 링크로 둡니다.
- Fed-ISIC2019는 ‘출처·촬영 장비 구획 6개’로 표기하고 병원 6곳으로 쓰지 않습니다. P1은 이번 제출(고정 특징 + DP 분류기)과 원래 설계(마지막 block/LoRA)를 전환해 봅니다. B4는 가중 P1이며 이전 설계표의 가중 B3와 같은 행에 두지 않습니다.
- `explain.html`의 4단계 애니메이션을 공유 컴포넌트(`assets/medfl.js`)로 바꿨습니다. 클라이언트 6개, 이미지는 로컬에 고정, 로컬 학습에 DP-SGD(샘플별 클리핑 + 노이즈), 화살표는 모델 파라미터·보호된 업데이트만, P2는 노이즈 클래스 통계 화살표를 따로 표시합니다. 노이즈 슬라이더에는 ‘개념 설명용 강도(실제 ε나 정확도 아님)’를 붙였습니다.
- 초등학생용 7단계 애니메이션(`assets/kids.js`)을 부록으로 추가했습니다. 상자 6개, 실험 수치 없음.
- 이전 홈페이지는 `versions/v2-design/`에 보존했고 이전 앵커(`#s0`–`#s6`, `#research-update-20261103`, `#public-explainer`, `#changes`)는 새 모듈로 연결됩니다. 언어를 바꾸면 보고 있던 모듈로 이동합니다.
- 확인: 세 언어 페이지 구조(모듈·표 행·상태 표시·링크) 일치, 375px 화면 5개 페이지 가로 넘침 없음, 콘솔 오류 없음, JavaScript 없이도 본문 읽기 가능.

## English

- Rebuilt the three homepages as six modules: the question → data → public-data federation → methods → progress → summary. Each module has one question, a one-sentence answer, one explanatory figure and one technical-details expander.
- Facts, statuses and results live in one place, `tools/site_content.py`; `python tools/build_site.py` writes `index.html`, `en.html`, `zh.html` and `data/medfl-data.json` / `data/medfl-data.js`. `explain.html` and `progress.html` read their dates and statuses from the same data file.
- Statuses use four values only: Submitted, Pending review, Reviewed, Not started. Work submitted to the private repository after the Nov 3 public record — round 4 (B1, B5, P1-block, membership inference, chest X-ray) and rounds 10–12 (PathMNIST course setting) — now shows as Submitted · Pending review. The LoRA version of P1, K=10 and distribution shift on ISIC are Not started.
- Detailed values stay private. Metrics, actual ε, δ and seed counts are `null` in the result objects, render as “to be added”, and link to fixed commits in the private repository as evidence.
- Fed-ISIC2019 is described as six source / imaging-device partitions, never six hospitals. P1 can be switched between this round (frozen features + DP head) and the original design (last block / LoRA). B4 is weighted P1 and is never placed in the same row as the old design’s weighted B3.
- The four-step animation of `explain.html` is now a shared component (`assets/medfl.js`): six clients, images fixed locally, DP-SGD (per-sample clipping + noise) during local training, arrows carrying only model parameters / protected updates, and a separate noisy-class-statistics arrow for P2. The noise slider is labelled “concept intensity (not a real ε or accuracy value)”.
- Added a seven-step animation for kids (`assets/kids.js`) as an appendix: six boxes, no experimental numbers.
- The previous homepages are kept in `versions/v2-design/`; old anchors (`#s0`–`#s6`, `#research-update-20261103`, `#public-explainer`, `#changes`) land on the new modules. Switching language keeps the module in view.
- Checked: identical page structure across the three languages (modules, table rows, status badges, links), no horizontal overflow at 375px on all five pages, no console errors, body text readable without JavaScript.

## 中文

- 三语首页改为 6 个模块：研究什么 → 数据 → 公开数据联邦 → 方法 → 进展 → 总结。每个模块含 1 个问题、1 句直接回答、1 张解释图和 1 个技术细节展开入口。
- 事实、状态和结果只写在 `tools/site_content.py`；运行 `python tools/build_site.py` 同时生成 `index.html`、`en.html`、`zh.html` 与 `data/medfl-data.json`、`data/medfl-data.js`。`explain.html`、`progress.html` 也从同一数据文件读取日期和状态。
- 状态只用四个值：已提交、待复核、已复核、尚未开展。11-03 公开记录之后提交到私有库的第 4 轮（B1、B5、P1-block、成员推断攻击、胸片）和第 10–12 轮（PathMNIST 课程设置）标为“已提交 · 待复核”；LoRA 版 P1、K=10、ISIC 分布变化验证标为“尚未开展”。
- 详细数值继续不公开。结果对象中的指标、实际 ε、δ、种子数为 `null`，页面显示“待补充”，证据链接指向私有库的固定提交。
- Fed-ISIC2019 写作“6 个来源/成像设备分区”，不写成 6 家医院。P1 可在本轮提交版（冻结特征 + DP 分类头）与原设计（最后 block/LoRA）之间切换；B4 为加权 P1，不与旧设计表的加权 B3 放在同一行。
- `explain.html` 的四步动画改用共享组件（`assets/medfl.js`）：6 个客户端，图像固定在本地，本地训练标出 DP-SGD（逐样本裁剪 + 加噪），箭头只传模型参数/受保护的更新，P2 另标加噪类别统计箭头。噪声滑块标注“概念示意强度（非真实 ε 或准确率数值）”。
- 新增给小学生的 7 步动画（`assets/kids.js`）作为附录：6 个箱子，不含实验数字。
- 改版前首页保存在 `versions/v2-design/`；旧锚点（`#s0`–`#s6`、`#research-update-20261103`、`#public-explainer`、`#changes`）跳到对应新模块。切换语言时停留在当前模块。
- 已检查：三语页面结构（模块、表格行、状态徽章、链接）一致；5 个页面在 375px 宽度下无横向溢出；无控制台错误；关闭 JavaScript 时正文可读。

## 같은 날 보완 / Same-day refinement / 同日补充

한국어: 4단계 애니메이션에 이동하는 파라미터·보호된 업데이트 표시, 클라이언트별 학습 진행과 DP 노이즈 표시, 서버 집계 효과를 넣었습니다. P2 통계 화살표는 1단계가 끝난 뒤 한 번만 움직이고, 4단계에 P2의 가상 특징 재학습을 표시합니다. 초등학생용 애니메이션은 실제 순서(모델 복사 → 학습 중 노이즈 → 노트만 전송)로 바꿨습니다. 이전 판은 로봇이 상자를 차례로 방문하고 노트에 나중에 안개를 뿌려, 병렬 학습과 학습 중 DP-SGD라는 설명과 맞지 않았습니다. 집계가 클라이언트 표본 수 가중 평균(Flower FedAvg)인 것은 코드로 확인했습니다.

English: The four-step animation now shows travelling parameters and protected updates, per-client training progress with DP noise, and a server aggregation pulse. The P2 statistics arrow moves once, after the first stage, and step 4 shows P2’s retraining on virtual features. The kids animation now follows the real order (model copies → noise during training → only notes travel); the earlier version had one robot visiting boxes in turn and fog added to notes afterwards, which contradicted parallel training and DP-SGD during training. Aggregation weighted by client size (Flower FedAvg) was confirmed in the code.

中文：四步动画加入了移动的模型参数与受保护更新、各客户端的训练进度和 DP 噪声，以及服务器聚合效果；P2 统计箭头只在第一阶段结束后移动一次，第 4 步显示 P2 用虚拟特征重训。小学生动画改为真实顺序（复制模型 → 训练中加噪 → 只传笔记）；旧版是一个机器人挨个访问箱子、事后给笔记加雾，与并行训练和“训练中做 DP-SGD”的说明不符。已在代码中确认聚合按客户端样本量加权（Flower FedAvg）。

## Sources · 근거 · 依据（研究库需协作者登录）

- [Round 4 report](https://github.com/jasonventus/healthcare-ai-project05/blob/b24f91f554e6e998fb79f4af87edb4a7ca275f5e/experiments/2026-11-03_round4_all-experiments/REPORT.md)
- [Rounds 10–12 report](https://github.com/jasonventus/healthcare-ai-project05/blob/edeec2bf2aaa66a0dd082ed0d1d308884229a34d/experiments/2026-11-07_round10-12_course-target/REPORT.md)
- [Rounds 2–3 report](https://github.com/jasonventus/healthcare-ai-project05/blob/84ab6a2e9433db4023fe40629eff7814c2d09043/experiments/2026-11-03_round2-3_fedisic/REPORT.md)
- [FLamby Fed-ISIC2019](https://github.com/owkin/FLamby/blob/main/flamby/datasets/fed_isic2019/README.md)
