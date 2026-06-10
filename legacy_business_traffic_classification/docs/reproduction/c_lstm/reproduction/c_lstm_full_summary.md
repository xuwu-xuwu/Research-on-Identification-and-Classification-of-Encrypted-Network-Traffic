# C-LSTM 论文复现完整版总结

## 1. 复现对象

本次复现的论文为：

- Yan et al., *Deep Learning-Based Efficient Analysis for Encrypted Traffic*
- 期刊：*Applied Sciences*
- 发表日期：`2023-10-27`
- 论文链接：https://www.mdpi.com/2076-3417/13/21/11776
- 作者 review report：https://www.mdpi.com/2076-3417/13/21/11776/review_report

论文核心方法是 `C-LSTM`，目标是在不解密业务内容的前提下，对加密流量进行快速分类。与本项目此前基于流统计特征的 `RandomForest` 基线不同，这篇论文使用的是**单包级别分类**思路，即直接对每个数据包的字节序列进行建模。

## 2. 复现目标

本次复现的目标不是简单运行一个开源仓库，而是尽量按照论文公开披露的实验设置，在本地数据条件下完成一条可独立运行的复现链路，包括：

- 从原始 `PCAP/PCAPNG` 中提取论文定义的输入；
- 构建论文风格的 `C-LSTM` 网络结构；
- 在本地可获得的加密流量数据上完成训练和评估；
- 使用训练好的模型完成预测实验；
- 对复现结果、偏差来源和局限性做出说明。

## 3. 复现环境

本次复现使用的环境如下：

- Python 解释器：`D:\ProgramData\anaconda3\envs\ai\python.exe`
- 深度学习框架：`torch 2.10.0+cpu`
- 抓包解析相关库：
  - `scapy 2.7.0`
  - `dpkt 1.9.8`
  - `zipfile-inflate64`

其中 `zipfile-inflate64` 是为了解决本地 [NonVPN-PCAPs-03.zip](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/data/NonVPN-PCAPs-03.zip) 使用 `Deflate64` 压缩导致标准库无法读取的问题。

## 4. 本地实现文件

本次复现新增和使用的核心文件如下：

- 预处理与公共工具：[common.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/common.py)
- 数据集生成脚本：[prepare_dataset.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/reproduction/prepare_dataset.py)
- 训练脚本：[train_c_lstm.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/reproduction/train_c_lstm.py)
- 预测脚本：[predict_c_lstm.py](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/src/reproduction/c_lstm/reproduction/predict_c_lstm.py)
- 简版复现说明：[c_lstm_reproduction.md](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/docs/reproduction/c_lstm/reproduction/c_lstm_reproduction.md)

## 5. 论文方法理解

### 5.1 输入表示

论文并不是使用流统计特征，而是直接把单个包作为输入样本。根据论文页面和 review report，本次复现采用如下输入构造方式：

- 去掉链路层头部；
- 去掉网络层头部；
- 保留传输层头部与上层负载；
- 对 UDP 包补零，将 `8B` 的 UDP 头扩展到 `20B`，使其与 TCP 头长度对齐；
- 每个包最终统一成 `1480` 字节定长向量：
  - 长于 `1480` 的部分截断；
  - 短于 `1480` 的部分补零。

因此，本次复现的输入本质上是：

- `packet -> bytes[1480] -> model`

### 5.2 模型结构

根据论文披露的结构和维度说明，本地实现的 `C-LSTM` 结构为：

- `Conv1d(1, 50, kernel_size=5, stride=3)`
- `Conv1d(50, 50, kernel_size=4, stride=3)`
- `MaxPool1d(kernel_size=3, stride=2)`
- `LSTM(input_size=81, hidden_size=50, batch_first=True)`
- `Linear(2500, 500)`
- `Linear(500, 50)`
- `Linear(50, num_classes)`

激活函数使用 `ReLU`，并在全连接层前后使用 `dropout=0.05`。

### 5.3 一个需要说明的实现细节

论文相关材料中，池化层的步长描述与输出张量尺寸存在不一致。如果严格按表格中的输出尺寸 `50 x 81` 倒推，池化层步长应为 `2`，而不是 `3`。因此，本地实现中采用了：

- `MaxPool1d(kernel_size=3, stride=2)`

这个调整不是“自行优化”，而是为了使网络维度与论文公开尺寸保持一致。

## 6. 数据来源与本地数据现实

本地复现使用的数据来源如下：

- [NonVPN-PCAPs-01](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/data/NonVPN-PCAPs-01)
- [NonVPN-PCAPs-03.zip](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/data/NonVPN-PCAPs-03.zip)
- [VPN-PCAPs-02.zip](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/data/VPN-PCAPs-02.zip)

