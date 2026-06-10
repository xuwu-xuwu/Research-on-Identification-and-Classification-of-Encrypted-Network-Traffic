# 当前工作目录文件说明（截至 2026-04-07）

本文档基于当前工作目录中的实际文件自动生成，覆盖源码、文档、数据集、实验输出、缓存文件以及 Git 元数据。

说明：

- 为了保证覆盖范围，文档包含 `.git`、`__pycache__`、训练缓存和自动生成结果。
- 关键项目文件采用人工增强描述；重复性很强的缓存、抓包和 Git 内部文件采用统一规则描述。
- 统计口径不包含本文档自身，共记录 `1172` 个文件。

## 顶层统计

| 顶层路径 | 文件数 |
| --- | ---: |
| `.git` | 32 |
| `.gitignore` | 1 |
| `.vscode` | 2 |
| `catboost_info` | 5 |
| `data` | 54 |
| `docs` | 18 |
| `optimization.md` | 1 |
| `outputs` | 176 |
| `project_plan_15_weeks.md` | 1 |
| `readme.md` | 1 |
| `src` | 866 |
| `tools` | 2 |
| `信息系统安全与对抗技术-报告模板` | 11 |
| `信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx` | 1 |
| `组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx` | 1 |

## 文件清单

### `.git`（32 个文件）

<details>
<summary>展开查看 <code>.git</code> 下的全部文件</summary>

- `.git/COMMIT_EDITMSG`（13 B）：Git 内部元数据文件。
- `.git/config`（366 B）：Git 仓库配置文件。
- `.git/description`（73 B）：Git 仓库描述文件。
- `.git/HEAD`（21 B）：Git 当前分支或提交引用文件。
- `.git/hooks/applypatch-msg.sample`（478 B）：Git hook 示例脚本。
- `.git/hooks/commit-msg.sample`（896 B）：Git hook 示例脚本。
- `.git/hooks/fsmonitor-watchman.sample`（4.6 KB）：Git hook 示例脚本。
- `.git/hooks/post-update.sample`（189 B）：Git hook 示例脚本。
- `.git/hooks/pre-applypatch.sample`（424 B）：Git hook 示例脚本。
- `.git/hooks/pre-commit.sample`（1.6 KB）：Git hook 示例脚本。
- `.git/hooks/pre-merge-commit.sample`（416 B）：Git hook 示例脚本。
- `.git/hooks/pre-push.sample`（1.3 KB）：Git hook 示例脚本。
- `.git/hooks/pre-rebase.sample`（4.8 KB）：Git hook 示例脚本。
- `.git/hooks/pre-receive.sample`（544 B）：Git hook 示例脚本。
- `.git/hooks/prepare-commit-msg.sample`（1.5 KB）：Git hook 示例脚本。
- `.git/hooks/push-to-checkout.sample`（2.7 KB）：Git hook 示例脚本。
- `.git/hooks/sendemail-validate.sample`（2.3 KB）：Git hook 示例脚本。
- `.git/hooks/update.sample`（3.6 KB）：Git hook 示例脚本。
- `.git/index`（473 B）：Git 暂存区索引文件。
- `.git/info/exclude`（240 B）：Git 局部忽略规则文件。
- `.git/logs/HEAD`（524 B）：Git 当前分支或提交引用文件。
- `.git/logs/refs/heads/main`（342 B）：Git 引用文件，记录分支或远程分支指向。
- `.git/logs/refs/remotes/origin/main`（144 B）：Git 引用文件，记录分支或远程分支指向。
- `.git/objects/00/eb3d4de752ebf50c5c72cd91c267b814dc45b7`（3.5 KB）：Git 对象文件，存储提交、树或 blob 数据。
- `.git/objects/07/4589f9ff4fc007a6e61728f42c0a26773fb5c3`（4.0 KB）：Git 对象文件，存储提交、树或 blob 数据。
- `.git/objects/79/0c8139dfba8e1f3aaca75ad650038c56740dde`（1.8 KB）：Git 对象文件，存储提交、树或 blob 数据。
- `.git/objects/ac/46f093977e160859c663c96ef6c22276a69a4c`（139 B）：Git 对象文件，存储提交、树或 blob 数据。
- `.git/objects/c2/7f7962732754dd0ddc7dcee76d1523072cd426`（246 B）：Git 对象文件，存储提交、树或 blob 数据。
- `.git/objects/e3/8e6533ff7e6d6ea273a54c1cdeb90866583ea1`（205 B）：Git 对象文件，存储提交、树或 blob 数据。
- `.git/objects/e8/42c3da3bbf1673d02434e0aa0ef01ab1e44817`（3.3 KB）：Git 对象文件，存储提交、树或 blob 数据。
- `.git/refs/heads/main`（41 B）：Git 引用文件，记录分支或远程分支指向。
- `.git/refs/remotes/origin/main`（41 B）：Git 引用文件，记录分支或远程分支指向。

</details>

### `.gitignore`（1 个文件）

<details>
<summary>展开查看 <code>.gitignore</code> 下的全部文件</summary>

- `.gitignore`（268 B）：Git 忽略规则文件，控制哪些生成物、缓存和本地资源不纳入版本管理。

</details>

### `.vscode`（2 个文件）

<details>
<summary>展开查看 <code>.vscode</code> 下的全部文件</summary>

- `.vscode/launch.json`（476 B）：VS Code 调试启动配置。
- `.vscode/settings.json`（135 B）：VS Code 工作区设置。

</details>

### `catboost_info`（5 个文件）

<details>
<summary>展开查看 <code>catboost_info</code> 下的全部文件</summary>

- `catboost_info/catboost_training.json`（2.1 KB）：CatBoost 训练过程元数据。
- `catboost_info/learn/events.out.tfevents`（1.2 KB）：TensorBoard 事件日志。
- `catboost_info/learn_error.tsv`（315 B）：CatBoost 学习误差日志。
- `catboost_info/time_left.tsv`（361 B）：CatBoost 剩余时间日志。
- `catboost_info/tmp/cat_feature_index.d674d4dd-f69689e7-4a52d50d-5d0c572a.tmp`（4 B）：CatBoost 训练过程中生成的临时文件。

</details>

### `data`（54 个文件）

<details>
<summary>展开查看 <code>data</code> 下的全部文件</summary>

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

### `docs`（18 个文件）

<details>
<summary>展开查看 <code>docs</code> 下的全部文件</summary>

- `docs/analysis/next_optimization_points.md`（8.4 KB）：下一轮优化方向整理文档。
- `docs/analysis/teammate_optimization_analysis.md`（5.9 KB）：同事优化版整体策略分析文档。
- `docs/analysis/train_final_optimized_code_analysis.md`（18.6 KB）：优化训练脚本的代码级解析文档。
- `docs/analysis/train_final_optimized_tech_stack.md`（9.6 KB）：优化版技术栈与方法路线说明。
- `docs/project_memory.md`（12.4 KB）：项目记忆文档，用于后续续接时快速恢复上下文。
- `docs/references/Machine_Learning-Powered_Encrypted_Network_Traffic_Analysis_A_Comprehensive_Survey.pdf`（5.6 MB）：加密流量机器学习分析综述论文 PDF。
- `docs/reports/requirements_report_fixed.docx`（64.9 KB）：修整后的需求分析报告 Word 文件。
- `docs/reports/workspace_file_catalog_2026-04-07.md`（209.0 KB）：当前工作目录文件说明的英文版。
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
<summary>展开查看 <code>optimization.md</code> 下的全部文件</summary>

- `optimization.md`（6.6 KB）：优化思路、实验笔记或阶段性方案记录。

</details>

### `outputs`（176 个文件）

<details>
<summary>展开查看 <code>outputs</code> 下的全部文件</summary>

