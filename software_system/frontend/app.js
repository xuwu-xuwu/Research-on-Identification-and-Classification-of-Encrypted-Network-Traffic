const numericFeatures = [
  "duration",
  "packet_count",
  "fwd_packet_count",
  "bwd_packet_count",
  "byte_count",
  "fwd_byte_count",
  "bwd_byte_count",
  "packets_per_second",
  "bytes_per_second",
  "mean_packet_len",
  "std_packet_len",
  "min_packet_len",
  "max_packet_len",
  "mean_iat",
  "std_iat",
  "min_iat",
  "max_iat",
  "direction_packet_ratio",
  "direction_byte_ratio",
  "avg_packet_size",
  "encrypted_packet_ratio",
];

const featureHints = {
  duration: { zh: "流持续时间", detail: "单位：秒，最后一个包时间减第一个包时间" },
  packet_count: { zh: "总包数", detail: "该双向流中的数据包总数" },
  fwd_packet_count: { zh: "前向包数", detail: "端点 A 到端点 B 的包数" },
  bwd_packet_count: { zh: "反向包数", detail: "端点 B 到端点 A 的包数" },
  byte_count: { zh: "总字节数", detail: "该双向流中的字节总量" },
  fwd_byte_count: { zh: "前向字节数", detail: "端点 A 到端点 B 的字节数" },
  bwd_byte_count: { zh: "反向字节数", detail: "端点 B 到端点 A 的字节数" },
  packets_per_second: { zh: "包速率", detail: "总包数 / 流持续时间" },
  bytes_per_second: { zh: "字节速率", detail: "总字节数 / 流持续时间" },
  mean_packet_len: { zh: "平均包长", detail: "该流数据包长度均值" },
  std_packet_len: { zh: "包长标准差", detail: "该流数据包长度波动程度" },
  min_packet_len: { zh: "最小包长", detail: "该流中最短包长度" },
  max_packet_len: { zh: "最大包长", detail: "该流中最长包长度" },
  mean_iat: { zh: "平均包间隔", detail: "相邻包到达时间间隔均值，单位：秒" },
  std_iat: { zh: "包间隔标准差", detail: "相邻包到达时间间隔波动程度" },
  min_iat: { zh: "最小包间隔", detail: "最短相邻包时间间隔，单位：秒" },
  max_iat: { zh: "最大包间隔", detail: "最长相邻包时间间隔，单位：秒" },
  direction_packet_ratio: { zh: "方向包数比", detail: "前向包数 / (反向包数 + 1)" },
  direction_byte_ratio: { zh: "方向字节比", detail: "前向字节数 / (反向字节数 + 1)" },
  avg_packet_size: { zh: "平均包大小", detail: "通常与 mean_packet_len 相同，用于兼容训练字段" },
  encrypted_packet_ratio: { zh: "加密包比例", detail: "可见协议被识别为加密的包数 / 总包数" },
};

const sampleRecord = {
  duration: 12.8,
  packet_count: 18,
  fwd_packet_count: 10,
  bwd_packet_count: 8,
  byte_count: 3210,
  fwd_byte_count: 1880,
  bwd_byte_count: 1330,
  packets_per_second: 1.406,
  bytes_per_second: 250.78,
  mean_packet_len: 178.3,
  std_packet_len: 44.1,
  min_packet_len: 66,
  max_packet_len: 420,
  mean_iat: 0.75,
  std_iat: 0.31,
  min_iat: 0,
  max_iat: 1.8,
  direction_packet_ratio: 1.25,
  direction_byte_ratio: 1.41,
  avg_packet_size: 178.3,
  encrypted_packet_ratio: 1,
  transport: "TCP",
  sequence_text: "F_LEN_0100 IAT_00000 B_LEN_0150 IAT_00120 F_LEN_0200 IAT_00240 B_LEN_0180 IAT_00300",
};

let lastCsvRows = [];
let liveTimer = null;
let liveLastId = 0;
let liveRows = [];

function formatMetric(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
  return Number(value).toFixed(6);
}

