# 旧业务流量分类归档

本目录保存项目早期“应用/业务流量分类”相关内容。当前研究主线已经切换为“加密方法识别与分类”，因此这些文件从主目录归档到这里，避免和当前实验混淆。

## 归档内容

- `src/`：旧业务分类代码，包括 baseline、同学优化版、深度学习分支、C-LSTM 和 TrafficFormer 复现。
- `outputs/`：旧业务分类实验输出，包括 baseline、optimized、deep_learning、c_lstm 和 catboost 信息。
- `data/`：旧业务分类使用的 ARFF 数据。
- `docs/`：旧业务分类分析、复现说明、早期项目进度和命令汇总。
- `root_files/`：早期根目录说明和优化方案。
- `tools/`：早期开题/需求报告生成工具。

## 未归档的共享数据

以下原始 PCAP 或通用数据仍保留在仓库根目录 `data/` 下，因为当前加密方法识别和 PCAP 论文方法对比仍会使用：

- `data/NonVPN-PCAPs-01`
- `data/NonVPN-PCAPs-03`
- `data/VPN-PCAPs-02`
- `data/NonTor`
- `data/Tor`
- `data/Dataset.csv`
- `data/BCCC-Darknet-2025 (6)(1)`

## 使用说明

本目录内容只作为历史复现和材料参考，不再作为当前论文主表实验入口。当前实验入口见仓库根目录 `readme.md` 和 `src/encryption_method/`。
