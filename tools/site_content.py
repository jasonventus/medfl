# Single source for the MedFL site: facts, statuses, results (null until published) and ko/en/zh copy.
# Results come from tools/results_data.py (copied from the experiment summaries).
# build_site.py turns DATA into data/medfl-data.{json,js} (read by every page) and PAGE into index/en/zh.html.

from results_data import PER_CLASS, METHODS, EPS, DELTA

PRIV = 'https://github.com/jasonventus/healthcare-ai-project05/blob/'
R23, R4, R12 = '84ab6a2e9433db4023fe40629eff7814c2d09043', 'b24f91f554e6e998fb79f4af87edb4a7ca275f5e', 'edeec2bf2aaa66a0dd082ed0d1d308884229a34d'
EV = {
    'r23_report': PRIV + R23 + '/experiments/2026-11-03_round2-3_fedisic/REPORT.md',
    'r23_class': PRIV + R23 + '/src/runs_fedisic/round3_summary/per_class_dp_cost.csv',
    'r23_methods': PRIV + R23 + '/src/runs_fedisic/round3_summary/methods_eps3.csv',
    'r4_report': PRIV + R4 + '/experiments/2026-11-03_round4_all-experiments/REPORT.md',
    'r4_main': PRIV + R4 + '/src/runs_fedisic/round4_isic_summary/main.csv',
    'r4_mia': PRIV + R4 + '/src/runs_fedisic/round4_mia_summary/metrics.json',
    'r4_chest': PRIV + R4 + '/src/runs_fedisic/round4_chest_summary/main.csv',
    'r12_report': PRIV + R12 + '/experiments/2026-11-07_round10-12_course-target/REPORT.md',
    'flamby': 'https://github.com/owkin/FLamby/blob/main/flamby/datasets/fed_isic2019/README.md',
    'opacus': 'https://opacus.ai/docs/faq',
    'fedavg': 'https://arxiv.org/abs/1602.05629',
}

EV_LABEL = {
    'r23_report': {'zh': '第 2–3 轮报告', 'ko': '2–3차 보고서', 'en': 'Rounds 2–3 report'},
    'r23_class': {'zh': '类别 DP 代价 CSV', 'ko': '클래스별 DP 비용 CSV', 'en': 'Per-class DP cost CSV'},
    'r23_methods': {'zh': '方法对照 CSV', 'ko': '방법 비교 CSV', 'en': 'Method comparison CSV'},
    'r4_report': {'zh': '第 4 轮报告', 'ko': '4차 보고서', 'en': 'Round 4 report'},
    'r4_main': {'zh': '第 4 轮主表', 'ko': '4차 주 표', 'en': 'Round 4 main table'},
    'r4_mia': {'zh': '成员推断攻击汇总', 'ko': '멤버십 추론 요약', 'en': 'Membership-inference summary'},
    'r4_chest': {'zh': '胸片主表', 'ko': '흉부 영상 주 표', 'en': 'Chest main table'},
    'r12_report': {'zh': '第 10–12 轮报告', 'ko': '10–12차 보고서', 'en': 'Rounds 10–12 report'},
}

STATUS = {  # enumerated review states; every badge shows a symbol and text, never colour alone
    'submitted': {'sym': '●', 'zh': '已提交', 'ko': '제출됨', 'en': 'Submitted'},
    'pending_review': {'sym': '◐', 'zh': '待复核', 'ko': '검토 대기', 'en': 'Pending review'},
    'reviewed': {'sym': '✓', 'zh': '已复核', 'ko': '검토 완료', 'en': 'Reviewed'},
    'not_started': {'sym': '○', 'zh': '尚未开展', 'ko': '시작 전', 'en': 'Not started'},
    'not_required': {'sym': '–', 'zh': '无需复核', 'ko': '검토 불필요', 'en': 'Review not required'},  # project lead's decision, 2026-11-09
}


def T(zh, ko, en):
    return {'zh': zh, 'ko': ko, 'en': en}


SPLIT = 'Fed-ISIC2019 (FLamby): train 18,597 in 6 clients / test 4,650 pooled'


ROUND4_ONLY = {'B1', 'B5', 'P1-block', 'P1-block+LA'}
ISIC_ORDER = ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'P1', 'P1-block', 'P2', 'P2-PCA', 'P2-LA', 'P1-block+LA']


def isic_result(m):
    d, pc = METHODS[m], {r['class']: r for r in PER_CLASS}
    per_class = {c: r[m][0] for c, r in pc.items()} if m in ('B0', 'B2', 'B3', 'P1') else {'DF': d['DF'][0], 'VASC': d['VASC'][0]}
    return {'experiment_id': 'isic-' + m, 'method_version': 'submitted', 'data_split': SPLIT, 'dp': EPS[m] is not None,
            'metrics': {'per_class_recall': per_class, 'balanced_acc': d['balanced_acc'][0], 'balanced_acc_sd': d['balanced_acc'][1],
                        'macro_f1': d['macro_f1'][0], 'macro_f1_sd': d['macro_f1'][1], 'minority_recall': d['minority_mean'][0],
                        'minority_recall_sd': d['minority_mean'][1], 'unit': 'percent, mean and sample SD over seeds'},
            'seeds': d['seeds'], 'epsilon': EPS[m], 'delta': DELTA if EPS[m] is not None else None, 'source_date': '2026-11-03',
            'status': 'submitted', 'review_status': 'not_required', 'evidence': ['r4_main'] if m in ROUND4_ONLY else ['r23_methods', 'r23_class']}


OTHER_RESULTS = [
    {'experiment_id': 'mia-r4', 'method_version': 'submitted', 'data_split': 'Fed-ISIC2019: 2,315 members + 2,315 non-members per seed', 'dp': True,
     'metrics': {'attack_auc_private_models': [0.501, 0.503], 'attack_auc_centralized': 0.613, 'attack_auc_overfit_control': 0.864},
     'seeds': 3, 'epsilon': None, 'delta': DELTA, 'source_date': '2026-11-03', 'status': 'submitted', 'review_status': 'not_required', 'evidence': ['r4_mia', 'r4_report']},
    {'experiment_id': 'chest-hernia', 'method_version': 'submitted', 'data_split': 'NIH ChestX-ray14: 10 hospital settings (K=3 with α∈{0.1,0.5,1}, K=5 and K=10 at α=0.5; Hernia spread or concentrated)', 'dp': True,
     'metrics': {'settings_hernia_cost_above_top3': '10/10', 'settings_paired_ci_excludes_0': 7, 'settings_significant_after_holm': 5,
                 'mean_auc_14_labels_nondp': [0.612, 0.661], 'mean_auc_14_labels_dp': [0.528, 0.575]},
     'seeds': 3, 'epsilon': None, 'delta': DELTA, 'source_date': '2026-11-03', 'status': 'submitted', 'review_status': 'not_required', 'evidence': ['r4_chest', 'r4_report']},
    {'experiment_id': 'pathmnist-course', 'method_version': 'submitted', 'data_split': 'PathMNIST: 3 non-IID nodes, image-patch-level DP', 'dp': True,
     'metrics': {'accuracy_retention_general_encoders_percent': [96.11, 96.77], 'accuracy_retention_phikon_v2_percent': [99.57, 0.62],
                 'denominator': 'best centralized head on the same encoder'},
     'seeds': 3, 'epsilon': 2.9985, 'delta': None, 'source_date': '2026-11-07', 'status': 'submitted', 'review_status': 'not_required', 'evidence': ['r12_report']},
]


