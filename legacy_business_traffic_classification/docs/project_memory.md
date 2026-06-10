# 项目记忆文档

更新时间：2026-04-07  
项目名称：网络加密数据流识别与分类技术研究

## 1. 这份文档的用途

这是一份面向后续续接工作的本地项目备忘录。它记录当前仓库已经完成了什么、主线结果是什么、论文复现做到哪一步、深度学习新增分支有哪些、关键代码和结果放在哪里，以及后面继续推进时最应该从哪里接上。

## 2. 当前项目的真实状态

当前仓库已经不再是单一的传统机器学习分类实验，而是形成了三条并行技术线：

1. 流级统计特征主线  
   基于 `ARFF` 流级统计特征做 7 分类，是当前项目最稳定、最适合作为课程主结果的方向。
2. 论文复现线  
   已完成 `C-LSTM` 和 `TrafficFormer` 两个论文方向的本地复现与增强，用于支撑文献方法对比和研究说明。
3. 深度学习补充线  
   新增了 `MLP`、`TextCNN + RIFA`、`BiLSTM/Transformer`、`TrafficFormer wrapper` 等训练脚本，用于补齐项目中的深度学习方案。

当前推荐结论：

1. 主线结果仍然以流级统计特征上的优化集成模型为主。
2. 论文复现方面，`C-LSTM` 和 `TrafficFormer` 都已经落地，其中 `TrafficFormer + RIFA` 是当前最强的深度学习结果。
3. 自研深度学习分支已经补齐，其中 `TextCNN + RIFA` 是当前最值得保留的轻量级方案。
4. 更复杂的纯 `BiLSTM/Transformer` 路线已经实现，但在当前数据规模下没有打过 `TextCNN + RIFA`，也没有超过复现得到的 `TrafficFormer`。

## 3. 当前目录结构

```text
.
├─ data/
├─ docs/
│  ├─ analysis/
│  ├─ references/
│  ├─ reproduction/
│  ├─ reports/
│  └─ project_memory.md
├─ outputs/
│  ├─ baseline/
│  ├─ optimized/
│  ├─ c_lstm/
│  └─ deep_learning/
├─ src/
│  ├─ baseline/
│  ├─ teammate_optimized/
│  ├─ reproduction/
│  │  ├─ c_lstm/
│  │  └─ TrafficFormer/
│  ├─ deep_learning/
│  └─ README.md
├─ tools/
├─ project_plan_15_weeks.md
├─ readme.md
└─ 课程过程与报告材料
```

## 4. 代码目录说明

### 4.1 流级统计特征主线

- `src/baseline/train_baseline.py`
  - 基线训练脚本
- `src/baseline/predict_baseline.py`
  - 使用已保存模型对无标签数据做预测
- `src/teammate_optimized/train_final_optimized.py`
  - 当前主线最优结果对应的优化版训练脚本

### 4.2 论文复现

- `src/reproduction/c_lstm/`
  - `C-LSTM` 论文复现与改进实现
- `src/reproduction/TrafficFormer/`
  - `TrafficFormer` 官方仓库本地化复现、数据构造、预训练模型微调与 `RIFA` 增强

### 4.3 新增深度学习分支

- `src/deep_learning/train_tabular_mlp.py`
  - 基于当前 `ARFF` 特征的 `MLP` 训练脚本
- `src/deep_learning/train_rifa_textcnn.py`
  - 自研 `TextCNN` 序列模型，支持 `RIFA`
- `src/deep_learning/train_rifa_bilstm_transformer.py`
  - 更强的 `BiLSTM/Transformer` 尝试版本
- `src/deep_learning/run_pretrained_trafficformer.py`
  - 对 `TrafficFormer` 复现结果做项目内标准化训练/输出包装

### 4.4 工具脚本

- `tools/build_opening_report_docx.py`
  - 开题报告文档生成工具
- `tools/build_requirements_docx.py`
  - 需求分析报告文档生成工具

## 5. 文档目录说明

### 5.1 分析文档

- `docs/analysis/teammate_optimization_analysis.md`
  - 同事优化版整体分析
- `docs/analysis/train_final_optimized_code_analysis.md`
  - 优化脚本代码级解析
- `docs/analysis/train_final_optimized_tech_stack.md`
  - 优化版技术路线说明

### 5.2 论文复现文档

- `docs/reproduction/c_lstm/reproduction/c_lstm_full_summary.md`
  - `C-LSTM` 复现完整版总结

### 5.3 报告文档

- `docs/reports/需求分析报告-网络加密数据流识别与分类技术研究.md`
  - 当前需求分析报告
- `docs/reports/开题报告-网络加密数据流识别与分类技术研究.md`
  - 当前开题报告
- `docs/reports/当前项目进度总结-2026-04-07.md`
  - 当前整体进度总结

## 6. 当前已确定的数据与任务口径

### 6.1 项目主线数据

