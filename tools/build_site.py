# Build index.html (ko), en.html, zh.html and data/medfl-data.{json,js} from tools/site_content.py.
# Run from anywhere: python tools/build_site.py   (no third-party packages)
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from site_content import DATA, EV  # noqa: E402

FILES = {'ko': 'index.html', 'en': 'en.html', 'zh': 'zh.html'}
CLASSES = ['MEL', 'NV', 'BCC', 'AK', 'BKL', 'DF', 'VASC', 'SCC']
MINOR = {'DF', 'VASC'}

PAGE = {
    'zh': dict(
        html_lang='zh-CN', title='MedFL · 隐私保护训练中的少数类别', desc='课题 05：用公开皮肤病变图像模拟 6 个客户端的联邦学习，研究隐私保护对少数类别识别的影响。',
        skip='跳到正文', toc_label='页面目录', record='最新公开记录', record_note='详细数值保存在私有研究库',
        toc=['研究什么', '数据', '公开数据联邦', '方法', '进展', '总结', '小学生版', '团队'],
        names={'MEL': '黑色素瘤', 'NV': '色素痣', 'BCC': '基底细胞癌', 'AK': '光化性角化病', 'BKL': '良性角化病', 'DF': '皮肤纤维瘤', 'VASC': '血管病变', 'SCC': '鳞状细胞癌'},
        answer='直接回答',
        m1=dict(eyebrow='课题 05 · 公开皮肤病变图像 · 隐私保护训练',
                h1='保护隐私时，样本少的皮肤病变类别会不会更容易被漏识别？',
                sub='我们用公开皮肤病变图像，在六个客户端中开展联邦学习模拟，研究隐私保护对少数类别*识别的影响，并比较缓解这种影响的方法。',
                note='* 少数类别：当前训练划分中样本占比较低的类别，本研究看皮肤纤维瘤（DF）和血管病变（VASC）；不等于临床罕见病。',
                a='目前的观察是：会。加入隐私保护后，皮肤纤维瘤和血管病变比常见的色素痣下降得多；试过的缓解办法还没有稳定改善。结果待复核。',
                b1='3 分钟看懂研究', b2='查看实验进展', repo='成员协作仓库', kids='小学生版动画',
                fig_img='皮肤病变图像', fig_img_note='示意图标，非真实病例', fig_model='模型', fig_model_note='提取图像特征 → 分类',
                fig_out='8 类预测概率', fig_minor='少数类别', fig_focus='关注：少数类别有没有被找回', fig_focus_note='召回率 = 这一类图像中被正确找回的比例',
                fig_cap='一张图进去，8 个类别各得一个概率；我们看少数类别的召回率。',
                det_t='技术细节：任务、指标与隐私单位',
                det=['任务：Fed-ISIC2019 的 8 类皮肤病变分类。',
                     '指标：逐类别召回率；平衡准确率（8 个类别召回率的平均）；Macro-F1（8 个类别 F1 的平均）。',
                     '隐私：图像/样本级差分隐私（DP-SGD 训练，RDP 记账），每个模型的目标上限 ε≤3。图像级保护不自动等于患者级保护。',
                     '适用范围：公开数据上的联邦模拟，6 个来源分区。']),
        m2=dict(q='我们研究的数据是什么？', a='主实验用 Fed-ISIC2019：23,247 张公开皮肤镜图像，8 个类别，按图像来源和成像设备分成 6 个分区。',
                stats=[('23,247', '张皮肤镜图像（官方规模）'), ('8', '个病变类别'), ('6', '个来源/成像设备分区'), ('18,597 / 4,650', '训练 / 测试（官方划分）')],
                io_in='输入：一张皮肤镜图像', io_out='输出：8 个类别的预测概率',
                aux_t='其他数据各做什么', det_t='技术细节：官方规模与本轮实际划分',
                split_head=['', '官方（FLamby）', '本轮实际'],
                split=[['总量', '23,247 张', '23,247 张'],
                       ['训练', '18,597 张，6 个客户端（每个 351–9,930 张）', '同官方；各客户端在本地训练'],
                       ['验证', '未单独划分', '不用 ISIC 图像；超参数在 DermaMNIST 上选'],
                       ['测试', '4,650 张，按客户端划分', '4,650 张；6 个客户端合并评价']],
                src='来源：FLamby Fed-ISIC2019 官方文档', ham='DermaMNIST 与 ISIC 都来自 HAM10000：剔除与 ISIC 测试集的重叠后，留下的 DermaMNIST 图片仍在 ISIC 训练集中。'),
        m3=dict(q='公开数据为什么还能做联邦学习？', a='我们使用可获取、可复现的公开数据，模拟数据分散在不同参与方的条件，比较不同协作训练与隐私保护方法。',
                cards=[('公开数据', '材料来源', '图像来自公开数据集，可下载核对；没有使用医院病历。'),
                       ('联邦学习', '分区协作', '图像留在各分区，本地训练后只把模型参数交给服务器合并，这叫联邦学习（FL）。'),
                       ('差分隐私', '限制单条记录的影响', '训练时限制每张图的影响并加噪，看不出某张图在不在里面，这叫差分隐私（DP）；预算 ε 越小保护越强。')],
                tabs=['视图 A · 实验准备', '视图 B · 一轮训练怎么走'],
                va_src='Fed-ISIC2019 公开数据集', va_src_note='23,247 张 · 8 类', va_map='按官方来源 / 成像设备映射', va_client='客户端', va_part='来源分区', va_local='本地训练集 + 本地测试集',
                va_note='每个分区有自己的训练集和测试集（共 18,597 / 4,650，固定划分）；不从 ISIC 划验证集。节点等大，只表示结构。',
                noise_t='为什么少数类别可能更吃亏？',
                det_t='技术细节：隐私设置',
                det=['联邦平均（FedAvg）：服务器按各客户端样本量加权平均模型参数。',
                     'DP-SGD：每一步先把每张图像的梯度裁剪到固定范数，再加高斯噪声；用 RDP 记账换算成 (ε, δ)，δ 固定。',
                     '保护单位：ISIC 实验为图像/样本级；胸片扩展实验为患者级。',
                     '预算：每个模型的目标上限 ε≤3；P2 的类别统计发布也计入预算。各方法的实际累计 ε 不完全相同，结果单列实际 ε、δ。',
                     'ε 只针对单个模型；多次重复与调参的整体发布没有合并计算。']),
        m4=dict(q='我们具体尝试了什么方法？', a='先用已有图像特征只训练分类部分（P1），再交换受保护的类别摘要，让分类器更均衡地学习（P2 及两个修正版）。',
                ver=['本轮实际提交版本', '查看原研究设计'], ver_note='本轮实现与原设计在 P1、B4、B5 上不同。',
                p1_t='P1 · 只训练最后负责分类的部分',
                p1_sub=[('图像', 'io'), ('特征提取器（ImageNet 预训练）', 'frozen'), ('分类头', 'train'), ('8 类概率', 'io')],
                p1_orig=[('图像', 'io'), ('特征提取器（大部分）', 'frozen'), ('最后一个 block 或 LoRA', 'train'), ('分类头', 'train'), ('8 类概率', 'io')],
                frozen='冻结', train='DP 训练',
                p1_cap_sub='本轮提交：特征提取器全部冻结，只有分类头用 DP 训练。',
                p1_cap_orig='原设计：最后一个 block 或 LoRA 与分类头一起用 DP 微调。block 版已在第 4 轮提交（P1-block），LoRA 版尚未开展。',
                p2_t='P2 · 交换受保护的类别摘要，再均衡地重训分类头',
                p2_steps=[('逐记录特征裁剪', ''), ('按类别求和与计数', ''), ('对汇总量加噪', ''), ('发布类别摘要', ''), ('构造均衡虚拟特征', '数值向量，不是图像'), ('重训分类头', '')],
                fix_t='后续修正尝试：P2-PCA 与 P2-LA',
                fixes=[('P2-PCA', '先用公开辅助特征（DermaMNIST）拟合 PCA 降维，再在低维空间做上面 6 步。DermaMNIST 已剔除与 ISIC 测试集重叠的图片；留下的图片仍在 ISIC 训练集中。', '观察：各类别有升有降。'),
                       ('P2-LA', '不发布特征和，也不重训分类头；用 DP 类别计数校正预测分数（Logit Adjustment）。', '观察：有限改善。')],
                table_t='核心方法表', th=['方法名称', '具体实现', '检验假设', '当前状态'], swipe='← 左右滑动查看 →',
                more_t='展开其余方法：B0、B1、B4、B5、P1-block、P1-LoRA、P2-PCA、P2-LA', vlab=['本轮：', '原设计：']),
        m5=dict(q='我们做到了哪一步，发现了什么？', a='对照、改进和扩展实验都已提交，待其他成员复核。目前只有 P2-LA 有有限改善，没有方法稳定解决少数类别的损失。',
                cols=['已提交工作', '当前观察', '下一步验证'], ev='证据', charts_t='两张结果图表',
                pending='数值待公开', null='待补充', fields=['实际 ε', 'δ', '随机种子数', '复核状态', '包含方法'], nodp='不加 DP（无 ε）', priv='私有库，需协作者登录',
                null_note='详细数值目前只在私有研究库；数据文件里对应字段为 null，页面显示“待补充”。',
                fill='公开数值时，只在 tools/site_content.py 的 results 里填写，再运行 python tools/build_site.py，三语页面和数据文件一起更新。', det_t='技术细节：结果对象（data/medfl-data.json）', det_head=['experiment_id', '数据划分', '实际 ε', 'δ', '种子', '日期', '状态']),
        m6=dict(q='总结与下一步',
                sum=['我们研究的是隐私保护训练对样本少的皮肤病变类别的影响。', '我们用公开数据和六客户端联邦模拟，比较实际训练方案与改进尝试。', '实验已经开展，部分观察和修正结果已提交，稳定改善仍需进一步验证。'],
                next_t='下一步重点', links_t='资料与历史版本',
                links=[('explain.html?lang=zh', '公众互动讲解（四步动画、噪声滑块、P1/P2）'), ('progress.html?lang=zh', '研究进展页'), ('versions/v2-design/zh.html', '改版前的首页（研究设计 v2，11-03）'),
                       ('versions/v1/zh.html', '最初网站 v1'), ('https://github.com/jasonventus/medfl', '网站源码（GitHub）')]),
        kids_t='附：给小学生的 1 分钟动画', kids_p='七个画面讲完我们在做什么。图是示意，不含实验数字。',
        team_t='团队', ai='AI 工具（Codex、Claude、Gemini）协助了实验、写作和网页制作；结论由成员负责，并接受复核。',
        team=[('范润堃', 'fanrunkun1', '项目负责人。指挥 AI 工具（Codex、Claude、Gemini）完成数据整理、实验、分析、可视化以及论文初稿和修改。'),
              ('金銀潔 김은결 (Kim eungyeul)', 'kimeg02', '撰写了本研究依据的实验设计书；小组计划中负责背景、文献和韩语沟通。'),
              ('郭津阳', 'guo03122-commits', '小组计划中负责联邦训练、聚合和差分隐私。'),
              ('张皓', 'jasonventus', '小组计划中负责评估、攻击测试、原型和整合；搭建了共享仓库和本网站。')],
        foot='课题 05 · 公开数据上的联邦模拟 · 没有使用医院病历'),
    'ko': dict(
        html_lang='ko', title='MedFL · 프라이버시 보호 학습과 소수 클래스', desc='과제 05: 공개 피부 병변 이미지로 클라이언트 6개의 연합학습을 모의 실험하고, 프라이버시 보호가 소수 클래스 인식에 주는 영향을 연구합니다.',
        skip='본문으로 건너뛰기', toc_label='페이지 목차', record='최신 공개 기록', record_note='상세 수치는 비공개 연구 저장소에 보관',
        toc=['무엇을 연구하나', '데이터', '공개 데이터 연합', '방법', '진행', '요약', '초등학생용', '팀'],
        names={'MEL': '흑색종', 'NV': '멜라닌세포 모반', 'BCC': '기저세포암', 'AK': '광선각화증', 'BKL': '양성 각화증', 'DF': '피부섬유종', 'VASC': '혈관 병변', 'SCC': '편평세포암'},
        answer='바로 답하면',
        m1=dict(eyebrow='과제 05 · 공개 피부 병변 이미지 · 프라이버시 보호 학습',
                h1='프라이버시를 보호하면, 표본이 적은 피부 병변은 더 쉽게 놓칠까요?',
                sub='공개 피부 병변 이미지로 클라이언트 6개의 연합학습을 모의 실험해, 프라이버시 보호가 소수 클래스* 인식에 주는 영향을 연구하고 이를 줄이는 방법을 비교합니다.',
                note='* 소수 클래스: 현재 학습 분할에서 표본 비율이 낮은 클래스. 이 연구는 피부섬유종(DF)과 혈관 병변(VASC)을 보며, 임상적 희귀 질환과 같지 않습니다.',
                a='지금까지의 관찰로는 그렇습니다. 프라이버시 보호를 넣으면 피부섬유종과 혈관 병변이 흔한 멜라닌세포 모반보다 크게 떨어지고, 시험한 완화 방법은 아직 안정적으로 개선하지 못했습니다. 결과는 검토 대기입니다.',
                b1='3분 만에 연구 이해하기', b2='실험 진행 보기', repo='구성원 협업 저장소', kids='초등학생용 애니메이션',
                fig_img='피부 병변 이미지', fig_img_note='설명용 아이콘, 실제 증례 아님', fig_model='모델', fig_model_note='이미지 특징 추출 → 분류',
                fig_out='8개 클래스 예측 확률', fig_minor='소수 클래스', fig_focus='중점: 소수 클래스를 찾아냈는가', fig_focus_note='재현율 = 그 클래스 이미지 중 올바르게 찾아낸 비율',
                fig_cap='이미지 한 장이 들어가면 8개 클래스마다 확률이 나오고, 우리는 소수 클래스의 재현율을 봅니다.',
                det_t='기술 세부: 과제, 지표, 프라이버시 단위',
                det=['과제: Fed-ISIC2019의 8개 클래스 피부 병변 분류.',
                     '지표: 클래스별 재현율, 균형 정확도(8개 클래스 재현율의 평균), Macro-F1(8개 클래스 F1의 평균).',
                     '프라이버시: 이미지/표본 단위 차등 프라이버시(DP-SGD 학습, RDP 회계), 모델마다 목표 상한 ε≤3. 이미지 단위 보호가 곧 환자 단위 보호는 아닙니다.',
                     '적용 범위: 공개 데이터의 연합학습 모의 실험, 출처 구획 6개.']),
        m2=dict(q='어떤 데이터를 연구하나요?', a='주 실험은 Fed-ISIC2019입니다. 공개 피부경 이미지 23,247장, 8개 클래스이며, 이미지 출처와 촬영 장비에 따라 6개 구획으로 나뉩니다.',
                stats=[('23,247', '장의 피부경 이미지 (공식 규모)'), ('8', '개 병변 클래스'), ('6', '개 출처·촬영 장비 구획'), ('18,597 / 4,650', '학습 / 시험 (공식 분할)')],
                io_in='입력: 피부경 이미지 한 장', io_out='출력: 8개 클래스의 예측 확률',
                aux_t='다른 데이터의 역할', det_t='기술 세부: 공식 규모와 이번 실제 분할',
                split_head=['', '공식 (FLamby)', '이번 실제'],
                split=[['전체', '23,247장', '23,247장'],
                       ['학습', '18,597장, 클라이언트 6개 (각 351–9,930장)', '공식과 같음, 각 클라이언트가 로컬에서 학습'],
                       ['검증', '따로 나누지 않음', 'ISIC 이미지를 쓰지 않음, 하이퍼파라미터는 DermaMNIST에서 선택'],
                       ['시험', '4,650장, 클라이언트별 분할', '4,650장, 클라이언트 6개를 합쳐 평가']],
                src='출처: FLamby Fed-ISIC2019 공식 문서', ham='DermaMNIST와 ISIC는 모두 HAM10000에서 왔습니다. ISIC 시험 세트와의 중복을 뺀 뒤 남은 DermaMNIST 이미지는 ISIC 학습 세트에 들어 있습니다.'),
        m3=dict(q='공개 데이터로 왜 연합학습을 하나요?', a='누구나 구해서 재현할 수 있는 공개 데이터로, 데이터가 여러 참여자에게 흩어진 조건을 모의하고, 협력 학습과 프라이버시 보호 방법을 비교합니다.',
                cards=[('공개 데이터', '재료의 출처', '공개 데이터셋 이미지라 누구나 내려받아 확인할 수 있습니다. 병원 진료 기록은 쓰지 않았습니다.'),
                       ('연합학습', '구획별 협력', '이미지는 각 구획에 두고 로컬에서 학습한 뒤 모델 파라미터만 서버에 보내 합칩니다. 이것이 연합학습(FL)입니다.'),
                       ('차등 프라이버시', '기록 한 건의 영향 제한', '이미지 한 장의 영향을 제한하고 노이즈를 더해, 그 이미지가 들어 있었는지 알 수 없게 합니다. 이것이 차등 프라이버시(DP)이며 예산 ε가 작을수록 보호가 강합니다.')],
                tabs=['보기 A · 실험 준비', '보기 B · 학습 한 라운드'],
                va_src='Fed-ISIC2019 공개 데이터셋', va_src_note='23,247장 · 8개 클래스', va_map='공식 출처·촬영 장비에 따라 매핑', va_client='클라이언트', va_part='출처 구획', va_local='로컬 학습 세트 + 로컬 시험 세트',
                va_note='구획마다 자체 학습·시험 세트가 있습니다(합계 18,597 / 4,650, 고정 분할). ISIC에서 검증 세트를 나누지 않으며, 같은 크기의 노드는 구조만 보여 줍니다.',
                noise_t='소수 클래스는 왜 더 손해를 볼 수 있을까요?',
                det_t='기술 세부: 프라이버시 설정',
                det=['연합 평균(FedAvg): 서버가 클라이언트별 표본 수로 모델 파라미터를 가중 평균합니다.',
                     'DP-SGD: 매 단계 이미지마다 그래디언트를 고정 노름으로 자른 뒤 가우스 노이즈를 더하고, RDP 회계로 (ε, δ)를 계산합니다. δ는 고정합니다.',
                     '보호 단위: ISIC 실험은 이미지/표본 단위, 흉부 영상 확장 실험은 환자 단위입니다.',
                     '예산: 모델마다 목표 상한 ε≤3이며 P2의 클래스 통계 공개도 예산에 포함합니다. 방법마다 실제 누적 ε가 조금씩 달라 결과에 실제 ε·δ를 따로 적습니다.',
                     'ε는 모델 하나에 대한 값이며, 반복 실행과 하이퍼파라미터 탐색 전체의 공개는 합쳐 계산하지 않았습니다.']),
        m4=dict(q='구체적으로 어떤 방법을 시험했나요?', a='이미 있는 이미지 특징으로 분류 부분만 학습하고(P1), 보호된 클래스 요약을 주고받아 분류기가 더 고르게 배우게 했습니다(P2와 수정판 두 가지).',
                ver=['이번 실제 제출 버전', '원래 연구 설계 보기'], ver_note='이번 구현과 원래 설계는 P1·B4·B5가 다릅니다.',
                p1_t='P1 · 마지막 분류 부분만 학습',
                p1_sub=[('이미지', 'io'), ('특징 추출기 (ImageNet 사전학습)', 'frozen'), ('분류기', 'train'), ('8개 클래스 확률', 'io')],
                p1_orig=[('이미지', 'io'), ('특징 추출기 (대부분)', 'frozen'), ('마지막 block 또는 LoRA', 'train'), ('분류기', 'train'), ('8개 클래스 확률', 'io')],
                frozen='고정', train='DP 학습',
                p1_cap_sub='이번 제출: 특징 추출기는 모두 고정하고 분류기만 DP로 학습합니다.',
                p1_cap_orig='원래 설계: 마지막 block 또는 LoRA를 분류기와 함께 DP로 미세조정합니다. block 버전은 4차에 제출했고(P1-block), LoRA 버전은 시작 전입니다.',
                p2_t='P2 · 보호된 클래스 요약을 주고받아 분류기를 고르게 재학습',
                p2_steps=[('기록별 특징 클리핑', ''), ('클래스별 합과 개수', ''), ('합계에 노이즈', ''), ('클래스 요약 공개', ''), ('균형 가상 특징 생성', '이미지가 아닌 숫자 벡터'), ('분류기 재학습', '')],
                fix_t='이후 수정 시도: P2-PCA와 P2-LA',
                fixes=[('P2-PCA', '공개 보조 특징(DermaMNIST)으로 PCA 차원 축소를 맞춘 뒤 저차원에서 위의 6단계를 수행합니다. ISIC 시험 세트와 겹치는 DermaMNIST 이미지는 뺐고, 남은 이미지는 ISIC 학습 세트에 들어 있습니다.', '관찰: 클래스마다 오르내림.'),
                       ('P2-LA', '특징 합을 공개하지 않고 분류기도 다시 학습하지 않습니다. DP 클래스 개수로 예측 점수를 보정합니다(Logit Adjustment).', '관찰: 제한적 개선.')],
                table_t='핵심 방법 표', th=['방법', '구체적 구현', '검증 가설', '현재 상태'], swipe='← 좌우로 밀어 보기 →',
                more_t='나머지 방법 펼치기: B0·B1·B4·B5·P1-block·P1-LoRA·P2-PCA·P2-LA', vlab=['이번: ', '원 설계: ']),
        m5=dict(q='어디까지 했고, 무엇을 발견했나요?', a='대조·개선·확장 실험을 모두 제출했고 다른 구성원의 검토를 기다립니다. 지금은 P2-LA만 제한적으로 개선했고, 소수 클래스 손실을 안정적으로 해결한 방법은 없습니다.',
                cols=['제출한 작업', '현재 관찰', '다음 검증'], ev='근거', charts_t='결과 그래프 두 개',
                pending='수치 공개 전', null='추후 보완', fields=['실제 ε', 'δ', '시드 수', '검토 상태', '포함 방법'], nodp='DP 없음 (ε 없음)', priv='비공개 저장소, 협업자 로그인 필요',
                null_note='상세 수치는 현재 비공개 연구 저장소에만 있으며, 데이터 파일의 해당 필드는 null이고 화면에는 “추후 보완”으로 표시됩니다.',
                fill='수치를 공개할 때는 tools/site_content.py의 results에만 적고 python tools/build_site.py를 실행하면 세 언어 페이지와 데이터 파일이 함께 갱신됩니다.', det_t='기술 세부: 결과 객체 (data/medfl-data.json)', det_head=['experiment_id', '데이터 분할', '실제 ε', 'δ', '시드', '날짜', '상태']),
        m6=dict(q='요약과 다음 단계',
                sum=['우리는 프라이버시 보호 학습이 표본이 적은 피부 병변 클래스에 주는 영향을 연구합니다.', '공개 데이터와 클라이언트 6개의 연합학습 모의 실험으로 실제 학습 방식과 개선 시도를 비교합니다.', '실험은 진행되었고 일부 관찰과 수정 결과를 제출했으며, 안정적 개선은 더 검증해야 합니다.'],
                next_t='다음 단계의 중점', links_t='자료와 이전 버전',
                links=[('explain.html?lang=ko', '공개 인터랙티브 설명 (4단계 애니메이션·노이즈 슬라이더·P1/P2)'), ('progress.html?lang=ko', '연구 진행 페이지'), ('versions/v2-design/index.html', '개편 전 홈페이지 (연구 설계 v2, 11-03)'),
                       ('versions/v1/index.html', '첫 웹사이트 v1'), ('https://github.com/jasonventus/medfl', '웹사이트 소스 (GitHub)')]),
        kids_t='부록: 초등학생을 위한 1분 애니메이션', kids_p='일곱 장면으로 우리가 하는 일을 설명합니다. 그림은 설명용이며 실험 수치가 없습니다.',
        team_t='팀', ai='AI 도구(Codex·Claude·Gemini)가 실험, 글쓰기, 웹 제작을 도왔으며 결론은 구성원이 책임지고 검토를 받습니다.',
        team=[('范润堃', 'fanrunkun1', '프로젝트 총괄. AI 도구(Codex·Claude·Gemini)를 지휘해 데이터 정리, 실험, 분석, 시각화, 논문 초안과 수정을 수행했습니다.'),
              ('金銀潔 김은결 (Kim eungyeul)', 'kimeg02', '연구의 바탕이 된 실험설계서를 썼습니다. 조 계획에서 배경·문헌·한국어 소통을 담당했습니다.'),
              ('郭津阳', 'guo03122-commits', '조 계획에서 연합 학습·집계·차등 프라이버시를 담당했습니다.'),
              ('张皓', 'jasonventus', '조 계획에서 평가·공격 시험·시제품·통합을 담당했고, 공유 저장소와 이 웹사이트를 만들었습니다.')],
        foot='과제 05 · 공개 데이터의 연합학습 모의 실험 · 병원 진료 기록 사용 안 함'),
    'en': dict(
        html_lang='en', title='MedFL · Minority classes under private training', desc='Project 05: a six-client federated simulation on public skin-lesion images, studying how privacy protection affects minority-class recognition.',
        skip='Skip to content', toc_label='On this page', record='Latest public record', record_note='detailed values are kept in the private research repository',
        toc=['The question', 'Data', 'Public-data federation', 'Methods', 'Progress', 'Summary', 'For kids', 'Team'],
        names={'MEL': 'melanoma', 'NV': 'nevus', 'BCC': 'basal cell carcinoma', 'AK': 'actinic keratosis', 'BKL': 'benign keratosis', 'DF': 'dermatofibroma', 'VASC': 'vascular lesion', 'SCC': 'squamous cell carcinoma'},
        answer='Short answer',
        m1=dict(eyebrow='Project 05 · Public skin-lesion images · Privacy-preserving training',
                h1='When training protects privacy, are skin-lesion classes with few samples missed more often?',
                sub='We simulate federated learning across six clients with public skin-lesion images, study how privacy protection affects minority-class* recognition, and compare ways to soften that effect.',
                note='* Minority class: a class with a low share of images in the current training split; we look at dermatofibroma (DF) and vascular lesions (VASC). Not the same as a clinical rare disease.',
                a='So far, yes. With privacy protection, dermatofibroma and vascular lesions fall further than the common nevus, and the fixes we tried have not improved them reliably. Results await review.',
                b1='Understand it in 3 minutes', b2='See experiment progress', repo='Member collaboration repository', kids='Animation for kids',
                fig_img='Skin-lesion image', fig_img_note='illustrative icon, not a real case', fig_model='Model', fig_model_note='extract image features → classify',
                fig_out='8-class prediction', fig_minor='minority class', fig_focus='Focus: are minority classes found?', fig_focus_note='recall = share of a class’s images found correctly',
                fig_cap='One image in, a probability for each of 8 classes out; we watch minority-class recall.',
                det_t='Technical details: task, metrics, privacy unit',
                det=['Task: 8-class skin-lesion classification on Fed-ISIC2019.',
                     'Metrics: per-class recall; balanced accuracy (mean recall over 8 classes); macro-F1 (mean F1 over 8 classes).',
                     'Privacy: image/sample-level differential privacy (DP-SGD training, RDP accounting) with a target cap of ε≤3 per model. Image-level protection is not automatically patient-level protection.',
                     'Scope: a federated simulation on public data with six source partitions.']),
        m2=dict(q='What data do we study?', a='The main experiment uses Fed-ISIC2019: 23,247 public dermoscopy images in 8 classes, split into 6 partitions by image source and imaging device.',
                stats=[('23,247', 'dermoscopy images (official size)'), ('8', 'lesion classes'), ('6', 'source / imaging-device partitions'), ('18,597 / 4,650', 'train / test (official split)')],
                io_in='Input: one dermoscopy image', io_out='Output: predicted probabilities for 8 classes',
                aux_t='What the other datasets do', det_t='Technical details: official size and this round’s split',
                split_head=['', 'Official (FLamby)', 'This round'],
                split=[['Total', '23,247 images', '23,247 images'],
                       ['Train', '18,597 images in 6 clients (351–9,930 each)', 'As official; each client trains locally'],
                       ['Validation', 'not defined', 'no ISIC images; hyperparameters chosen on DermaMNIST'],
                       ['Test', '4,650 images, per client', '4,650 images, 6 clients pooled for evaluation']],
                src='Source: FLamby Fed-ISIC2019 documentation', ham='DermaMNIST and ISIC both come from HAM10000: after removing overlap with the ISIC test set, the remaining DermaMNIST images sit inside the ISIC training set.'),
        m3=dict(q='Why run federated learning on public data?', a='We use obtainable, reproducible public data to simulate data spread across separate parties, and compare collaborative training and privacy-protection methods.',
                cards=[('Public data', 'where the material comes from', 'Public datasets anyone can download and check; no hospital records.'),
                       ('Federated learning', 'partitions collaborate', 'Images stay in each partition; clients train locally and send only model parameters to a server that merges them. This is federated learning (FL).'),
                       ('Differential privacy', 'limit what one record can change', 'Cap each image’s influence and add noise, so no one can tell whether an image was used. This is differential privacy (DP); a smaller budget ε means stronger protection.')],
                tabs=['View A · Experiment setup', 'View B · One training round'],
                va_src='Fed-ISIC2019 public dataset', va_src_note='23,247 images · 8 classes', va_map='mapped by official source / imaging device', va_client='Client', va_part='source partition', va_local='local train set + local test set',
                va_note='Each partition keeps its own train and test set (18,597 / 4,650 in total, fixed split); no validation set is cut from ISIC. Equal-size nodes show structure only.',
                noise_t='Why might minority classes lose more?',
                det_t='Technical details: privacy settings',
                det=['Federated averaging (FedAvg): the server averages model parameters weighted by client size.',
                     'DP-SGD: at every step each image’s gradient is clipped to a fixed norm and Gaussian noise is added; RDP accounting converts this to (ε, δ) at a fixed δ.',
                     'Protection unit: image/sample level for ISIC; patient level for the chest X-ray extension.',
                     'Budget: target cap ε≤3 per model; P2’s class-statistics release counts toward it. Actual cumulative ε differs between methods, so results list actual ε and δ separately.',
                     'ε covers a single model; the overall release across repeated runs and tuning is not composed.']),
        m4=dict(q='Which methods did we try?', a='Reuse existing image features and train only the classification part (P1); then exchange protected class summaries so the classifier learns more evenly (P2 and two revisions).',
                ver=['What this round submitted', 'Original research design'], ver_note='This round differs from the original design in P1, B4 and B5.',
                p1_t='P1 · Train only the final classification part',
                p1_sub=[('Image', 'io'), ('Feature extractor (ImageNet-pretrained)', 'frozen'), ('Classification head', 'train'), ('8-class probabilities', 'io')],
                p1_orig=[('Image', 'io'), ('Feature extractor (most of it)', 'frozen'), ('Last block or LoRA', 'train'), ('Classification head', 'train'), ('8-class probabilities', 'io')],
                frozen='frozen', train='DP-trained',
                p1_cap_sub='Submitted this round: the whole feature extractor is frozen; only the classification head is trained with DP.',
                p1_cap_orig='Original design: the last block or LoRA is DP fine-tuned together with the head. The block version was submitted in round 4 (P1-block); the LoRA version has not started.',
                p2_t='P2 · Exchange protected class summaries, then retrain the head evenly',
                p2_steps=[('Clip each record’s features', ''), ('Sum and count per class', ''), ('Add noise to the totals', ''), ('Release class summaries', ''), ('Build balanced virtual features', 'number vectors, not images'), ('Retrain the head', '')],
                fix_t='Later fixes: P2-PCA and P2-LA',
                fixes=[('P2-PCA', 'Fit PCA on public auxiliary features (DermaMNIST), then run the six steps above in fewer dimensions. DermaMNIST images overlapping the ISIC test set were removed; the remaining images sit inside the ISIC training set.', 'Observation: classes move up and down.'),
                       ('P2-LA', 'No feature sums are released and the head is not retrained; DP class counts adjust the prediction scores (logit adjustment).', 'Observation: a limited improvement.')],
                table_t='Core method table', th=['Method', 'Implementation', 'Hypothesis tested', 'Status'], swipe='← swipe sideways →',
                more_t='Show the other methods: B0, B1, B4, B5, P1-block, P1-LoRA, P2-PCA, P2-LA', vlab=['This round: ', 'Original: ']),
        m5=dict(q='How far have we got, and what did we find?', a='Baselines, fixes and extensions are all submitted and await review by other members. So far only P2-LA shows a limited gain; no method reliably closes the minority-class loss.',
                cols=['Submitted work', 'Current observations', 'Next validation'], ev='Evidence', charts_t='Two result charts',
                pending='Values not yet public', null='to be added', fields=['Actual ε', 'δ', 'Seeds', 'Review status', 'Methods included'], nodp='no DP (no ε)', priv='private repository, collaborator login required',
                null_note='Detailed values live only in the private research repository; in the data file these fields are null and the page shows “to be added”.',
                fill='To publish values, fill them in only under results in tools/site_content.py and run python tools/build_site.py; the three pages and the data file update together.', det_t='Technical details: result objects (data/medfl-data.json)', det_head=['experiment_id', 'Data split', 'Actual ε', 'δ', 'Seeds', 'Date', 'Status']),
        m6=dict(q='Summary and next steps',
                sum=['We study how privacy-preserving training affects skin-lesion classes with few samples.', 'Using public data and a six-client federated simulation, we compare the training setups actually run with the fixes we tried.', 'The experiments are under way and some observations and fixes are submitted; a stable improvement still needs validation.'],
                next_t='Next priorities', links_t='Materials and earlier versions',
                links=[('explain.html?lang=en', 'Public interactive tour (four-step animation, noise slider, P1/P2)'), ('progress.html?lang=en', 'Research progress page'), ('versions/v2-design/en.html', 'Homepage before this redesign (design v2, Nov 3)'),
                       ('versions/v1/en.html', 'First website v1'), ('https://github.com/jasonventus/medfl', 'Website source (GitHub)')]),
        kids_t='Appendix: a 1-minute animation for kids', kids_p='Seven scenes explain what we do. The pictures are sketches with no experimental numbers.',
        team_t='Team', ai='AI tools (Codex, Claude, Gemini) helped with experiments, writing and this website; members own the conclusions, which remain under review.',
        team=[('Runkun Fan 范润堃', 'fanrunkun1', 'Project lead. Directing AI tools (Codex, Claude, Gemini), carried out data curation, experiments, analysis, visualization, and the paper draft and revisions.'),
              ('Eungyeul Kim 김은결', 'kimeg02', 'Wrote the experimental design behind the study; in the group plan, responsible for background, literature and Korean communication.'),
              ('Jinyang Guo 郭津阳', 'guo03122-commits', 'In the group plan, responsible for federated training, aggregation and differential privacy.'),
              ('Hao Zhang 张皓', 'jasonventus', 'In the group plan, responsible for evaluation, attack testing, the prototype and integration; built the shared repository and this website.')],
        foot='Project 05 · Federated simulation on public data · No hospital records used'),
}