DATA = {
    'schema': 'medfl-site-data/1',
    'public_record_date': '2026-11-09',
    'previous_public_record': '2026-11-03',
    'status': STATUS,
    'evidence': EV,
    'evidence_labels': EV_LABEL,
    'results': [isic_result(m) for m in ISIC_ORDER] + OTHER_RESULTS,
    'charts': [
        {'id': 'dp-cost-by-class', 'results': ['isic-B2', 'isic-B3'], 'evidence': ['r23_class'],
         'title': T('图表 ①　B2 与 B3 各类别召回率：隐私代价差异',
                    '그래프 ①　B2와 B3의 클래스별 재현율: 프라이버시 비용 차이',
                    'Chart ①　Per-class recall, B2 vs B3: the cost of privacy')},
        {'id': 'minority-vs-overall', 'results': ['isic-B2', 'isic-B3', 'isic-P1', 'isic-P2', 'isic-P2-PCA', 'isic-P2-LA'], 'evidence': ['r23_methods', 'r4_main'],
         'title': T('图表 ②　B3 / P1 / P2 / P2 变体：少数类别召回率与平衡准确率、Macro-F1',
                    '그래프 ②　B3 / P1 / P2 / P2 변형: 소수 클래스 재현율과 균형 정확도·Macro-F1',
                    'Chart ②　B3 / P1 / P2 / P2 variants: minority recall vs balanced accuracy and macro-F1')},
    ],
    'methods': [
        # id, main row?, status, date, name, submitted implementation, original design, hypothesis
        {'id': 'B2', 'main': True, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('B2 普通联邦', 'B2 일반 연합학습', 'B2 Plain federated'),
         'sub': T('6 个客户端用联邦平均训练全模型，不加隐私保护', '6개 클라이언트가 연합 평균으로 전체 모델을 학습, 프라이버시 보호 없음', 'Six clients train the full model with federated averaging, no privacy protection'),
         'orig': T('同左', '왼쪽과 같음', 'Same'),
         'hyp': T('不加隐私时的联邦参照', '프라이버시 없는 연합학습 기준', 'Federated reference without privacy')},
        {'id': 'B3', 'main': True, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('B3 全量 DP 联邦', 'B3 전체 DP 연합학습', 'B3 Full-model DP federated'),
         'sub': T('同 B2，每个客户端用 DP-SGD 训练', 'B2와 같고 각 클라이언트가 DP-SGD로 학습', 'As B2, with DP-SGD on every client'),
         'orig': T('同左', '왼쪽과 같음', 'Same'),
         'hyp': T('RQ1：隐私保护是否让少数类别损失更大', 'RQ1: 프라이버시 보호가 소수 클래스에 더 큰 손실을 주는가', 'RQ1: does privacy cost minority classes more?')},
        {'id': 'P1', 'main': True, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('P1 冻结特征 + DP 分类头', 'P1 고정 특징 + DP 분류기', 'P1 Frozen features + DP head'),
         'sub': T('冻结 ImageNet 预训练特征，只用 DP 训练分类头', 'ImageNet 사전학습 특징을 고정하고 분류기만 DP로 학습', 'Frozen ImageNet-pretrained features; only the head is trained with DP'),
         'orig': T('冻结大部分参数，最后一个 block 或 LoRA 与分类头一起 DP 微调', '대부분 고정하고 마지막 block 또는 LoRA를 분류기와 함께 DP 미세조정', 'Freeze most parameters; DP fine-tune the last block or LoRA together with the head'),
         'hyp': T('少训练参数能否减轻噪声伤害', '학습 파라미터를 줄이면 노이즈 피해가 줄어드는가', 'Do fewer trainable parameters soften the noise?')},
        {'id': 'P2', 'main': True, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('P2 均衡虚拟特征', 'P2 균형 가상 특징', 'P2 Balanced virtual features'),
         'sub': T('在 P1 上发布加噪类别摘要，构造均衡虚拟特征，重训分类头', 'P1 위에서 노이즈 클래스 요약을 공개하고 균형 가상 특징으로 분류기 재학습', 'On top of P1: release noisy class summaries, build balanced virtual features, retrain the head'),
         'orig': T('同左', '왼쪽과 같음', 'Same'),
         'hyp': T('RQ2：类别均衡能否提高少数类别召回', 'RQ2: 클래스 균형이 소수 클래스 재현율을 높이는가', 'RQ2: does balancing raise minority recall?')},
        {'id': 'B0', 'main': False, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('B0 集中训练', 'B0 중앙 학습', 'B0 Centralized'),
         'sub': T('把全部训练图像放在一起训练全模型，不加隐私保护', '모든 학습 이미지를 한곳에 모아 전체 모델 학습, 프라이버시 보호 없음', 'Pool all training images and train the full model, no privacy protection'),
         'orig': T('同左', '왼쪽과 같음', 'Same'),
         'hyp': T('性能上限参照', '성능 상한 기준', 'Upper reference')},
        {'id': 'B1', 'main': False, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('B1 单客户端 DP', 'B1 단일 클라이언트 DP', 'B1 Single-client DP'),
         'sub': T('每个客户端只用自己的图像做 DP 训练，不协作（第 4 轮）', '각 클라이언트가 자기 이미지로만 DP 학습, 협력 없음 (4차)', 'Each client trains with DP on its own images only (round 4)'),
         'orig': T('同左', '왼쪽과 같음', 'Same'),
         'hyp': T('协作是否有帮助', '협력이 도움이 되는가', 'Does collaboration help?')},
        {'id': 'B4', 'main': False, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('B4 类别加权', 'B4 클래스 가중', 'B4 Class-weighted'),
         'sub': T('加权 P1：P1 的分类头按类别加权', '가중 P1: P1 분류기에 클래스 가중치 적용', 'Weighted P1: class weights on the P1 head'),
         'orig': T('加权 B3（旧设计表）；不与本轮 B4 放在同一行比较', '가중 B3(이전 설계표). 이번 B4와 같은 행에서 비교하지 않음', 'Weighted B3 (old design table); never compared in the same row as this round’s B4'),
         'hyp': T('简单重加权能否补偿少数类别', '단순 재가중으로 소수 클래스를 보완할 수 있는가', 'Can simple reweighting compensate minority classes?')},
        {'id': 'B5', 'main': False, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('B5 自适应裁剪', 'B5 적응형 클리핑', 'B5 Adaptive clipping'),
         'sub': T('把 DPSGD-F（按类别自适应裁剪）用在 P1 分类头（第 4 轮）', 'DPSGD-F(클래스별 적응형 클리핑)를 P1 분류기에 적용 (4차)', 'DPSGD-F (class-adaptive clipping) on the P1 head (round 4)'),
         'orig': T('DPSGD-F 自适应裁剪基线', 'DPSGD-F 적응형 클리핑 기준선', 'DPSGD-F adaptive-clipping baseline'),
         'hyp': T('按类别调整裁剪能否减少少数类别损失', '클래스별 클리핑 조정이 소수 클래스 손실을 줄이는가', 'Does class-aware clipping reduce the minority loss?')},
        {'id': 'P1-block', 'main': False, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('P1-block', 'P1-block', 'P1-block'),
         'sub': T('最后一个 block 与分类头一起 DP 微调（第 4 轮）', '마지막 block과 분류기를 함께 DP 미세조정 (4차)', 'DP fine-tuning of the last block together with the head (round 4)'),
         'orig': T('即原设计 P1 的 block 版', '원 설계 P1의 block 버전', 'The block variant of the original P1'),
         'hyp': T('多放开一个 block 是否更好', 'block 하나를 더 학습하면 나아지는가', 'Does unfreezing one block help?')},
        {'id': 'P1-LoRA', 'main': False, 'status': 'not_started', 'date': None,
         'name': T('P1-LoRA', 'P1-LoRA', 'P1-LoRA'),
         'sub': T('尚未实现', '아직 구현하지 않음', 'Not implemented yet'),
         'orig': T('LoRA 与分类头一起 DP 微调', 'LoRA와 분류기를 함께 DP 미세조정', 'DP fine-tuning of LoRA together with the head'),
         'hyp': T('低秩微调能否在同样预算下学得更好', '저랭크 미세조정이 같은 예산에서 더 잘 배우는가', 'Does low-rank tuning learn better at the same budget?')},
        {'id': 'P2-PCA', 'main': False, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('P2-PCA', 'P2-PCA', 'P2-PCA'),
         'sub': T('先用公开辅助特征（DermaMNIST）拟合 PCA 降维，再在低维空间做 P2', '공개 보조 특징(DermaMNIST)으로 PCA 차원 축소를 맞춘 뒤 저차원에서 P2 수행', 'Fit PCA on public auxiliary features (DermaMNIST), then run P2 in the reduced space'),
         'orig': T('原设计没有此项（本轮修正尝试）', '원 설계에 없음 (이번 수정 시도)', 'Not in the original design (a fix attempted this round)'),
         'hyp': T('降维后加噪摘要是否更稳定', '차원을 줄이면 노이즈 요약이 더 안정적인가', 'Are noisy summaries steadier in fewer dimensions?')},
        {'id': 'P2-LA', 'main': False, 'status': 'submitted', 'date': '2026-11-03',
         'name': T('P2-LA', 'P2-LA', 'P2-LA'),
         'sub': T('用 DP 类别计数校正预测分数（Logit Adjustment）；不发布特征和，不重训分类头', 'DP 클래스 개수로 예측 점수를 보정(Logit Adjustment). 특징 합을 공개하지 않고 분류기도 다시 학습하지 않음', 'Adjust prediction scores with DP class counts (logit adjustment); no feature sums released, no retraining'),
         'orig': T('原设计没有此项（本轮修正尝试）', '원 설계에 없음 (이번 수정 시도)', 'Not in the original design (a fix attempted this round)'),
         'hyp': T('只用计数校正能否改善少数类别', '개수 보정만으로 소수 클래스가 나아지는가', 'Can count-based correction alone help minority classes?')},
    ],
    'work': [  # submitted work, newest last
        {'date': '2026-11-03', 'status': 'submitted', 'review': 'pending_review', 'ev': 'r23_report',
         'text': T('Fed-ISIC 对照实验：B0、B2、B3、P1，多个随机种子（第 2–3 轮）', 'Fed-ISIC 대조 실험: B0·B2·B3·P1, 여러 시드 (2–3차)', 'Fed-ISIC baselines: B0, B2, B3 and P1 with several seeds (rounds 2–3)')},
        {'date': '2026-11-03', 'status': 'submitted', 'review': 'pending_review', 'ev': 'r23_methods',
         'text': T('P2 与两种修正：P2-PCA、P2-LA（第 3 轮）', 'P2와 두 가지 수정: P2-PCA·P2-LA (3차)', 'P2 and two fixes: P2-PCA and P2-LA (round 3)')},
        {'date': '2026-11-03', 'status': 'submitted', 'review': 'pending_review', 'ev': 'r4_report',
         'text': T('B1、B5、P1-block、成员推断攻击、胸片训练（第 4 轮）', 'B1·B5·P1-block·멤버십 추론 공격·흉부 영상 학습 (4차)', 'B1, B5, P1-block, membership-inference attacks and chest X-ray training (round 4)')},
        {'date': '2026-11-07', 'status': 'submitted', 'review': 'pending_review', 'ev': 'r12_report',
         'text': T('PathMNIST 课程设置（3 个节点）实验与更强的公开特征提取器（第 10–12 轮）', 'PathMNIST 과목 설정(3개 노드) 실험과 더 강한 공개 특징 추출기 (10–12차)', 'PathMNIST course setting (3 nodes) and stronger public feature extractors (rounds 10–12)')},
    ],
    'observations': [
        {'date': '2026-11-03', 'text': T('B2→B3：DF 召回 52.1%→0、VASC 76.3%→0，平均降 64.2 个百分点；NV 只降 0.3。', 'B2→B3: DF 재현율 52.1%→0, VASC 76.3%→0으로 평균 64.2%p 하락, NV는 0.3%p 하락.', 'B2→B3: DF recall 52.1%→0 and VASC 76.3%→0, a 64.2-point average drop; NV drops 0.3.')},
        {'date': '2026-11-03', 'text': T('原版 P2 平衡准确率 17.1%，低于 P1 的 30.3%；P2-PCA 把 DF 召回提到 37.6%，Macro-F1 却只有 4.0%；P2-LA 31.1%，为加隐私方案中最高。', '원래 P2의 균형 정확도는 17.1%로 P1(30.3%)보다 낮고, P2-PCA는 DF 재현율을 37.6%로 올렸지만 Macro-F1이 4.0%입니다. P2-LA는 31.1%로 프라이버시를 적용한 10개 방법 중 가장 높습니다.', 'Original P2 reaches 17.1% balanced accuracy, below P1’s 30.3%; P2-PCA lifts DF recall to 37.6% but macro-F1 falls to 4.0%; P2-LA scores 31.1%, the best of the 10 private setups.')},
        {'date': '2026-11-03', 'text': T('胸片：10 种医院设置中，疝气的 AUC 代价都大于最常见的 3 个标签（Holm 校正后 5 种显著）；14 个标签平均 AUC 从 0.612–0.661 降到 0.528–0.575。', '흉부 영상: 병원 설정 10개 모두에서 탈장의 AUC 비용이 가장 흔한 레이블 3개보다 컸고, Holm 보정 후 5개가 유의했습니다. 레이블 14개의 평균 AUC는 0.612–0.661에서 0.528–0.575로 떨어졌습니다.', 'Chest X-rays: in all 10 hospital settings Hernia lost more AUC than the three most common labels (5 remain significant after Holm); mean AUC over 14 labels fell from 0.612–0.661 to 0.528–0.575.')},
        {'date': '2026-11-03', 'text': T('成员推断攻击：加隐私模型的 AUC 为 0.501–0.503（随机猜测为 0.5），集中训练模型为 0.613，过拟合对照为 0.864。', '멤버십 추론 공격: 프라이버시 모델의 AUC는 0.501–0.503(무작위 추측 0.5), 중앙 학습 모델은 0.613, 과적합 대조군은 0.864입니다.', 'Membership inference: AUC 0.501–0.503 on the private models (0.5 is random guessing), 0.613 on the centralized model, 0.864 on an overfitted control.')},
        {'date': '2026-11-07', 'text': T('PathMNIST（3 个非 IID 节点，ε=2.9985，3 个种子）：DP 联邦分类头的准确率保留率为 96.11–96.77%（4 个通用公开编码器），达到课程目标 ≥95%；病理专用 Phikon-v2 为 99.57±0.62%。', 'PathMNIST(비IID 노드 3개, ε=2.9985, 시드 3개): DP 연합 분류기의 정확도 유지율은 일반 공개 인코더 4개에서 96.11–96.77%로 과목 목표 ≥95%를 넘었고, 병리 전용 Phikon-v2는 99.57±0.62%입니다.', 'PathMNIST (3 non-IID nodes, ε=2.9985, 3 seeds): the DP federated head keeps 96.11–96.77% of centralized accuracy with four general public encoders, meeting the course target of ≥95%; the pathology-specific Phikon-v2 keeps 99.57±0.62%.')},
    ],
    'next': [
        {'status': 'not_started', 'text': T('把各方法的实际 ε 对齐（目前 2.2894–3.0000）后再比较', '방법별 실제 ε(현재 2.2894–3.0000)를 맞춘 뒤 다시 비교', 'Compare methods again at matched actual ε (now 2.2894–3.0000)')},
        {'status': 'not_started', 'text': T('补 LoRA 版 P1，并增加种子数', 'LoRA 버전 P1 추가, 시드 수 확대', 'Add the LoRA version of P1 and more seeds')},
        {'status': 'not_started', 'text': T('在 ISIC 上做分布变化实验', 'ISIC에서 분포 변화 실험', 'Run distribution-shift experiments on ISIC')},
    ],
    'todo': [
        {'status': 'not_started', 'text': T('对齐实际 ε 后重跑对照', '실제 ε를 맞춘 대조 재실행', 'Rerun comparisons at matched actual ε')},
        {'status': 'not_started', 'text': T('LoRA 版 P1', 'LoRA 버전 P1', 'LoRA version of P1')},
        {'status': 'not_started', 'text': T('ISIC 上的分布变化验证', 'ISIC 분포 변화 검증', 'Distribution-shift validation on ISIC')},
    ],
    'datasets': [
        {'id': 'imagenet', 'name': 'ImageNet', 'status': None,
         'role': T('预训练特征', '사전학습 특징', 'Pretrained features'),
         'text': T('提供初始图像特征；本轮 P1 冻结这部分。', '처음 이미지 특징을 제공합니다. 이번 P1은 이 부분을 고정합니다.', 'Supplies the starting image features; this round’s P1 keeps them frozen.')},
        {'id': 'dermamnist', 'name': 'DermaMNIST', 'status': None,
         'role': T('选参与辅助', '하이퍼파라미터 선택·보조', 'Tuning and auxiliary'),
         'text': T('只用来选超参数和拟合 P2-PCA 的降维；已剔除与 ISIC 测试集重叠的图片。', '하이퍼파라미터 선택과 P2-PCA 차원 축소에만 씁니다. ISIC 시험 세트와 겹치는 이미지는 뺐습니다.', 'Used only to choose hyperparameters and fit the P2-PCA projection; images overlapping the ISIC test set were removed.')},
        {'id': 'pathmnist', 'name': 'PathMNIST', 'status': 'submitted',
         'role': T('流程验证', '파이프라인 점검', 'Pipeline check'),
         'text': T('早期流程检查（11-02）；11-07 课程设置（3 个节点）实验：准确率保留率 96.11–96.77%，达到 ≥95%。', '초기 파이프라인 점검(11-02). 11-07 과목 설정(3개 노드) 실험: 정확도 유지율 96.11–96.77%로 ≥95% 달성.', 'Early pipeline check (Nov 2); course setting with 3 nodes (Nov 7): accuracy retention 96.11–96.77%, meeting ≥95%.')},
        {'id': 'chestxray14', 'name': 'NIH ChestX-ray14', 'status': 'submitted',
         'role': T('扩展数据', '확장 데이터', 'Extension'),
         'text': T('公开胸片 112,120 张、30,805 名患者；10 种医院设置（K=3/5/10）的胸片训练已完成。', '공개 흉부 X선 112,120장, 환자 30,805명. 병원 설정 10개(K=3/5/10)의 흉부 영상 학습 완료.', 'Public chest X-rays: 112,120 images, 30,805 patients. Chest training done in 10 hospital settings (K=3/5/10).')},
    ],
}

