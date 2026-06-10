# 宽泛 fallback 模型与自动路由策略

更新时间：2026-06-10

## 目的

当前主模型 `full_enhanced_fusion_xgboost` 依赖 21 个流级数值特征、`transport` 和可选 `sequence_text`。当外部输入没有完整 21 维流级特征时，继续用主模型的中位数填充会给出形式上可用、但可信度不足的结果。

因此新增一个宽泛 fallback 模型：

- 主模型：输入 21 维数值特征完整时使用
- fallback 模型：21 维数值特征缺失或不完整时使用

## 训练方式

训练脚本：

```powershell
python src\encryption_method\train_broad_fallback_model.py `
  --output-dir outputs\encryption_method\broad_fallback_v1
```

训练数据仍使用：

```text
data/unified_encryption_method_v2_all_data/multiclass_finetune.csv
```

训练时对每条训练样本构造 4 种输入场景：

- `full`：完整 21 维数值特征
- `partial_numeric`：随机缺失部分数值特征
- `no_numeric`：21 维数值特征全部缺失，保留 `transport` 和 `sequence_text`
- `transport_only`：21 维数值特征全部缺失，同时清空 `sequence_text`

模型输入维度为 62：

- 21 个数值特征标准化值
- 21 个数值特征缺失指示位
- 2 个 `transport` one-hot
- 18 个 `sequence_text` 派生统计特征

## 当前结果

输出目录：

```text
outputs/encryption_method/broad_fallback_v1
```

| 场景 | Accuracy | Macro-F1 | Weighted-F1 | Macro Recall |
| --- | ---: | ---: | ---: | ---: |
| `full` | 0.990504 | 0.850941 | 0.990654 | 0.878045 |
| `partial_numeric` | 0.961342 | 0.705741 | 0.962178 | 0.721044 |
| `no_numeric` | 0.526298 | 0.289372 | 0.513755 | 0.316867 |
| `transport_only` | 0.420074 | 0.110943 | 0.396931 | 0.159676 |

## 软件系统路由规则

软件系统现在使用 `RoutedModelPredictor`：

- 如果一条输入记录 21 个数值特征全部存在且可转换为数值：使用 `full_enhanced_fusion_xgboost`
- 如果任意一个数值特征缺失、为空或不可转换为数值：使用 `broad_fallback_xgboost`

接口输出会额外包含：

- `model_used`
- `input_profile`
- `missing_numeric_features`

这样前端和 API 调用方可以明确知道每条预测到底用了哪个模型。

## 结论

主模型仍然是论文和系统中的高精度模型。fallback 模型不是替代主模型，而是为了在输入信息不足时提供更稳妥的兜底预测。尤其是 `no_numeric` 和 `transport_only` 场景，性能明显受限，应在界面和报告中标明其可信度低于完整输入预测。