- 数据文件：`data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-15s-AllinOne.arff`
- 数据形态：流级统计特征
- 当前主任务：7 分类
- 类别包括：
  - `BROWSING`
  - `CHAT`
  - `FT`
  - `MAIL`
  - `P2P`
  - `STREAMING`
  - `VOIP`

这是当前项目最核心、最适合作为课程主交付的数据口径。

### 6.2 `TrafficFormer` 复现数据

- 数据目录：`src/reproduction/TrafficFormer/data/iscxvpn_service/dataset/`
- 当前有效训练文件：
  - `train_dataset.tsv`
  - `train_base_dataset.tsv`
  - `train_rifa_dataset.tsv`
  - `valid_dataset.tsv`
  - `test_dataset.tsv`
- 任务口径：`ISCX-VPN service` 4 分类序列任务
- 当前类别：
  - `Chat`
  - `FileTransfer`
  - `Streaming`
  - `VoIP`

注意：这条线服务的是论文复现和序列建模，不要直接与 7 分类流级主线做横向数值比较。

### 6.3 `C-LSTM` 复现数据

- 复现方向：单包字节序列建模
- 当前结果数据文件：`outputs/c_lstm/local_partial/packets_1480.npz`
- 复现输入方式：将单包处理为固定长度 `1480` 字节向量

这条线同样不是流级统计特征主线，而是包级/序列级论文复现。

## 7. 当前关键实验结果

### 7.1 流级主线结果

| 方案 | 输出路径 | Accuracy | Macro-F1 | 说明 |
| --- | --- | ---: | ---: | --- |
| Baseline RandomForest | `outputs/baseline/baseline_run/metrics.json` | 0.8905 | 0.8625 | 已完成基础闭环 |
| Optimized Ensemble | `outputs/optimized/final_optimized_v2_run/metrics.json` | 0.9312 | 0.9117 | 当前主线最优结果 |

当前最推荐保留和对外汇报的主结果是：

- `outputs/optimized/final_optimized_v2_run/metrics.json`

### 7.2 `C-LSTM` 复现结果

| 阶段 | 输出路径 | Accuracy | Macro-F1 | 说明 |
| --- | --- | ---: | ---: | --- |
| 原始复现版 | `outputs/c_lstm/reproduction/local_partial/run_e3/metrics.json` | 0.7269 | 0.6882 | 本地初步复现成功 |
| 改进版 | `outputs/c_lstm/improved/run_v1/metrics.json` | 0.7597 | 0.7629 | 训练策略改进后更稳定 |

当前最应该保留的是：

- `outputs/c_lstm/improved/run_v1/metrics.json`

### 7.3 `TrafficFormer` 论文复现结果

核心状态文档：

- `src/reproduction/TrafficFormer/docs/STATUS.md`

文档中记录的复现结果为：

| 方案 | 记录位置 | Accuracy | Macro-F1 | Weighted-F1 |
| --- | --- | ---: | ---: | ---: |
| TrafficFormer Baseline | `src/reproduction/TrafficFormer/docs/STATUS.md` | 0.8657 | 0.6525 | 0.8534 |
| TrafficFormer + `RIFA` | `src/reproduction/TrafficFormer/docs/STATUS.md` | 0.9403 | 0.8587 | 0.9482 |

这里需要特别记住：

1. `TrafficFormer` 的论文复现成果本体在 `src/reproduction/TrafficFormer/`。
2. 当前最强结果来自预训练 `Transformer + RIFA` 微调。
3. 最终强结果使用的是 `train_dataset.tsv` 这个当前激活的 paper-style 训练文件。

### 7.4 新增深度学习分支结果

| 方案 | 输出路径 | Accuracy | Macro-F1 | 说明 |
| --- | --- | ---: | ---: | --- |
| Flow MLP | `outputs/deep_learning/flow_mlp_v1/metrics.json` | 0.8473 | 0.8092 | 当前主数据上的深度学习补充基线 |
| TextCNN Base | `outputs/deep_learning/rifa_textcnn_base_v1/metrics.json` | 0.8806 | 0.7554 | 不带 `RIFA` 的序列模型基线 |
| TextCNN + `RIFA` | `outputs/deep_learning/rifa_textcnn_rifa_v1/metrics.json` | 0.8955 | 0.8356 | 当前自研轻量序列模型最佳 |
| BiLSTM-only + `RIFA` v2 | `outputs/deep_learning/rifa_bilstm_only_rifa_v2/metrics.json` | 0.8507 | 0.7991 | 更强结构已实现但未超过 TextCNN |
| TrafficFormer wrapper + `RIFA` | `outputs/deep_learning/trafficformer_transformer_rifa_v2/metrics.json` | 0.9403 | 0.8587 | 项目内统一输出的最强深度学习结果 |

其中：

1. `TextCNN + RIFA` 是当前最值得保留的自研轻量深度学习方案。
2. `BiLSTM/Transformer` 路线已经实现，但当前性价比不如 `TextCNN + RIFA`。
3. `run_pretrained_trafficformer.py` 产生的结果，本质上是对 `TrafficFormer` 复现成果的项目内统一包装输出。

