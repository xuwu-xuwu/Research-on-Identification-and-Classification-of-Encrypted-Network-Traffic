# 当前工作目录文件说明（精简中文版，截至 2026-04-07）

本文档按“真正和项目有关”的标准，对当前工作目录中的重要文件进行整理。它保留源码、项目文档、原始/关键数据、当前主结果和后续续接所需的文件，排除了大量缓存、版本控制内部文件和中间生成物。

## 保留标准

- 保留当前项目源码、复现代码、工具脚本和实际使用的文档。
- 保留原始数据集压缩包、实际参与训练或复现的数据文件。
- 保留当前主线结果、论文复现主结果和当前推荐深度学习结果。
- 保留项目当前实际使用的课程材料和报告成果。

## 已排除内容

- `/.git` 与 `src/reproduction/TrafficFormer/.git` 下的版本控制内部文件
- `/.vscode`、`__pycache__`、`.pyc`、`catboost_info` 等缓存或环境文件
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/` 下的大批量中间切分 PCAP
- `信息系统安全与对抗技术-报告模板/` 下的通用课程模板文件
- 冒烟测试、探索性旧实验、重复性较强且当前不作为主结果保留的部分输出

当前精简版本共保留 `281` 个文件。

## 顶层统计

| 顶层路径 | 文件数 |
| --- | ---: |
| `.gitignore` | 1 |
| `data` | 54 |
| `docs` | 19 |
| `optimization.md` | 1 |
| `outputs` | 73 |
| `project_plan_15_weeks.md` | 1 |
| `readme.md` | 1 |
| `src` | 127 |
| `tools` | 2 |
| `信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx` | 1 |
| `组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx` | 1 |

## 文件清单

### `.gitignore`（1 个文件）

<details>
<summary>展开查看 <code>.gitignore</code> 下的保留文件</summary>

- `.gitignore`（268 B）：Git 忽略规则文件，控制哪些生成物、缓存和本地资源不纳入版本管理。

</details>

### `data`（54 个文件）

<details>
<summary>展开查看 <code>data</code> 下的保留文件</summary>

- `data/NonVPN-PCAPs-01.zip`（800.3 MB）：原始数据集压缩包。
- `data/NonVPN-PCAPs-01/aim_chat_3a.pcap`（748.2 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/aim_chat_3b.pcap`（440.2 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/AIMchat1.pcapng`（65.5 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/AIMchat2.pcapng`（64.9 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/email1a.pcap`（3.1 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/email1b.pcap`（3.1 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/email2a.pcap`（789.2 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/email2b.pcap`（944.9 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_audio1a.pcap`（8.2 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_audio1b.pcapng`（9.1 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_audio2a.pcap`（15.7 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_audio2b.pcapng`（17.0 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_audio3.pcapng`（100.4 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_audio4.pcapng`（143.2 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_chat_4a.pcap`（857.4 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_chat_4b.pcap`（1.6 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_video1a.pcap`（140.1 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_video1b.pcapng`（85.2 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_video2a.pcap`（219.9 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebook_video2b.pcapng`（223.8 MB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebookchat1.pcapng`（442.6 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebookchat2.pcapng`（168.9 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-01/facebookchat3.pcapng`（646.0 KB）：NonVPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/NonVPN-PCAPs-03.zip`（9.6 GB）：原始数据集压缩包。
- `data/Scenario A1-ARFF.zip`（4.3 MB）：原始数据集压缩包。
- `data/Scenario A2-ARFF.zip`（4.0 MB）：原始数据集压缩包。
- `data/Scenario B-ARFF.zip`（8.6 MB）：原始数据集压缩包。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-120s-AllinOne.arff`（1.9 MB）：ARFF 格式流级统计特征数据文件。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-120s.arff`（1.9 MB）：ARFF 格式流级统计特征数据文件。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-15s-AllinOne.arff`（3.4 MB）：ARFF 格式流级统计特征数据文件。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-15s.arff`（3.5 MB）：ARFF 格式流级统计特征数据文件。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-30s-AllinOne.arff`（2.7 MB）：ARFF 格式流级统计特征数据文件。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-30s.arff`（2.7 MB）：ARFF 格式流级统计特征数据文件。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-60s-AllinOne.arff`（2.8 MB）：ARFF 格式流级统计特征数据文件。
- `data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-60s.arff`（2.8 MB）：ARFF 格式流级统计特征数据文件。
- `data/VPN-PCAPs-02.zip`（1.6 GB）：原始数据集压缩包。
- `data/VPN-PCAPs-02/vpn_icq_chat1a.pcap`（475.2 KB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_icq_chat1b.pcap`（409.4 KB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_netflix_A.pcap`（769.1 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_sftp_A.pcap`（78.5 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_sftp_B.pcap`（17.1 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_skype_audio1.pcap`（47.2 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_skype_audio2.pcap`（47.1 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_skype_chat1a.pcap`（829.3 KB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_skype_chat1b.pcap`（980.9 KB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_skype_files1a.pcap`（8.6 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_skype_files1b.pcap`（6.4 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_spotify_A.pcap`（98.6 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_vimeo_A.pcap`（118.8 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_vimeo_B.pcap`（242.8 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_voipbuster1a.pcap`（49.3 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_voipbuster1b.pcap`（49.2 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。
- `data/VPN-PCAPs-02/vpn_youtube_A.pcap`（173.8 MB）：VPN 原始抓包文件，文件名对应具体应用或业务场景。