function renderNumericFields() {
  const container = document.getElementById("numericFields");
  container.innerHTML = numericFeatures
    .map((feature) => {
      const hint = featureHints[feature] || { zh: "特征参数", detail: "" };
      return `
        <label class="field">
          <span class="feature-name">${feature}</span>
          <small>${hint.zh}${hint.detail ? `：${hint.detail}` : ""}</small>
          <input name="${feature}" type="number" step="any" placeholder="可留空" />
        </label>
      `;
    })
    .join("");
}

async function loadModelInfo() {
  const dot = document.getElementById("statusDot");
  const statusText = document.getElementById("statusText");
  const modelName = document.getElementById("modelName");
  try {
    const response = await fetch("/api/model/info");
    if (!response.ok) throw new Error(await response.text());
    const info = await response.json();
    dot.classList.add("ok");
    statusText.textContent = "后端已连接";
    const fallbackText = info.routing?.fallback_available ? "fallback 已启用" : "fallback 未启用";
    modelName.textContent = `${info.model_name}，${fallbackText}`;
    const metricGrid = document.getElementById("metricGrid");
    const metrics = info.metrics || {};
    metricGrid.innerHTML = [
      ["Accuracy", metrics.accuracy],
      ["Macro-F1", metrics.f1_macro],
      ["Weighted-F1", metrics.f1_weighted],
      ["Macro Recall", metrics.macro_recall],
    ]
      .map(([label, value]) => `<article><span>${label}</span><strong>${formatMetric(value)}</strong></article>`)
      .join("");
  } catch (error) {
    dot.classList.add("fail");
    statusText.textContent = "后端连接失败";
    modelName.textContent = error.message;
  }
}

