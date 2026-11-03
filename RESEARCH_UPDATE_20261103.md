# 2026-11-03 · 연구 진행 업데이트 / Research progress update / 研究进展更新

[한국어](https://jasonventus.github.io/medfl/progress.html?lang=ko) · [English](https://jasonventus.github.io/medfl/progress.html?lang=en) · [中文](https://jasonventus.github.io/medfl/progress.html?lang=zh)

## 한국어

范润堃의 `member/fanrunkun1/round2-3-fedisic` 분기, 고정 commit `84ab6a2e9433db4023fe40629eff7814c2d09043`을 확인했습니다. 제출 날짜는 2026-11-03이며 작성자는 fanrunkun1, 공동 작성 표시는 Claude입니다. 확인 시 연구 main에는 병합되지 않았고 보고서는 사람 검토자를 미정으로 표시했습니다.

### 공개 페이지의 변경

- 세 홈페이지 상단에 날짜가 있는 진행 안내와 `progress.html` 입구를 추가했습니다.
- PathMNIST는 파이프라인 점검으로 보존하고 Fed-ISIC 비교 및 P2/PCA/LA 시도를 구성원 제출로 설명합니다. 성공을 확정하지 않습니다.
- 보고된 RQ1 관찰은 현재 설정에 한정하고, 원래 P2의 안정적 이득 부재·PCA의 클래스별 불일치·LA의 제한적 이득을 구분했습니다. 상세 수치는 비공개로 유지합니다.
- 구현의 P1은 분류기만 학습하고 B4는 가중 P1입니다. 원 설계의 마지막 block/LoRA 미세조정 및 가중 B3와 혼동하지 않도록 했습니다.
- BatchNorm eval 고정, Derma 선택 및 중복 제거의 보고, B3 관문 미통과와 추가 seed 수행의 기록을 공개 요약에 반영했습니다. 독립 확인된 프라이버시 보장으로 취급하지 않습니다.
- 이미지/표본 DP와 환자 DP, 모델별 예산 상한과 실제 합성 ε, 여러 실험의 전체 공개 예산을 구분했습니다.
- B5·흉부 영상 학습·MIA·마지막 block 미세조정 및 사람의 검토는 미완료로 표시했습니다.
- 기존 인터랙티브 설명은 개념 그림을 유지하며 새 진행을 안내합니다. 원 설계 v2와 역사 페이지를 보존했습니다.

### 확인 범위

보고서, 결정 기록, 실행 안내, 3차 회고, 방법 비교 CSV와 클래스별 DP 비용 CSV를 읽었습니다. CSV의 B2−B3 계산 및 보고서와의 대조를 점검했습니다. 전체 학습·원시 데이터 감사·모든 계수기의 독립 재현·임상 검증은 하지 않았습니다. 모든 주장은 구성원 보고에 근거한 단계적 진행으로 표시합니다.

이번 작업 도구: Codex와 Chrome의 GitHub UI. 변경은 jasonventus로 로그인된 Chrome에서 수행합니다. 이전 AI HUB·Gemini·WorkBuddy·Muse·Canva 호출은 11월 2일 설명 페이지 제작 기록이며 이번 실험 검증으로 재사용하지 않습니다.

## English

Reviewed Fan Runkun’s `member/fanrunkun1/round2-3-fedisic` at fixed commit `84ab6a2e9433db4023fe40629eff7814c2d09043`, dated 2026-11-03, authored by fanrunkun1 with a Claude co-author credit. At inspection it was not merged into research main, and the report listed human reviewers as unassigned.

### Public-page changes

- Added a dated progress panel at the top of all three homepages and a `progress.html` destination.
- Retained PathMNIST as a pipeline check and described Fed-ISIC comparisons plus P2/PCA/LA attempts as a member submission, not an established success.
- Scoped the reported RQ1 observation to the current configuration. Distinguished no stable original-P2 benefit, inconsistent PCA class outcomes and limited LA gains. Detailed values stay private.
- Distinguished head-only P1 and class-weighted P1 as B4 from the original last-block/LoRA fine-tuning and class-weighted B3 design.
- Summarized reported frozen BatchNorm eval statistics, Derma selection/overlap removal, and the failed B3 gate followed by additional seeds. These are not independently established privacy guarantees.
- Distinguished image/sample DP from patient DP, per-model caps from actual composed ε, and model accounting from the combined release of repeated experiments.
- Marked B5, chest-image training, MIA, last-block fine-tuning and human review as unfinished.
- Kept the conceptual interactive demonstrations, linked them to current progress, and retained design v2 and historical pages.

### Review scope

Read the report, decision record, run guide, round-three write-up, method-comparison CSV and class DP-cost CSV. Checked the B2−B3 CSV arithmetic and agreement with the report. Did not independently rerun all training, audit source data, reproduce every accountant, or perform clinical validation. Public statements are explicitly attributed to an interim member report.

Tools for this update: Codex and Chrome’s GitHub UI. Changes use Chrome signed in as jasonventus. The earlier AI HUB/Gemini/WorkBuddy/Muse/Canva calls belong to the Nov 2 explainer, not validation of these experiments.

## 中文

已检查范润堃的 `member/fanrunkun1/round2-3-fedisic`，固定提交为 `84ab6a2e9433db4023fe40629eff7814c2d09043`，日期为2026-11-03，作者为 fanrunkun1，带有 Claude 联合作者标记。检查时尚未合并研究 main，报告中的人类复核人仍待指定。

### 公开网页修改

- 三语首页顶部新增带日期的进展入口，链接到 `progress.html`。
- PathMNIST仅保留为流程验证，Fed-ISIC对照及P2/PCA/LA尝试标记为成员提交，不能视为方案已成功。
- RQ1的报告观察限定在当前配置；区分原P2无稳定收益、PCA各类别效果不一致、LA仅有限改善。详细数值留在私有库。
- 区分实际仅训练分类头的P1、以加权P1实现的B4，与原计划最后block/LoRA微调、加权B3之间的差别。
- 摘要反映报告中的固定BatchNorm eval、Derma选参及重叠剔除、B3关口未通过后补齐种子的记录，不将这些报告表述等同于独立核验过的隐私保证。
- 区分图像/样本级DP和患者级DP、逐模型预算上限和实际累计ε，以及全部重复实验合计发布的预算范围。
- B5、胸片训练、MIA、最后block微调和人类评审仍标记未完成。
- 保留公众互动页的概念示意，新增当前进展提示；原设计第二版与历史页面保留。

### 本次检查范围

已读取报告、决定记录、运行说明、第三轮回报、方法对照CSV及类别DP代价CSV，检查了CSV中B2−B3算术关系及与报告的一致性。未独立重跑全部训练、审计原始数据、复算全部隐私会计或进行临床验证。公开陈述均归因于成员阶段报告。

本次工具：Codex与Chrome GitHub界面。修改使用Chrome已登录的jasonventus。之前AI HUB、Gemini、WorkBuddy、Muse、Canva的调用属于11月2日科普页制作，不作为本次实验验证的证据。

## Sources · 근거 · 依据（研究库内容需协作者登录）

- [Fixed source commit](https://github.com/jasonventus/healthcare-ai-project05/commit/84ab6a2e9433db4023fe40629eff7814c2d09043)
- [Experiment report](https://github.com/jasonventus/healthcare-ai-project05/blob/84ab6a2e9433db4023fe40629eff7814c2d09043/experiments/2026-11-03_round2-3_fedisic/REPORT.md)
- [Round-three write-up](https://github.com/jasonventus/healthcare-ai-project05/blob/84ab6a2e9433db4023fe40629eff7814c2d09043/experiments/2026-11-03_round2-3_fedisic/claude_codex/Codex回报_第3轮.md)
- [Decision record](https://github.com/jasonventus/healthcare-ai-project05/blob/84ab6a2e9433db4023fe40629eff7814c2d09043/experiments/2026-11-03_round2-3_fedisic/claude_codex/决定记录.md)
- [Method-comparison CSV](https://github.com/jasonventus/healthcare-ai-project05/blob/84ab6a2e9433db4023fe40629eff7814c2d09043/src/runs_fedisic/round3_summary/methods_eps3.csv)
- [Class DP-cost CSV](https://github.com/jasonventus/healthcare-ai-project05/blob/84ab6a2e9433db4023fe40629eff7814c2d09043/src/runs_fedisic/round3_summary/per_class_dp_cost.csv)

## History · 이력 · 历史

[Website before this update / 이번 변경 전 / 本次修改前的网站库](https://github.com/jasonventus/medfl/tree/397893584fff0b8c07c8068ec9111c8b0d77cbdc)

기존 commit과 `versions/`는 수정하지 않습니다. 새 commit으로 이력을 추가하며 철회는 revert를 사용합니다. / Existing commits and `versions/` are retained. Add new commits; undo by revert. / 不改写旧commit及`versions/`；使用新提交保留全库快照，撤销用revert。


## Website checks · 웹 검사 · 网页验证

한국어: 두 JS 구문 검사, 세 언어 전환 시 방법 선택 유지, 설명↔진행 링크, 390px 한국어 화면의 가로 넘침 없음, 원본 CSV 산술 대조를 확인했습니다. 환자 데이터나 상세 실험 수치를 공개 파일에 복사하지 않았습니다.

English: Checked both JS syntaxes, language switching with method selection preserved, explainer↔progress links, no horizontal overflow at 390px in Korean, and source CSV arithmetic. No patient data or detailed experimental values were copied into public files.

中文：已检查两页JS语法、语言切换保留方案、互动页与进展页双向链接、390px韩语手机布局无横向溢出，以及源CSV算术一致性。未将患者数据或详细实验数值复制到公开文件。