- `outputs/baseline/baseline_run/classification_report.txt`（609 B）：文本版分类报告。
- `outputs/baseline/baseline_run/confusion_matrix.png`（66.7 KB）：混淆矩阵图像。
- `outputs/baseline/baseline_run/metrics.json`（399 B）：该实验运行的核心指标汇总。
- `outputs/baseline/baseline_saved_test/classification_report.txt`（609 B）：文本版分类报告。
- `outputs/baseline/baseline_saved_test/confusion_matrix.png`（67.1 KB）：混淆矩阵图像。
- `outputs/baseline/baseline_saved_test/metrics.json`（399 B）：该实验运行的核心指标汇总。
- `outputs/baseline/baseline_saved_test/model.joblib`（10.0 MB）：scikit-learn 模型序列化文件。
- `outputs/baseline/baseline_smoke/classification_report.txt`（609 B）：文本版分类报告。
- `outputs/baseline/baseline_smoke/confusion_matrix.png`（67.3 KB）：混淆矩阵图像。
- `outputs/baseline/baseline_smoke/metrics.json`（400 B）：该实验运行的核心指标汇总。
- `outputs/baseline/predictions/predictions_smoke.csv`（3.7 MB）：基线预测链路的冒烟测试输出。
- `outputs/c_lstm/improved/prediction_raw_nonvpn01/capture_predictions.json`（8.7 KB）：按抓包或会话聚合的预测结果摘要。
- `outputs/c_lstm/improved/prediction_raw_nonvpn01/packet_predictions.csv`（163.4 KB）：逐数据包预测结果。
- `outputs/c_lstm/improved/prediction_raw_nonvpn01/prediction_summary.json`（813 B）：预测任务总体摘要。
- `outputs/c_lstm/improved/run_v1/classification_report.json`（1.7 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/run_v1/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/run_v1/confusion_matrix.png`（93.5 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/run_v1/history.json`（3.8 KB）：训练过程历史记录。
- `outputs/c_lstm/improved/run_v1/metrics.json`（770 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/run_v1/model.pt`（5.0 MB）：PyTorch 模型权重文件。
- `outputs/c_lstm/improved/run_v1/splits.npz`（68.1 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/improved/xgboost_gpu_scout.json`（111 B）：实验输出结构化结果。
- `outputs/c_lstm/improved/xgboost_gpu_v1/classification_report.json`（1.6 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/xgboost_gpu_v1/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/xgboost_gpu_v1/confusion_matrix.png`（86.1 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/xgboost_gpu_v1/metrics.json`（513 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/xgboost_gpu_v1/model.json`（14.7 MB）：XGBoost 或类似模型的结构或权重导出文件。
- `outputs/c_lstm/improved/xgboost_gpu_v1/model_meta.json`（341 B）：模型元数据与标签映射说明。
- `outputs/c_lstm/improved/xgboost_gpu_v1/predictions.npz`（20.9 KB）：数值化预测输出缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v1/splits.npz`（67.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v1_prediction_raw_nonvpn01/capture_predictions.json`（6.5 KB）：按抓包或会话聚合的预测结果摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v1_prediction_raw_nonvpn01/packet_predictions.csv`（109.4 KB）：逐数据包预测结果。
- `outputs/c_lstm/improved/xgboost_gpu_v1_prediction_raw_nonvpn01/prediction_summary.json`（810 B）：预测任务总体摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/classification_report.json`（1.6 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/confusion_matrix.png`（94.7 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/metrics.json`（634 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/model.json`（13.5 MB）：XGBoost 或类似模型的结构或权重导出文件。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/model_meta.json`（369 B）：模型元数据与标签映射说明。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/predictions.npz`（9.5 KB）：数值化预测输出缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/split_summary.json`（4.1 KB）：数据切分统计摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_balanced/splits.npz`（38.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/classification_report.json`（1.6 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/confusion_matrix.png`（95.2 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/metrics.json`（607 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/model.json`（14.0 MB）：XGBoost 或类似模型的结构或权重导出文件。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/model_meta.json`（369 B）：模型元数据与标签映射说明。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/predictions.npz`（9.5 KB）：数值化预测输出缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/split_summary.json`（4.1 KB）：数据切分统计摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_base/splits.npz`（38.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/classification_report.json`（1.6 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/confusion_matrix.png`（94.4 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/metrics.json`（608 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/model.json`（8.0 MB）：XGBoost 或类似模型的结构或权重导出文件。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/model_meta.json`（369 B）：模型元数据与标签映射说明。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/predictions.npz`（9.6 KB）：数值化预测输出缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/split_summary.json`（4.1 KB）：数据切分统计摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_medium/splits.npz`（38.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/classification_report.json`（1.7 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/confusion_matrix.png`（94.3 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/metrics.json`（606 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/model.json`（14.6 MB）：XGBoost 或类似模型的结构或权重导出文件。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/model_meta.json`（369 B）：模型元数据与标签映射说明。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/predictions.npz`（9.6 KB）：数值化预测输出缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/split_summary.json`（4.1 KB）：数据切分统计摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v2_capture_regularized/splits.npz`（38.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/classification_report.json`（1.6 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/confusion_matrix.png`（86.2 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/metrics.json`（607 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/model.json`（26.2 MB）：XGBoost 或类似模型的结构或权重导出文件。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/model_meta.json`（368 B）：模型元数据与标签映射说明。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/predictions.npz`（20.9 KB）：数值化预测输出缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/split_summary.json`（8.1 KB）：数据切分统计摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_deep/splits.npz`（68.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/classification_report.json`（1.6 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/confusion_matrix.png`（86.3 KB）：混淆矩阵图像。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/metrics.json`（606 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/model.json`（26.8 MB）：XGBoost 或类似模型的结构或权重导出文件。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/model_meta.json`（368 B）：模型元数据与标签映射说明。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/predictions.npz`（20.9 KB）：数值化预测输出缓存。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/split_summary.json`（8.1 KB）：数据切分统计摘要。
- `outputs/c_lstm/improved/xgboost_gpu_v2_random_wide/splits.npz`（68.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/reproduction/local_partial/packets_1480.npz`（7.7 MB）：Numpy 压缩缓存文件。
- `outputs/c_lstm/reproduction/local_partial/packets_1480.summary.json`（5.3 KB）：实验输出结构化结果。
- `outputs/c_lstm/reproduction/local_partial/run_e3/classification_report.json`（1.7 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/reproduction/local_partial/run_e3/classification_report.txt`（784 B）：文本版分类报告。
- `outputs/c_lstm/reproduction/local_partial/run_e3/confusion_matrix.png`（99.4 KB）：混淆矩阵图像。
- `outputs/c_lstm/reproduction/local_partial/run_e3/metrics.json`（426 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/reproduction/local_partial/run_e3/model.pt`（5.0 MB）：PyTorch 模型权重文件。
- `outputs/c_lstm/reproduction/local_partial/run_e3/splits.npz`（67.8 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/reproduction/prediction_raw_nonvpn01/capture_predictions.json`（9.0 KB）：按抓包或会话聚合的预测结果摘要。
- `outputs/c_lstm/reproduction/prediction_raw_nonvpn01/packet_predictions.csv`（166.4 KB）：逐数据包预测结果。
- `outputs/c_lstm/reproduction/prediction_raw_nonvpn01/prediction_summary.json`（815 B）：预测任务总体摘要。
- `outputs/c_lstm/reproduction/prediction_test_split/capture_predictions.json`（39.7 KB）：按抓包或会话聚合的预测结果摘要。
- `outputs/c_lstm/reproduction/prediction_test_split/packet_predictions.csv`（395.2 KB）：逐数据包预测结果。
- `outputs/c_lstm/reproduction/prediction_test_split/prediction_summary.json`（1.3 KB）：预测任务总体摘要。
- `outputs/c_lstm/reproduction/smoke/run/classification_report.json`（1.3 KB）：JSON 版分类报告，便于程序读取。
- `outputs/c_lstm/reproduction/smoke/run/classification_report.txt`（724 B）：文本版分类报告。
- `outputs/c_lstm/reproduction/smoke/run/confusion_matrix.png`（72.0 KB）：混淆矩阵图像。
- `outputs/c_lstm/reproduction/smoke/run/metrics.json`（410 B）：该实验运行的核心指标汇总。
- `outputs/c_lstm/reproduction/smoke/run/model.pt`（5.0 MB）：PyTorch 模型权重文件。
- `outputs/c_lstm/reproduction/smoke/run/splits.npz`（6.3 KB）：训练/验证/测试切分缓存。
- `outputs/c_lstm/reproduction/smoke/smoke_packets.npz`（523.2 KB）：冒烟测试用的数据包张量缓存。
- `outputs/c_lstm/reproduction/smoke/smoke_packets.summary.json`（2.3 KB）：冒烟测试数据摘要。
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
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/classification_report.csv`（462 B）：CSV 版分类报告，便于后续表格处理。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/classification_report.txt`（444 B）：文本版分类报告。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/confusion_matrix.csv`（107 B）：混淆矩阵数值表。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/confusion_matrix.png`（45.3 KB）：混淆矩阵图像。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/encoded_test_outputs.npz`（1.7 KB）：编码后的测试集张量与标签缓存。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/history.json`（3.6 KB）：训练过程历史记录。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/metrics.json`（2.0 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/model.pt`（42.6 MB）：PyTorch 模型权重文件。
- `outputs/deep_learning/rifa_bilstm_transformer_rifa_v1/test_predictions.csv`（3.0 KB）：测试集逐样本预测结果。
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
- `outputs/deep_learning/trafficformer_transformer_rifa_v1/command.json`（908 B）：运行命令与参数记录。
- `outputs/deep_learning/trafficformer_transformer_rifa_v1/metrics.json`（1.3 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/trafficformer_transformer_rifa_v1/model.bin`（504.1 MB）：二进制模型权重文件。
- `outputs/deep_learning/trafficformer_transformer_rifa_v1/train.log`（4.4 KB）：训练日志。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/command.json`（924 B）：运行命令与参数记录。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/metrics.json`（1.3 KB）：该实验运行的核心指标汇总。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/model.bin`（504.1 MB）：二进制模型权重文件。
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/train.log`（5.0 KB）：训练日志。
- `outputs/optimized/final_optimized_model.joblib`（138.3 MB）：优化版集成模型序列化文件。
- `outputs/optimized/final_optimized_run/final_optimized_model.joblib`（138.5 MB）：优化版集成模型序列化文件。
- `outputs/optimized/final_optimized_run/final_report.txt`（627 B）：实验或优化版总结报告文本。
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
<summary>展开查看 <code>project_plan_15_weeks.md</code> 下的全部文件</summary>

- `project_plan_15_weeks.md`（7.5 KB）：项目 15 周推进计划文档。

</details>

### `readme.md`（1 个文件）

<details>
<summary>展开查看 <code>readme.md</code> 下的全部文件</summary>

- `readme.md`（6.4 KB）：项目总览与使用说明。

</details>

### `src`（866 个文件）

<details>
<summary>展开查看 <code>src</code> 下的全部文件</summary>

