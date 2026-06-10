# 加密方法识别主表口径说明

更新时间：`2026-06-03`

## 1. 为什么要重定义第一层主表

当前项目的正式主任务已经转为“加密方法识别”，统一标签为：

- `NON_ENCRYPTED`
- `TLS_FAMILY`
- `SSH`
- `QUIC`
- `VPN`
- `TOR`
- `I2P`
- `FREENET`
- `ZERONET`

因此，旧仓库中面向业务类型分类的复现结果，例如：

- `TrafficFormer` 的 `Chat / FileTransfer / Streaming / VoIP`
- `C-LSTM` 的 `Chat / Email / File Transfer / VPN-*`

都不能直接作为当前主表结果。

## 2. 为什么 ET-BERT / TFE-GNN / Deep Packet 不能直接进全量主表

对 `data/unified_encryption_method_v2_all_data/multiclass_finetune.csv` 的实际检查显示：

- 总样本数：`316601`
- 带非空 `sequence_text` 的样本数：`50934`

按来源分布：

- `DATASET_CSV`：`239176` 条，`sequence_text = 0`
- `BCCC_BINARY`：`18570` 条，`sequence_text = 0`
- `BCCC_MULTI`：`7921` 条，`sequence_text = 0`
- `FLOW_LABELED`：`2387` 条，`sequence_text = 2387`
- `RAW_NONTOR`：`48411` 条，`sequence_text = 48411`
- `RAW_TOR`：`136` 条，`sequence_text = 136`

这意味着：

1. `ET-BERT` 属于包/序列级 Transformer，需要序列输入，不能公平覆盖全量样本。
2. `TFE-GNN` 官方实现依赖原始 `pcap` 构图，也不能直接覆盖当前全量统一数据。
3. `Deep Packet` 同样依赖原始包字节输入，不适合作为全量主表方法。

因此，以上三类方法后续应进入“序列子表”，而不是第一层全量主表。

## 3. 主表中的另一个风险：source leakage

当前最强的统一模型把 `source_name` 作为输入特征之一，但统一数据中标签与来源高度耦合。例如：

- `FREENET / I2P / ZERONET` 全部来自 `BCCC_MULTI`
- `TOR` 主要来自 `BCCC_MULTI`，少量来自 `RAW_TOR`
- `VPN` 绝大部分来自 `DATASET_CSV`
- `SSH` 几乎全部来自 `DATASET_CSV`

这会导致模型利用“数据来源”而不是“流量行为模式”完成分类，降低主表说服力。

因此，第一层主表默认采用：

- 不使用 `source_name`
- 只使用全量可用的流级数值特征
- 可选使用 `transport` 作为通用协议元信息

## 4. 当前新增的第一层主表代码

- `src/encryption_method/unified_benchmark_utils.py`
  - 统一数据加载、标准化、评测与结果落盘
- `src/encryption_method/benchmark_tabular_baselines.py`
  - 面向全量统一数据的公平 `tabular` 基线脚本

该脚本默认训练：

- `RandomForest`
- `ExtraTrees`
- `XGBoost`

并统一输出：

- `metrics.json`
- `classification_report.txt`
- `classification_report.csv`
- `confusion_matrix.csv`
- `comparison.csv`
- `comparison.md`

## 5. 当前建议的主表结构

第一层主表：

- 你的公平版主方法（后续需要去掉 `source_name` 后重训）
- `RandomForest`
- `ExtraTrees`
- `XGBoost`
- 可选 `MLP`

第二层序列子表：

- `ET-BERT`
- `TFE-GNN`
- `Deep Packet`

这样可以把“全量统一口径的公平比较”和“更强序列模型的局部对照”分开，避免任务口径和输入粒度混杂。