async function refreshInterfaces() {
  const select = document.getElementById("interfaceSelect");
  const message = document.getElementById("captureMessage");
  const tsharkPath = encodeURIComponent(document.getElementById("tsharkPathInput").value || "auto");
  select.innerHTML = `<option value="">正在读取网卡...</option>`;
  try {
    const response = await fetch(`/api/capture/interfaces?tshark_path=${tsharkPath}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "读取网卡失败");
    if (!data.interfaces.length) {
      select.innerHTML = `<option value="">没有发现网卡</option>`;
      return;
    }
    select.innerHTML = data.interfaces
      .map((item) => `<option value="${item.id}">${item.raw}</option>`)
      .join("");
    message.textContent = "网卡列表已刷新。选择接口后点击开始实时预测。";
  } catch (error) {
    select.innerHTML = `<option value="">读取失败</option>`;
    message.textContent = `读取网卡失败：${error.message}`;
  }
}

function liveRequestBody() {
  return {
    interface: document.getElementById("interfaceSelect").value,
    tshark_path: document.getElementById("tsharkPathInput").value || "auto",
    capture_filter: document.getElementById("captureFilterInput").value || "tcp or udp",
    flow_idle_timeout: Number(document.getElementById("flowIdleInput").value || 5),
    min_packets: Number(document.getElementById("minPacketsInput").value || 3),
    emit_interval: Number(document.getElementById("emitIntervalInput").value || 1),
    include_probabilities: document.getElementById("liveProbabilities").checked,
  };
}

async function startCapture() {
  const body = liveRequestBody();
  if (!body.interface) {
    alert("请先选择网卡接口。");
    return;
  }
  try {
    const response = await fetch("/api/capture/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "启动失败");
    liveRows = [];
    liveLastId = 0;
    renderLiveTable();
    updateLiveStatus(data);
    startLivePolling();
  } catch (error) {
    document.getElementById("captureMessage").textContent = `启动失败：${error.message}`;
    document.getElementById("liveState").className = "live-pill error";
    document.getElementById("liveState").textContent = "启动失败";
  }
}

async function stopCapture() {
  try {
    const response = await fetch("/api/capture/stop", { method: "POST" });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "停止失败");
    updateLiveStatus(data);
  } catch (error) {
    document.getElementById("captureMessage").textContent = `停止失败：${error.message}`;
  } finally {
    stopLivePolling();
    await pollLiveOnce();
  }
}

function startLivePolling() {
  stopLivePolling();
  liveTimer = window.setInterval(pollLiveOnce, 1200);
  pollLiveOnce();
}

function stopLivePolling() {
  if (liveTimer) {
    window.clearInterval(liveTimer);
    liveTimer = null;
  }
}

async function pollLiveOnce() {
  try {
    const [statusResponse, resultResponse] = await Promise.all([
      fetch("/api/capture/status"),
      fetch(`/api/capture/results?limit=100&since_id=${liveLastId}`),
    ]);
    const status = await statusResponse.json();
    const resultData = await resultResponse.json();
    if (statusResponse.ok) updateLiveStatus(status);
    if (resultResponse.ok && resultData.results.length) {
      liveRows = liveRows.concat(resultData.results).slice(-200);
      liveLastId = Math.max(...liveRows.map((row) => Number(row.id || 0)));
      renderLiveTable();
    }
  } catch (error) {
    document.getElementById("captureMessage").textContent = `实时状态更新失败：${error.message}`;
  }
}

function updateLiveStatus(status) {
  const state = document.getElementById("liveState");
  const startBtn = document.getElementById("startCaptureBtn");
  const stopBtn = document.getElementById("stopCaptureBtn");
  const message = document.getElementById("captureMessage");
  state.className = status.running ? "live-pill running" : "live-pill";
  state.textContent = status.running ? "运行中" : "未启动";
  startBtn.disabled = Boolean(status.running);
  stopBtn.disabled = !status.running;
  if (status.last_error) {
    state.className = "live-pill error";
    message.textContent = `tshark/实时预测提示：${status.last_error}`;
  } else if (status.running) {
    message.textContent = `正在监听接口 ${status.interface}，流空闲后会自动输出预测。`;
  } else {
    message.textContent = "实时抓取未启动。";
  }
  document.getElementById("liveStats").innerHTML = [
    ["已处理包", status.packets_seen || 0],
    ["活跃流", status.active_flows || 0],
    ["预测流", status.results_total || 0],
    ["运行秒数", Math.round(status.uptime_seconds || 0)],
  ]
    .map(([label, value]) => `<article><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
}

function renderLiveTable() {
  const table = document.getElementById("liveTable");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");
  if (!liveRows.length) {
    thead.innerHTML = "";
    tbody.innerHTML = `<tr><td>暂无实时预测结果。产生网络流量并等待流空闲封口后会显示。</td></tr>`;
    return;
  }
  const keys = [
    "id",
    "predicted_label",
    "confidence",
    "model_used",
    "input_profile",
    "observed_protocol_label",
    "transport",
    "flow_key",
    "packet_count",
    "byte_count",
    "duration",
    "created_at",
  ];
  thead.innerHTML = `<tr>${keys.map((key) => `<th>${key}</th>`).join("")}</tr>`;
  tbody.innerHTML = liveRows
    .slice()
    .reverse()
    .map(
      (row) => `
        <tr>
          ${keys
            .map((key) => {
              let value = row[key] ?? "";
              if (key === "confidence" || key === "duration") value = formatMetric(value);
              if (key === "created_at" && value) value = new Date(value * 1000).toLocaleTimeString();
              return `<td>${value}</td>`;
            })
            .join("")}
        </tr>
      `,
    )
    .join("");
}

function fillSample() {
  document.getElementById("transportInput").value = sampleRecord.transport;
  document.getElementById("sequenceInput").value = sampleRecord.sequence_text;
  for (const feature of numericFeatures) {
    const input = document.querySelector(`[name="${feature}"]`);
    if (input) input.value = sampleRecord[feature];
  }
}

function collectSingleRecord() {
  const record = {
    transport: document.getElementById("transportInput").value,
    sequence_text: document.getElementById("sequenceInput").value,
  };
  for (const feature of numericFeatures) {
    const input = document.querySelector(`[name="${feature}"]`);
    record[feature] = input && input.value !== "" ? Number(input.value) : null;
  }
  return record;
}

async function submitSingle(event) {
  event.preventDefault();
  const includeProbabilities = document.getElementById("includeProbabilities").checked;
  const result = document.getElementById("singleResult");
  result.textContent = "预测中...";
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        records: [collectSingleRecord()],
        include_probabilities: includeProbabilities,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "预测失败");
    const prediction = data.predictions[0];
    const probs = prediction.probabilities
      ? `<pre>${JSON.stringify(prediction.probabilities, null, 2)}</pre>`
      : "";
    const missing = prediction.missing_numeric_features?.length
      ? `<p>缺失数值特征：${prediction.missing_numeric_features.join(", ")}</p>`
      : "";
    result.innerHTML = `
      <span>预测类别</span><br />
      <strong>${prediction.predicted_label}</strong>
      <p>置信度：${formatMetric(prediction.confidence)}</p>
      <p>使用模型：${prediction.model_used || data.model_name}</p>
      <p>输入类型：${prediction.input_profile || "unknown"}</p>
      ${missing}
      ${probs}
    `;
  } catch (error) {
    result.textContent = `预测失败：${error.message}`;
  }
}

