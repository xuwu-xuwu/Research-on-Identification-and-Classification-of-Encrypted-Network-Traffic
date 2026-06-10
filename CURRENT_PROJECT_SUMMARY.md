# 当前工作进展总结

更新时间：2026-06-03

## 1. 研究主线

当前仓库主线已经从旧的“应用/业务流量分类”整理为“加密方法识别与分类”。

当前全量任务是 9 类加密方法或匿名通信机制识别：

- `NON_ENCRYPTED`
- `TLS_FAMILY`
- `SSH`
- `QUIC`
- `VPN`
- `TOR`
- `I2P`
- `FREENET`
- `ZERONET`

旧业务分类代码、输出、ARFF 数据和早期复现文档已经归档到 `legacy_business_traffic_classification/`。

## 2. 当前数据集

全量主数据集：

- 目录：`data/unified_encryption_method_v2_all_data/`
- 主文件：`multiclass_finetune.csv`
- 样本总数：316601
- 划分方式：直接使用 CSV 中已有的 `split` 字段，不重新随机拆分
- 训练集：221617
- 验证集：47490
- 测试集：47494

测试集按类别数量：

| 类别 | Test 样本数 |
| --- | ---: |
| `NON_ENCRYPTED` | 25371 |
| `TLS_FAMILY` | 5044 |
| `SSH` | 7318 |
| `QUIC` | 52 |
| `VPN` | 8811 |
| `TOR` | 210 |
| `I2P` | 315 |
| `FREENET` | 24 |
| `ZERONET` | 349 |

完整统计见 `data/unified_encryption_method_v2_all_data/metadata.json`。

## 3. 当前最新主方法

当前最新主方法是 `full_enhanced_fusion_xgboost`。

实现脚本：

- `src/encryption_method/train_full_enhanced_fusion.py`

输出目录：

- `outputs/encryption_method/full_enhanced_fusion_v1/`

方法输入：

- 21 个全量样本共有的流级统计特征
- `transport` one-hot 特征
- 从 `sequence_text` 中抽取的序列统计特征
- 排除 `source_name`，避免来源泄漏

当前全量 9 类测试结果：

| 指标 | 数值 |
| --- | ---: |
| Accuracy | 0.993978 |
| Macro-F1 | 0.892797 |
| Weighted-F1 | 0.994046 |
| Macro Recall | 0.909893 |

主要输出：

- `outputs/encryption_method/full_enhanced_fusion_v1/model.json`
- `outputs/encryption_method/full_enhanced_fusion_v1/model.joblib`
- `outputs/encryption_method/full_enhanced_fusion_v1/metrics.json`
- `outputs/encryption_method/full_enhanced_fusion_v1/classification_report.txt`
- `outputs/encryption_method/full_enhanced_fusion_v1/confusion_matrix.csv`

## 4. 第一层公平对比

第一层公平对比用于全量 9 类主表，原则是：

- 同一任务：都做 9 类加密方法识别
- 同一数据：都用 `data/unified_encryption_method_v2_all_data/multiclass_finetune.csv`
- 同一划分：复用 `split = train / valid / test`
- 同一评测：Accuracy / Macro-F1 / Weighted-F1 / 各类 Recall / 混淆矩阵
- 不使用 `source_name`，避免来源泄漏

已经跑通的 XGBoost 表格基线：

- 输出目录：`outputs/encryption_method/tabular_main_table_smoke_xgb/`
- Accuracy：0.993136
- Macro-F1：0.828463
- Weighted-F1：0.992758

当前增强主方法相对该基线主要提升 Macro-F1：

| 方法 | Accuracy | Macro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: |
| XGBoost tabular baseline | 0.993136 | 0.828463 | 0.992758 |
| `full_enhanced_fusion_xgboost` | 0.993978 | 0.892797 | 0.994046 |

## 5. 论文方法 PCAP 子表对比

ET-BERT、TFE-GNN、Deep Packet 这类论文方法需要原始包、字节序列或包图结构输入，不能直接公平覆盖全量 `multiclass_finetune.csv` 中所有样本。因此当前将它们放到第二层 PCAP 子表。

PCAP 子表数据：

- 目录：`data/paper_benchmark/encryption_method_5class_pcap_v1/`
- 类别：`NON_ENCRYPTED / TLS_FAMILY / SSH / QUIC / TOR`
- 总样本：146
- 训练集：98
- 验证集：23
- 测试集：25

