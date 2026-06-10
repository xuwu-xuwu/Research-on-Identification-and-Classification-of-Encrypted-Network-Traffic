# 全量 9 类增强融合主方法

更新时间：`2026-06-03`

## 1. 方法定位

`full_enhanced_fusion_xgboost` 是当前仓库面向全量 9 类加密方法识别任务的最新主方法。

它继承了第二层 PCAP 子表增强实验的核心思路：融合多粒度证据，而不是只依赖单一流级统计特征。但由于全量 `multiclass_finetune.csv` 中大多数样本没有真实包字节，本方法在全量主表上采用全量可用的融合特征：

- 21 个流级统计特征。
- `transport` one-hot 特征。
- 从 `sequence_text` 派生的 18 个序列统计特征。
- 不使用 `source_name`，避免数据来源泄漏。

## 2. 训练脚本

新增脚本：

- `src/encryption_method/train_full_enhanced_fusion.py`

训练命令：

```powershell
python src\encryption_method\train_full_enhanced_fusion.py `
  --data-dir data\unified_encryption_method_v2_all_data `
  --output-dir outputs\encryption_method\full_enhanced_fusion_v1 `
  --n-estimators 350 `
  --max-depth 7 `
  --learning-rate 0.05 `
  --class-weight-power 0.5
```

模型输出：

- `outputs/encryption_method/full_enhanced_fusion_v1/model.json`
- `outputs/encryption_method/full_enhanced_fusion_v1/model.joblib`
- `outputs/encryption_method/full_enhanced_fusion_v1/metrics.json`
- `outputs/encryption_method/full_enhanced_fusion_v1/comparison.md`

## 3. 当前结果

数据：

- `data/unified_encryption_method_v2_all_data/multiclass_finetune.csv`

任务：

- `NON_ENCRYPTED`
- `TLS_FAMILY`
- `SSH`
- `QUIC`
- `VPN`
- `TOR`
- `I2P`
- `FREENET`
- `ZERONET`

划分：

| split | samples |
| --- | ---: |
| `train` | 221617 |
| `valid` | 47490 |
| `test` | 47494 |

主结果：

| method | Accuracy | Macro-F1 | Weighted-F1 | Macro Recall |
| --- | ---: | ---: | ---: | ---: |
| Full enhanced fusion XGBoost | 0.993978 | 0.892797 | 0.994046 | 0.909893 |

各类 Recall：

| label | recall |
| --- | ---: |
| `NON_ENCRYPTED` | 0.997083 |
| `TLS_FAMILY` | 0.997423 |
| `SSH` | 0.998907 |
| `QUIC` | 1.000000 |
| `VPN` | 0.994893 |
| `TOR` | 0.766667 |
| `I2P` | 0.831746 |
| `FREENET` | 0.708333 |
| `ZERONET` | 0.893983 |

## 4. 与上一版第一层基线对比

上一版全量公平 XGBoost smoke 结果：

| method | Accuracy | Macro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: |
| XGBoost tabular baseline | 0.993136 | 0.828463 | 0.992758 |

增强后：

| method | Accuracy | Macro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: |
| Full enhanced fusion XGBoost | 0.993978 | 0.892797 | 0.994046 |

提升：

| metric | improvement |
| --- | ---: |
| Accuracy | +0.000842 |
| Macro-F1 | +0.064334 |
| Weighted-F1 | +0.001288 |

主要收益来自小类召回提升，尤其是 `FREENET / TOR / I2P / ZERONET` 这类样本较少或来源复杂的类别。

## 5. 当前结论

当前全量主表建议采用 `full_enhanced_fusion_xgboost` 作为最新主方法。它比之前的全量 tabular XGBoost 更适合作为论文主结果，因为它在保持高 Accuracy 的同时显著提升 Macro-F1，更能说明模型对小类的识别能力。

第二层 PCAP 子表中的 `current_pcap_fusion` 仍作为论文方法对比子表结果保留；第一层全量 9 类主表则以 `full_enhanced_fusion_xgboost` 作为当前主流方法。