ALIASES = {'what': ['s0'], 'data': ['s1'], 'public-fl': ['public-explainer', 's4'], 'methods': ['s2', 's3'], 'progress': ['research-update-20261103', 's5'], 'summary': ['changes'], 'team': ['s6']}


def badge(key, lang):
    if not key:
        return ''
    s = DATA['status'][key]
    cls = {'submitted': 'sub', 'pending_review': 'pend', 'reviewed': 'rev', 'not_started': 'none'}[key]
    return f'<span class="st st-{cls}"><span aria-hidden="true">{s["sym"]}</span> {s[lang]}</span>'


def ev_link(key, label):
    return f'<a class="ev" href="{EV[key]}" rel="noopener">{label} ↗</a>'


def aliases(sec):
    return ''.join(f'<span id="{a}" class="alias"></span>' for a in ALIASES.get(sec, []))


def details(title, body):
    return f'<details class="tech"><summary>{title}</summary><div class="tech-body">{body}</div></details>'


def section(sec, num, q, ans_label, a, body):
    return (f'<section class="mod" id="{sec}" aria-labelledby="{sec}-h">{aliases(sec)}<span class="section-num">{num}</span>'
            f'<h2 id="{sec}-h">{q}</h2><p class="answer"><b>{ans_label}</b>{a}</p>{body}</section>')


