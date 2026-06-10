# 论文方法 5 类 PCAP 子表对比实验

更新时间：`2026-06-03`

## 1. 实验定位

这组实验用于补充第一层全量 tabular 主表。第一层主表面向 `multiclass_finetune.csv` 的 9 类加密方法识别；本实验面向论文方法所需的原始包/序列输入，因此单独构建 5 类 PCAP 子表：

- `NON_ENCRYPTED`
- `TLS_FAMILY`
- `SSH`
- `QUIC`
- `TOR`

这不是把旧的业务分类复现结果直接拿来比较，而是在当前项目的加密方法标签下重新构建数据、重新训练、重新评测。

## 2. 对比方法

本轮选择三类论文方法作为第二层对比对象：

- `Deep Packet style CNN`：对应 Deep Packet 的原始包字节建模思想，使用首包字节序列训练 1D CNN。
- `ET-BERT style Transformer`：对应 ET-BERT 的 datagram/token 序列 Transformer 思路，使用多包字节 token 序列训练 Transformer。
- `TFE-GNN style GCN`：对应 TFE-GNN 的字节图/图神经网络思路，使用字节转移共现图训练 GCN。
- `Current project hybrid`：当前项目的 hybrid classifier，裁剪到同一个 5 类 PCAP 子表上重新训练。

说明：本轮是本地同口径实现，不是声称已经完整复刻三篇论文的官方训练流水线。尤其是 ET-BERT 的官方预训练权重与 TFE-GNN 的完整图构造流程，后续可以作为更严格版本继续接入。

## 3. 数据集

构建脚本：

```powershell
python src\encryption_method\build_paper_benchmark_dataset.py `
  --max-flows-per-label 40 `
  --max-packets-per-flow 6 `
  --packet-size 256 `
  --max-capture-packets 8000 `
  --max-auto-captures-per-label 4 `
  --output-dir data\paper_benchmark\encryption_method_5class_pcap_v1
```

输出位置：

- `data/paper_benchmark/encryption_method_5class_pcap_v1/packet/flows_5class.npz`
- `data/paper_benchmark/encryption_method_5class_pcap_v1/trafficformer/`
- `data/paper_benchmark/encryption_method_5class_pcap_v1/hybrid/`

当前子表规模：

| label | samples |
| --- | ---: |
| `NON_ENCRYPTED` | 40 |
| `TLS_FAMILY` | 40 |
| `SSH` | 40 |
| `QUIC` | 8 |
| `TOR` | 18 |

划分规模：

| split | samples |
| --- | ---: |
| `train` | 98 |
| `valid` | 23 |
| `test` | 25 |

## 4. 结果

论文方法训练命令：

```powershell
python src\encryption_method\benchmark_paper_methods.py `
  --data data\paper_benchmark\encryption_method_5class_pcap_v1\packet\flows_5class.npz `
  --output-dir outputs\encryption_method\paper_methods_5class_v1 `
  --epochs 5 `
  --batch-size 16 `
  --models deep_packet_cnn et_bert_transformer tfe_gnn
```

当前项目方法训练命令：

```powershell
python src\encryption_method\train_hybrid_classifier.py `
  --data-dir data\paper_benchmark\encryption_method_5class_pcap_v1\hybrid `
  --output-dir outputs\encryption_method\paper_methods_5class_v1\current_hybrid `
  --binary-epochs 4 `
  --multiclass-epochs 8 `
  --batch-size 32 `
  --hidden-dim 96 `
  --seq-embedding-dim 32 `
  --max-seq-len 64 `
  --early-stop-patience 3
```

统一结果表：

