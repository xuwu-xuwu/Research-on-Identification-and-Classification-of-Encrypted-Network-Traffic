# 网络流量加密方法识别与分类

当前仓库主线已经整理为“加密方法识别”任务，不再以旧的应用/业务流量分类作为主线。

## 当前任务

目标是在统一数据集上识别网络流量对应的加密方法或匿名通信机制。当前全量任务为 9 类：

- `NON_ENCRYPTED`
- `TLS_FAMILY`
- `SSH`
- `QUIC`
- `VPN`
- `TOR`
- `I2P`
- `FREENET`
- `ZERONET`

## 目录结构

- `src/encryption_method/`：当前加密方法识别代码，包括统一数据构建、全量主表基线、PCAP 论文方法对比、当前增强模型训练。
- `data/unified_encryption_method_v2_all_data/`：当前全量 9 类训练数据，主文件为 `multiclass_finetune.csv`。
- `data/paper_benchmark/`：用于 ET-BERT / TFE-GNN / Deep Packet 风格方法对比的 5 类 PCAP 子表数据。
- `outputs/encryption_method/`：当前加密方法识别实验输出、模型和指标。
- `docs/analysis/`：当前实验口径、方法说明和对比分析。
- `docs/reports/`：当前阶段报告和论文对比实验进度文档。
- `docs/templates/`：课程报告模板、过程控制表和占位报告文件。
- `legacy_business_traffic_classification/`：旧的应用/业务流量分类代码、输出、ARFF 数据和历史文档归档。

共享原始 PCAP 数据仍保留在 `data/` 下，例如 `NonVPN-PCAPs-*`、`VPN-PCAPs-02`、`NonTor`、`Tor`，因为当前 PCAP 论文对比仍会用到。

## 当前最新主方法

全量 9 类主方法为：

```powershell
python src\encryption_method\train_full_enhanced_fusion.py `
  --data-dir data\unified_encryption_method_v2_all_data `
  --output-dir outputs\encryption_method\full_enhanced_fusion_v1
```

方法名：`full_enhanced_fusion_xgboost`

输入特征：

- 21 个全量样本都有的流级数值特征
- `transport` one-hot
- `sequence_text` 可用时抽取的序列统计特征
- 明确排除 `source_name`，避免数据来源泄漏

当前测试集结果见 `outputs/encryption_method/full_enhanced_fusion_v1/metrics.json`：

| 方法 | Accuracy | Macro-F1 | Weighted-F1 | Macro Recall |
| --- | ---: | ---: | ---: | ---: |
| `full_enhanced_fusion_xgboost` | 0.993978 | 0.892797 | 0.994046 | 0.909893 |

## 数据划分

当前全量 9 类数据直接使用 `multiclass_finetune.csv` 中已有的 `split` 字段，不重新随机拆分。

- Train：221617 条
- Valid：47490 条
- Test：47494 条

各类划分统计见 `data/unified_encryption_method_v2_all_data/metadata.json`。

## 论文方法对比

第一层公平主表使用全量 9 类统一数据，主要比较流级表格方法。

第二层 PCAP 子表用于对比需要原始包/包序列输入的论文方法，包括 ET-BERT 风格 Transformer、TFE-GNN 风格 GCN、Deep Packet 风格 CNN，以及当前增强 PCAP fusion 方法。

5 类 PCAP 子表结果见：

- `data/paper_benchmark/encryption_method_5class_pcap_v1/`
- `outputs/encryption_method/paper_methods_5class_v1/comparison_with_enhanced_current.md`

当前 5 类 PCAP 子表中，增强版当前方法结果为：

| 方法 | Accuracy | Macro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: |
| Enhanced current PCAP fusion | 0.920000 | 0.884615 | 0.920000 |

## 当前进展总结

详细进展见 `CURRENT_PROJECT_SUMMARY.md`。

## 软件系统

现有结果已经封装为完整前后端系统：

- 后端：`software_system/backend/`
- 前端：`software_system/frontend/`
- 实时抓包：通过 `tshark` 抓取网卡流量并进行流级实时预测
- 自动路由：21 维完整时走主模型，21 维缺失时走宽泛 fallback 模型
- 启动脚本：`software_system/start_backend.ps1`
- 使用说明：`software_system/README.md`

启动：

```powershell
.\software_system\start_backend.ps1
```

访问：

```text
http://127.0.0.1:8000
```