# strings for the shared components (assets/medfl.js, assets/kids.js) and the explain/progress overrides
DATA['i18n'] = {
    'zh': {
        'round': {
            'aria': '一轮联邦训练示意：6 个客户端与服务器', 'server': '服务器', 'agg': '加权平均 → 下一轮模型', 'client': '客户端',
            'local': '图像留在本地', 'dp1': 'DP-SGD', 'dp2': '逐样本裁剪 + 加噪',
            'down': '↓ 模型参数', 'up': '↑ 受保护的模型更新', 'stats': '↑ 加噪类别统计（仅 P2，一次）', 'agg2': 'P2：均衡虚拟特征 → 重训分类头',
            'steps': ['下发模型', '本地训练', '上传更新', '服务器聚合'],
            'titles': ['服务器把当前模型发给 6 个客户端', '各客户端在本地训练：DP-SGD 逐样本梯度裁剪 + 加噪', '只上传受保护的模型更新', '服务器加权平均，得到下一轮模型'],
            'copies': ['发出的是模型参数，不含任何图像。', '每一步训练先限制每张图像的梯度贡献，再加入高斯噪声。图像始终留在本地。', '上传的是用 DP-SGD 训练后的模型参数，不是图像。P2 在第一阶段训练结束后，另外一次性上传加噪的类别统计。', '按各客户端样本量加权平均（FedAvg），发回去再练，重复多轮。P2 最后再用加噪统计构造均衡虚拟特征、重训分类头。效果要用测试集评价。'],
            'prev': '◀ 上一步', 'next': '下一步 ▶', 'play': '▶ 自动播放', 'pause': '❚❚ 暂停', 'p2': '显示 P2 额外上传的类别统计', 'tag': '流程示意 · 不是实验结果'},
        'noise': {
            'tag': '概念示意强度（非真实 ε 或准确率数值）', 'label': '调节示意噪声强度', 'low': '低', 'high': '高', 'unit': '示意强度',
            'common': '● 常见类别 · 信号多', 'rare': '◆ 少数类别 · 信号少',
            'states': ['干扰较少：两边的示意信号都容易看清。', '同一层干扰下，数量少的菱形更难辨认。', '干扰很强：两边都被遮住；少数类别实际受多大影响，要看实验。'],
            'note': '滑块只改变图层遮挡，不运行 DP，也不对应真实 ε 或准确率。'},
        'kids': {
            'server': '老师（服务器）', 'box': '箱子', 'stay': '照片留在箱子里', 'legend': ['● 常见的斑点：照片很多', '◆ 少见的斑点：照片很少'],
            'memory': '机器人的记忆', 'commonOk': '常见斑点：记得住 ✓', 'rareLost': '少见斑点：容易忘 ✗', 'illus': '示意图，不是真实数字',
            'tryT': '我们在试的办法', 'tries': ['P2：交换受保护的类别摘要', 'P2-PCA：先压缩，再交换', 'P2-LA：用数量校正答案'], 'checking': '◐ 结果还在等同学检查',
            'steps': [
                ['这是什么？', '电脑要学会认 8 种皮肤斑点。有的斑点照片很多（棕色圆点），有的很少（紫色菱形）。'],
                ['照片不出门', '照片分放在 6 个箱子里（模拟 6 个来源），一张也不拿出来。'],
                ['机器人分身去学习', '老师（服务器）把小机器人（模型）复制成 6 个，每个箱子一个，同时看照片学习。'],
                ['边学边撒雾', '机器人每学一步，都撒一点“雾”（噪声），谁也看不出某一张照片在不在里面。这叫差分隐私。'],
                ['只带回笔记', '机器人只把“学习笔记”（模型参数）交给老师，老师把 6 份笔记合成一份。照片一直留在箱子里。这叫联邦学习。'],
                ['少的更容易忘', '雾一样大，照片少的斑点更容易被忘掉。这是实验里看到的现象，图是示意。'],
                ['我们在想办法', '我们试了几种办法，让少见的斑点也被记住。目前只有小的改善，结果还在等同学检查。']],
            'prev': '◀ 上一步', 'next': '下一步 ▶', 'play': '▶ 播放', 'pause': '❚❚ 暂停', 'stepOf': '第', 'stage': '联邦学习与差分隐私的动画说明'},
    },
    'ko': {
        'round': {
            'aria': '연합학습 한 라운드: 클라이언트 6개와 서버', 'server': '서버', 'agg': '가중 평균 → 다음 라운드 모델', 'client': '클라이언트',
            'local': '이미지는 로컬에', 'dp1': 'DP-SGD', 'dp2': '샘플별 클리핑+노이즈',
            'down': '↓ 모델 파라미터', 'up': '↑ 보호된 모델 업데이트', 'stats': '↑ 노이즈 클래스 통계(P2, 1회)', 'agg2': 'P2: 가상 특징으로 분류기 재학습',
            'steps': ['모델 보내기', '로컬 학습', '업데이트 올리기', '서버 집계'],
            'titles': ['서버가 현재 모델을 클라이언트 6개에 보냅니다', '각 클라이언트가 로컬에서 학습: DP-SGD 샘플별 그래디언트 클리핑 + 노이즈', '보호된 모델 업데이트만 올립니다', '서버가 가중 평균해 다음 라운드 모델을 만듭니다'],
            'copies': ['보내는 것은 모델 파라미터이며 이미지는 없습니다.', '학습의 매 단계에서 이미지 한 장의 그래디언트 기여를 제한한 뒤 가우스 노이즈를 더합니다. 이미지는 계속 로컬에 있습니다.', 'DP-SGD로 학습한 모델 파라미터를 올리며 이미지는 올리지 않습니다. P2는 1단계 학습이 끝난 뒤 노이즈를 더한 클래스 통계를 한 번 더 올립니다.', '클라이언트별 표본 수로 가중 평균(FedAvg)해 다시 보내고 여러 라운드 반복합니다. P2는 마지막에 노이즈 통계로 균형 가상 특징을 만들어 분류기를 다시 학습합니다. 효과는 시험 세트로 평가합니다.'],
            'prev': '◀ 이전', 'next': '다음 ▶', 'play': '▶ 자동 재생', 'pause': '❚❚ 멈춤', 'p2': 'P2가 추가로 올리는 클래스 통계 보기', 'tag': '흐름 설명 · 실험 결과 아님'},
        'noise': {
            'tag': '개념 설명용 강도 (실제 ε나 정확도 값이 아님)', 'label': '설명용 노이즈 강도 조절', 'low': '낮음', 'high': '높음', 'unit': '설명용 강도',
            'common': '● 흔한 클래스 · 신호 많음', 'rare': '◆ 소수 클래스 · 신호 적음',
            'states': ['간섭이 적으면 두 쪽 신호가 모두 잘 보입니다.', '같은 간섭에서도 수가 적은 마름모가 더 알아보기 어렵습니다.', '간섭이 강하면 두 쪽 모두 가려집니다. 소수 클래스가 실제로 얼마나 영향을 받는지는 실험으로 봅니다.'],
            'note': '슬라이더는 그림의 가림만 바꾸며, DP를 실행하지 않고 실제 ε나 정확도와 대응하지 않습니다.'},
        'kids': {
            'server': '선생님 (서버)', 'box': '상자', 'stay': '사진은 상자 안에', 'legend': ['● 흔한 점: 사진이 많아요', '◆ 드문 점: 사진이 적어요'],
            'memory': '로봇의 기억', 'commonOk': '흔한 점: 잘 기억해요 ✓', 'rareLost': '드문 점: 잘 잊어요 ✗', 'illus': '설명 그림이며 실제 숫자가 아니에요',
            'tryT': '우리가 시험하는 방법', 'tries': ['P2: 보호된 클래스 요약 주고받기', 'P2-PCA: 먼저 줄이고 주고받기', 'P2-LA: 개수로 답 고치기'], 'checking': '◐ 결과는 친구들이 확인 중',
            'steps': [
                ['무엇을 하나요?', '컴퓨터가 피부 점 8종류를 알아보도록 가르쳐요. 어떤 점은 사진이 많고(갈색 동그라미), 어떤 점은 적어요(보라색 마름모).'],
                ['사진은 밖으로 안 나가요', '사진은 상자 6개(서로 다른 출처 6곳을 흉내 냄)에 나뉘어 있고, 한 장도 꺼내지 않아요.'],
                ['로봇이 나눠서 공부해요', '선생님(서버)이 꼬마 로봇(모델)을 6개로 복사해 상자마다 하나씩 보내고, 로봇들이 동시에 사진을 보며 공부해요.'],
                ['공부하며 안개 뿌리기', '로봇은 한 걸음 배울 때마다 ‘안개’(노이즈)를 조금 뿌려요. 어떤 사진이 들어 있었는지 아무도 알 수 없어요. 이것이 차등 프라이버시예요.'],
                ['공부 노트만 가져와요', '로봇은 ‘공부 노트’(모델 파라미터)만 선생님에게 주고, 선생님은 노트 6개를 하나로 합쳐요. 사진은 계속 상자 안에 있어요. 이것이 연합학습이에요.'],
                ['적은 것은 잘 잊어요', '안개가 같아도 사진이 적은 점은 더 쉽게 잊혀요. 실험에서 본 현상이고, 그림은 설명용이에요.'],
                ['방법을 찾고 있어요', '드문 점도 기억하도록 여러 방법을 시험했어요. 아직 조금 나아진 정도이고, 결과는 친구들이 확인하고 있어요.']],
            'prev': '◀ 이전', 'next': '다음 ▶', 'play': '▶ 재생', 'pause': '❚❚ 멈춤', 'stepOf': '단계', 'stage': '연합학습과 차등 프라이버시 애니메이션 설명'},
    },
    'en': {
        'round': {
            'aria': 'One federated round: six clients and a server', 'server': 'Server', 'agg': 'Weighted average → next model', 'client': 'Client',
            'local': 'Images stay local', 'dp1': 'DP-SGD', 'dp2': 'per-sample clip+noise',
            'down': '↓ Model parameters', 'up': '↑ Protected model update', 'stats': '↑ Noisy class stats (P2, once)', 'agg2': 'P2: retrain on virtual features',
            'steps': ['Send model', 'Train locally', 'Upload update', 'Aggregate'],
            'titles': ['The server sends the current model to six clients', 'Each client trains locally: DP-SGD per-sample gradient clipping + noise', 'Only the protected model update goes up', 'The server averages the updates into the next model'],
            'copies': ['What travels is model parameters, never images.', 'At every training step, each image’s gradient contribution is capped, then Gaussian noise is added. The images never leave the client.', 'Clients upload the parameters trained with DP-SGD, not images. After the first stage, P2 also uploads noisy class statistics once.', 'Updates are averaged by client size (FedAvg), sent back, and the round repeats. At the end, P2 builds balanced virtual features from the noisy statistics and retrains the head. The test set decides whether it helped.'],
            'prev': '◀ Back', 'next': 'Next ▶', 'play': '▶ Autoplay', 'pause': '❚❚ Pause', 'p2': 'Show the class statistics P2 also uploads', 'tag': 'Flow illustration · not results'},
        'noise': {
            'tag': 'Concept intensity (not a real ε or accuracy value)', 'label': 'Illustrative noise intensity', 'low': 'Low', 'high': 'High', 'unit': 'Illustrative intensity',
            'common': '● Common class · many signals', 'rare': '◆ Minority class · few signals',
            'states': ['Little interference: both groups are easy to see.', 'With the same interference, the few diamonds are harder to pick out.', 'Strong interference hides both groups. How much minority classes really suffer is for the experiments to show.'],
            'note': 'The slider only changes a visual overlay; it runs no DP and maps to no real ε or accuracy.'},
        'kids': {
            'server': 'Teacher (server)', 'box': 'Box', 'stay': 'Photos stay in the boxes', 'legend': ['● Common spots: lots of photos', '◆ Rare spots: only a few photos'],
            'memory': 'Robots’ memory', 'commonOk': 'Common: remembered ✓', 'rareLost': 'Rare: easily forgotten ✗', 'illus': 'A sketch, not real numbers',
            'tryT': 'Ideas we are testing', 'tries': ['P2: share protected class summaries', 'P2-PCA: shrink first, then share', 'P2-LA: fix answers using counts'], 'checking': '◐ Teammates are still checking the results',
            'steps': [
                ['What is this?', 'We teach a computer to tell 8 kinds of skin spots apart. Some spots have lots of photos (brown dots); some have very few (purple diamonds).'],
                ['Photos stay put', 'The photos sit in 6 boxes (standing in for 6 sources). Not one photo is taken out.'],
                ['Robot copies study', 'The teacher (server) copies the little robot (the model) six times, one per box, and all six study their photos at the same time.'],
                ['Fog while studying', 'At every study step the robots sprinkle a little fog (noise), so nobody can tell whether one photo was used. This is differential privacy.'],
                ['Only notes travel', 'The robots hand only their study notes (model parameters) to the teacher, who merges the six notes into one. The photos never leave the boxes. This is federated learning.'],
                ['Few photos fade first', 'With the same fog, spots with few photos are forgotten more easily. We saw this in the experiments; the picture is a sketch.'],
                ['Looking for fixes', 'We tried several ideas to help the robots remember rare spots. So far the gains are small, and teammates are still checking.']],
            'prev': '◀ Back', 'next': 'Next ▶', 'play': '▶ Play', 'pause': '❚❚ Pause', 'stepOf': 'Step', 'stage': 'Animated explainer of federated learning and differential privacy'},
    },
}