当前已实现的对比方法：

- ET-BERT style Transformer
- TFE-GNN style GCN
- Deep Packet style CNN
- Original current hybrid
- Enhanced current PCAP fusion

当前 5 类 PCAP 子表结果：

| 方法 | Accuracy | Macro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: |
| Enhanced current PCAP fusion | 0.920000 | 0.884615 | 0.920000 |
| Deep Packet style CNN | 0.920000 | 0.869778 | 0.921422 |
| ET-BERT style Transformer | 0.720000 | 0.607692 | 0.658462 |
| Original current hybrid | 0.600000 | 0.406667 | 0.612889 |
| TFE-GNN style GCN | 0.480000 | 0.137143 | 0.356571 |

完整结果见：

- `outputs/encryption_method/paper_methods_5class_v1/comparison_with_enhanced_current.md`
- `docs/analysis/paper_methods_5class_comparison.md`

## 6. 当前可复现实验命令

训练当前全量 9 类最新主方法：

```powershell
python src\encryption_method\train_full_enhanced_fusion.py `
  --data-dir data\unified_encryption_method_v2_all_data `
  --output-dir outputs\encryption_method\full_enhanced_fusion_v1
```

构建 5 类 PCAP 论文方法子表：

```powershell
python src\encryption_method\build_paper_benchmark_dataset.py `
  --max-flows-per-label 40 `
  --output-dir data\paper_benchmark\encryption_method_5class_pcap_v1
```

运行论文方法对比：

```powershell
python src\encryption_method\benchmark_paper_methods.py `
  --data-dir data\paper_benchmark\encryption_method_5class_pcap_v1 `
  --output-dir outputs\encryption_method\paper_methods_5class_v1
```

训练当前增强 PCAP fusion 方法：

```powershell
python src\encryption_method\train_enhanced_pcap_fusion.py `
  --data-dir data\paper_benchmark\encryption_method_5class_pcap_v1 `
  --output-dir outputs\encryption_method\paper_methods_5class_v1\current_pcap_fusion
```

## 7. 目录整理结果

当前主线保留在：

- `src/encryption_method/`
- `data/unified_encryption_method_v2_all_data/`
- `data/encryption_method_identification/`
- `data/paper_benchmark/`
- `outputs/encryption_method/`
- `docs/analysis/`
- `docs/reports/`

旧业务流量分类归档在：

- `legacy_business_traffic_classification/src/`
- `legacy_business_traffic_classification/outputs/`
- `legacy_business_traffic_classification/data/`
- `legacy_business_traffic_classification/docs/`
- `legacy_business_traffic_classification/root_files/`

## 8. 后续建议

下一步如果要把对比实验写成论文主表，建议按两个层次呈现：

- 全量 9 类主表：以当前 `full_enhanced_fusion_xgboost` 为最新方法，和全量流级表格基线比较。
- 5 类 PCAP 子表：以 ET-BERT / TFE-GNN / Deep Packet 风格方法作为论文方法对比，说明它们只能在有原始 PCAP 的子集上公平比较。

当前仍需注意：5 类 PCAP 子表测试集只有 25 条，适合作为“方法复现与输入粒度对比”的初步实验，不应直接替代全量 9 类主表结论。

## 9. 软件系统与 fallback 模型

当前软件系统已经加入自动路由预测：

- 输入 21 个流级数值特征完整：使用 `full_enhanced_fusion_xgboost`
- 输入 21 个流级数值特征不完整：使用 `broad_fallback_xgboost`

fallback 模型输出目录：

- `outputs/encryption_method/broad_fallback_v1/`

fallback 模型当前结果：

| 场景 | Accuracy | Macro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: |
| 完整 21 维 | 0.990504 | 0.850941 | 0.990654 |
| 随机缺失部分数值特征 | 0.961342 | 0.705741 | 0.962178 |
| 21 维数值全缺失 | 0.526298 | 0.289372 | 0.513755 |
| 仅 `transport` | 0.420074 | 0.110943 | 0.396931 |

系统预测输出会标注 `model_used`、`input_profile` 和 `missing_numeric_features`，便于区分高可信完整输入预测和低信息量 fallback 预测。