## 8. 当前最推荐保留的成果

### 8.1 课程主线结果

- `outputs/optimized/final_optimized_v2_run/metrics.json`

原因：

1. 与项目主任务口径完全一致。
2. 结果最稳定。
3. 最适合写入课程报告正文和答辩主图表。

### 8.2 论文复现成果

- `outputs/c_lstm/improved/run_v1/metrics.json`
- `src/reproduction/TrafficFormer/docs/STATUS.md`
- `outputs/deep_learning/trafficformer_transformer_rifa_v2/metrics.json`

原因：

1. `C-LSTM` 代表经典序列模型复现与改进。
2. `TrafficFormer` 代表预训练 `Transformer + RIFA` 的完整论文复现。
3. 标准化 `metrics.json` 方便当前项目统一汇总和写表格。

### 8.3 自研深度学习补充成果

- `outputs/deep_learning/flow_mlp_v1/metrics.json`
- `outputs/deep_learning/rifa_textcnn_rifa_v1/metrics.json`

原因：

1. `MLP` 证明主数据也可以直接接深度学习。
2. `TextCNN + RIFA` 证明轻量模型配合增强策略是有效的。

## 9. 环境与运行注意事项

### 9.1 推荐环境

用户指定的环境是：

```bash
conda activate ai
```

### 9.2 当前已经验证可用的 Python

在本机上，以下解释器已被用于实际运行：

- `D:\ProgramData\anaconda3\envs\ai\python.exe`

如果 PowerShell 下直接 `conda activate ai` 出现编码或会话问题，优先使用：

```bash
conda run -n ai python ...
```

或者直接调用解释器：

```bash
D:\ProgramData\anaconda3\envs\ai\python.exe ...
```

### 9.3 `TrafficFormer` 环境确认

`src/reproduction/TrafficFormer/docs/STATUS.md` 中已经记录，当前本机验证环境包括：

1. Python `3.13.11`
2. PyTorch `2.10.0 + CUDA 12.6`
3. NVIDIA GeForce RTX 4060 Laptop GPU

## 10. 当前已知问题与风险

1. 不同实验线使用的数据集、类别数和输入表示不同，不能直接把所有结果放进一个表里比较优劣。
2. `TrafficFormer` 的最强结果属于 4 分类序列任务，不能直接拿来替代当前 7 分类流级主线。
3. 自研 `BiLSTM/Transformer` 已实现，但说明当前瓶颈更多可能在数据构造、增强策略和迁移方式，而不是单纯堆复杂网络。
4. 仓库当前 `git status --short` 仍显示较多未跟踪目录和历史迁移痕迹，后续若要提交仓库，需要先做一次整理。
5. 根目录旧版 `train_baseline.py`、`predict_baseline.py` 显示为已删除，当前有效代码入口已经迁移到 `src/` 目录。

## 11. 当前仓库状态提醒

根据最近一次 `git status --short`，当前仓库仍处于未完全收口状态：

1. `docs/`、`src/`、`tools/` 等目录在当前状态下显示为未跟踪。
2. 根目录旧版 `train_baseline.py`、`predict_baseline.py` 显示为已删除。
3. 存在课程文档、Office 文件与目录迁移并存的情况。

这不影响本地继续实验，但如果后续需要提交、打包或给老师展示目录，建议先做一次工作区清理。

## 12. 如果下次继续做，优先从哪里接上

如果后续继续推进项目，建议按下面的顺序续接：

1. 先看 `docs/reports/当前项目进度总结-2026-04-07.md`
   - 先建立对当前总体状态的全局认识。
2. 再看 `docs/project_memory.md`
   - 用来确认当前仓库结构、结果路径和续接点。
3. 主线实验从这里接：
   - `src/teammate_optimized/train_final_optimized.py`
   - `outputs/optimized/final_optimized_v2_run/metrics.json`
4. `C-LSTM` 复现从这里接：
   - `docs/reproduction/c_lstm/reproduction/c_lstm_full_summary.md`
   - `src/reproduction/c_lstm/`
5. `TrafficFormer` 复现从这里接：
   - `src/reproduction/TrafficFormer/docs/STATUS.md`
   - `src/reproduction/TrafficFormer/`
6. 自研深度学习从这里接：
   - `src/deep_learning/train_rifa_textcnn.py`
   - `src/deep_learning/train_rifa_bilstm_transformer.py`
   - `src/deep_learning/run_pretrained_trafficformer.py`

## 13. 当前最短结论

截至 `2026-04-07`，本项目已经形成如下结构：

1. 流级统计特征优化集成模型是当前课程主线最优结果。
2. `C-LSTM` 与 `TrafficFormer` 两条论文复现线都已完成落地。
3. 深度学习补充线已经建立，其中 `TextCNN + RIFA` 是当前最值得保留的自研轻量方案。
4. `TrafficFormer + RIFA` 是当前最强的深度学习结果，但它属于论文复现和序列建模支线，不直接替代主线流级任务。