# overrides merged into explain.html / progress.html copy objects (same keys those pages already use)
DATA['pages'] = {
    'explain': {
        'zh': {'notice': '研究计划与阶段进展 · 截至 11 月 9 日：实验结果已在首页公开。下面的点、噪声和流程是概念示意，没有真实患者数据，也不是临床工具。',
               'latest': '11 月 9 日更新：实验结果已公开，四步动画为 6 个客户端', 'latestLink': '查看最新进展 →',
               'flowLead': '点按四个步骤，看一轮联邦训练怎么走。图中 6 个客户端对应 Fed-ISIC2019 的 6 个来源分区；图像始终留在本地，本地训练用 DP-SGD。',
               'slider': '调节示意噪声强度（概念示意，非真实 ε 或准确率数值）',
               'evidenceTitle': '用实验回答：结果已在首页公开', 'end': '我们已从计划走到 Fed-ISIC 实验：结果和没有成功的尝试都公开在首页“进展”模块。'},
        'ko': {'notice': '연구 계획과 단계별 진행 · 11월 9일 기준: 실험 결과를 홈페이지에 공개했습니다. 아래 점·노이즈·흐름은 개념 설명이며 실제 환자 데이터나 임상 도구가 아닙니다.',
               'latest': '11월 9일 업데이트: 실험 결과 공개, 4단계 애니메이션은 클라이언트 6개', 'latestLink': '최신 진행 보기 →',
               'flowLead': '네 단계를 눌러 연합학습 한 라운드를 보세요. 클라이언트 6개는 Fed-ISIC2019의 출처 구획 6개에 대응합니다. 이미지는 계속 로컬에 있고, 로컬 학습은 DP-SGD로 합니다.',
               'slider': '설명용 노이즈 강도 조절 (개념 설명, 실제 ε나 정확도 값이 아님)',
               'evidenceTitle': '실험으로 답합니다: 결과는 홈페이지에 공개', 'end': '계획에서 Fed-ISIC 실험까지 진행했고, 결과와 실패한 시도를 홈페이지 ‘진행’ 모듈에 공개했습니다.'},
        'en': {'notice': 'Research plan and progress · As of Nov 9: experimental results are published on the homepage. The dots, noise and flows below are conceptual. No real patient data; not a clinical tool.',
               'latest': 'Nov 9 update: results published; the four-step animation shows six clients', 'latestLink': 'Read the latest progress →',
               'flowLead': 'Click through one federated round. The six clients match the six source partitions of Fed-ISIC2019; images stay local and local training uses DP-SGD.',
               'slider': 'Illustrative noise intensity (concept only, not a real ε or accuracy value)',
               'evidenceTitle': 'Experiments answer: results are on the homepage', 'end': 'We have moved from planning to Fed-ISIC experiments; results and failed attempts are published in the homepage Progress module.'},
    },
    'progress': {
        'zh': {'r4': '第 4 轮报告：B1、B5、P1-block、成员推断攻击、胸片（私有，需协作者登录）', 'r12': '第 10–12 轮报告：PathMNIST 课程设置（私有，需协作者登录）', 'log9': '11 月 9 日三语修改记录', 'nextTitle': '下一步', 'next': '把各方法的实际 ε 对齐后再比较；补 LoRA 版 P1 并增加种子数；在 ISIC 上做分布变化实验。',
               'status': '2026-11-09 · 成员提交 · 结果已公开 · 尚未合并研究 main',
               'lead': '范润堃已提交 Fed-ISIC 第 2–4 轮与课程设置（第 10–12 轮）实验。本页记录真实进展，也保留没有成功的尝试。',
               'scope': '本页记录进展与方法变化；具体数值见首页“进展”模块和 data/medfl-data.json。逐次日志和代码仍在私有研究库。',
               'stages': [['已提交', '01 · 流程预试验', 'PathMNIST 第一轮只作流程验证（11-02）。'],
                          ['已提交', '02 · Fed-ISIC 对照实验', 'B0、B2、B3、P1 各 3 个种子；B2→B3 时 DF/VASC 召回平均降 64.2 个百分点，NV 降 0.3（11-03）。'],
                          ['已提交', '03 · 第二阶段与修正尝试', '平衡准确率：P2 17.1%、P2-PCA 15.9%、P2-LA 31.1%。“实现了”不等于“解决了”（11-03）。'],
                          ['已提交', '04 · 补齐设计中的实验', 'B1、B5、P1-block、成员推断攻击、胸片 10 种设置（11-03 起）；PathMNIST 课程设置保留率 96.11–96.77%（11-07）。'],
                          ['尚未开展', '05 · 扩展', 'LoRA 版 P1；ISIC 上的分布变化验证；对齐实际 ε 后重跑对照。']],
               'findings': [['RQ1 · 本配置下成立', '加隐私后 DF/VASC 召回平均降 64.2 个百分点，NV 降 0.3；胸片 10 种设置中疝气的 AUC 代价都大于最常见的 3 个标签。结论限于当前公开数据模拟和固定配方。'],
                            ['RQ2 · 没有方案稳定解决', '10 种加隐私方案的平衡准确率都不超过 31.1%（P2-LA），不加隐私的联邦训练为 61.1%、集中训练为 73.9%。'],
                            ['RQ3 · 部分推进', '胸片的 10 种医院设置（K=3/5/10、疝气分散或集中）已完成；ISIC 上的分布变化验证尚未开展。']],
               'variants': {'P2': ['P2 · 受保护的特征和与计数', '在第一阶段模型之上，发布 DP 类别特征和、计数，再构造均衡虚拟特征重训分类器。报告中未得到稳定收益；对少样本类别，高维加噪摘要可能过于不稳定。'],
                            'P2-PCA': ['P2-PCA · 先用公开特征降维，再做摘要', '用 DermaMNIST 特征拟合 PCA，再在低维空间执行第二阶段。DermaMNIST 已剔除与 ISIC 测试集重叠的图片；两者都来自 HAM10000，留下的图片仍在 ISIC 训练集中。报告中部分少数类指标上升，但各类别表现不一致。'],
                            'P2-LA': ['P2-LA · 用受保护计数调整预测分数', '不发布第二阶段特征和，也不生成虚拟特征重训分类器；使用 DP 类别计数调整第一阶段预测分数。报告为有限改善；各方法的实际累计 ε 不完全相同，不能称为同一实际 ε 的严格比较。']},
               'changes': [['P1 的范围', '本轮 P1 使用固定 ImageNet 特征，只用 DP 训练分类头；第 4 轮另交了最后一个 block 与分类头共同微调的 P1-block。LoRA 版尚未开展。'],
                           ['B4 的定义', '本轮 B4 是 P1 加类别权重，不等于旧研究设计表中的 B3 加权。阅读对比时必须先核对实现。'],
                           ['BatchNorm', '本轮报告采用固定 ImageNet 统计量的 BatchNorm（eval），并非统一替换 GroupNorm；模块兼容性及隐私前提仍需技术复核。'],
                           ['数据使用', 'DermaMNIST 用于选参和 P2-PCA 降维，已剔除与 ISIC 测试图像的重叠，留下的图片仍在 ISIC 训练集中；NIH ChestX-ray14 在第 4 轮用于胸片训练。'],
                           ['关口与失败', 'B3 seed0 未达到原定继续关口。提交记录说明在保留原配方的情况下补齐种子，并保留这一偏离与失败记录；不能当作已通过关口。']]},
        'ko': {'r4': '4차 보고서: B1·B5·P1-block·멤버십 추론 공격·흉부 영상 (비공개, 협업자 로그인 필요)', 'r12': '10–12차 보고서: PathMNIST 과목 설정 (비공개, 협업자 로그인 필요)', 'log9': '11월 9일 3개 언어 변경 기록', 'nextTitle': '다음 단계', 'next': '방법별 실제 ε를 맞춘 뒤 다시 비교하고, LoRA 버전 P1과 시드를 추가하며, ISIC에서 분포 변화 실험을 합니다.',
               'status': '2026-11-09 · 구성원 제출 · 결과 공개 · 연구 main 미병합',
               'lead': '范润堃이 Fed-ISIC 2–4차와 과목 설정(10–12차) 실험을 제출했습니다. 이 페이지는 실제 진행을 기록하고, 성공하지 못한 시도도 남깁니다.',
               'scope': '이 페이지는 진행과 방법 변화를 기록합니다. 구체적 수치는 홈페이지 ‘진행’ 모듈과 data/medfl-data.json에 있고, 실행 로그와 코드는 비공개 연구 저장소에 있습니다.',
               'stages': [['제출됨', '01 · 파이프라인 예비 실험', 'PathMNIST 1차는 파이프라인 점검으로만 둡니다 (11-02).'],
                          ['제출됨', '02 · Fed-ISIC 대조 실험', 'B0·B2·B3·P1 각 시드 3개. B2→B3에서 DF/VASC 재현율이 평균 64.2%p, NV는 0.3%p 떨어졌습니다 (11-03).'],
                          ['제출됨', '03 · 2단계와 수정 시도', '균형 정확도 P2 17.1%, P2-PCA 15.9%, P2-LA 31.1%. ‘구현’이 ‘해결’은 아닙니다 (11-03).'],
                          ['제출됨', '04 · 설계의 나머지 실험', 'B1·B5·P1-block·멤버십 추론 공격·흉부 영상 10개 설정 (11-03부터), PathMNIST 과목 설정 유지율 96.11–96.77% (11-07).'],
                          ['시작 전', '05 · 확장', 'LoRA 버전 P1, ISIC 분포 변화 검증, 실제 ε를 맞춘 대조 재실행.']],
               'findings': [['RQ1 · 현재 설정에서 성립', '프라이버시를 넣으면 DF/VASC 재현율이 평균 64.2%p, NV는 0.3%p 떨어지고, 흉부 영상 10개 설정 모두에서 탈장의 AUC 비용이 가장 흔한 레이블 3개보다 큽니다. 현재 공개 데이터 시뮬레이션과 고정 레시피의 결과입니다.'],
                            ['RQ2 · 안정적으로 해결한 방법 없음', '프라이버시를 적용한 10개 방법의 균형 정확도는 모두 31.1%(P2-LA) 이하이며, 프라이버시 없는 연합학습은 61.1%, 중앙 학습은 73.9%입니다.'],
                            ['RQ3 · 일부 진행', '흉부 영상의 병원 설정 10개(K=3/5/10, 탈장 분산 또는 집중)는 완료했고, ISIC 분포 변화 검증은 시작 전입니다.']],
               'variants': {'P2': ['P2 · 보호된 특징 합과 개수', '1단계 모델 위에서 DP 클래스 특징 합과 개수를 공개하고, 균형 가상 특징을 만들어 분류기를 다시 학습합니다. 보고상 안정적 이득은 없었고, 표본이 적은 클래스에서는 고차원 노이즈 요약이 불안정할 수 있습니다.'],
                            'P2-PCA': ['P2-PCA · 공개 특징으로 먼저 차원 축소', 'DermaMNIST 특징으로 PCA를 맞춘 뒤 저차원에서 2단계를 수행합니다. ISIC 시험 세트와 겹치는 이미지는 뺐지만, 둘 다 HAM10000에서 왔으므로 남은 이미지는 ISIC 학습 세트에 들어 있습니다. 일부 소수 클래스 지표는 올랐으나 클래스별로 일정하지 않습니다.'],
                            'P2-LA': ['P2-LA · 보호된 개수로 예측 점수 보정', '2단계 특징 합을 공개하지 않고 가상 특징으로 다시 학습하지도 않습니다. DP 클래스 개수로 1단계 예측 점수를 보정합니다. 개선은 제한적이며, 방법마다 실제 누적 ε가 조금씩 달라 같은 실제 ε의 엄격한 비교라고 할 수 없습니다.']},
               'changes': [['P1의 범위', '이번 P1은 고정 ImageNet 특징 위에서 분류기만 DP로 학습합니다. 4차에서 마지막 block과 분류기를 함께 미세조정한 P1-block을 따로 제출했고, LoRA 버전은 시작 전입니다.'],
                           ['B4의 정의', '이번 B4는 클래스 가중 P1이며 이전 설계표의 가중 B3와 다릅니다. 비교 전에 구현을 먼저 확인합니다.'],
                           ['BatchNorm', 'ImageNet 통계를 고정한 BatchNorm(eval)을 썼으며 GroupNorm으로 일괄 교체하지 않았습니다. 모듈 호환성과 프라이버시 전제는 기술 검토가 필요합니다.'],
                           ['데이터 사용', 'DermaMNIST는 하이퍼파라미터 선택과 P2-PCA 차원 축소에 쓰고 ISIC 시험 이미지와의 중복을 뺐으며, 남은 이미지는 ISIC 학습 세트에 들어 있습니다. NIH ChestX-ray14는 4차 흉부 영상 학습에 썼습니다.'],
                           ['관문과 실패', 'B3 seed0은 계속 진행 관문에 미달했습니다. 원래 레시피를 유지한 채 시드를 채웠고 이 이탈과 실패 기록을 남겼습니다. 관문 통과로 보지 않습니다.']]},
        'en': {'r4': 'Round 4 report: B1, B5, P1-block, membership inference, chest X-ray (private, collaborator login)', 'r12': 'Rounds 10–12 report: PathMNIST course setting (private, collaborator login)', 'log9': 'Nov 9 trilingual change log', 'nextTitle': 'Next', 'next': 'Compare methods again at matched actual ε; add the LoRA version of P1 and more seeds; run distribution-shift experiments on ISIC.',
               'status': '2026-11-09 · Member submission · Results published · Not merged into research main',
               'lead': 'Fan Runkun has submitted Fed-ISIC rounds 2–4 and the course-setting runs (rounds 10–12). This page records real progress and keeps the attempts that did not work.',
               'scope': 'This page records progress and method changes; the numbers are in the homepage Progress module and data/medfl-data.json. Run logs and code stay in the private research repository.',
               'stages': [['Submitted', '01 · Pipeline pilot', 'The first PathMNIST round remains a pipeline check (Nov 2).'],
                          ['Submitted', '02 · Fed-ISIC baselines', 'B0, B2, B3 and P1 with 3 seeds each; from B2 to B3, DF/VASC recall drops 64.2 points on average and NV 0.3 (Nov 3).'],
                          ['Submitted', '03 · Second stage and fixes', 'Balanced accuracy: P2 17.1%, P2-PCA 15.9%, P2-LA 31.1%. Implemented is not the same as solved (Nov 3).'],
                          ['Submitted', '04 · Remaining designed experiments', 'B1, B5, P1-block, membership inference, chest X-rays in 10 settings (from Nov 3); PathMNIST course setting retains 96.11–96.77% (Nov 7).'],
                          ['Not started', '05 · Extensions', 'LoRA version of P1; distribution shift on ISIC; rerun comparisons at matched actual ε.']],
               'findings': [['RQ1 · Holds in this setup', 'With privacy, DF/VASC recall drops 64.2 points on average and NV 0.3; in all 10 chest settings Hernia loses more AUC than the three most common labels. This applies to the current public-data simulation and fixed recipe.'],
                            ['RQ2 · No method closes the gap', 'All 10 private setups stay at or below 31.1% balanced accuracy (P2-LA), against 61.1% for non-private federated training and 73.9% for centralized training.'],
                            ['RQ3 · Partly done', 'The 10 chest hospital settings (K=3/5/10, Hernia spread or concentrated) are done; distribution shift on ISIC has not started.']],
               'variants': {'P2': ['P2 · Protected feature sums and counts', 'On top of the first-stage model, release DP per-class feature sums and counts, build balanced virtual features and retrain the classifier. No stable gain was reported; for sparse classes, high-dimensional noisy summaries can be too unstable.'],
                            'P2-PCA': ['P2-PCA · Reduce dimensions with public features first', 'Fit PCA on DermaMNIST features, then run the second stage in fewer dimensions. Images overlapping the ISIC test set were removed, but both datasets come from HAM10000, so the remaining images sit inside the ISIC training set. Some minority metrics rose; class results were inconsistent.'],
                            'P2-LA': ['P2-LA · Adjust prediction scores with protected counts', 'No second-stage feature sums and no retraining on virtual features; DP class counts adjust the first-stage scores. Gains were limited, and actual cumulative ε differs slightly between methods, so this is not a strict same-ε comparison.']},
               'changes': [['Scope of P1', 'This round’s P1 trains only the classification head with DP on fixed ImageNet features. Round 4 separately submitted P1-block, which fine-tunes the last block with the head; the LoRA version has not started.'],
                           ['Definition of B4', 'This round’s B4 is class-weighted P1, not the weighted B3 of the old design table. Check the implementation before comparing.'],
                           ['BatchNorm', 'BatchNorm runs in eval mode with fixed ImageNet statistics rather than a blanket GroupNorm replacement. Module compatibility and privacy assumptions need technical review.'],
                           ['Data use', 'DermaMNIST serves hyperparameter selection and the P2-PCA projection; overlap with ISIC test images was removed and the remaining images sit inside the ISIC training set. NIH ChestX-ray14 was used for chest training in round 4.'],
                           ['Gates and failures', 'B3 seed 0 missed the planned continuation gate. The original recipe was kept, the seeds were completed, and the deviation is recorded. It does not count as passing the gate.']]},
    },
}