</details>

### `docs`（19 个文件）

<details>
<summary>展开查看 <code>docs</code> 下的保留文件</summary>

- `docs/analysis/next_optimization_points.md`（8.4 KB）：下一轮优化方向整理文档。
- `docs/analysis/teammate_optimization_analysis.md`（5.9 KB）：同事优化版整体策略分析文档。
- `docs/analysis/train_final_optimized_code_analysis.md`（18.6 KB）：优化训练脚本的代码级解析文档。
- `docs/analysis/train_final_optimized_tech_stack.md`（9.6 KB）：优化版技术栈与方法路线说明。
- `docs/project_memory.md`（12.4 KB）：项目记忆文档，用于后续续接时快速恢复上下文。
- `docs/references/Machine_Learning-Powered_Encrypted_Network_Traffic_Analysis_A_Comprehensive_Survey.pdf`（5.6 MB）：加密流量机器学习分析综述论文 PDF。
- `docs/reports/requirements_report_fixed.docx`（64.9 KB）：修整后的需求分析报告 Word 文件。
- `docs/reports/workspace_file_catalog_2026-04-07.md`（209.0 KB）：当前工作目录文件说明的英文版。
- `docs/reports/workspace_file_catalog_zh_2026-04-07.md`（230.8 KB）：当前工作目录文件说明的中文版全量版本。
- `docs/reports/开题报告-网络加密数据流识别与分类技术研究-模板规范版.docx`（67.3 KB）：按模板规范整理后的开题报告 Word 版本。
- `docs/reports/开题报告-网络加密数据流识别与分类技术研究.docx`（67.3 KB）：开题报告 Word 版本。
- `docs/reports/开题报告-网络加密数据流识别与分类技术研究.md`（28.7 KB）：当前项目开题报告 Markdown 版本。
- `docs/reports/当前项目进度总结-2026-04-07.md`（11.8 KB）：截至 2026-04-07 的项目整体进度总结。
- `docs/reports/数据集调整报告.docx`（836.8 KB）：数据集调整情况说明文档。
- `docs/reports/需求分析报告-修正版-2.docx`（57.2 KB）：需求分析报告 Word 修订版。
- `docs/reports/需求分析报告-网络加密数据流识别与分类技术研究.md`（20.0 KB）：当前项目需求分析报告 Markdown 版本。
- `docs/reproduction/c_lstm/improved/c_lstm_improved_summary.md`（4.6 KB）：C-LSTM 改进版实验总结。
- `docs/reproduction/c_lstm/reproduction/c_lstm_full_summary.md`（13.9 KB）：C-LSTM 论文复现完整版总结。
- `docs/reproduction/c_lstm/reproduction/c_lstm_reproduction.md`（4.0 KB）：C-LSTM 初版复现实验说明。