async function predictCsv() {
  const fileInput = document.getElementById("csvFile");
  if (!fileInput.files.length) {
    alert("请先选择 CSV 文件。");
    return;
  }
  const text = await fileInput.files[0].text();
  const response = await fetch("/api/predict/csv?include_probabilities=false", {
    method: "POST",
    headers: { "Content-Type": "text/csv; charset=utf-8" },
    body: text,
  });
  const data = await response.json();
  if (!response.ok) {
    alert(`批量预测失败：${data.detail || "未知错误"}`);
    return;
  }
  lastCsvRows = data.predictions;
  renderTable(lastCsvRows);
  document.getElementById("downloadCsvBtn").disabled = lastCsvRows.length === 0;
  document.getElementById("resultCount").textContent = `${lastCsvRows.length} 条结果`;
}

function renderTable(rows) {
  const table = document.getElementById("resultTable");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");
  if (!rows.length) {
    thead.innerHTML = "";
    tbody.innerHTML = "";
    return;
  }
  const keys = Object.keys(rows[0]).slice(0, 12);
  if (!keys.includes("predicted_label")) keys.push("predicted_label");
  if (!keys.includes("confidence")) keys.push("confidence");
  if (!keys.includes("model_used")) keys.push("model_used");
  if (!keys.includes("input_profile")) keys.push("input_profile");
  if (!keys.includes("missing_numeric_features")) keys.push("missing_numeric_features");
  thead.innerHTML = `<tr>${keys.map((key) => `<th>${key}</th>`).join("")}</tr>`;
  tbody.innerHTML = rows
    .slice(0, 100)
    .map(
      (row) => `
        <tr>
          ${keys.map((key) => `<td>${row[key] ?? ""}</td>`).join("")}
        </tr>
      `,
    )
    .join("");
}

function downloadCsv() {
  if (!lastCsvRows.length) return;
  const keys = Object.keys(lastCsvRows[0]);
  const escapeCell = (value) => {
    const text = String(value ?? "");
    if (/[",\n]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
    return text;
  };
  const csv = [keys.join(",")]
    .concat(lastCsvRows.map((row) => keys.map((key) => escapeCell(row[key])).join(",")))
    .join("\n");
  const blob = new Blob(["\ufeff", csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "encryption_method_predictions.csv";
  link.click();
  URL.revokeObjectURL(url);
}

document.addEventListener("DOMContentLoaded", () => {
  renderNumericFields();
  renderLiveTable();
  loadModelInfo();
  refreshInterfaces();
  document.getElementById("fillSampleBtn").addEventListener("click", fillSample);
  document.getElementById("singleForm").addEventListener("submit", submitSingle);
  document.getElementById("predictCsvBtn").addEventListener("click", predictCsv);
  document.getElementById("downloadCsvBtn").addEventListener("click", downloadCsv);
  document.getElementById("refreshInterfacesBtn").addEventListener("click", refreshInterfaces);
  document.getElementById("startCaptureBtn").addEventListener("click", startCapture);
  document.getElementById("stopCaptureBtn").addEventListener("click", stopCapture);
});