论文原实验是 `12` 类分类任务：

- `Chat`
- `Email`
- `File Transfer`
- `P2P`
- `Streaming`
- `VoIP`
- `VPN-Chat`
- `VPN-Email`
- `VPN-File Transfer`
- `VPN-P2P`
- `VPN-Streaming`
- `VPN-VoIP`

但根据本地原始数据的实际可用情况，本次复现最终只覆盖到 `9` 类：

- `Chat`
- `Email`
- `File Transfer`
- `Streaming`
- `VoIP`
- `VPN-Chat`
- `VPN-File Transfer`
- `VPN-Streaming`
- `VPN-VoIP`

当前缺失类别为：

- `P2P`
- `VPN-Email`
- `VPN-P2P`

这意味着本次工作属于：

- **论文方法完整复现**
- **论文数据集部分复现**

而不是严格意义上的“论文原始 `12` 类实验完全复现”。

## 7. 数据集构建结果

使用预处理脚本从上述原始抓包中构建得到的单包级数据集为：

- 数据文件：[packets_1480.npz](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/packets_1480.npz)
- 数据摘要：[packets_1480.summary.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/packets_1480.summary.json)

数据集规模如下：

- 总包数：`25339`
- 类别数：`9`
- 每个样本输入长度：`1480`

各类别包数分布为：

- `Chat`: `2816`
- `Email`: `1024`
- `File Transfer`: `6907`
- `Streaming`: `5888`
- `VoIP`: `4352`
- `VPN-Chat`: `1024`
- `VPN-File Transfer`: `1024`
- `VPN-Streaming`: `1280`
- `VPN-VoIP`: `1024`

可以看出：

- 数据存在类别不平衡；
- `File Transfer` 和 `Streaming` 占比较大；
- `Email`、`VPN-*` 类别样本相对较少。

## 8. 训练设置

本次正式训练尽量按论文公开设置进行，主要参数如下：

- 训练集/测试集划分：`80% / 20%`
- `batch_size = 32`
- `epochs = 3`
- 优化器：`Adam`
- 学习率：`0.001`
- 权重衰减：`0`
- 设备：`CPU`
- 随机种子：`42`

正式训练输出目录为：

- [run_e3](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/run_e3)

关键产物如下：

- 模型文件：[model.pt](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/run_e3/model.pt)
- 评测指标：[metrics.json](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/run_e3/metrics.json)
- 分类报告：[classification_report.txt](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/run_e3/classification_report.txt)
- 混淆矩阵图：[confusion_matrix.png](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/run_e3/confusion_matrix.png)
- 数据划分索引：[splits.npz](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/run_e3/splits.npz)

## 9. 训练结果

本次正式训练的总体结果如下：

- Accuracy：`0.7269`
- Macro-F1：`0.6882`
- Weighted-F1：`0.7283`

各类别主要表现如下：

- `Chat`：Recall `0.6359`
- `Email`：Recall `0.6439`
- `File Transfer`：Recall `0.7726`
- `Streaming`：Recall `0.8166`
- `VoIP`：Recall `0.6828`
- `VPN-Chat`：Recall `0.8878`
- `VPN-File Transfer`：Recall `0.6000`
- `VPN-Streaming`：Recall `0.5469`
- `VPN-VoIP`：Recall `0.6146`

从结果可以看出：

- `Streaming`、`File Transfer`、`VPN-Chat` 分类效果较好；
- `VPN-Streaming`、`VPN-File Transfer` 相对较弱；
- 整体已经能反映出 `C-LSTM` 对单包字节模式的捕捉能力，但不同类别间仍有明显混淆。

## 10. 预测实验

为了验证训练得到的模型具备实际推理能力，本次又补做了两组预测实验。

### 10.1 测试集纯推理复现实验

该实验直接加载已经训练好的 [model.pt](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/local_partial/run_e3/model.pt)，再对训练阶段划出的测试集执行独立推理。

输出目录：

- [prediction_test_split](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/prediction_test_split)

主要结果：

- 预测包数：`5068`
- Accuracy：`0.7269`

这与训练阶段的评估结果完全一致，说明：

- 模型保存与加载正常；
- 推理脚本与训练脚本使用的输入格式一致；
- 预测流程没有出现标签错位或维度不一致问题。

### 10.2 原始 PCAP 直接预测实验

该实验直接以 [NonVPN-PCAPs-01](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/data/NonVPN-PCAPs-01) 作为输入，由预测脚本在线完成：

- 原始抓包读取；
- 论文风格预处理；
- 包级预测；
- 按文件多数投票汇总。

输出目录：