</details>

### `optimization.md`（1 个文件）

<details>
<summary>展开查看 <code>optimization.md</code> 下的保留文件</summary>

- `optimization.md`（6.6 KB）：优化思路、实验笔记或阶段性方案记录。

</details>

### `outputs`（73 个文件）

<details>
<summary>展开查看 <code>outputs</code> 下的保留文件</summary>

- `outputs/baseline/baseline_run/classification_report.txt`（609 B）：文本版分类报告。
- `outputs/baseline/baseline_run/confusion_matrix.png`（66.7 KB）：混淆矩阵图像。
- `outputs/baseline/baseline_run/metrics.json`（399 B）：该实验运行的核心指标汇总。
- `outputs/baseline/baseline_saved_test/classification_report.txt`（609 B）：文本版分类报告。
- `outputs/baseline/baseline_saved_test/confusion_matrix.png`（67.1 KB）：混淆矩阵图像。
- `outputs/baseline/baseline_saved_test/metrics.json`（399 B）：该实验运行的核心指标汇总。
- `outputs/baseline/baseline_saved_test/model.joblib`（10.0 MB）：scikit-learn 模型序列化文件。
- `outputs/c_lstm/improved/run_v1/classification_report.json`（1.7 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/run_v1/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/run_v1/confusion_matrix.png`（93.5 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/run_v1/history.json`（3.8 KB）：训练过程历史记录。
- `outputs/c_lstm/improved/run_v1/metrics.json`（770 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/run_v1/model.pt`（5.0 MB）：PyTorch 模型权重文件。
- `outputs/c_lstm/improved/run_v1/splits.npz`（68.1 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/reproduction/local_partial/packets_1480.npz`（7.7 MB）：C-LSTM 复现用的数据包张量数据集缓存。
- `outputs/c_lstm/reproduction/local_partial/packets_1480.summary.json`（5.3 KB）：C-LSTM 数据集构造摘要。
- `outputs/c_lstm/reproduction/local_partial/run_e3/classification_report.json`（1.7 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/reproduction/local_partial/run_e3/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/reproduction/local_partial/run_e3/confusion_matrix.png`（99.4 KB）：混淆矩阵图像。
- `outputs/c_lstm/reproduction/local_partial/run_e3/metrics.json`（426 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/reproduction/local_partial/run_e3/model.pt`（5.0 MB）：PyTorch 模型权重文件。
- `outputs/c_lstm/reproduction/local_partial/run_e3/splits.npz`（67.8 KB）：训练/验证/测试切分缓存。
- `outputs/deep_learning/flow_mlp_v1/classification_report.csv`（752 B）：CSV 版分类报告，便于后续表格处理。
- `outputs/deep_learning/flow_mlp_v1/classification_report.txt`（609 B）：文本版分类报告。
- `outputs/deep_learning/flow_mlp_v1/confusion_matrix.csv`（221 B）：混淆矩阵数值表。
- `outputs/deep_learning/flow_mlp_v1/confusion_matrix.png`（68.0 KB）：混淆矩阵图像。
- `outputs/deep_learning/flow_mlp_v1/history.json`（23.5 KB）：训练过程历史记录。
- `outputs/deep_learning/flow_mlp_v1/metrics.json`（3.7 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/flow_mlp_v1/model.pt`（231.4 KB）：PyTorch 模型权重文件。
- `outputs/deep_learning/flow_mlp_v1/preprocessor.joblib`（6.0 KB）：预处理器或特征工程流水线序列化文件。
- `outputs/deep_learning/flow_mlp_v1/splits.npz`（49.7 KB）：训练/验证/测试切分缓存。
- `outputs/deep_learning/flow_mlp_v1/test_predictions.csv`（162.2 KB）：测试集逐样本预测结果。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/classification_report.csv`（493 B）：CSV 版分类报告，便于后续表格处理。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/classification_report.txt`（444 B）：文本版分类报告。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/confusion_matrix.csv`（107 B）：混淆矩阵数值表。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/confusion_matrix.png`（46.9 KB）：混淆矩阵图像。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/encoded_test_outputs.npz`（1.7 KB）：编码后的测试集张量与标签缓存。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/history.json`（4.8 KB）：训练过程历史记录。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/metrics.json`（2.1 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/model.pt`（34.7 MB）：PyTorch 模型权重文件。
- `outputs/deep_learning/rifa_bilstm_only_rifa_v2/test_predictions.csv`（3.1 KB）：测试集逐样本预测结果。
- `outputs/deep_learning/rifa_textcnn_base_v1/classification_report.csv`（511 B）：CSV 版分类报告，便于后续表格处理。
- `outputs/deep_learning/rifa_textcnn_base_v1/classification_report.txt`（444 B）：文本版分类报告。
- `outputs/deep_learning/rifa_textcnn_base_v1/confusion_matrix.csv`（107 B）：混淆矩阵数值表。
- `outputs/deep_learning/rifa_textcnn_base_v1/confusion_matrix.png`（44.7 KB）：混淆矩阵图像。
- `outputs/deep_learning/rifa_textcnn_base_v1/encoded_test_outputs.npz`（1.7 KB）：编码后的测试集张量与标签缓存。
- `outputs/deep_learning/rifa_textcnn_base_v1/history.json`（6.8 KB）：训练过程历史记录。
- `outputs/deep_learning/rifa_textcnn_base_v1/metrics.json`（1.9 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/rifa_textcnn_base_v1/model.pt`（30.2 MB）：PyTorch 模型权重文件。
- `outputs/deep_learning/rifa_textcnn_base_v1/test_predictions.csv`（3.1 KB）：测试集逐样本预测结果。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/classification_report.csv`（510 B）：CSV 版分类报告，便于后续表格处理。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/classification_report.txt`（444 B）：文本版分类报告。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/confusion_matrix.csv`（107 B）：混淆矩阵数值表。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/confusion_matrix.png`（44.8 KB）：混淆矩阵图像。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/encoded_test_outputs.npz`（1.7 KB）：编码后的测试集张量与标签缓存。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/history.json`（3.5 KB）：训练过程历史记录。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/metrics.json`（1.9 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/model.pt`（30.2 MB）：PyTorch 模型权重文件。
- `outputs/deep_learning/rifa_textcnn_rifa_v1/test_predictions.csv`（3.1 KB）：测试集逐样本预测结果。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/command.json`（924 B）：运行命令与参数记录。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/metrics.json`（1.3 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/model.bin`（504.1 MB）：二进制模型权重文件。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/train.log`（5.0 KB）：训练日志。
- `outputs/optimized/final_optimized_v2_run/classification_report.csv`（723 B）：CSV 版分类报告，便于后续表格处理。
- `outputs/optimized/final_optimized_v2_run/classification_report.txt`（609 B）：文本版分类报告。
- `outputs/optimized/final_optimized_v2_run/confusion_matrix.csv`（214 B）：混淆矩阵数值表。
- `outputs/optimized/final_optimized_v2_run/feature_importance_summary.csv`（5.2 KB）：特征重要性汇总结果。
- `outputs/optimized/final_optimized_v2_run/final_optimized_model.joblib`（492.1 MB）：优化版集成模型序列化文件。
- `outputs/optimized/final_optimized_v2_run/metrics.json`（4.1 KB）：该实验运行的核心指标汇总。
- `outputs/optimized/final_optimized_v2_run/misclassification_pairs.csv`（499 B）：误分类类别对统计。
- `outputs/optimized/final_optimized_v2_run/misclassified_samples.csv`（153.8 KB）：误分类样本明细。
- `outputs/optimized/final_optimized_v2_run/test_predictions_detailed.csv`（2.4 MB）：测试集详细预测结果。
- `outputs/optimized/final_report.txt`（627 B）：实验或优化版总结报告文本。

