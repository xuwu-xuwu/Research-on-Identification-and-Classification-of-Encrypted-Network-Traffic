# C-LSTM 改进版目录说明

## 说明

这个目录用于存放基于本地数据做过优化后的加密流量包级分类材料，与“论文复现版”分开保存，避免两者混淆。

改进版入口脚本：

- [train_c_lstm_improved.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/improved/train_c_lstm_improved.py)
- [predict_c_lstm.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/improved/predict_c_lstm.py)
- [train_xgboost_gpu.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/improved/train_xgboost_gpu.py)
- [predict_xgboost_gpu.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/improved/predict_xgboost_gpu.py)

改进版输出目录：

- [run_v1](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/run_v1)
- [prediction_raw_nonvpn01](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/prediction_raw_nonvpn01)
- [xgboost_gpu_v1](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/xgboost_gpu_v1)
- [xgboost_gpu_v1_prediction_raw_nonvpn01](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/xgboost_gpu_v1_prediction_raw_nonvpn01)

## 当前结果

基于本地 `9` 类数据，目前有两条改进路线：

- `C-LSTM` 本地优化版
- `XGBoost(cuda)` 包级分类器

其中效果最强的是 `XGBoost(cuda)`，结果如下：

- Accuracy：`0.9665`
- Macro-F1：`0.9736`
- Weighted-F1：`0.9665`

对应结果文件：

- [metrics.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/xgboost_gpu_v1/metrics.json)
- [classification_report.txt](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/xgboost_gpu_v1/classification_report.txt)
- [model.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/xgboost_gpu_v1/model.json)
- [model_meta.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/xgboost_gpu_v1/model_meta.json)

原始 `pcap` 预测结果：

- packet-level Accuracy：`0.9932`
- capture-level：`23 / 23` 正确
- 结果文件：[prediction_summary.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/xgboost_gpu_v1_prediction_raw_nonvpn01/prediction_summary.json)

原来的 `C-LSTM` 本地优化版结果如下：

- Accuracy：`0.7597`
- Macro-F1：`0.7629`
- Weighted-F1：`0.7686`

对应结果文件：

- [metrics.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/run_v1/metrics.json)
- [classification_report.txt](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/run_v1/classification_report.txt)
- [model.pt](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/run_v1/model.pt)

原始 `pcap` 预测结果：

- packet-level Accuracy：`0.7857`
- 结果文件：[prediction_summary.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/improved/prediction_raw_nonvpn01/prediction_summary.json)

## 与复现版的关系

这里的“改进版”不是论文原始设定，而是在本地数据条件下，为了提升效果加入了：

- 训练/验证/测试三段划分
- 类别加权损失
- 带权采样
- `AdamW`
- 学习率调度
- 早停
- 更高 dropout
- label smoothing
- `XGBoost(cuda)` 强分类器

因此写报告时应区分：

- `复现版`：用于说明论文方法是否被正确实现
- `改进版`：用于说明在本地数据条件下如何进一步提升效果

还要单独说明一个实验前提：

- 当前 `96%+` 的结果是在**包级随机划分**下得到的，训练集和测试集可能来自同一批原始抓包文件的不同数据包。
- 这类设定适合说明“当前输入表示和分类器在现有数据上的判别能力”，但不能直接等同于“跨文件、跨场景、跨时间”的真实泛化能力。
