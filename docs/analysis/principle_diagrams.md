# 加密流量识别原理图

本文只描述当前项目的识别原理，不按工程模块、前后端、脚本调用关系绘制。
核心问题是：在看不到明文载荷的前提下，从流量留下的可观测侧信道痕迹中识别加密方法或匿名通信机制。

## 图 1：识别问题与证据来源

```mermaid
flowchart TD
    A["网络通信流"] --> B["明文载荷不可直接使用"]
    B --> C["保留可观测侧信道痕迹"]

    C --> D["包长与字节规模"]
    C --> E["前向/后向交互方向"]
    C --> F["包间隔与持续时间"]
    C --> G["传输层协议线索"]
    C --> H["原始包字节结构"]

    D --> I["流级统计特征"]
    E --> I
    F --> I
    G --> J["transport"]
    D --> K["长度桶 token"]
    E --> K
    F --> L["IAT 桶 token"]
    H --> M["PCAP 包级证据"]

    I --> N["统一样本表示"]
    J --> N
    K --> N
    L --> N
    M --> O["仅用于 PCAP 子表"]

    N --> P["统一 9 类标签空间"]
    P --> P1["NON_ENCRYPTED"]
    P --> P2["TLS_FAMILY / SSH / QUIC / VPN"]
    P --> P3["TOR / I2P / FREENET / ZERONET"]

    O --> Q["5 类包级对照标签"]
    Q --> Q1["NON_ENCRYPTED / TLS_FAMILY / SSH / QUIC / TOR"]
```

要点：项目不是解密流量，而是利用加密通信仍然暴露的包长、方向、时序、传输层和包字节形态来识别加密方法或匿名通信机制。全量主任务使用统一 9 类标签；需要原始包字节的方法只在 PCAP 子表中比较。

## 图 2：全量 9 类主方法融合判别原理

```mermaid
flowchart TD
    A["统一全量样本"] --> B["21 个流级数值特征"]
    A --> C["transport"]
    A --> D["sequence_text"]

    B --> B1["缺失值用训练集中位数填补"]
    B1 --> B2["signed log1p 压缩长尾"]
    B2 --> B3["标准化"]

    C --> C1["传输层 one-hot"]

    D --> D1["解析方向、长度桶、IAT 桶"]
    D1 --> D2["18 个序列派生统计"]
    D2 --> D3["log 缩放与标准化"]

    B3 --> E["多粒度证据融合向量"]
    C1 --> E
    D3 --> E

    E --> F["XGBoost 学习多分类判别边界"]
    F --> G["9 类概率分布"]
    G --> H["最终预测标签"]

    S["source_name"] -. "排除" .-> E
    S --> T["避免数据来源泄漏"]
```

要点：主模型 `full_enhanced_fusion_xgboost` 的核心是把流统计、传输层和序列节奏三类证据压到同一个特征空间，再由 XGBoost 学习 9 类边界。`source_name` 被明确排除，避免模型记住数据来自哪里。

## 图 3：包级对照、低信息输入与公平评估边界

```mermaid
flowchart TD
    A["待评估或待预测样本"] --> B{"输入信息形态"}

    B -- "完整流级特征" --> C["主模型证据空间"]
    C --> C1["流统计 + transport + sequence_text"]
    C1 --> C2["full_enhanced_fusion_xgboost"]
    C2 --> C3["高信息量 9 类预测"]

    B -- "数值特征缺失" --> D["缺失鲁棒证据空间"]
    D --> D1["可用数值 + 缺失指示位 + transport + sequence_text"]
    D1 --> D2["broad_fallback_xgboost"]
    D2 --> D3["低信息量兜底预测"]

    B -- "有真实 PCAP 包字节" --> E["包级证据空间"]
    E --> E1["首包字节序列"]
    E --> E2["多包字节 token"]
    E --> E3["字节转移图"]
    E --> E4["字节直方图 + 首包 + 流统计"]

    E1 --> F1["Deep Packet 风格 CNN"]
    E2 --> F2["ET-BERT 风格 Transformer"]
    E3 --> F3["TFE-GNN 风格 GCN"]
    E4 --> F4["当前增强 PCAP fusion"]
    F1 --> G["5 类 PCAP 子表对照"]
    F2 --> G
    F3 --> G
    F4 --> G

    C3 --> H["公平评估约束"]
    D3 --> H
    G --> H
    H --> H1["同一任务与标签"]
    H --> H2["同一 train / valid / test 划分"]
    H --> H3["Accuracy / Macro-F1 / Weighted-F1 / Macro Recall"]
    H --> H4["混淆矩阵"]
```

要点：完整输入走主模型；缺失输入走 fallback，并在结果中体现信息不足；需要原始包字节的论文方法只在 PCAP 子表比较。所有结果都必须在同一划分、同一标签和同一指标下解释，才能说明识别原理本身有效。

