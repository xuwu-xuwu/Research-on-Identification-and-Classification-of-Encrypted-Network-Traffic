# 网络加密数据流识别与分类技术研究项目计划书（15周）

## 1. 项目基本信息
- 项目名称：网络加密数据流识别与分类技术研究
- 项目周期：15 周
- 项目目标：在不解密载荷内容的前提下，基于流量统计特征与握手特征，实现对加密流量应用类型的分类与评估。
- 预期成果：可复现实验代码、实验数据与图表、课程报告、答辩 PPT。

## 2. 总体阶段划分
- 第 1-3 周：项目启动与技术预研
- 第 4-7 周：数据构建与特征工程
- 第 8-11 周：模型训练与对比实验
- 第 12-15 周：泛化验证与答辩交付

## 3. 每周任务与完成方式

| 周次 | 本周要完成的任务 | 如何完成任务（执行步骤） | 周交付物 |
| --- | --- | --- | --- |
| 第1周 | 明确研究边界与评分目标 | 召开启动会；拆解课程评分标准；明确只做分类不做解密；建立仓库目录与命名规范 | 项目章程、分工表、仓库初始化 |
| 第2周 | 完成文献调研 | 检索关键词（TLS Fingerprinting、JA3、Flow Classification）；阅读并整理 10-15 篇文献；提炼常用特征与模型 | 文献综述初稿、参考文献清单 |
| 第3周 | 完成环境与工具链搭建 | 统一 Python 版本与依赖；安装 Wireshark、CICFlowMeter；编写环境安装文档和脚本 | 环境说明文档、依赖清单 |
| 第4周 | 确定数据方案并完成数据获取 | 确定主数据集（如 ISCX VPN-nonVPN）与备选数据集；下载并校验字段完整性与标签可用性 | 原始数据目录、数据来源说明 |
| 第5周 | 设计并试运行自采集方案（可选） | 制定采集场景与标签规则；在授权环境中小规模抓包；记录采集时间、场景、工具参数 | 采集方案文档、试采样本 |
| 第6周 | 完成流切分与数据清洗 | 按五元组切分 Flow；处理缺失值、异常值、重复样本；统一标签命名 | 清洗后数据 v1、字段字典 |
| 第7周 | 完成特征提取与探索分析 | 提取 Flow Duration、包长/IAT 统计、上下行比值等特征；绘制分布图识别偏态与不平衡 | 特征数据集 v1、EDA 图表 |
| 第8周 | 建立基线模型并形成首轮结果 | 训练决策树/逻辑回归基线；固定随机种子；输出 Accuracy、Precision、Recall、F1 | 基线实验记录、混淆矩阵 |
| 第9周 | 完成主模型训练与调参 | 训练随机森林；使用 Stratified K-Fold 与网格/随机搜索调参；记录参数-指标对应关系 | 主模型结果 v1、调参日志 |
| 第10周 | 完成对比模型实验 | 训练 SVM/KNN；保持统一数据划分与评价口径；横向比较性能与代价 | 模型对比表、实验结论 v1 |
| 第11周 | 完成消融实验与可解释性分析 | 做统计特征 vs 统计+握手特征对比；输出特征重要性排序；分析关键特征贡献 | 消融实验报告、特征重要性图 |
| 第12周 | 完成泛化与鲁棒性测试 | 执行跨时间/跨场景测试；分析类别不平衡处理前后性能变化 | 泛化测试报告、误判样本集 |
| 第13周 | 完成误差分析与改进方案 | 分类整理误判原因（业务相似、CDN、样本偏差）；提出可验证改进措施并复测 | 误差分析文档、改进实验记录 |
| 第14周 | 完成报告与答辩材料初稿 | 按“背景-方法-实验-结论”结构写报告；整理图表编号与引用；制作 PPT 初稿 | 报告初稿、PPT 初稿 |
| 第15周 | 完成联调演练与最终提交 | 全流程演练 1-2 次；修复演示问题；按清单提交代码、数据、报告、PPT | 最终提交包、答辩讲稿 |

## 4. 每周执行与验收机制
- 每周组会（60-90 分钟）：检查上周交付物、确认本周任务和风险。
- 每周技术同步（30 分钟）：统一字段、标签、数据划分和指标口径。
- 每周周报：按“已完成/问题/下周计划/需协助”四项提交。
- 里程碑验收周：第 7、11、15 周进行阶段验收，未达标则启动补救任务。

