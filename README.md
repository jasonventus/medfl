# MedFL · 한국어 / English / 中文

**https://jasonventus.github.io/medfl/**

[한국어](index.html) · [English](en.html) · [中文](zh.html)

## 한국어
공개 연구 소개 사이트입니다. 연구 계획은 검증된 임상 결과가 아닙니다. 웹사이트 수정은 본인의 GitHub 계정으로 로그인하고 협업자 권한으로 진행합니다. 개인 브랜치 → Pull Request → 다른 구성원 검토 → merge commit 순서를 사용합니다. main의 루트 폴더가 GitHub Pages에 자동 게시됩니다. 한국어·영어·중국어를 함께 갱신합니다.

연구 문서·미공개 실험은 [비공개 연구 저장소](https://github.com/jasonventus/healthcare-ai-project05)에 보관합니다. 이 저장소에는 공개 정적 HTML만 포함합니다. 환자 정보·비밀키·미공개 실험을 올리지 않습니다.

## English
Public research introduction, presenting a study plan rather than validated clinical results. Sign in with your own GitHub account and collaborator access to edit. Use a personal branch → Pull Request → review by another member → merge commit. GitHub Pages automatically publishes the root of main. Update Korean, English and Chinese together.

Research documents and unpublished experiments stay in the [private research repository](https://github.com/jasonventus/healthcare-ai-project05). This repository contains public static HTML only. Never upload patient information, credentials or unpublished experiments.

## 中文
公开研究介绍网站，展示研究计划，尚非已验证的临床结果。修改请使用自己的 GitHub 账号登录并获得协作者权限，采用个人分支 → Pull Request → 另一名成员评审 → merge commit。GitHub Pages 自动发布 main 根目录，请同步更新韩语、英语、中文。

研究文档及未公开实验保存在[私有研究仓库](https://github.com/jasonventus/healthcare-ai-project05)。本库仅含公开静态网页，不上传患者信息、凭据或未公开实验。

## 2026-11-09 · 홈페이지 개편 / Homepage redesign / 首页改版

[한국어](https://jasonventus.github.io/medfl/index.html) · [English](https://jasonventus.github.io/medfl/en.html) · [中文](https://jasonventus.github.io/medfl/zh.html) · [변경 기록 / Change log / 修改记录](RESEARCH_UPDATE_20261109.md)

한국어: 6개 모듈(무엇을 연구하나·데이터·공개 데이터 연합·방법·진행·요약)과 애니메이션 설명. 사실·상태·결과는 `tools/site_content.py` 한 곳에서 고치고 `python tools/build_site.py`로 세 언어 페이지와 `data/medfl-data.json`을 함께 다시 만듭니다. 실험 결과(12개 방법, 시드 3개)는 `tools/results_data.py`에서 읽어 그래프와 표로 공개합니다.

English: Six modules (question, data, public-data federation, methods, progress, summary) plus an animated explainer. Edit facts, statuses and results only in `tools/site_content.py`, then run `python tools/build_site.py` to regenerate all three pages and `data/medfl-data.json`. Results for the 12 setups (3 seeds) are read from `tools/results_data.py` and published as charts and a table.

中文：6 个模块（研究什么、数据、公开数据联邦、方法、进展、总结）和动画说明。事实、状态和结果只改 `tools/site_content.py`，再运行 `python tools/build_site.py` 同时重建三语页面和 `data/medfl-data.json`。12 种方案（3 个种子）的实验结果从 `tools/results_data.py` 读取，以图和表公开。

## Versions · 버전 · 历史版本
- [v1 한국어](versions/v1/index.html) · [v1 English](versions/v1/en.html) · [v1 中文](versions/v1/zh.html)
- [Before v2 한국어](versions/before-v2/index.html) · [Before v2 English](versions/before-v2/en.html) · [第二版前 中文](versions/before-v2/zh.html)
- [v2 + 11-03 한국어](versions/v2-design/index.html) · [v2 + Nov 3 English](versions/v2-design/en.html) · [第二版 + 11-03 中文](versions/v2-design/zh.html)

2026-11-02 · GitHub Pages로 이전하고 기존 공개 역사 페이지를 원문 보존했습니다. / Migrated to GitHub Pages and retained earlier public pages verbatim. / 迁移至 GitHub Pages，原样保留既有公开历史页面。

모든 commit은 파일 전체의 논리적 스냅샷입니다. / Each commit preserves a logical snapshot of all tracked files. / 每次 commit 均保留全部已跟踪文件的逻辑快照。
이력은 Commits → Browse files에서 확인합니다. / Inspect history through Commits → Browse files. / 通过 Commits → Browse files 查看历史；撤销使用 revert，禁止 force push、squash 或改写共享历史。


## Interactive tour · 인터랙티브 설명 · 公众互动讲解

[한국어](https://jasonventus.github.io/medfl/explain.html?lang=ko) · [English](https://jasonventus.github.io/medfl/explain.html?lang=en) · [中文](https://jasonventus.github.io/medfl/explain.html?lang=zh)

한국어: 4단계 연합학습·개념 노이즈 슬라이더·P1/P2·이해 확인을 제공합니다. 홈페이지 상단에서 시작하세요. 연구 효과는 미검증이며 환자 데이터는 없습니다.

English: Explore four federation steps, a conceptual noise slider, P1/P2 and a comprehension check. Start from the prominent homepage panel. Benefits remain unverified; no patient data is used.

中文：体验四步联邦训练、概念噪声滑块、P1/P2切换与理解检查。三语首页上方均有醒目入口。效果待验证，无患者数据。

[제작·변경 기록 / Production and change log / 制作与修改日志](PUBLIC_EXPLAINER_LOG.md)


## 2026-11-03 · 연구 진행 / Research progress / 研究进展

[한국어](https://jasonventus.github.io/medfl/progress.html?lang=ko) · [English](https://jasonventus.github.io/medfl/progress.html?lang=en) · [中文](https://jasonventus.github.io/medfl/progress.html?lang=zh)

한국어: 范润堃의 Fed-ISIC 2–3차 제출을 반영했습니다. 사람 검토 대기이며 상세 수치는 비공개입니다.

English: Reflects Fan Runkun’s Fed-ISIC rounds 2–3 submission. Human review is pending; detailed values remain private.

中文：已反映范润堃的 Fed-ISIC 第二、三轮提交，仍待人类复核，详细数值继续留在私有研究库。

[변경 기록 / Update log / 修改日志](RESEARCH_UPDATE_20261103.md)