| method | implementation | accuracy | f1_macro | f1_weighted | macro_recall | samples_test |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Deep Packet style CNN | `deep_packet_cnn` | 0.9200 | 0.8698 | 0.9214 | 0.8846 | 25 |
| ET-BERT style Transformer | `et_bert_transformer` | 0.7200 | 0.6077 | 0.6585 | 0.6846 | 25 |
| Current project hybrid | `current_hybrid` | 0.6000 | 0.4067 | 0.6129 | 0.4677 | 25 |
| TFE-GNN style GCN | `tfe_gnn` | 0.4800 | 0.1371 | 0.3566 | 0.1846 | 25 |

完整输出：

- `outputs/encryption_method/paper_methods_5class_v1/comparison_with_current.md`
- `outputs/encryption_method/paper_methods_5class_v1/comparison_with_current.csv`
- `outputs/encryption_method/paper_methods_5class_v1/*/metrics.json`

## 5. 当前结论

在当前小规模 PCAP 子表上，原始字节 CNN 的 `Deep Packet style` 表现最好，说明包字节局部模式对 5 类加密方法识别有明显价值。`ET-BERT style` 能跑通并取得中等结果，但本轮没有接入官方预训练权重，因此不应直接等同于完整 ET-BERT。`TFE-GNN style` 目前较弱，主要原因是本轮只实现了紧凑字节转移图，且训练样本较少。

当前项目 hybrid 方法在全量 tabular 主表上更合适；在这个小型 PCAP 子表上样本少、二阶段层级误差明显，因此结果低于 Deep Packet style。

## 6. 局限

- 该实验是第二层 PCAP 子表，不替代第一层 9 类全量主表。
- `QUIC` 和 `TOR` 样本仍偏少，测试集只有 25 条流，结果需要后续扩样本确认。
- 本轮 ET-BERT/TFE-GNN 是本地同口径实现，后续如要写成最终论文结果，应继续接入官方预训练模型和完整图构造流程。

## 7. 当前方法增强结果

根据首轮对比，原始 `Current project hybrid` 在 PCAP 子表上主要受两个因素限制：

- 它采用二阶段层级分类，二分类阶段错误会继续传递到后续多分类。
- 它主要依赖流级统计和长度/IAT 序列，没有直接利用真实包字节。

因此新增增强脚本：

- `src/encryption_method/train_enhanced_pcap_fusion.py`

增强版当前方法改为单阶段 5 类分类，并融合三类输入：

- 原有 21 个流级统计特征。
- 全流包字节直方图。
- 首包字节序列。

训练命令：

```powershell
python src\encryption_method\train_enhanced_pcap_fusion.py `
  --packet-data data\paper_benchmark\encryption_method_5class_pcap_v1\packet\flows_5class.npz `
  --hybrid-csv data\paper_benchmark\encryption_method_5class_pcap_v1\hybrid\multiclass_finetune.csv `
  --output-dir outputs\encryption_method\paper_methods_5class_v1\current_pcap_fusion `
  --n-estimators 800
```

增强后统一结果：

| method | implementation | accuracy | f1_macro | f1_weighted |
| --- | --- | ---: | ---: | ---: |
| Enhanced current PCAP fusion | `current_pcap_fusion` | 0.9200 | 0.8846 | 0.9200 |
| Deep Packet style CNN | `deep_packet_cnn` | 0.9200 | 0.8698 | 0.9214 |
| ET-BERT style Transformer | `et_bert_transformer` | 0.7200 | 0.6077 | 0.6585 |
| Original current hybrid | `current_hybrid` | 0.6000 | 0.4067 | 0.6129 |
| TFE-GNN style GCN | `tfe_gnn` | 0.4800 | 0.1371 | 0.3566 |

完整输出：

- `outputs/encryption_method/paper_methods_5class_v1/current_pcap_fusion/metrics.json`
- `outputs/encryption_method/paper_methods_5class_v1/comparison_with_enhanced_current.md`
- `outputs/encryption_method/paper_methods_5class_v1/comparison_with_enhanced_current.csv`

该增强说明：在 PCAP 子表上，当前方法需要显式加入包字节证据；继续只调原来的层级 hybrid 结构收益有限。
