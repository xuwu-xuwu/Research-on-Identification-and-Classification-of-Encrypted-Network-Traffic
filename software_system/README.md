# 加密方法识别软件系统

本目录把现有实验结果封装成一个完整的前后端软件系统。

## 架构

- 后端：`FastAPI`
- 前端：原生 `HTML / CSS / JavaScript` 静态页面
- 模型：当前最新 `outputs/encryption_method/full_enhanced_fusion_v1/model.joblib`
- fallback 模型：`outputs/encryption_method/broad_fallback_v1/model.joblib`
- 预处理：读取同目录 `feature_metadata.json`，复现训练阶段的特征变换
- 实时抓包：通过 `tshark` 读取网卡包字段，按五元组聚合为流后实时预测
- 默认任务：9 类加密方法识别

## 目录

- `backend/app/`：后端 API、模型加载和推理核心
- `backend/cli.py`：命令行批量预测入口
- `frontend/`：前端页面
- `examples/`：CSV 和 JSON 示例输入
- `start_backend.ps1`：Windows PowerShell 一键启动脚本
- `requirements.txt`：运行依赖

## 启动

在项目根目录执行：

```powershell
pip install -r software_system\requirements.txt
.\software_system\start_backend.ps1
```

然后打开：

```text
http://127.0.0.1:8000
```

后端管理页面：

```text
http://127.0.0.1:8000/admin
```

管理页面用于查看服务状态、主模型/fallback 路由、实时抓包状态、网卡列表、路径配置和快速预测测试。

如果 `tshark` 不在系统 `PATH` 中，可以设置环境变量。优先使用相对项目根目录的路径：

```powershell
$env:EIM_TSHARK_PATH = ".\tools\tshark.exe"
.\software_system\start_backend.ps1
```

## 自动路由预测

系统现在使用两个模型：

- 主模型 `full_enhanced_fusion_xgboost`：当 21 个数值流级特征完整时使用。
- fallback 模型 `broad_fallback_xgboost`：当任意数值特征缺失、为空或不可转换为数值时使用。

每条预测结果会返回：

- `model_used`：实际使用的模型
- `input_profile`：`complete_21_numeric` 或 `incomplete_numeric_fallback`
- `missing_numeric_features`：缺失的 21 维数值字段列表

fallback 模型的当前结果：

| 场景 | Accuracy | Macro-F1 | Weighted-F1 |
| --- | ---: | ---: | ---: |
| 完整 21 维 | 0.990504 | 0.850941 | 0.990654 |
| 随机缺失部分数值特征 | 0.961342 | 0.705741 | 0.962178 |
| 21 维数值全缺失 | 0.526298 | 0.289372 | 0.513755 |
| 仅 `transport` | 0.420074 | 0.110943 | 0.396931 |

说明：fallback 是输入不完整时的兜底模型，不替代完整输入下的主模型。

## API

健康检查：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
```

模型信息：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/model/info
```

单条或多条 JSON 预测：

```powershell
$body = Get-Content software_system\examples\sample_request.json -Raw
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/api/predict `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

CSV 批量预测：

```powershell
$csv = Get-Content software_system\examples\sample_records.csv -Raw
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/predict/csv" `
  -Method Post `
  -ContentType "text/csv; charset=utf-8" `
  -Body $csv
```

实时抓包相关 API：

```powershell
# 列出可抓取网卡
Invoke-RestMethod http://127.0.0.1:8000/api/capture/interfaces

# 开始抓取第 5 个接口，接口编号以 tshark -D 输出为准
$body = @{
  interface = "5"
  tshark_path = "tshark"
  capture_filter = "tcp or udp"
  flow_idle_timeout = 5
  emit_interval = 1
  min_packets = 3
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/api/capture/start `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

# 查看状态
Invoke-RestMethod http://127.0.0.1:8000/api/capture/status

# 拉取最新实时预测结果
Invoke-RestMethod "http://127.0.0.1:8000/api/capture/results?limit=50"

# 停止抓包
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/capture/stop -Method Post
```

## CLI

CSV 批量预测：

```powershell
python -m software_system.backend.cli `
  --input software_system\examples\sample_records.csv `
  --output outputs\software_system\sample_predictions.csv
```

混合完整/缺失输入预测：

```powershell
python -m software_system.backend.cli `
  --input software_system\examples\sample_mixed_records.csv `
  --output outputs\software_system\sample_mixed_predictions.csv
```

单条 JSON 预测：

```powershell
python -m software_system.backend.cli `
  --record-json '{"duration":12.8,"packet_count":18,"byte_count":3210,"transport":"TCP"}' `
  --include-probabilities
```

## 输入字段

推荐输入字段：

- 21 个数值特征：`duration`、`packet_count`、`fwd_packet_count`、`bwd_packet_count`、`byte_count`、`fwd_byte_count`、`bwd_byte_count`、`packets_per_second`、`bytes_per_second`、`mean_packet_len`、`std_packet_len`、`min_packet_len`、`max_packet_len`、`mean_iat`、`std_iat`、`min_iat`、`max_iat`、`direction_packet_ratio`、`direction_byte_ratio`、`avg_packet_size`、`encrypted_packet_ratio`
- `transport`：`TCP` / `UDP` / `OTHER`
- `sequence_text`：可为空；如果有包序列 token，会抽取序列统计特征

数值字段缺失时，系统会使用训练阶段保存的中位数补齐。`source_name` 不参与预测，避免数据来源泄漏。

## 实时抓包预测机制

实时功能不是逐包分类，而是流级分类：

1. 后端调用 `tshark -l -i <interface> -T fields` 实时读取包字段。
2. 按 `transport + endpoint_a + endpoint_b` 归一化五元组聚合为双向流。
3. 流空闲超过 `flow_idle_timeout` 秒，并且包数达到 `min_packets` 后封口。
4. 生成 21 个流级数值特征、`transport` 和 `sequence_text`。
5. 调用 `full_enhanced_fusion_xgboost` 输出预测类别和置信度。

注意事项：

- 需要安装 Wireshark 或单独安装 `tshark`。
- Windows 下通常需要安装 Npcap，并允许当前用户抓取网卡。
- 前端“刷新网卡”对应后端执行 `tshark -D`。
- 抓包过滤器默认为 `tcp or udp`，可以按需要改成 `host 192.168.1.10`、`port 443` 等 BPF 表达式。
- 实时预测结果取决于当前网络流量是否足够形成 flow；没有网络活动时不会产生预测行。

## 默认模型结果

默认加载的加强版模型：

- 模型目录：`outputs/encryption_method/full_enhanced_fusion_v1/`
- Accuracy：`0.993978`
- Macro-F1：`0.892797`
- Weighted-F1：`0.994046`
- Macro Recall：`0.909893`