- `src/baseline/predict_baseline.py`（4.8 KB）：基线模型的无标签数据预测脚本。
- `src/baseline/train_baseline.py`（8.6 KB）：流级统计特征基线训练脚本。
- `src/deep_learning/run_pretrained_trafficformer.py`（6.3 KB）：对 TrafficFormer 预训练微调流程做项目内包装的运行脚本。
- `src/deep_learning/train_rifa_bilstm_transformer.py`（23.0 KB）：更强的 BiLSTM/Transformer 序列模型训练脚本。
- `src/deep_learning/train_rifa_textcnn.py`（18.0 KB）：自研 TextCNN 序列模型训练脚本，支持 RIFA。
- `src/deep_learning/train_tabular_mlp.py`（26.6 KB）：基于 ARFF 流级特征训练 MLP 的脚本。
- `src/README.md`（144 B）：源码目录布局说明。
- `src/reproduction/c_lstm/__pycache__/common.cpython-313.pyc`（8.5 KB）：Python 字节码缓存，对应源文件 `common.py`。
- `src/reproduction/c_lstm/__pycache__/predict_c_lstm.cpython-313.pyc`（12.7 KB）：Python 字节码缓存，对应源文件 `predict_c_lstm.py`。
- `src/reproduction/c_lstm/__pycache__/prepare_dataset.cpython-313.pyc`（7.1 KB）：Python 字节码缓存，对应源文件 `prepare_dataset.py`。
- `src/reproduction/c_lstm/__pycache__/train_c_lstm.cpython-313.pyc`（16.7 KB）：Python 字节码缓存，对应源文件 `train_c_lstm.py`。
- `src/reproduction/c_lstm/__pycache__/train_c_lstm_improved.cpython-313.pyc`（14.9 KB）：Python 字节码缓存，对应源文件 `train_c_lstm_improved.py`。
- `src/reproduction/c_lstm/common.py`（6.0 KB）：C-LSTM 复现公用函数与数据处理工具。
- `src/reproduction/c_lstm/improved/__pycache__/predict_c_lstm.cpython-313.pyc`（562 B）：Python 字节码缓存，对应源文件 `predict_c_lstm.py`。
- `src/reproduction/c_lstm/improved/__pycache__/predict_xgboost_gpu.cpython-313.pyc`（11.2 KB）：Python 字节码缓存，对应源文件 `predict_xgboost_gpu.py`。
- `src/reproduction/c_lstm/improved/__pycache__/train_c_lstm_improved.cpython-313.pyc`（576 B）：Python 字节码缓存，对应源文件 `train_c_lstm_improved.py`。
- `src/reproduction/c_lstm/improved/__pycache__/train_xgboost_gpu.cpython-313.pyc`（14.4 KB）：Python 字节码缓存，对应源文件 `train_xgboost_gpu.py`。
- `src/reproduction/c_lstm/improved/predict_c_lstm.py`（249 B）：C-LSTM 改进版预测脚本。
- `src/reproduction/c_lstm/improved/predict_xgboost_gpu.py`（8.1 KB）：XGBoost GPU 支线预测脚本。
- `src/reproduction/c_lstm/improved/train_c_lstm_improved.py`（256 B）：C-LSTM 改进版训练脚本的改进目录副本。
- `src/reproduction/c_lstm/improved/train_xgboost_gpu.py`（10.8 KB）：C-LSTM 复现支线中的 XGBoost GPU 训练脚本。
- `src/reproduction/c_lstm/predict_c_lstm.py`（9.4 KB）：C-LSTM 预测脚本。
- `src/reproduction/c_lstm/prepare_dataset.py`（5.5 KB）：C-LSTM 数据集生成脚本。
- `src/reproduction/c_lstm/reproduction/__pycache__/predict_c_lstm.cpython-313.pyc`（566 B）：Python 字节码缓存，对应源文件 `predict_c_lstm.py`。
- `src/reproduction/c_lstm/reproduction/__pycache__/prepare_dataset.cpython-313.pyc`（568 B）：Python 字节码缓存，对应源文件 `prepare_dataset.py`。
- `src/reproduction/c_lstm/reproduction/__pycache__/train_c_lstm.cpython-313.pyc`（562 B）：Python 字节码缓存，对应源文件 `train_c_lstm.py`。
- `src/reproduction/c_lstm/reproduction/predict_c_lstm.py`（249 B）：C-LSTM 论文复现实验专用预测脚本。
- `src/reproduction/c_lstm/reproduction/prepare_dataset.py`（250 B）：C-LSTM 论文复现实验专用数据准备脚本。
- `src/reproduction/c_lstm/reproduction/train_c_lstm.py`（247 B）：C-LSTM 论文复现实验专用训练脚本。
- `src/reproduction/c_lstm/train_c_lstm.py`（10.9 KB）：C-LSTM 基础训练脚本。
- `src/reproduction/c_lstm/train_c_lstm_improved.py`（11.0 KB）：C-LSTM 改进版训练脚本。
- `src/reproduction/TrafficFormer/.git/config`（337 B）：Git 仓库配置文件。
- `src/reproduction/TrafficFormer/.git/description`（73 B）：Git 仓库描述文件。
- `src/reproduction/TrafficFormer/.git/HEAD`（21 B）：Git 当前分支或提交引用文件。
- `src/reproduction/TrafficFormer/.git/hooks/applypatch-msg.sample`（478 B）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/commit-msg.sample`（896 B）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/fsmonitor-watchman.sample`（4.6 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/post-update.sample`（189 B）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/pre-applypatch.sample`（424 B）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/pre-commit.sample`（1.6 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/pre-merge-commit.sample`（416 B）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/pre-push.sample`（1.3 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/pre-rebase.sample`（4.8 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/pre-receive.sample`（544 B）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/prepare-commit-msg.sample`（1.5 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/push-to-checkout.sample`（2.7 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/sendemail-validate.sample`（2.3 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/hooks/update.sample`（3.6 KB）：Git hook 示例脚本。
- `src/reproduction/TrafficFormer/.git/index`（13.2 KB）：Git 暂存区索引文件。
- `src/reproduction/TrafficFormer/.git/info/exclude`（240 B）：Git 局部忽略规则文件。
- `src/reproduction/TrafficFormer/.git/logs/HEAD`（187 B）：Git 当前分支或提交引用文件。
- `src/reproduction/TrafficFormer/.git/logs/refs/heads/main`（187 B）：Git 引用文件，记录分支或远程分支指向。
- `src/reproduction/TrafficFormer/.git/logs/refs/remotes/origin/HEAD`（187 B）：Git 当前分支或提交引用文件。
- `src/reproduction/TrafficFormer/.git/objects/pack/pack-e0f40045c5555e073c6d5ace80ff24d0786c6515.idx`（5.5 KB）：Git packfile 或索引文件，用于存储压缩后的版本对象。
- `src/reproduction/TrafficFormer/.git/objects/pack/pack-e0f40045c5555e073c6d5ace80ff24d0786c6515.pack`（624.3 KB）：Git packfile 或索引文件，用于存储压缩后的版本对象。
- `src/reproduction/TrafficFormer/.git/objects/pack/pack-e0f40045c5555e073c6d5ace80ff24d0786c6515.rev`（704 B）：Git packfile 或索引文件，用于存储压缩后的版本对象。
- `src/reproduction/TrafficFormer/.git/packed-refs`（112 B）：Git 打包引用文件。
- `src/reproduction/TrafficFormer/.git/refs/heads/main`（41 B）：Git 引用文件，记录分支或远程分支指向。
- `src/reproduction/TrafficFormer/.git/refs/remotes/origin/HEAD`（30 B）：Git 当前分支或提交引用文件。
- `src/reproduction/TrafficFormer/.gitignore`（176 B）：文件用途未显式标注，可根据所在目录继续追踪。
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
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_icq_chat1a.pcap.TCP_10-8-8-178_40028_137-117-177-33_443.pcap`（11.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_icq_chat1a.pcap.TCP_10-8-8-178_51318_178-237-17-103_443.pcap`（874.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_icq_chat1a.pcap.TCP_10-8-8-178_54269_134-170-25-26_443.pcap`（32.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_icq_chat1a.pcap.TCP_10-8-8-178_56909_157-56-52-13_40011.pcap`（13.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_icq_chat1b.pcap.TCP_10-8-8-130_34342_178-237-18-202_443.pcap`（817.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1a.pcap.TCP_10-8-8-178_41463_50-136-133-26_35737.pcap`（5.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1a.pcap.TCP_10-8-8-178_48723_137-116-224-167_443.pcap`（27.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1a.pcap.TCP_10-8-8-178_52449_86-4-212-228_59222.pcap`（406.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1a.pcap.TCP_10-8-8-178_54269_134-170-25-26_443.pcap`（461.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1a.pcap.TCP_10-8-8-178_55623_91-190-218-125_12350.pcap`（15.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1a.pcap.TCP_10-8-8-178_56909_157-56-52-13_40011.pcap`（28.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1a.pcap.TCP_2-30-116-54_58139_10-8-8-178_43020.pcap`（680.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_10-8-8-130_33104_157-56-192-53_443.pcap`（555.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_10-8-8-130_38181_91-190-216-125_12350.pcap`（13.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_10-8-8-130_38182_91-190-216-125_12350.pcap`（5.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_10-8-8-130_51146_64-4-23-162_40019.pcap`（30.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_10-8-8-130_52719_77-103-197-35_47872.pcap`（192.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_10-8-8-130_59320_86-4-212-228_59222.pcap`（251.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_2-101-222-231_9396_10-8-8-130_34461.pcap`（137.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Chat/vpn_skype_chat1b.pcap.TCP_2-30-116-54_58139_10-8-8-130_48835.pcap`（758.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.TCP_10-8-8-138_43336_75-101-155-12_22.pcap`（140.2 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.TCP_10-8-8-138_47126_75-101-155-12_22.pcap`（16.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.TCP_10-8-8-138_49156_75-101-155-12_22.pcap`（12.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.TCP_10-8-8-138_51827_74-125-226-38_443.pcap`（13.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.TCP_10-8-8-138_51828_74-125-226-38_443.pcap`（13.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.TCP_10-8-8-138_59218_23-21-114-223_443.pcap`（100.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.UDP_10-8-8-138_39162_74-125-226-38_443.pcap`（54.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_A.pcap.UDP_10-8-8-138_51753_74-125-226-38_443.pcap`（9.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_B.pcap.TCP_10-8-8-138_35968_75-101-155-12_22.pcap`（30.4 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_B.pcap.TCP_10-8-8-138_43336_75-101-155-12_22.pcap`（3.9 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_B.pcap.TCP_10-8-8-138_49156_75-101-155-12_22.pcap`（18.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_B.pcap.TCP_10-8-8-138_51142_74-125-226-56_443.pcap`（5.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_sftp_B.pcap.UDP_10-8-8-138_54576_74-125-226-56_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_32822_45-48-229-255_19290.pcap`（32.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_32875_45-48-229-255_19290.pcap`（77.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_33059_69-181-136-22_57191.pcap`（135.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_33103_69-181-136-22_57191.pcap`（609.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_34251_134-170-18-137_443.pcap`（566.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_34909_24-121-103-220_43206.pcap`（82.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_36137_184-166-38-160_11767.pcap`（234.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_36795_50-183-58-89_61070.pcap`（77.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_36828_50-183-58-89_61070.pcap`（76.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_37843_71-179-224-152_47644.pcap`（151.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_37938_73-25-184-121_58698.pcap`（582.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_37992_73-25-184-121_58698.pcap`（22.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_38035_70-245-66-95_56106.pcap`（87.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_38082_70-245-66-95_56106.pcap`（335.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_38347_174-62-248-162_2276.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_38968_158-222-191-234_55045.pcap`（32.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_39016_158-222-191-234_55045.pcap`（59.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_39081_129-98-43-99_24011.pcap`（425.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_39086_129-98-43-99_24011.pcap`（72.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_39090_129-98-43-99_24011.pcap`（142.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_39095_129-98-43-99_24011.pcap`（25.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_39099_129-98-43-99_24011.pcap`（745.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_40904_69-92-223-126_15157.pcap`（134.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_40937_69-92-223-126_15157.pcap`（41.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_41106_81-137-205-196_23528.pcap`（726.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_42201_24-196-36-15_63443.pcap`（209.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_43163_70-20-28-143_4395.pcap`（80.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_43216_70-20-28-143_4395.pcap`（67.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_44588_99-29-0-18_46385.pcap`（12.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_44637_99-29-0-18_46385.pcap`（175.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_44696_74-7-71-14_62639.pcap`（98.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_45067_108-40-10-184_53583.pcap`（37.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_45549_68-39-103-211_65514.pcap`（85.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_45599_68-39-103-211_65514.pcap`（69.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_46835_137-117-177-33_443.pcap`（11.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_47772_75-108-3-177_49178.pcap`（195.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_48807_108-20-79-218_33345.pcap`（144.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_48915_174-21-67-7_36864.pcap`（11.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_49458_50-152-152-105_46932.pcap`（10.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_49749_144-118-64-164_9987.pcap`（13.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_50304_67-180-224-48_35916.pcap`（221.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_50838_73-45-157-98_36950.pcap`（156.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_50920_108-237-134-2_7124.pcap`（1.1 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_50946_108-237-134-2_7124.pcap`（26.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_50951_108-237-134-2_7124.pcap`（25.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_50955_108-237-134-2_7124.pcap`（37.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_50960_108-237-134-2_7124.pcap`（37.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_51882_98-251-71-160_16311.pcap`（255.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_52561_68-224-106-140_24222.pcap`（219.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_52908_71-59-228-102_5624.pcap`（82.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_52956_71-59-228-102_5624.pcap`（94.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_53176_70-162-82-238_3792.pcap`（356.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_55199_68-190-134-49_5840.pcap`（11.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_56230_128-78-14-125_26965.pcap`（77.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_56277_128-78-14-125_26965.pcap`（141.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_56604_130-88-8-60_56289.pcap`（3.0 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_56748_157-56-52-13_40011.pcap`（218.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_57340_75-171-70-99_60538.pcap`（67.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_57342_75-171-70-99_60538.pcap`（3.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_57451_98-245-157-115_32614.pcap`（45.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_57665_71-94-76-197_47302.pcap`（442.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_58157_24-36-174-173_47044.pcap`（20.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_58161_24-36-174-173_47044.pcap`（20.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_58165_24-36-174-173_47044.pcap`（46.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_58170_24-36-174-173_47044.pcap`（39.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_60077_70-100-90-44_14783.pcap`（147.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_60106_70-100-90-44_14783.pcap`（97.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_60228_73-6-148-222_18722.pcap`（24.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_60674_68-186-166-162_11413.pcap`（146.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.TCP_10-8-8-134_60702_68-186-166-162_11413.pcap`（89.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-130_49539_10-8-8-134_15685.pcap`（61.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_108-237-134-2_7124.pcap`（265.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_111-221-77-153_40033.pcap`（53.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_111-221-77-154_40007.pcap`（48.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_129-98-43-99_24011.pcap`（210.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_130-88-8-60_56289.pcap`（1.6 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_144-118-64-164_9987.pcap`（10.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_157-55-130-168_40019.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_157-55-56-153_40033.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_158-222-191-234_55045.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_213-199-179-153_40033.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_24-36-174-173_47044.pcap`（20.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_46-17-57-54_4883.pcap`（7.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_46-17-57-54_49539.pcap`（61.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_46-17-57-54_4956.pcap`（14.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_46-17-57-54_5144.pcap`（7.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_50-183-58-89_61070.pcap`（10.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_64-4-23-153_40033.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_64-4-23-162_40019.pcap`（39.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_68-186-166-162_11413.pcap`（5.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_69-181-136-22_57191.pcap`（96.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_69-92-223-126_15157.pcap`（6.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_70-20-28-143_4395.pcap`（12.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_71-59-228-102_5624.pcap`（4.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_81-137-205-196_23528.pcap`（684.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_98-245-157-115_32614.pcap`（14.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1a.pcap.UDP_10-8-8-134_15685_99-29-0-18_46385.pcap`（20.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_33831_91-190-216-55_12350.pcap`（7.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_34575_157-56-198-10_80.pcap`（4.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_34698_88-166-212-83_30735.pcap`（6.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_34777_88-166-212-83_30735.pcap`（64.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_34813_86-193-232-51_40406.pcap`（8.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_34820_86-193-232-51_40406.pcap`（3.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_35827_23-194-214-46_443.pcap`（10.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_35843_23-194-214-46_443.pcap`（10.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_35857_23-194-214-46_443.pcap`（10.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_35863_23-194-214-46_443.pcap`（8.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_35880_23-194-214-46_443.pcap`（11.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_36858_108-237-134-2_7124.pcap`（823.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_37114_23-194-214-42_443.pcap`（11.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_38562_82-28-221-2_17920.pcap`（36.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_38619_82-28-221-2_17920.pcap`（3.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_38639_82-28-221-2_17920.pcap`（16.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_39118_91-190-218-34_443.pcap`（143.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_39696_184-162-79-221_21315.pcap`（7.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41495_82-245-24-95_38324.pcap`（4.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41942_137-117-177-33_443.pcap`（28.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41950_137-117-177-33_443.pcap`（28.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41955_137-117-177-33_443.pcap`（27.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41964_137-117-177-33_443.pcap`（28.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41970_137-117-177-33_443.pcap`（27.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41987_137-117-177-33_443.pcap`（28.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_41993_137-117-177-33_443.pcap`（27.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_42490_130-88-8-60_56289.pcap`（2.1 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_42934_131-253-61-84_443.pcap`（19.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_42935_131-253-61-84_443.pcap`（16.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_42936_131-253-61-84_443.pcap`（22.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_43219_104-45-158-137_443.pcap`（15.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_45952_108-162-232-203_80.pcap`（6.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_47169_137-116-224-167_443.pcap`（27.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_47182_137-116-224-167_443.pcap`（27.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_47195_137-116-224-167_443.pcap`（27.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_47218_137-116-224-167_443.pcap`（27.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_47233_137-116-224-167_443.pcap`（28.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48064_157-56-53-42_12350.pcap`（8.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48769_81-137-205-196_23528.pcap`（36.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48789_81-137-205-196_23528.pcap`（4.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48803_81-137-205-196_23528.pcap`（4.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48826_81-137-205-196_23528.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48846_81-137-205-196_23528.pcap`（18.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48849_82-75-235-147_17697.pcap`（9.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_48860_81-137-205-196_23528.pcap`（723.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_49637_91-190-216-53_12350.pcap`（8.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_51012_173-194-113-48_443.pcap`（10.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_51906_157-56-192-53_443.pcap`（209.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_51951_157-56-192-53_443.pcap`（116.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_51966_157-56-192-53_443.pcap`（116.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_51989_157-56-192-53_443.pcap`（38.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_52009_157-56-192-53_443.pcap`（304.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_52058_64-4-23-162_40019.pcap`（83.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_52090_23-97-219-200_80.pcap`（4.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_52104_64-4-23-162_40019.pcap`（21.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_52118_64-4-23-162_40019.pcap`（24.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_52141_64-4-23-162_40019.pcap`（19.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_52161_64-4-23-162_40019.pcap`（47.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_53288_69-181-136-22_57191.pcap`（531.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_54815_157-56-53-49_12350.pcap`（8.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_55321_82-66-32-219_26617.pcap`（4.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_55398_82-66-32-219_26617.pcap`（57.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_55569_109-209-186-130_58661.pcap`（6.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_55642_109-209-186-130_58661.pcap`（128.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_56596_129-98-43-99_24011.pcap`（310.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_56615_129-98-43-99_24011.pcap`（20.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_56630_129-98-43-99_24011.pcap`（33.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_56653_129-98-43-99_24011.pcap`（18.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_56673_129-98-43-99_24011.pcap`（538.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_56854_94-245-90-63_443.pcap`（15.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_56890_94-245-90-63_443.pcap`（15.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_58258_82-120-137-248_39942.pcap`（6.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_58336_82-120-137-248_39942.pcap`（6.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_59341_23-101-70-72_443.pcap`（15.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_59443_91-189-92-57_443.pcap`（134.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_59914_86-170-118-247_12431.pcap`（8.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_59991_86-170-118-247_12431.pcap`（110.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_60795_23-54-136-70_443.pcap`（13.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_60796_23-54-136-70_443.pcap`（24.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.TCP_10-8-8-130_60797_23-54-136-70_443.pcap`（221.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_10-8-8-134_15685.pcap`（60.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_108-237-134-2_7124.pcap`（514.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_111-221-77-153_40033.pcap`（8.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_111-221-77-158_40007.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_129-98-43-99_24011.pcap`（610.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_130-88-8-60_56289.pcap`（2.4 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_151-236-19-39_15685.pcap`（60.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_151-236-19-39_59520.pcap`（7.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_151-236-19-39_59533.pcap`（7.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_151-236-19-39_59534.pcap`（10.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_151-236-19-39_59577.pcap`（11.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_151-236-19-39_59683.pcap`（8.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_157-55-130-168_40019.pcap`（8.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_157-55-130-174_40022.pcap`（8.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_157-55-56-153_40033.pcap`（11.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_157-55-56-155_40021.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_157-55-56-159_40005.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_157-56-52-13_40011.pcap`（70.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_213-199-179-140_40004.pcap`（25.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_213-199-179-153_40033.pcap`（34.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_213-199-179-158_40007.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_64-4-23-153_40033.pcap`（10.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_64-4-23-155_40021.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_64-4-23-158_40007.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_64-4-23-159_40005.pcap`（4.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_69-181-136-22_57191.pcap`（138.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_81-137-205-196_23528.pcap`（689.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/FileTransfer/vpn_skype_files1b.pcap.UDP_10-8-8-130_49539_82-120-137-248_39942.pcap`（6.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_34040_74-125-226-32_443.pcap`（6.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_35936_107-22-243-234_443.pcap`（762.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_35968_107-22-243-234_443.pcap`（55.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_36057_74-125-226-65_443.pcap`（7.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_36320_108-160-163-107_443.pcap`（89.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_37207_216-58-219-205_443.pcap`（6.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_38170_74-125-226-56_443.pcap`（6.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_38246_54-230-53-213_443.pcap`（13.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_40633_108-160-172-204_443.pcap`（15.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_41296_209-148-205-32_80.pcap`（8.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_42086_54-243-70-179_443.pcap`（141.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_42220_74-125-226-34_443.pcap`（14.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_42637_173-223-153-85_80.pcap`（483.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_43533_185-2-220-137_80.pcap`（1.5 GB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_43534_185-2-220-137_80.pcap`（71.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_43535_185-2-220-137_80.pcap`（1.6 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_43536_185-2-220-137_80.pcap`（71.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_43537_185-2-220-137_80.pcap`（71.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_44443_74-125-226-55_443.pcap`（6.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_44471_50-16-198-195_443.pcap`（269.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_44660_54-243-90-245_443.pcap`（91.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_44914_74-125-226-36_443.pcap`（15.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_46958_23-21-207-234_443.pcap`（355.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_46959_23-21-207-234_443.pcap`（55.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_48899_216-58-221-142_443.pcap`（25.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_49969_107-22-243-234_80.pcap`（20.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_49970_107-22-243-234_80.pcap`（47.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_49971_107-22-243-234_80.pcap`（10.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_51761_54-243-108-61_443.pcap`（55.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_54020_209-148-205-33_80.pcap`（269.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_55191_54-225-199-51_80.pcap`（13.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_55375_173-194-204-188_5228.pcap`（11.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_55467_50-19-232-176_443.pcap`（137.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_57042_74-125-226-63_443.pcap`（15.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_57466_54-204-30-249_443.pcap`（55.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_57488_54-204-30-249_443.pcap`（237.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_57746_209-148-205-41_80.pcap`（87.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_57747_209-148-205-41_80.pcap`（33.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_57836_209-148-205-41_80.pcap`（110.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_57838_209-148-205-41_80.pcap`（9.1 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_58187_74-125-226-33_443.pcap`（14.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.TCP_10-8-8-138_59118_173-223-153-85_443.pcap`（9.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_17500_255-255-255-255_17500.pcap`（31.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_36943_74-125-226-36_443.pcap`（29.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_37700_74-125-226-55_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_37957_74-125-226-65_443.pcap`（21.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_39095_74-125-226-33_443.pcap`（38.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_42833_216-58-219-205_443.pcap`（8.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_44264_74-125-226-63_443.pcap`（24.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_47025_74-125-226-32_443.pcap`（9.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_55602_216-58-221-142_443.pcap`（19.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_56126_74-125-226-56_443.pcap`（8.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_59312_216-58-221-142_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_netflix_A.pcap.UDP_10-8-8-138_59391_74-125-226-34_443.pcap`（9.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_33832_74-125-226-32_443.pcap`（77.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_33834_74-125-226-32_443.pcap`（20.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_33875_54-230-52-100_443.pcap`（82.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_33876_54-230-52-100_443.pcap`（49.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_35014_207-223-241-72_80.pcap`（5.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_35523_194-132-198-82_4070.pcap`（2.8 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_37008_216-58-219-205_443.pcap`（14.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_37123_74-125-226-46_443.pcap`（15.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_38001_74-125-226-56_443.pcap`（14.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_38629_54-192-55-186_80.pcap`（4.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_42283_74-125-226-58_443.pcap`（25.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_42284_74-125-226-58_443.pcap`（4.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_43152_54-240-190-108_443.pcap`（19.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_43241_74-125-226-71_443.pcap`（15.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_43577_108-160-170-38_443.pcap`（195.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_44220_74-125-226-55_443.pcap`（14.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_44233_74-125-226-55_443.pcap`（7.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_45325_74-125-226-47_443.pcap`（6.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_45349_74-125-226-47_443.pcap`（7.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_45836_74-125-226-57_443.pcap`（15.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_47268_24-156-140-49_443.pcap`（18.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_47400_23-235-40-246_80.pcap`（282.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_47420_23-235-40-246_80.pcap`（284.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_51748_74-125-226-69_443.pcap`（14.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_52699_74-125-226-40_443.pcap`（15.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_52718_74-125-226-40_443.pcap`（18.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_52719_74-125-226-40_443.pcap`（15.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_53284_74-125-226-37_443.pcap`（15.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_54113_74-125-226-35_443.pcap`（6.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_55375_173-194-204-188_5228.pcap`（29.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_55782_24-156-130-203_80.pcap`（192.4 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_56856_74-125-226-63_443.pcap`（14.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_56862_74-125-226-63_443.pcap`（7.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_56871_74-125-226-63_443.pcap`（6.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_57111_198-41-30-199_80.pcap`（4.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_57112_198-41-30-199_80.pcap`（4.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_57159_108-160-172-236_443.pcap`（15.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.TCP_10-8-8-138_57976_74-125-226-33_443.pcap`（8.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-137_57621_10-8-8-138_57621.pcap`（22.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_17500_255-255-255-255_17500.pcap`（69.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_33262_74-125-226-40_443.pcap`（27.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_33588_74-125-226-63_443.pcap`（7.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_35247_74-125-226-46_443.pcap`（9.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_37960_216-58-219-205_443.pcap`（22.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_38380_74-125-226-55_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_39020_74-125-226-47_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_39029_74-125-226-69_443.pcap`（16.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_39794_74-125-226-37_443.pcap`（9.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_41914_74-125-226-63_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_41928_74-125-226-40_443.pcap`（8.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_41951_74-125-226-47_443.pcap`（7.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_42030_74-125-226-32_443.pcap`（10.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_42623_74-125-226-40_443.pcap`（46.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_43676_74-125-226-71_443.pcap`（30.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_45451_74-125-226-33_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_46514_74-125-226-55_443.pcap`（22.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_49132_74-125-226-35_443.pcap`（12.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_50093_74-125-226-35_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_51784_74-125-226-32_443.pcap`（32.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_52197_74-125-226-40_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_52548_74-125-226-35_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_54454_74-125-226-56_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_55316_74-125-226-63_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_spotify_A.pcap.UDP_10-8-8-138_57596_74-125-226-32_443.pcap`（72.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_32809_108-160-163-110_443.pcap`（22.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_33646_23-235-37-217_443.pcap`（10.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_35198_104-156-81-217_443.pcap`（249.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_35238_104-156-81-217_443.pcap`（10.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_36320_108-160-163-107_443.pcap`（51.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_39606_74-125-226-72_443.pcap`（14.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_39890_23-235-40-143_443.pcap`（17.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_39899_23-235-40-143_443.pcap`（58.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_39900_23-235-40-143_443.pcap`（31.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_39901_23-235-40-143_443.pcap`（40.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_42010_209-148-205-35_443.pcap`（236.9 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_44627_74-125-226-41_443.pcap`（15.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_50673_172-230-99-79_443.pcap`（99.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_53305_74-125-226-40_443.pcap`（7.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_53306_74-125-226-40_443.pcap`（6.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_55375_173-194-204-188_5228.pcap`（8.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.TCP_10-8-8-138_57465_74-125-226-63_443.pcap`（6.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.UDP_10-8-8-138_17500_255-255-255-255_17500.pcap`（24.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.UDP_10-8-8-138_40427_74-125-226-41_443.pcap`（21.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.UDP_10-8-8-138_44795_74-125-226-40_443.pcap`（9.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.UDP_10-8-8-138_50886_74-125-226-40_443.pcap`（31.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.UDP_10-8-8-138_55005_74-125-226-41_443.pcap`（29.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.UDP_10-8-8-138_55586_74-125-226-72_443.pcap`（14.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_A.pcap.UDP_10-8-8-138_58312_74-125-226-63_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_32809_108-160-163-110_443.pcap`（45.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_33969_104-156-85-217_443.pcap`（165.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_37776_216-58-219-205_443.pcap`（5.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_38080_23-235-46-143_443.pcap`（17.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_42190_209-148-205-35_443.pcap`（354.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_50673_172-230-99-79_443.pcap`（68.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_52515_74-125-226-69_443.pcap`（6.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_54064_74-125-226-37_443.pcap`（5.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_54880_74-125-226-35_443.pcap`（6.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_55375_173-194-204-188_5228.pcap`（5.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_57642_74-125-226-63_443.pcap`（6.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_57923_108-160-172-236_443.pcap`（15.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.TCP_10-8-8-138_60124_209-148-205-41_443.pcap`（130.6 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.UDP_10-8-8-138_17500_255-255-255-255_17500.pcap`（17.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.UDP_10-8-8-138_36617_216-58-219-205_443.pcap`（8.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.UDP_10-8-8-138_39956_74-125-226-37_443.pcap`（9.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.UDP_10-8-8-138_41415_74-125-226-63_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.UDP_10-8-8-138_43355_74-125-226-35_443.pcap`（12.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.UDP_10-8-8-138_51481_74-125-226-32_443.pcap`（29.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_vimeo_B.pcap.UDP_10-8-8-138_54309_74-125-226-69_443.pcap`（16.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_32809_108-160-163-110_443.pcap`（134.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_34714_74-125-226-32_443.pcap`（18.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_34722_74-125-226-32_443.pcap`（6.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_37899_74-125-226-46_443.pcap`（74.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_37961_74-125-226-46_443.pcap`（11.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_37997_74-125-226-46_443.pcap`（14.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_38020_74-125-226-46_443.pcap`（24.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_38025_74-125-226-46_443.pcap`（215.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_38026_74-125-226-46_443.pcap`（31.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_38029_74-125-226-46_443.pcap`（7.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_38850_74-125-226-56_443.pcap`（7.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_41534_74-125-226-38_443.pcap`（15.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_46238_74-125-226-47_443.pcap`（6.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_46266_74-125-226-47_443.pcap`（6.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_46762_74-125-226-57_443.pcap`（14.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_51892_74-125-226-39_443.pcap`（15.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_54159_74-125-226-37_443.pcap`（15.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_54185_74-125-226-37_443.pcap`（14.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_54222_74-125-226-37_443.pcap`（5.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_54977_74-125-226-35_443.pcap`（14.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_55375_173-194-204-188_5228.pcap`（32.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56155_74-125-226-73_443.pcap`（14.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56550_208-117-251-116_443.pcap`（61.2 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56557_208-117-251-116_443.pcap`（18.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56559_208-117-251-116_443.pcap`（5.7 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56560_208-117-251-116_443.pcap`（23.8 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56570_208-117-251-116_443.pcap`（691.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56571_208-117-251-116_443.pcap`（6.2 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56574_208-117-251-116_443.pcap`（3.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56575_208-117-251-116_443.pcap`（2.9 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56576_208-117-251-116_443.pcap`（7.7 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56577_208-117-251-116_443.pcap`（31.0 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56587_208-117-251-116_443.pcap`（21.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56596_208-117-251-116_443.pcap`（686.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56597_208-117-251-116_443.pcap`（13.0 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56602_208-117-251-116_443.pcap`（3.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56603_208-117-251-116_443.pcap`（5.9 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56604_208-117-251-116_443.pcap`（7.4 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56605_208-117-251-116_443.pcap`（21.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56610_208-117-251-116_443.pcap`（16.3 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56617_208-117-251-116_443.pcap`（9.7 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56618_208-117-251-116_443.pcap`（3.9 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56622_208-117-251-116_443.pcap`（29.9 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56623_208-117-251-116_443.pcap`（3.6 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56632_208-117-251-116_443.pcap`（684.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56633_208-117-251-116_443.pcap`（16.6 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56639_208-117-251-116_443.pcap`（2.9 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56640_208-117-251-116_443.pcap`（684.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56641_208-117-251-116_443.pcap`（14.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56642_208-117-251-116_443.pcap`（6.3 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56646_208-117-251-116_443.pcap`（685.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_56647_208-117-251-116_443.pcap`（4.6 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_58847_74-125-226-33_443.pcap`（7.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_58868_108-160-169-170_443.pcap`（12.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_58882_74-125-226-33_443.pcap`（7.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.TCP_10-8-8-138_58883_74-125-226-33_443.pcap`（6.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_17500_255-255-255-255_17500.pcap`（47.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_33367_74-125-226-37_443.pcap`（310.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_33809_74-125-226-37_443.pcap`（10.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_35657_74-125-226-47_443.pcap`（8.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_35870_74-125-226-37_443.pcap`（16.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_35958_74-125-226-38_443.pcap`（18.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_36034_74-125-226-56_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_36089_74-125-226-36_443.pcap`（147.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_36291_74-125-226-34_443.pcap`（33.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_37934_74-125-226-39_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_38890_74-125-226-39_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_39094_74-125-226-33_443.pcap`（20.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_39496_74-125-226-39_443.pcap`（20.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_39606_74-125-226-37_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_39793_74-125-226-33_443.pcap`（33.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_40646_74-125-226-35_443.pcap`（18.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_41726_74-125-226-37_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_42040_74-125-226-35_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_42184_74-125-226-37_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_42350_74-125-226-46_443.pcap`（150.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_43017_74-125-226-37_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_44350_74-125-226-38_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_44373_74-125-226-46_443.pcap`（150.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_44993_74-125-226-34_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_45667_74-125-226-39_443.pcap`（20.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_46117_74-125-226-38_443.pcap`（18.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_46440_74-125-226-35_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_46477_74-125-226-46_443.pcap`（13.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_46612_74-125-226-37_443.pcap`（18.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_47471_74-125-226-38_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_47503_74-125-226-34_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_47739_74-125-226-33_443.pcap`（11.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_48158_74-125-226-33_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_48603_74-125-226-46_443.pcap`（67.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_49154_74-125-226-46_443.pcap`（27.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_50048_74-125-226-39_443.pcap`（9.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_50543_74-125-226-37_443.pcap`（22.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_50675_74-125-226-57_443.pcap`（9.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_51424_74-125-226-37_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_51740_74-125-226-37_443.pcap`（18.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_52861_74-125-226-47_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_53583_74-125-226-33_443.pcap`（16.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_54813_74-125-226-37_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_55343_74-125-226-32_443.pcap`（12.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_55467_74-125-226-34_443.pcap`（8.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_55929_74-125-226-37_443.pcap`（8.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_56017_74-125-226-46_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_56384_74-125-226-46_443.pcap`（102.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_56625_74-125-226-33_443.pcap`（41.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_56956_74-125-226-46_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_58180_74-125-226-38_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_58205_74-125-226-46_443.pcap`（10.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_58291_74-125-226-33_443.pcap`（17.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_58323_74-125-226-46_443.pcap`（154.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_58708_74-125-226-73_443.pcap`（15.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_59322_74-125-226-38_443.pcap`（12.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_59924_74-125-226-32_443.pcap`（7.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_60371_74-125-226-32_443.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/Streaming/vpn_youtube_A.pcap.UDP_10-8-8-138_60814_74-125-226-39_443.pcap`（20.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_34575_10-8-0-10_18420.pcap`（39.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_35990_199-16-156-201_443.pcap`（6.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_36439_157-55-56-157_40008.pcap`（198.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_37315_91-190-218-59_12350.pcap`（5.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_38342_24-102-232-252_17326.pcap`（75.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_38497_134-170-24-108_443.pcap`（312.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_38664_74-125-226-14_443.pcap`（22.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_39047_173-194-123-5_443.pcap`（26.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_39244_173-194-123-97_443.pcap`（11.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_39435_74-125-226-183_443.pcap`（8.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_40440_137-116-224-167_443.pcap`（11.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_41234_173-194-123-9_443.pcap`（25.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_41378_174-4-162-172_57397.pcap`（4.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_42844_141-219-235-176_60830.pcap`（4.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_42887_141-219-235-176_60830.pcap`（182.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_43286_207-189-227-29_28812.pcap`（180.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_43623_173-194-123-103_443.pcap`（19.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_45990_69-145-8-82_18977.pcap`（5.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_47987_173-194-207-188_5228.pcap`（24.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_48558_68-180-110-66_12732.pcap`（4.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_49515_178-211-244-196_27425.pcap`（5.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_50127_72-39-249-200_18990.pcap`（4.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_50214_74-125-226-95_443.pcap`（17.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_51338_97-89-116-200_29810.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_52104_74-125-226-174_443.pcap`（16.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_52785_173-194-123-127_443.pcap`（8.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_52952_74-125-226-160_443.pcap`（19.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_53591_74-125-226-32_443.pcap`（22.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_56160_74-125-226-191_443.pcap`（8.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_57411_72-11-163-216_56230.pcap`（4.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_58256_91-190-218-125_12350.pcap`（19.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_59298_74-125-226-185_443.pcap`（20.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_60225_68-63-177-114_20718.pcap`（16.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.TCP_10-8-0-6_60645_216-58-219-237_443.pcap`（10.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_10-8-0-10_18420.pcap`（92.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_111-221-74-25_40002.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_111-221-74-38_40018.pcap`（5.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_111-221-77-149_40014.pcap`（4.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_111-221-77-162_40019.pcap`（6.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_111-221-77-171_40004.pcap`（5.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-130-140_40014.pcap`（8.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-130-150_40022.pcap`（12.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-130-152_40018.pcap`（5.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-130-152_40021.pcap`（7.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-130-152_40023.pcap`（4.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-130-172_40009.pcap`（3.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-130-173_40001.pcap`（4.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-235-153_40002.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-235-166_40018.pcap`（7.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-235-166_40024.pcap`（4.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-56-149_40028.pcap`（6.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-56-153_40001.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-56-153_40012.pcap`（3.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-55-56-169_40001.pcap`（7.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-56-52-25_40002.pcap`（4.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-56-52-38_40018.pcap`（9.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_157-56-52-44_40023.pcap`（4.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_188-76-51-188_29757.pcap`（4.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_213-199-179-141_40030.pcap`（6.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_213-199-179-143_33033.pcap`（10.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_213-199-179-147_40003.pcap`（4.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_213-199-179-176_40018.pcap`（5.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_213-199-179-176_40026.pcap`（3.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_64-4-23-151_40023.pcap`（5.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_64-4-23-159_40031.pcap`（5.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_65-55-223-15_40016.pcap`（6.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_65-55-223-18_40010.pcap`（4.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_65-55-223-22_40005.pcap`（6.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_65-55-223-38_40018.pcap`（6.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_90-163-21-193_34347.pcap`（7.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_95-121-28-148_12089.pcap`（6.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio1.pcap.UDP_10-8-0-6_40273_95-62-106-124_37582.pcap`（5.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_34024_23-65-248-82_80.pcap`（152.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_34031_209-148-205-26_443.pcap`（11.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_34032_209-148-205-26_443.pcap`（12.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_34034_209-148-205-26_443.pcap`（4.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_34035_209-148-205-26_443.pcap`（4.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_34036_209-148-205-26_443.pcap`（4.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_34054_173-194-123-98_443.pcap`（56.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_35066_216-58-219-237_443.pcap`（12.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_35730_173-252-110-27_443.pcap`（18.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_35745_173-252-110-27_443.pcap`（87.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_37560_178-255-83-1_80.pcap`（3.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_37617_72-21-91-29_80.pcap`（4.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_38914_173-194-123-121_80.pcap`（43.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_40159_91-189-90-41_80.pcap`（4.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_40446_88-198-10-10_443.pcap`（24.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_41982_173-194-123-108_443.pcap`（64.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_42566_173-194-123-70_80.pcap`（4.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_44814_82-165-251-100_80.pcap`（71.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_44816_82-165-251-100_80.pcap`（7.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_44817_82-165-251-100_80.pcap`（5.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_44866_173-194-123-111_443.pcap`（12.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_45331_91-189-89-22_443.pcap`（16.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_45332_91-189-89-22_443.pcap`（41.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_46824_23-65-243-33_443.pcap`（12.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_48811_173-194-123-78_443.pcap`（24.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_49348_184-26-44-96_80.pcap`（6.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_50480_173-194-123-64_443.pcap`（31.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_53270_24-156-140-33_443.pcap`（11.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_54685_134-170-18-175_443.pcap`（232.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_55376_91-190-216-125_12350.pcap`（13.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_55817_65-55-223-17_40020.pcap`（164.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_55869_173-252-120-6_443.pcap`（12.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_56874_137-116-224-167_443.pcap`（10.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_56876_137-116-224-167_443.pcap`（18.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_57370_137-116-32-77_443.pcap`（11.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-10_58077_74-125-226-169_80.pcap`（6.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.TCP_10-8-0-6_34575_10-8-0-10_18420.pcap`（50.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.UDP_10-8-0-10_18420_111-221-77-159_40005.pcap`（4.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.UDP_10-8-0-10_18420_213-199-179-168_40016.pcap`（5.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_skype_audio2.pcap.UDP_10-8-0-6_40273_10-8-0-10_18420.pcap`（92.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61102_131-202-6-26_13000.pcap`（31.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61105_131-202-6-26_13000.pcap`（862.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61106_131-202-6-26_13000.pcap`（26.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61107_131-202-6-26_13000.pcap`（25.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61108_131-202-6-26_13000.pcap`（25.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61114_161-69-13-21_443.pcap`（808.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61122_178-255-83-1_80.pcap`（4.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61133_161-69-13-21_443.pcap`（41.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61134_161-69-13-21_443.pcap`（61.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61136_161-69-13-21_443.pcap`（21.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61138_131-202-6-26_13000.pcap`（26.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61141_212-73-221-202_80.pcap`（36.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61148_131-202-6-26_13000.pcap`（27.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61149_131-202-6-26_13000.pcap`（26.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61151_131-202-6-26_13000.pcap`（32.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61156_131-202-6-26_13000.pcap`（34.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.TCP_10-8-8-222_61161_216-58-210-46_443.pcap`（18.5 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.UDP_10-8-8-222_137_10-8-8-223_137.pcap`（87.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.UDP_10-8-8-222_53075_77-72-169-133_11113.pcap`（18.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.UDP_10-8-8-222_53075_80-239-235-110_11666.pcap`（96.2 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.UDP_8-8-8-8_53_10-8-8-222_49378.pcap`（9.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1a.pcap.UDP_fe80--b91c-3e86-e6e4-d43d_546_ff02--1-2_547.pcap`（20.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29902_184-27-206-8_443.pcap`（17.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29908_191-232-139-4_443.pcap`（16.3 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29910_131-202-6-26_13000.pcap`（31.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29913_131-202-6-26_13000.pcap`（893.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29915_131-202-6-26_13000.pcap`（27.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29916_131-202-6-26_13000.pcap`（26.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29917_131-202-6-26_13000.pcap`（25.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29918_131-202-6-26_13000.pcap`（25.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29921_191-232-139-4_443.pcap`（19.2 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29923_131-202-6-26_13000.pcap`（31.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29927_134-170-58-123_443.pcap`（14.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29937_131-202-6-26_13000.pcap`（31.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29938_131-202-6-26_13000.pcap`（27.0 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29941_80-239-174-47_80.pcap`（36.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29948_131-202-6-26_13000.pcap`（25.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.TCP_10-8-8-246_29949_131-202-6-26_13000.pcap`（25.9 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.UDP_10-8-8-246_137_10-8-8-247_137.pcap`（135.4 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.UDP_10-8-8-246_138_10-8-8-247_138.pcap`（4.6 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.UDP_10-8-8-246_60245_77-72-169-133_11113.pcap`（19.7 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.UDP_10-8-8-246_60245_80-239-235-110_11666.pcap`（96.5 MB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.UDP_8-8-8-8_53_10-8-8-246_64162.pcap`（10.8 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
- `src/reproduction/TrafficFormer/data/iscxvpn_service/splitcap/VoIP/vpn_voipbuster1b.pcap.UDP_fe80--8c14-5120-4519-bd3f_546_ff02--1-2_547.pcap`（21.1 KB）：TrafficFormer 通过 SplitCap 切分得到的单流 PCAP 文件，文件名包含五元组信息。
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
- `src/reproduction/TrafficFormer/uer/__init__.py`（0 B）：UER 框架包初始化文件。
- `src/reproduction/TrafficFormer/uer/__pycache__/__init__.cpython-313.pyc`（221 B）：Python 字节码缓存，对应源文件 `__init__.py`。
- `src/reproduction/TrafficFormer/uer/__pycache__/model_loader.cpython-313.pyc`（4.9 KB）：Python 字节码缓存，对应源文件 `model_loader.py`。
- `src/reproduction/TrafficFormer/uer/__pycache__/model_saver.cpython-313.pyc`（673 B）：Python 字节码缓存，对应源文件 `model_saver.py`。
- `src/reproduction/TrafficFormer/uer/__pycache__/opts.cpython-313.pyc`（6.3 KB）：Python 字节码缓存，对应源文件 `opts.py`。
- `src/reproduction/TrafficFormer/uer/decoders/__init__.py`（173 B）：UER 解码器子包初始化文件。
- `src/reproduction/TrafficFormer/uer/decoders/transformer_decoder.py`（3.3 KB）：Transformer 解码器实现。
- `src/reproduction/TrafficFormer/uer/encoders/__init__.py`（843 B）：UER 编码器子包初始化文件。
- `src/reproduction/TrafficFormer/uer/encoders/__pycache__/__init__.cpython-313.pyc`（810 B）：Python 字节码缓存，对应源文件 `__init__.py`。
- `src/reproduction/TrafficFormer/uer/encoders/__pycache__/cnn_encoder.cpython-313.pyc`（5.7 KB）：Python 字节码缓存，对应源文件 `cnn_encoder.py`。
- `src/reproduction/TrafficFormer/uer/encoders/__pycache__/rnn_encoder.cpython-313.pyc`（8.5 KB）：Python 字节码缓存，对应源文件 `rnn_encoder.py`。
- `src/reproduction/TrafficFormer/uer/encoders/__pycache__/transformer_encoder.cpython-313.pyc`（5.9 KB）：Python 字节码缓存，对应源文件 `transformer_encoder.py`。
- `src/reproduction/TrafficFormer/uer/encoders/cnn_encoder.py`（2.8 KB）：CNN 编码器实现。
- `src/reproduction/TrafficFormer/uer/encoders/rnn_encoder.py`（5.8 KB）：RNN 编码器实现。
- `src/reproduction/TrafficFormer/uer/encoders/transformer_encoder.py`（5.1 KB）：Transformer 编码器实现。
- `src/reproduction/TrafficFormer/uer/layers/__init__.py`（531 B）：UER 网络层子包初始化文件。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/__init__.cpython-313.pyc`（577 B）：Python 字节码缓存，对应源文件 `__init__.py`。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/embeddings.cpython-313.pyc`（8.5 KB）：Python 字节码缓存，对应源文件 `embeddings.py`。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/layer_norm.cpython-313.pyc`（2.6 KB）：Python 字节码缓存，对应源文件 `layer_norm.py`。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/moe_layer.cpython-313.pyc`（11.6 KB）：Python 字节码缓存，对应源文件 `moe_layer.py`。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/multi_headed_attn.cpython-313.pyc`（4.0 KB）：Python 字节码缓存，对应源文件 `multi_headed_attn.py`。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/position_ffn.cpython-313.pyc`（4.0 KB）：Python 字节码缓存，对应源文件 `position_ffn.py`。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/relative_position_embedding.cpython-313.pyc`（5.1 KB）：Python 字节码缓存，对应源文件 `relative_position_embedding.py`。
- `src/reproduction/TrafficFormer/uer/layers/__pycache__/transformer.cpython-313.pyc`（10.6 KB）：Python 字节码缓存，对应源文件 `transformer.py`。
- `src/reproduction/TrafficFormer/uer/layers/embeddings.py`（4.9 KB）：输入嵌入层实现。
- `src/reproduction/TrafficFormer/uer/layers/layer_norm.py`（1.1 KB）：层归一化实现。
- `src/reproduction/TrafficFormer/uer/layers/moe_layer.py`（7.4 KB）：Mixture-of-Experts 层实现。
- `src/reproduction/TrafficFormer/uer/layers/multi_headed_attn.py`（2.6 KB）：多头注意力层实现。
- `src/reproduction/TrafficFormer/uer/layers/position_ffn.py`（2.4 KB）：位置前馈网络层实现。
- `src/reproduction/TrafficFormer/uer/layers/relative_position_embedding.py`（4.6 KB）：相对位置编码实现。
- `src/reproduction/TrafficFormer/uer/layers/synthesizer.py`（4.7 KB）：Synthesizer 结构实现。
- `src/reproduction/TrafficFormer/uer/layers/transformer.py`（10.2 KB）：Transformer 层实现。
- `src/reproduction/TrafficFormer/uer/model_builder.py`（675 B）：构建 UER 模型结构的核心模块。
- `src/reproduction/TrafficFormer/uer/model_loader.py`（2.6 KB）：加载预训练或已保存模型权重的模块。
- `src/reproduction/TrafficFormer/uer/model_saver.py`（210 B）：保存 UER 模型权重的模块。
- `src/reproduction/TrafficFormer/uer/models/__init__.py`（0 B）：UER 模型子包初始化文件。
- `src/reproduction/TrafficFormer/uer/models/model.py`（1.3 KB）：UER 模型主定义。
- `src/reproduction/TrafficFormer/uer/opts.py`（7.1 KB）：UER 命令行参数定义。
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
- `src/reproduction/TrafficFormer/uer/test.txt`（2 B）：UER 目录中的测试或示例文本文件。
- `src/reproduction/TrafficFormer/uer/trainer.py`（17.0 KB）：UER 训练流程封装模块。
- `src/reproduction/TrafficFormer/uer/utils/__init__.py`（2.3 KB）：UER 工具子包初始化文件。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/__init__.cpython-313.pyc`（1.8 KB）：Python 字节码缓存，对应源文件 `__init__.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/act_fun.cpython-313.pyc`（2.2 KB）：Python 字节码缓存，对应源文件 `act_fun.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/config.cpython-313.pyc`（820 B）：Python 字节码缓存，对应源文件 `config.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/constants.cpython-313.pyc`（371 B）：Python 字节码缓存，对应源文件 `constants.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/data.cpython-313.pyc`（73.7 KB）：Python 字节码缓存，对应源文件 `data.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/misc.cpython-313.pyc`（1.2 KB）：Python 字节码缓存，对应源文件 `misc.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/optimizers.cpython-313.pyc`（23.5 KB）：Python 字节码缓存，对应源文件 `optimizers.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/seed.cpython-313.pyc`（945 B）：Python 字节码缓存，对应源文件 `seed.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/tokenizers.cpython-313.pyc`（19.8 KB）：Python 字节码缓存，对应源文件 `tokenizers.py`。
- `src/reproduction/TrafficFormer/uer/utils/__pycache__/vocab.cpython-313.pyc`（6.3 KB）：Python 字节码缓存，对应源文件 `vocab.py`。
- `src/reproduction/TrafficFormer/uer/utils/act_fun.py`（1.0 KB）：激活函数相关工具。
- `src/reproduction/TrafficFormer/uer/utils/config.py`（287 B）：模型与训练配置读取工具。
- `src/reproduction/TrafficFormer/uer/utils/constants.py`（225 B）：常量定义。
- `src/reproduction/TrafficFormer/uer/utils/data.py`（57.3 KB）：数据读取与批处理工具。
- `src/reproduction/TrafficFormer/uer/utils/misc.py`（540 B）：杂项辅助函数。
- `src/reproduction/TrafficFormer/uer/utils/optimizers.py`（22.5 KB）：优化器与学习率调度工具。
- `src/reproduction/TrafficFormer/uer/utils/seed.py`（292 B）：随机种子设置工具。
- `src/reproduction/TrafficFormer/uer/utils/subword.py`（675 B）：子词处理相关工具。
- `src/reproduction/TrafficFormer/uer/utils/tokenizers.py`（15.4 KB）：分词器工具。
- `src/reproduction/TrafficFormer/uer/utils/vocab.py`（3.9 KB）：词表加载与处理工具。
- `src/teammate_optimized/__pycache__/train_final_optimized.cpython-313.pyc`（26.8 KB）：Python 字节码缓存，对应源文件 `train_final_optimized.py`。
- `src/teammate_optimized/__pycache__/train_final_optimized_v2.cpython-313.pyc`（26.9 KB）：Python 字节码缓存，对应源文件 `train_final_optimized_v2.py`。
- `src/teammate_optimized/train_final_optimized.py`（10.2 KB）：同事原始优化版训练脚本。
- `src/teammate_optimized/train_final_optimized_v2.py`（20.0 KB）：进一步整理后的优化版训练脚本。

</details>

### `tools`（2 个文件）

<details>
<summary>展开查看 <code>tools</code> 下的全部文件</summary>

- `tools/build_opening_report_docx.py`（12.6 KB）：将开题报告 Markdown 转换或整理为 Word 报告的工具脚本。
- `tools/build_requirements_docx.py`（5.8 KB）：将需求分析 Markdown 转换或整理为 Word 报告的工具脚本。

</details>

### `信息系统安全与对抗技术-报告模板`（11 个文件）

<details>
<summary>展开查看 <code>信息系统安全与对抗技术-报告模板</code> 下的全部文件</summary>

- `信息系统安全与对抗技术-报告模板/组编号-201-需求分析报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（62.4 KB）：课程需求分析报告模板。
- `信息系统安全与对抗技术-报告模板/组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（57.9 KB）：课程开题报告模板。
- `信息系统安全与对抗技术-报告模板/组编号-203-开题答辩PPT.pptx`（255.5 KB）：课程开题答辩 PPT 模板。
- `信息系统安全与对抗技术-报告模板/组编号-301-详细设计报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（60.3 KB）：课程详细设计报告模板。
- `信息系统安全与对抗技术-报告模板/组编号-302-中期报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（57.3 KB）：课程中期报告模板。
- `信息系统安全与对抗技术-报告模板/组编号-303-中期答辩PPT.pptx`（256.7 KB）：课程中期答辩 PPT 模板。
- `信息系统安全与对抗技术-报告模板/组编号-401-项目研制报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（61.4 KB）：课程项目研制报告模板。
- `信息系统安全与对抗技术-报告模板/组编号-402-结题报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（57.7 KB）：课程结题报告模板。
- `信息系统安全与对抗技术-报告模板/组编号-403-自测试报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（61.0 KB）：课程自测试报告模板。
- `信息系统安全与对抗技术-报告模板/组编号-404-验收答辩PPT.pptx`（256.7 KB）：课程验收答辩 PPT 模板。
- `信息系统安全与对抗技术-报告模板/组编号-501-班号-学号-姓名-课程学习体会.docx`（22.0 KB）：课程学习体会模板。

</details>

### `信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx`（1 个文件）

<details>
<summary>展开查看 <code>信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx</code> 下的全部文件</summary>

- `信息系统安全与对抗技术-过程控制简表-2026-v1.0-2026.02.11 .xlsx`（15.2 KB）：课程过程控制简表 Excel 文件。

</details>

### `组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（1 个文件）

<details>
<summary>展开查看 <code>组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx</code> 下的全部文件</summary>

- `组编号-202-开题报告-学号1-姓名1-学号2-姓名2-项目名称.docx`（44.1 KB）：课程开题报告 Word 文件。

</details>