- [prediction_raw_nonvpn01](d:/Research%20on%20Identification%20and%20Classification%20of%20Encrypted%20Network%20Traffic/outputs/c_lstm/reproduction/prediction_raw_nonvpn01)

主要结果：

- 参与预测包数：`2944`
- Packet-level Accuracy：`0.6498`
- 文件级多数投票正确数：`20 / 23`

这个结果说明：

- 单包级别预测比测试集环境更困难；
- 但在文件级聚合后，模型对整体业务类别已经有较稳定的判断能力。

## 11. 误差分析

本次预测实验中，较明显的错误集中在 `VoIP` 与 `Streaming` 之间。

文件级错误样本包括：

- `facebook_audio1a.pcap`：真实类别 `VoIP`，被预测为 `Streaming`
- `facebook_audio2a.pcap`：真实类别 `VoIP`，被预测为 `Streaming`
- `facebook_video2b.pcapng`：真实类别 `Streaming`，被预测为 `VoIP`

造成这种现象的主要原因可能包括：

- 音视频业务在包长分布和到达节奏上本身相近；
- 单包输入只利用局部字节模式，无法充分体现长时上下文；
- 当前本地数据类别不完整、类别分布不平衡，也会加剧某些边界模糊类别的混淆。

这与加密流量分类领域的常见难点是一致的，也说明论文方法虽然在效率上有优势，但在高度相似业务间仍存在局限。

## 12. 与原论文结果的关系

这次复现需要明确区分“方法是否复现”与“结果是否完全对齐”。

已经完成的部分：

- 论文输入构造规则已实现；
- 论文 `C-LSTM` 结构已实现；
- 训练与预测完整链路已打通；
- 原始 `PCAP -> 预测结果` 已经可以独立运行；
- 本地实验结果已经形成可复查产物。

尚未完全对齐论文的部分：

- 本地缺少 `P2P`、`VPN-Email`、`VPN-P2P` 三类原始流量；
- 因此当前只能完成 `9` 类实验，不能直接与论文 `12` 类最终结果做一一对应比较；
- 暂未重建论文完全一致的数据划分与全部实验表格。

因此，本次工作的合理结论应该是：

- 已完成 `C-LSTM` 方法的工程复现；
- 已在本地可获得数据条件下完成有效实验验证；
- 当前属于**部分数据条件下的论文复现**，而不是论文原始数据上的完全重复实验。

## 13. 本次复现的实际价值

这次复现对当前课题的价值主要体现在以下几个方面：

- 证明了你当前项目不仅能做流级统计特征分类，也能扩展到包级深度学习方法；
- 建立了从原始抓包到深度模型训练的完整工程链路；
- 为后续复现更复杂的时序模型、Transformer 模型提供了可直接复用的预处理基础；
- 形成了一套可用于课程报告、答辩展示和后续对比实验的实际结果。

## 14. 后续建议

如果后续继续推进，优先建议如下：

- 补齐缺失的 `P2P`、`VPN-Email`、`VPN-P2P` 原始数据，尽量逼近论文 `12` 类设定；
- 增加 `10-fold` 交叉验证结果，使实验更接近论文描述；
- 在当前 `C-LSTM` 基础上，与传统机器学习基线做正式对比；
- 对 `VoIP` 与 `Streaming` 混淆问题增加针对性分析；
- 如果老师要求“近几年多篇论文复现”，可以把当前这份 `C-LSTM` 作为第一篇，再继续复现 `Path Signature + LSTM` 或 `TransECA-Net`。

## 15. 可直接引用的结论

可以直接在报告中使用如下表述：

本次工作复现了 Yan 等人在 `2023-10-27` 发表的加密流量分类论文 *Deep Learning-Based Efficient Analysis for Encrypted Traffic* 中提出的 `C-LSTM` 方法。复现过程中，按照论文披露的规则完成了原始 `PCAP` 数据的包级预处理、`1480` 字节定长向量构造以及 `C-LSTM` 网络实现，并在本地可获得的 `9` 类加密流量数据上完成了训练与预测实验。实验结果表明，该模型在当前数据条件下取得了 `0.7269` 的 Accuracy 和 `0.6882` 的 Macro-F1，说明其能够有效捕捉加密数据包中的局部字节模式并实现较好的分类效果。同时，预测实验表明该模型在原始抓包文件上的文件级多数投票结果达到 `20/23` 正确，具有一定实际应用价值。需要说明的是，由于本地缺少 `P2P`、`VPN-Email` 和 `VPN-P2P` 三类原始数据，本次复现属于论文方法的完整实现和本地数据条件下的部分实验复现，而非对论文原始 `12` 类实验结果的完全重现。