</details>

### `project_plan_15_weeks.md`（1 个文件）

<details>
<summary>展开查看 <code>project_plan_15_weeks.md</code> 下的保留文件</summary>

- `project_plan_15_weeks.md`（7.5 KB）：项目 15 周推进计划文档。

</details>

### `readme.md`（1 个文件）

<details>
<summary>展开查看 <code>readme.md</code> 下的保留文件</summary>

- `readme.md`（6.4 KB）：项目总览与使用说明。

</details>

### `src`（127 个文件）

<details>
<summary>展开查看 <code>src</code> 下的保留文件</summary>

- `src/baseline/predict_baseline.py`（4.8 KB）：基线模型的无标签数据预测脚本。
- `src/baseline/train_baseline.py`（8.6 KB）：流级统计特征基线训练脚本。
- `src/deep_learning/run_pretrained_trafficformer.py`（6.3 KB）：对 TrafficFormer 预训练微调流程做项目内包装的运行脚本。
- `src/deep_learning/train_rifa_bilstm_transformer.py`（23.0 KB）：更强的 BiLSTM/Transformer 序列模型训练脚本。
- `src/deep_learning/train_rifa_textcnn.py`（18.0 KB）：自研 TextCNN 序列模型训练脚本，支持 RIFA。
- `src/deep_learning/train_tabular_mlp.py`（26.6 KB）：基于 ARFF 流级特征训练 MLP 的脚本。
- `src/README.md`（144 B）：源码目录布局说明。
- `src/reproduction/c_lstm/common.py`（6.0 KB）：C-LSTM 复现公用函数与数据处理工具。
- `src/reproduction/c_lstm/improved/predict_c_lstm.py`（249 B）：C-LSTM 改进版预测脚本。
- `src/reproduction/c_lstm/improved/predict_xgboost_gpu.py`（8.1 KB）：XGBoost GPU 支线预测脚本。
- `src/reproduction/c_lstm/improved/train_c_lstm_improved.py`（256 B）：C-LSTM 改进版训练脚本的改进目录副本。
- `src/reproduction/c_lstm/improved/train_xgboost_gpu.py`（10.8 KB）：C-LSTM 复现支线中的 XGBoost GPU 训练脚本。
- `src/reproduction/c_lstm/predict_c_lstm.py`（9.4 KB）：C-LSTM 预测脚本。
- `src/reproduction/c_lstm/prepare_dataset.py`（5.5 KB）：C-LSTM 数据集生成脚本。
- `src/reproduction/c_lstm/reproduction/predict_c_lstm.py`（249 B）：C-LSTM 论文复现实验专用预测脚本。
- `src/reproduction/c_lstm/reproduction/prepare_dataset.py`（250 B）：C-LSTM 论文复现实验专用数据准备脚本。
- `src/reproduction/c_lstm/reproduction/train_c_lstm.py`（247 B）：C-LSTM 论文复现实验专用训练脚本。
- `src/reproduction/c_lstm/train_c_lstm.py`（10.9 KB）：C-LSTM 基础训练脚本。
- `src/reproduction/c_lstm/train_c_lstm_improved.py`（11.0 KB）：C-LSTM 改进版训练脚本。
- `src/reproduction/TrafficFormer/.gitignore`（176 B）：TrafficFormer 子目录自己的 Git 忽略规则。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/dataset_stats.json`（191 B）：TrafficFormer 数据集统计信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/label_map.json`（72 B）：TrafficFormer 标签映射文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/test_dataset.tsv`（97.6 KB）：TrafficFormer 测试集 TSV。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/train_base_dataset.tsv`（773.7 KB）：TrafficFormer baseline 训练集 TSV。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/train_dataset.tsv`（3.8 MB）：TrafficFormer 当前激活的训练集 TSV，通常包含 paper-style 或 RIFA 处理结果。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/train_rifa_dataset.tsv`（3.8 MB）：TrafficFormer 仅 RIFA 增强后的训练集 TSV。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/valid_dataset.tsv`（96.6 KB）：TrafficFormer 验证集 TSV。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Chat/vpn_icq_chat1a.pcap`（475.2 KB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Chat/vpn_icq_chat1b.pcap`（409.4 KB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Chat/vpn_skype_chat1a.pcap`（829.3 KB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Chat/vpn_skype_chat1b.pcap`（980.9 KB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/FileTransfer/vpn_sftp_A.pcap`（78.5 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/FileTransfer/vpn_sftp_B.pcap`（17.1 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/FileTransfer/vpn_skype_files1a.pcap`（8.6 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/FileTransfer/vpn_skype_files1b.pcap`（6.4 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Streaming/vpn_netflix_A.pcap`（769.1 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Streaming/vpn_spotify_A.pcap`（98.6 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Streaming/vpn_vimeo_A.pcap`（118.8 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Streaming/vpn_vimeo_B.pcap`（242.8 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/Streaming/vpn_youtube_A.pcap`（173.8 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/VoIP/vpn_skype_audio1.pcap`（47.2 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/VoIP/vpn_skype_audio2.pcap`（47.1 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/VoIP/vpn_voipbuster1a.pcap`（49.3 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/pcap/VoIP/vpn_voipbuster1b.pcap`（49.2 MB）：TrafficFormer 复现中按类别整理的原始或筛选 PCAP 文件。
- `src/reproduction/TrafficFormer/data_generation/__init__.py`（0 B）：TrafficFormer 数据生成子包初始化文件。
- `src/reproduction/TrafficFormer/data_generation/finetuning_data_gen.py`（33.8 KB）：TrafficFormer 微调数据生成脚本。
- `src/reproduction/TrafficFormer/data_generation/pretrain_data_gen.py`（21.1 KB）：TrafficFormer 预训练数据生成脚本。
- `src/reproduction/TrafficFormer/data_generation/SplitCap.exe`（500.7 KB）：将原始 PCAP 切分为单流文件的可执行工具。
- `src/reproduction/TrafficFormer/data_generation/utils.py`（6.3 KB）：TrafficFormer 数据生成工具函数。
- `src/reproduction/TrafficFormer/data_generation/vocab_gen.py`（1.6 KB）：TrafficFormer 词表生成脚本。
- `src/reproduction/TrafficFormer/docs/REPRODUCE_legacy.md`（13.9 KB）：TrafficFormer 较早阶段的复现说明文档。
- `src/reproduction/TrafficFormer/docs/STATUS.md`（4.5 KB）：TrafficFormer 当前复现状态与结果说明。
- `src/reproduction/TrafficFormer/fine-tuning/run_classifier.py`（16.9 KB）：TrafficFormer 分类微调主脚本。
- `src/reproduction/TrafficFormer/fine-tuning/run_mlm.py`（18.0 KB）：TrafficFormer 掩码语言模型微调脚本。
- `src/reproduction/TrafficFormer/LICENSE`（1.1 KB）：TrafficFormer 原项目许可证。
- `src/reproduction/TrafficFormer/models/bert/base_config.json`（186 B）：BERT base 结构配置。
- `src/reproduction/TrafficFormer/models/bert/base_config2.json`（210 B）：BERT base 结构配置的备用版本。
- `src/reproduction/TrafficFormer/models/bert/large_config.json`（188 B）：BERT large 结构配置。
- `src/reproduction/TrafficFormer/models/bert/medium_config.json`（184 B）：BERT medium 结构配置。
- `src/reproduction/TrafficFormer/models/bert/mini_config.json`（184 B）：BERT mini 结构配置。
- `src/reproduction/TrafficFormer/models/bert/small_config.json`（184 B）：BERT small 结构配置。
- `src/reproduction/TrafficFormer/models/bert/tiny_config.json`（183 B）：BERT tiny 结构配置。
- `src/reproduction/TrafficFormer/models/encryptd_vocab.txt`（351.6 KB）：TrafficFormer 当前使用的加密流量词表。
- `src/reproduction/TrafficFormer/models/encryptd_vocab_base.txt`（124.0 KB）：TrafficFormer 基础词表文件。
- `src/reproduction/TrafficFormer/models/finetuned_model.bin`（504.1 MB）：TrafficFormer baseline 微调模型权重。
- `src/reproduction/TrafficFormer/models/finetuned_model_rifa.bin`（504.1 MB）：TrafficFormer 加入 RIFA 后的微调模型权重。
- `src/reproduction/TrafficFormer/models/pretrain_model.bin`（633.2 MB）：TrafficFormer 预训练模型权重。
- `src/reproduction/TrafficFormer/models/pretrain_model.resolved.bin`（682.4 MB）：解析归档后的预训练模型权重副本。
- `src/reproduction/TrafficFormer/pre-training/preprocess.py`（4.3 KB）：TrafficFormer 预训练前的数据预处理脚本。
- `src/reproduction/TrafficFormer/pre-training/pretrain.py`（7.6 KB）：TrafficFormer 预训练脚本。
- `src/reproduction/TrafficFormer/README.md`（17.2 KB）：TrafficFormer 复现目录的使用说明。
- `src/reproduction/TrafficFormer/requirements.txt`（314 B）：TrafficFormer 复现依赖列表。
- `src/reproduction/TrafficFormer/run_pipeline.bat`（4.8 KB）：Windows 下运行 TrafficFormer 数据准备与训练流程的批处理脚本。
- `src/reproduction/TrafficFormer/run_pipeline.sh`（3.1 KB）：Shell 下运行 TrafficFormer 数据准备与训练流程的脚本。
- `src/reproduction/TrafficFormer/scripts/check_env.py`（1.7 KB）：检查 TrafficFormer 运行环境与关键依赖的脚本。
- `src/reproduction/TrafficFormer/scripts/download_pretrain_model.py`（4.6 KB）：下载并整理 TrafficFormer 预训练模型的脚本。
- `src/reproduction/TrafficFormer/scripts/generate_finetune_data.py`（17.4 KB）：生成 TrafficFormer 微调数据集并支持 RIFA 的脚本。
- `src/reproduction/TrafficFormer/scripts/prepare_iscxvpn_data.py`（8.6 KB）：为 TrafficFormer 准备 ISCX-VPN service 数据的脚本。
- `src/reproduction/TrafficFormer/uer/__init__.py`（0 B）：Python 脚本或模块文件。
- `src/reproduction/TrafficFormer/uer/decoders/__init__.py`（173 B）：UER 解码器实现模块。
- `src/reproduction/TrafficFormer/uer/decoders/transformer_decoder.py`（3.3 KB）：UER 解码器实现模块。
- `src/reproduction/TrafficFormer/uer/encoders/__init__.py`（843 B）：UER 编码器实现模块。
- `src/reproduction/TrafficFormer/uer/encoders/cnn_encoder.py`（2.8 KB）：UER 编码器实现模块。
- `src/reproduction/TrafficFormer/uer/encoders/rnn_encoder.py`（5.8 KB）：UER 编码器实现模块。
- `src/reproduction/TrafficFormer/uer/encoders/transformer_encoder.py`（5.1 KB）：UER 编码器实现模块。
- `src/reproduction/TrafficFormer/uer/layers/__init__.py`（531 B）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/embeddings.py`（4.9 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/layer_norm.py`（1.1 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/moe_layer.py`（7.4 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/multi_headed_attn.py`（2.6 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/position_ffn.py`（2.4 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/relative_position_embedding.py`（4.6 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/synthesizer.py`（4.7 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/layers/transformer.py`（10.2 KB）：UER 网络层实现模块。
- `src/reproduction/TrafficFormer/uer/model_builder.py`（675 B）：Python 脚本或模块文件。
- `src/reproduction/TrafficFormer/uer/model_loader.py`（2.6 KB）：Python 脚本或模块文件。
- `src/reproduction/TrafficFormer/uer/model_saver.py`（210 B）：Python 脚本或模块文件。
- `src/reproduction/TrafficFormer/uer/models/__init__.py`（0 B）：UER 模型定义模块。
- `src/reproduction/TrafficFormer/uer/models/model.py`（1.3 KB）：UER 模型定义模块。
- `src/reproduction/TrafficFormer/uer/opts.py`（7.1 KB）：Python 脚本或模块文件。
- `src/reproduction/TrafficFormer/uer/targets/__init__.py`（944 B）：UER 训练目标函数模块。
- `src/reproduction/TrafficFormer/uer/targets/albert_target.py`（1.7 KB）：ALBERT 目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/bert_target.py`（1.6 KB）：BERT 目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/bertflow_target.py`（1.6 KB）：BERTFlow 风格目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/bilm_target.py`（1.1 KB）：双向语言模型目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/cls_target.py`（1.5 KB）：分类任务目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/lm_target.py`（1.7 KB）：语言模型目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/mlm_target.py`（3.8 KB）：掩码语言模型目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/nsp_target.py`（1.0 KB）：下一句预测目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/prefixlm_target.py`（111 B）：PrefixLM 目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/seq2seq_target.py`（1.1 KB）：序列到序列任务目标函数定义。
- `src/reproduction/TrafficFormer/uer/targets/t5_target.py`（1.0 KB）：T5 风格目标函数定义。
- `src/reproduction/TrafficFormer/uer/test.txt`（2 B）：源码目录中的文本资源文件。
- `src/reproduction/TrafficFormer/uer/trainer.py`（17.0 KB）：Python 脚本或模块文件。
- `src/reproduction/TrafficFormer/uer/utils/__init__.py`（2.3 KB）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/act_fun.py`（1.0 KB）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/config.py`（287 B）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/constants.py`（225 B）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/data.py`（57.3 KB）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/misc.py`（540 B）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/optimizers.py`（22.5 KB）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/seed.py`（292 B）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/subword.py`（675 B）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/tokenizers.py`（15.4 KB）：UER 工具模块。
- `src/reproduction/TrafficFormer/uer/utils/vocab.py`（3.9 KB）：UER 工具模块。
- `src/teammate_optimized/train_final_optimized.py`（10.2 KB）：同事原始优化版训练脚本。
- `src/teammate_optimized/train_final_optimized_v2.py`（20.0 KB）：进一步整理后的优化版训练脚本。

</details>

### `tools`（2 个文件）

<details>
<summary>展开查看 <code>tools</code> 下的保留文件</summary>

- `tools/build_opening_report_docx.py`（12.6 KB）：将开题报告 Markdown 转换或整理为 Word 报告的工具脚本。
- `tools/build_requirements_docx.py`（5.8 KB）：将需求分析 Markdown 转换或整理为 Word 报告的工具脚本。

</details>

### `信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx`（1 个文件）

<details>
<summary>展开查看 <code>信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx</code> 下的保留文件</summary>

- `信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx`（15.2 KB）：当前项目的课程过程控制简表。

</details>

### `组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（1 个文件）

<details>
<summary>展开查看 <code>组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx</code> 下的保留文件</summary>

- `组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（44.1 KB）：当前项目的开题报告 Word 文件。

</details>