def method_rows(lang, main):
    p, out = PAGE[lang], []
    for m in DATA['methods']:
        if m['main'] != main:
            continue
        impl = (f'<span class="v-sub"><i class="vlab">{p["m4"]["vlab"][0]}</i>{m["sub"][lang]}</span>'
                f'<span class="v-orig"><i class="vlab">{p["m4"]["vlab"][1]}</i>{m["orig"][lang]}</span>')
        st = badge(m['status'], lang) + (badge('pending_review', lang) if m['status'] == 'submitted' else '')
        date = f'<small class="date">{m["date"]}</small>' if m['date'] else ''
        out.append(f'<tr><th scope="row">{m["name"][lang]}</th><td>{impl}</td><td>{m["hyp"][lang]}</td><td class="stc">{st}{date}</td></tr>')
    th = ''.join(f'<th scope="col">{h}</th>' for h in p['m4']['th'])
    return f'<div class="tablewrap" tabindex="0" role="region" aria-label="{p["m4"]["table_t"] if main else p["m4"]["more_t"]}"><p class="swipe">{p["m4"]["swipe"]}</p><table><thead><tr>{th}</tr></thead><tbody>{"".join(out)}</tbody></table></div>'


def page(lang):
    p = PAGE[lang]
    m1, m2, m3, m4, m5, m6 = (p[k] for k in ('m1', 'm2', 'm3', 'm4', 'm5', 'm6'))
    rd = DATA['public_record_date']
    langs = ''.join(f'<a lang="{k}" hreflang="{k}" href="{v}" data-lang-link' + (' aria-current="page"' if k == lang else '') + f'>{n}</a>'
                    for k, v, n in (('ko', 'index.html', '한국어'), ('en', 'en.html', 'English'), ('zh', 'zh.html', '中文')))
    ids = ['what', 'data', 'public-fl', 'methods', 'progress', 'summary', 'kids', 'team']
    toc = ''.join(f'<a href="#{i}">{n}</a>' for i, n in zip(ids, p['toc']))
    record = f'<span class="rec-label">{p["record"]} <b>{rd}</b></span>{badge("submitted", lang)}{badge("pending_review", lang)}<span class="rec-note">{p["record_note"]}</span>'

    # M1 — hero with the task flow figure
    chips = ''.join(f'<li class="chip{" minor" if c in MINOR else ""}"><b>{c}</b> {p["names"][c]}' + (f' <em>{m1["fig_minor"]}</em>' if c in MINOR else '') + '</li>' for c in CLASSES)
    lesion = ('<svg class="lesion" viewBox="0 0 64 64" aria-hidden="true"><rect x="2" y="2" width="60" height="60" rx="10" fill="#e9d6c3"/>'
              '<path d="M18 34c0-10 8-17 16-16 9 1 13 8 12 16-1 9-8 13-15 12-8-1-13-5-13-12z" fill="#8a5a3c"/><circle cx="30" cy="30" r="4" fill="#5d3a26"/></svg>')
    fig1 = (f'<figure class="flow1" aria-label="{m1["fig_cap"]}">'
            f'<div class="f-box f-img">{lesion}<div><b>{m1["fig_img"]}</b><small>{m1["fig_img_note"]}</small></div></div><div class="f-arrow" aria-hidden="true">↓</div>'
            f'<div class="f-box"><b>{m1["fig_model"]}</b></div><div class="f-arrow" aria-hidden="true">↓</div>'
            f'<div class="f-box"><b>{m1["fig_out"]}</b><ul class="chips">{chips}</ul></div><div class="f-arrow" aria-hidden="true">↓</div>'
            f'<div class="f-box f-focus"><b>{m1["fig_focus"]}</b><small>{m1["fig_focus_note"]}</small></div>'
            '</figure>')
    m1_det = details(m1['det_t'], '<ul>' + ''.join(f'<li>{x}</li>' for x in m1['det']) + '</ul>')
    hero = (f'<section class="hero mod" id="what" aria-labelledby="what-h">{aliases("what")}<div class="hero-text"><div class="eyebrow">{m1["eyebrow"]}</div>'
            f'<h1 id="what-h">{m1["h1"]}</h1><p class="sub">{m1["sub"]}</p><p class="answer"><b>{p["answer"]}</b>{m1["a"]}</p>'
            f'<div class="links"><a class="button primary" href="#data">{m1["b1"]}</a><a class="button" href="progress.html?lang={lang}">{m1["b2"]}</a></div>'
            f'<p class="minor-links"><a href="https://github.com/jasonventus/medfl">{m1["repo"]} ↗</a><a href="#kids">{m1["kids"]}</a></p>'
            f'<p class="def">{m1["note"]}</p>{m1_det}</div>{fig1}</section>')

    # M2 — data
    stats = ''.join(f'<div class="stat"><strong>{a}</strong><span>{b}</span></div>' for a, b in m2['stats'])
    aux = ''.join(f'<article class="card"><h3>{d["name"]}</h3><p class="role">{d["role"][lang]}</p><p>{d["text"][lang]}</p>'
                  + (f'<p class="stline">{badge(d["status"], lang)}{badge("pending_review", lang)}</p>' if d['status'] else '') + '</article>' for d in DATA['datasets'])
    split = ''.join('<tr>' + f'<th scope="row">{r[0]}</th>' + ''.join(f'<td>{c}</td>' for c in r[1:]) + '</tr>' for r in m2['split'])
    sh = ''.join(f'<th scope="col">{h}</th>' for h in m2['split_head'])
    m2_body = (f'<div class="fig dataset"><div class="stats">{stats}</div><p class="io"><span>{m2["io_in"]}</span><span aria-hidden="true">→</span><span>{m2["io_out"]}</span></p></div>'
               f'<h3 class="sub-h">{m2["aux_t"]}</h3><div class="cards4">{aux}</div>'
               + details(m2['det_t'], f'<div class="tablewrap" tabindex="0" role="region" aria-label="{m2["det_t"]}"><p class="swipe">{m4["swipe"]}</p><table><thead><tr>{sh}</tr></thead><tbody>{split}</tbody></table></div><p>{m2["ham"]}</p><p class="src"><a href="{EV["flamby"]}">{m2["src"]} ↗</a></p>'))

    # M3 — public-data federation: concept cards, view A (static), view B (shared animation), concept noise slider
    cards = ''.join(f'<article class="card concept"><h3>{a}<small>{b}</small></h3><p>{c}</p></article>' for a, b, c in m3['cards'])
    nodes = ''.join(f'<li class="va-node"><b>{m3["va_client"]} {i}</b><span>{m3["va_part"]}</span></li>' for i in range(1, 7))
    view_a = (f'<div class="view" id="view-a" role="tabpanel" aria-labelledby="tab-a"><div class="fig va"><div class="f-box"><b>{m3["va_src"]}</b><small>{m3["va_src_note"]}</small></div>'
              f'<div class="f-arrow" aria-hidden="true">↓</div><div class="f-box f-thin">{m3["va_map"]}</div><div class="f-arrow" aria-hidden="true">↓</div>'
              f'<ol class="va-grid">{nodes}</ol><p class="va-note">{m3["va_note"]}</p></div></div>')
    rt = DATA['i18n'][lang]['round']
    fallback = '<ol class="flr-fallback">' + ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in zip(rt['titles'], rt['copies'])) + '</ol>'
    view_b = f'<div class="view" id="view-b" role="tabpanel" aria-labelledby="tab-b"><div class="fig"><div data-flr>{fallback}</div></div></div>'
    tabs = (f'<div class="tabs" role="tablist"><button type="button" role="tab" id="tab-a" data-view="view-a" aria-controls="view-a" aria-selected="true">{m3["tabs"][0]}</button>'
            f'<button type="button" role="tab" id="tab-b" data-view="view-b" aria-controls="view-b" aria-selected="false">{m3["tabs"][1]}</button></div>')
    nz = DATA['i18n'][lang]['noise']
    noise = f'<h3 class="sub-h">{m3["noise_t"]}</h3><div class="fig"><div data-noise><p class="tag">{nz["tag"]}</p><p>{nz["states"][1]}</p><p class="small">{nz["note"]}</p></div></div>'
    m3_body = (f'<div class="cards3">{cards}</div>{tabs}{view_a}{view_b}{noise}'
               + details(m3['det_t'], '<ul>' + ''.join(f'<li>{x}</li>' for x in m3['det']) + f'</ul><p class="src"><a href="{EV["opacus"]}">Opacus · DP-SGD ↗</a> <a href="{EV["fedavg"]}">FedAvg ↗</a></p>'))

    # M4 — methods with the version switcher
    def arch(items):
        return '<ol class="arch">' + ''.join(f'<li class="a-{k}"><b>{n}</b>' + (f'<small>{m4[k]}</small>' if k in ('frozen', 'train') else '') + '</li>' for n, k in items) + '</ol>'
    ver = (f'<div class="tabs ver" role="group" aria-label="{m4["ver"][0]} / {m4["ver"][1]}"><button type="button" data-ver="sub" aria-pressed="true">{m4["ver"][0]}</button>'
           f'<button type="button" data-ver="orig" aria-pressed="false">{m4["ver"][1]}</button></div><p class="small">{m4["ver_note"]}</p>')
    p1 = (f'<div class="fig"><h3 class="fig-h">{m4["p1_t"]}</h3><div class="v-sub">{arch(m4["p1_sub"])}<p class="small"><i class="vlab">{m4["vlab"][0]}</i>{m4["p1_cap_sub"]}</p></div>'
          f'<div class="v-orig">{arch(m4["p1_orig"])}<p class="small"><i class="vlab">{m4["vlab"][1]}</i>{m4["p1_cap_orig"]}</p></div></div>')
    p2 = (f'<div class="fig"><h3 class="fig-h">{m4["p2_t"]}</h3><ol class="pipe6">'
          + ''.join(f'<li><b>{a}</b>' + (f'<span>{b}</span>' if b else '') + '</li>' for a, b in m4['p2_steps']) + '</ol></div>')
    fixes = '<div class="cards2">' + ''.join(f'<article class="card"><h3>{a}</h3><p>{b}</p><p class="obs">{c}</p></article>' for a, b, c in m4['fixes']) + '</div>'
    m4_body = (ver + f'<div class="two-fig">{p1}{p2}</div>' + details(m4['fix_t'], fixes)
               + f'<h3 class="sub-h">{m4["table_t"]}</h3>' + method_rows(lang, True) + details(m4['more_t'], method_rows(lang, False)))

    # M5 — progress board and the two chart slots (values null until published)
    def meta(date, st, rv, ev=None):
        return (f'<p class="meta">{f"<span class=date>{date}</span>" if date else ""}{badge(st, lang)}{badge(rv, lang)}'
                + (ev_link(ev, DATA['evidence_labels'][ev][lang]) if ev else '') + '</p>')
    col1 = ''.join(f'<li>{w["text"][lang]}{meta(w["date"], w["status"], w["review"], w["ev"])}</li>' for w in DATA['work'])
    col2 = ''.join(f'<li>{o["text"][lang]}<p class="meta"><span class="date">{o["date"]}</span></p></li>' for o in DATA['observations'])
    col3 = ''.join(f'<li>{t["text"][lang]}{meta(None, t["status"], None)}</li>' for t in DATA['todo'])
    board = '<div class="board">' + ''.join(f'<div class="col"><h3>{h}</h3><ul>{c}</ul></div>' for h, c in zip(m5['cols'], (col1, col2, col3))) + '</div>'
    res = {r['experiment_id']: r for r in DATA['results']}

    def val(r, k):
        if k == 'epsilon' and not r['dp']:
            return m5['nodp']
        return f'<span class="null">{m5["null"]}</span>' if r[k] is None else str(r[k])
    charts = ''
    for c in DATA['charts']:
        rs = [res[i] for i in c['results']]
        f = m5['fields']
        dl = (f'<dt>{f[0]}</dt><dd>{"; ".join(i.split("-", 2)[2] + ": " + val(res[i], "epsilon") for i in c["results"])}</dd>'
              f'<dt>{f[1]}</dt><dd>{val(rs[0], "delta")}</dd><dt>{f[2]}</dt><dd>{val(rs[0], "seeds")}</dd>'
              f'<dt>{f[3]}</dt><dd>{badge("submitted", lang)}{badge("pending_review", lang)}</dd>')
        evs = ' '.join(ev_link(k, DATA['evidence_labels'][k][lang]) for k in c['evidence'])
        charts += (f'<article class="evcard" data-chart="{c["id"]}"><h4>{c["title"][lang]}</h4><p class="pending">{m5["pending"]}</p>'
                   f'<dl>{dl}</dl><p class="meta">{m5["ev"]}（{m5["priv"]}）: {evs}</p></article>')
    rows = ''.join(f'<tr><th scope="row"><code>{r["experiment_id"]}</code></th><td>{r["data_split"]}</td><td>{val(r, "epsilon")}</td><td>{val(r, "delta")}</td>'
                   f'<td>{val(r, "seeds")}</td><td>{r["source_date"]}</td><td>{badge(r["status"], lang)}{badge(r["review_status"], lang)}</td></tr>' for r in DATA['results'])
    dh = ''.join(f'<th scope="col">{h}</th>' for h in m5['det_head'])
    m5_body = (board + f'<h3 class="sub-h">{m5["charts_t"]}</h3><div class="evgrid">{charts}</div><p class="small">{m5["null_note"]}</p>'
               + details(m5['det_t'], f'<div class="tablewrap" tabindex="0" role="region" aria-label="{m5["det_t"]}"><p class="swipe">{m4["swipe"]}</p><table class="results-t"><thead><tr>{dh}</tr></thead><tbody>{rows}</tbody></table></div><p>{m5["fill"]}</p>'))

    # M6 — summary, next priorities, links
    nxt = ''.join(f'<li>{n["text"][lang]} {badge(n["status"], lang)}</li>' for n in DATA['next'])
    links = ''.join(f'<a class="doc" href="{h}"><span>{n}</span><span class="access" aria-hidden="true">↗</span></a>' for h, n in m6['links'])
    m6_body = (f'<ol class="sum3">' + ''.join(f'<li>{s}</li>' for s in m6['sum']) + f'</ol><h3 class="sub-h">{m6["next_t"]}</h3><ol class="next3">{nxt}</ol>'
               f'<h3 class="sub-h">{m6["links_t"]}</h3><div class="docs">{links}</div>')
    summary = (f'<section class="mod" id="summary" aria-labelledby="summary-h">{aliases("summary")}<span class="section-num">06</span><h2 id="summary-h">{m6["q"]}</h2>{m6_body}</section>')

    kids_fallback = '<ol class="kids-fallback">' + ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in DATA['i18n'][lang]['kids']['steps']) + '</ol>'
    kids = f'<section class="mod" id="kids" aria-labelledby="kids-h"><span class="section-num">+</span><h2 id="kids-h">{p["kids_t"]}</h2><p>{p["kids_p"]}</p><div class="kids">{kids_fallback}</div></section>'
    team = ''.join(f'<article class="person"><h3>{a}</h3><a class="handle" href="https://github.com/{b}">@{b}</a><p>{c}</p></article>' for a, b, c in p['team'])
    team = f'<section class="mod" id="team" aria-labelledby="team-h">{aliases("team")}<h2 id="team-h">{p["team_t"]}</h2><div class="team">{team}</div><p class="small">{p["ai"]}</p></section>'

    css = BASE_CSS + EXTRA_CSS
    return (f'<!doctype html><html translate="no" lang="{p["html_lang"]}"><head><meta charset="utf-8"><meta name="google" content="notranslate">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{p["desc"]}"><title>{p["title"]}</title>'
            f'<link rel="alternate" hreflang="ko" href="index.html"><link rel="alternate" hreflang="en" href="en.html"><link rel="alternate" hreflang="zh" href="zh.html">'
            f'<script>document.documentElement.classList.add("js")</script><style>{css}</style>'
            f'<link rel="stylesheet" href="assets/medfl.css"><link rel="stylesheet" href="assets/kids.css"></head><body>'
            f'<a class="skip" href="#main">{p["skip"]}</a>'
            f'<header><a class="brand" href="{FILES[lang]}">MEDFL <span>/ PROJECT 05</span></a><nav class="langs" aria-label="Language / 언어 / 语言">{langs}</nav></header>'
            f'<div class="recordbar" role="note">{record}</div><nav class="toc" aria-label="{p["toc_label"]}">{toc}</nav><main id="main">'
            + hero
            + section('data', '02', m2['q'], p['answer'], m2['a'], m2_body)
            + section('public-fl', '03', m3['q'], p['answer'], m3['a'], m3_body)
            + section('methods', '04', m4['q'], p['answer'], m4['a'], m4_body)
            + section('progress', '05', m5['q'], p['answer'], m5['a'], m5_body)
            + summary + kids + team
            + f'</main><footer class="footer"><p class="recordbar">{record}</p><p>{p["foot"]}</p><a href="https://github.com/jasonventus/medfl">https://github.com/jasonventus/medfl</a></footer>'
            '<script src="data/medfl-data.js"></script><script src="assets/medfl.js" defer></script><script src="assets/kids.js" defer></script></body></html>\n')