## 5. 风险与应对
- 数据质量不足：每周随机抽样人工核查标签，建立数据问题台账。
- 类别不平衡：采用类别权重、分层抽样，主指标使用 Macro-F1。
- 模型过拟合：交叉验证、特征筛选、限制模型复杂度。
- 进度延迟：关键任务设置备份负责人，优先保证最小可交付版本（MVP）。

## 6. 最终交付清单
- 代码仓库（数据处理、训练、评估、可视化脚本）
- 清洗后数据与字段说明
- 研究报告（Word/PDF）
- 答辩 PPT 与演示脚本
- 复现实验说明（环境、参数、运行步骤）

## 7. 推荐文献综述与论文（用于相关工作章节）

### 7.1 优先阅读的综述文献
1. 付钰等，2025，《基于机器学习的加密流量分类研究综述》（通信学报）
   - 链接：https://www.joconline.com.cn/zh/article/doi/10.11959/j.issn.1000-436x.2025006/
2. TONG Xin et al., 2024, A Survey of Machine Learning-Based Encrypted Traffic Analysis Methods
   - 链接：https://jcjs.siat.ac.cn/en/article/doi/10.12146/j.issn.2095-3135.20240130001
3. Alwhbi et al., 2024, Encrypted Network Traffic Analysis and Classification Utilizing Machine Learning (Sensors)
   - 链接：https://www.mdpi.com/1424-8220/24/11/3509
4. Sharma & Lashkari, 2025, A survey on encrypted network traffic... (Computer Networks)
   - 链接：https://www.sciencedirect.com/science/article/abs/pii/S1389128624008168
5. Papadogiannaki & Ioannidis, 2021, A Survey on Encrypted Network Traffic Analysis Applications, Techniques, and Countermeasures
   - 链接：https://zenodo.org/record/5525929
6. Shen et al., 2023, Machine Learning-Powered Encrypted Network Traffic Analysis: A Comprehensive Survey
   - 链接：https://dblp.org/rec/journals/comsur/ShenYLZKYLX23

### 7.2 代表性研究论文（按技术路线）
1. Draper-Gil et al., 2016，基于时间特征进行加密/VPN流量分类
   - 链接：https://www.scitepress.org/Papers/2016/57407/57407.pdf
2. Taylor et al., 2016，AppScanner（移动应用加密流量指纹识别）
   - 链接：https://dblp.org/rec/conf/eurosp/TaylorSCM16
3. Lotfollahi et al., 2017/2018，Deep Packet（深度学习经典工作）
   - 链接：https://arxiv.org/abs/1709.02656
4. van Ede et al., 2020，FlowPrint（半监督与未知应用识别）
   - 链接：https://www.ndss-symposium.org/ndss-paper/flowprint-semi-supervised-mobile-app-fingerprinting-on-encrypted-network-traffic/
5. Lin et al., 2022，ET-BERT（预训练模型方法）
   - 链接：https://arxiv.org/abs/2202.06335
6. Wang et al., 2023，BFCN（BERT + CNN 融合）
   - 链接：https://www.mdpi.com/2079-9292/12/3/516
7. Malekghaini et al., 2023，数据漂移条件下的分类性能研究
   - 链接：https://www.sciencedirect.com/science/article/pii/S1389128623000932
8. Yu et al., 2024，仅用包头信息的 BERT 方法
   - 链接：https://www.sciencedirect.com/science/article/pii/S1389128624005796

### 7.3 数据集与基准建议引用
1. ISCX VPN-nonVPN
   - 链接：https://www.unb.ca/cic/datasets/vpn.html
2. CIC-IDS2017
   - 链接：https://www.unb.ca/cic/datasets/ids-2017.html
3. CipherSpectrum（TLS 1.3 数据集）
   - 链接：https://cgi.cse.unsw.edu.au/~cspectrum/

### 7.4 建议写作方式（可直接用于报告）
1. 按“传统机器学习 -> 深度学习 -> 预训练模型 -> 泛化与鲁棒性”组织相关工作。
2. 每篇论文至少提炼 3 点：核心特征、模型方法、局限性。
3. 最后一段明确本项目定位：面向课程场景，强调可复现与可解释性。