BASE_CSS = re.search(r'<style>(.*?)</style>', (ROOT / 'versions' / 'v2-design' / 'index.html').read_text(encoding='utf-8'), re.S).group(1)
EXTRA_CSS = (
    '@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;z-index:9;background:#fff;padding:8px 12px;border-radius:6px}'
    'header{flex-wrap:wrap}.langs a{white-space:nowrap}'
    '.recordbar{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font-size:13px;color:#455f5e;padding:10px max(5vw,20px);border-bottom:1px solid #d5dfd9;margin:0}'
    '.rec-label b{color:#152e32}.rec-note{color:#60766e}'
    '.toc{display:flex;flex-wrap:wrap;gap:4px 6px;padding:10px max(5vw,20px);border-bottom:1px solid #d5dfd9;background:#f4f6f2}'
    '.toc a{font-size:13.5px;text-decoration:none;padding:5px 11px;border-radius:999px;border:1px solid #c9d7cf;background:#fafbf8}.toc a:hover{border-color:#487864}'
    '.st{display:inline-flex;align-items:center;gap:4px;border-radius:999px;padding:1px 9px;font-size:12.5px;font-weight:700;border:1px solid;margin:2px 4px 2px 0;white-space:nowrap}'
    '.st-sub{color:#1f5f52;border-color:#7fb3a3;background:#e6f2ec}.st-pend{color:#8a4b0f;border-color:#e0a860;background:#fbefdc}'
    '.st-rev{color:#1d5e2e;border-color:#79b48a;background:#e3f3e6}.st-none{color:#55625d;border-color:#b9c4bf;background:#eef1ee}'
    '.mod{padding:52px 0;border-bottom:1px solid #ccd8d1}.mod h2{font-size:clamp(24px,3vw,32px);letter-spacing:-.03em;line-height:1.3;margin:0 0 6px}'
    '.alias{position:absolute;width:0;height:0;overflow:hidden}'
    '.hero{grid-template-columns:1.15fr .85fr;gap:48px;padding:48px 0;align-items:start}.hero h1{font-size:clamp(30px,3.9vw,52px)}'
    '.hero .sub{font-size:18px;color:#3f5856;max-width:640px}'
    '.answer{font-size:17.5px;line-height:1.7;color:#152e32;background:#fff;border-left:4px solid #487864;padding:12px 16px;border-radius:0 10px 10px 0;max-width:930px;margin:12px 0 20px}'
    '.answer b{display:block;font-size:12px;letter-spacing:.08em;color:#487864;margin-bottom:2px}'
    '.minor-links{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:14px;margin:14px 0 0}.def{font-size:13.5px;color:#52736a;max-width:640px}'
    '.fig{background:#e9f0eb;border:1px solid #d1ded4;border-radius:14px;padding:16px;margin:14px 0}.fig-h{margin:0 0 10px;font-size:17px}'
    '.flow1{margin:0;background:#e4ece6;border:1px solid #d1ded4;border-radius:18px;padding:18px;display:grid;gap:4px}'
    '.f-box{background:#fafbf8;border:1px solid #c9d7cf;border-radius:10px;padding:10px 14px}.f-box b{display:block;font-size:15px}.f-box small{display:block;font-size:12.5px;color:#60766e}'
    '.f-img{display:flex;gap:12px;align-items:center}.lesion{width:52px;height:52px;flex:none}.f-focus{border:2px solid #c97a24;background:#fff8ee}'
    '.f-thin{text-align:center;font-size:14px}.f-arrow{text-align:center;color:#487864;font-size:18px;line-height:1.1}'
    '.flow1 figcaption{font-size:13px;color:#52736a;margin-top:6px}'
    '.chips{list-style:none;padding:0;margin:8px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:5px}'
    '.chip{font-size:12.5px;border:1px solid #c9d7cf;border-radius:7px;padding:3px 7px;background:#fff}.chip b{font-size:12.5px;display:inline}'
    '.chip.minor{border:2px solid #c97a24;background:#fff3e2}.chip em{font-style:normal;font-weight:700;color:#8a4b0f;font-size:11.5px}'
    'details.tech{margin:18px 0 0;border:1px solid #d2ddd5;border-radius:10px;background:#fafbf8;padding:0 16px;max-width:1000px}'
    'details.tech summary{padding:11px 0;font-weight:700;cursor:pointer;color:#173e40}details.tech[open] summary{border-bottom:1px solid #e1e8e3}'
    '.tech-body{padding:10px 0 14px;font-size:14.5px}.tech-body ul{margin:0;padding-left:20px}.tech-body li{margin:6px 0}'
    '.dataset .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.stat strong{display:block;font-size:26px;letter-spacing:-.02em;color:#173e40}.stat span{font-size:13px;color:#52736a}'
    '.io{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0 0;font-size:14.5px}.io span:not([aria-hidden]){background:#fafbf8;border:1px solid #c9d7cf;border-radius:8px;padding:4px 10px}'
    '.sub-h{margin:26px 0 8px;font-size:19px}'
    '.cards2,.cards3,.cards4{display:grid;gap:14px;margin:12px 0}.cards2{grid-template-columns:1fr 1fr}.cards3{grid-template-columns:repeat(3,1fr)}.cards4{grid-template-columns:repeat(4,1fr)}'
    '.card{background:#fafbf8;border:1px solid #d2ddd5;border-radius:12px;padding:16px}.card h3{margin:0 0 6px;font-size:17px}.card p{margin:6px 0 0;font-size:14.5px;color:#455f5e}'
    '.card .role{font-weight:700;color:#487864;margin:0}.concept h3 small{display:block;font-size:12.5px;color:#52736a;font-weight:600}.obs{font-weight:700;color:#8a4b0f!important}'
    '.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 6px}'
    '.tabs button{font:inherit;font-size:14.5px;padding:8px 15px;border-radius:999px;border:1px solid #b7c9c1;background:#fafbf8;color:#152e32;cursor:pointer}'
    '.tabs button[aria-selected=true],.tabs button[aria-pressed=true]{background:#173e40;color:#fff;border-color:#173e40}'
    'button:focus-visible,summary:focus-visible,.tablewrap:focus-visible{outline:3px solid #e09b35;outline-offset:3px}'
    '.va-grid{list-style:none;padding:0;margin:4px 0;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}'
    '.va-node{background:#fafbf8;border:1px solid #9fb8aa;border-radius:10px;padding:10px;text-align:center}.va-node b{display:block}.va-node span{font-size:13px;color:#487864}.va-node small{display:block;font-size:12px;color:#60766e}'
    '.va-note{font-size:13.5px;color:#455f5e;margin:10px 0 0}'
    '.arch{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px;align-items:stretch}'
    '.arch li{flex:1 1 120px;border-radius:10px;padding:10px;border:1px solid #c9d7cf;background:#fafbf8;position:relative}.arch li b{display:block;font-size:14px}.arch li small{display:block;font-size:12px;font-weight:700}'
    '.arch li.a-frozen{background:#e7ebe9;border-style:dashed;color:#4d5c57}.arch li.a-frozen small:before{content:"❄ "}'
    '.arch li.a-train{background:#dcefe6;border:2px solid #3f7f6d}.arch li.a-train small{color:#1f5f52}.arch li.a-train small:before{content:"✎ "}'
    '.two-fig{display:grid;grid-template-columns:1fr 1fr;gap:14px}'
    '.pipe6{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;counter-reset:s}'
    '.pipe6 li{counter-increment:s;background:#fafbf8;border:1px solid #c9d7cf;border-radius:10px;padding:10px 10px 10px 40px;position:relative;font-size:13.5px}'
    '.pipe6 li:before{content:counter(s);position:absolute;left:10px;top:10px;width:22px;height:22px;border-radius:50%;background:#173e40;color:#fff;font-weight:700;font-size:13px;display:grid;place-items:center}'
    '.pipe6 b{display:block;font-size:14px}.pipe6 span{color:#455f5e}'
    '.v-orig{display:none}html:not(.js) .v-orig{display:block}html:not(.js) span.v-orig{display:inline}html:not(.js) span.v-sub:after{content:" / "}'
    '.js .vlab{display:none}.vlab{font-style:normal;font-weight:700;color:#487864}'
    '.ver-orig .v-sub{display:none}.ver-orig .v-orig{display:block}.ver-orig span.v-orig{display:inline}'
    '.tablewrap{overflow-x:auto;margin:8px 0;border:1px solid #d2ddd5;border-radius:10px;background:#fafbf8}'
    '.tablewrap table{border-collapse:collapse;width:100%;min-width:680px;font-size:14px}.tablewrap th,.tablewrap td{text-align:left;vertical-align:top;padding:9px 11px;border-bottom:1px solid #e1e8e3}'
    '.tablewrap thead th{background:#e9f0eb;font-size:13px}.stc{min-width:150px}.date{display:inline-block;font-size:12px;color:#60766e;margin-right:6px}td small.date{display:block}'
    '.swipe{display:none;margin:6px 10px 0;font-size:12px;color:#60766e}'
    '.board{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:8px 0}.board .col{background:#fafbf8;border:1px solid #d2ddd5;border-radius:12px;padding:14px}'
    '.board h3{margin:0 0 8px;font-size:17px}.board ul{list-style:none;padding:0;margin:0}.board li{padding:9px 0;border-top:1px solid #e1e8e3;font-size:14.5px}.board li:first-child{border-top:0}'
    '.meta{margin:5px 0 0;font-size:12.5px;color:#60766e;display:flex;flex-wrap:wrap;align-items:center;gap:2px 4px}.ev{font-size:12.5px;margin-left:4px}'
    '.evgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.evcard{border:2px dashed #b7c9c1;border-radius:12px;padding:16px;background:#fff}'
    '.evcard h4{margin:0 0 6px;font-size:16px}.pending{font-weight:750;color:#8a4b0f;margin:0 0 8px}'
    '.evcard dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:0;font-size:14px}.evcard dt{font-weight:700;color:#455f5e}.evcard dd{margin:0}.null{color:#8a4b0f;font-weight:700}'
    '.results-t code{font-size:12.5px}.sum3,.next3{max-width:930px}.sum3 li,.next3 li{margin:6px 0}.small{font-size:13.5px;color:#52736a}'
    '.src{font-size:13px}.src a{margin-right:12px}.footer .recordbar{border:0;padding:0 0 8px}'
    '.docs{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.doc{display:flex;justify-content:space-between;gap:10px;text-decoration:none;border:1px solid #d2ddd5;border-radius:10px;padding:12px 14px;background:#fafbf8}'
    '@media(max-width:980px){.hero{grid-template-columns:1fr}.cards4{grid-template-columns:1fr 1fr}.two-fig{grid-template-columns:1fr}.pipe6{grid-template-columns:1fr 1fr}}'
    '@media(max-width:760px){.dataset .stats{grid-template-columns:1fr 1fr}.cards2,.cards3,.cards4,.board,.evgrid,.docs{grid-template-columns:1fr}.va-grid{grid-template-columns:1fr 1fr}'
    '.pipe6{grid-template-columns:1fr}.swipe{display:block}.mod{padding:38px 0}.answer{font-size:16px}header{padding:12px 16px}main{padding:0 16px}.recordbar,.toc{padding-left:16px;padding-right:16px}}'
)


def main():
    (ROOT / 'data').mkdir(exist_ok=True)
    blob = json.dumps(DATA, ensure_ascii=False, indent=1)
    (ROOT / 'data' / 'medfl-data.json').write_text(blob + '\n', encoding='utf-8')
    (ROOT / 'data' / 'medfl-data.js').write_text('/* generated by tools/build_site.py from tools/site_content.py; do not edit by hand */\nwindow.MEDFL_DATA = ' + blob + ';\n', encoding='utf-8')
    for lang, name in FILES.items():
        html = page(lang)
        (ROOT / name).write_text(html, encoding='utf-8')
        print('wrote', name, len(html.encode('utf-8')), 'bytes')
    # self-checks: no metric value may appear unless the source holds it; every result keeps the required fields
    req = {'experiment_id', 'method_version', 'data_split', 'metrics', 'seeds', 'epsilon', 'delta', 'source_date', 'review_status'}
    for r in DATA['results']:
        assert req <= r.keys(), r['experiment_id']
        assert set(r['metrics']) == {'per_class_recall', 'balanced_acc', 'macro_f1'}
    for lang, name in FILES.items():
        assert html_ok((ROOT / name).read_text(encoding='utf-8')), name
    print('data/medfl-data.json', len(blob), 'chars; results', len(DATA['results']))


def html_ok(s):
    return s.count('<section') == s.count('</section>') and s.count('<details') == s.count('</details>') and s.count('<table') == s.count('</table>')


if __name__ == '__main__':
    main()
