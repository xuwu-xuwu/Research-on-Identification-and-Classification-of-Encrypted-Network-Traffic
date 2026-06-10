let adminSummary = null;

function adminMetric(value) {
  if (value === null || value === undefined) return "-";
  if (typeof value === "number") return Number(value).toFixed(6);
  return String(value);
}

function shortStatus(value) {
  return value ? "ON" : "OFF";
}

async function loadAdminSummary() {
  const dot = document.getElementById("adminStatusDot");
  const text = document.getElementById("adminStatusText");
  const sub = document.getElementById("adminStatusSub");
  try {
    const response = await fetch("/api/admin/summary");
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "管理接口读取失败");
    adminSummary = data;
    dot.className = "status-dot ok";
    text.textContent = "后端运行正常";
    sub.textContent = `${data.service.title} v${data.service.version}`;
    renderSummary(data);
  } catch (error) {
    dot.className = "status-dot fail";
    text.textContent = "后端状态读取失败";
    sub.textContent = error.message;
  }
}

function renderSummary(data) {
  const routing = data.model.routing || {};
  document.getElementById("adminMetricGrid").innerHTML = [
    ["Model Loaded", shortStatus(data.service.model_loaded)],
    ["Fallback", shortStatus(routing.fallback_available)],
    ["Capture", data.capture.running ? "RUN" : "STOP"],
    ["Labels", data.model.labels.length],
  ]
    .map(([label, value]) => `<article><span>${label}</span><strong>${value}</strong></article>`)
    .join("");

  document.getElementById("routeModelName").textContent = data.model.model_name || "-";
  document.getElementById("primaryModelName").textContent = routing.primary_model || "-";
  document.getElementById("fallbackModelName").textContent = routing.fallback_model || "-";
  document.getElementById("routingPolicy").textContent = routing.policy || "-";

  renderMetricTable(data);
  renderKeyValue("pathList", data.paths);
  renderKeyValue("limitList", { ...data.limits, tshark_path: data.runtime.tshark_path });
  renderCaptureStatus(data.capture);
}

function renderMetricTable(data) {
  const table = document.getElementById("metricTable");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");
  const routing = data.model.routing || {};
  const fallback = routing.fallback_metrics || {};
  const rows = [
    { model: "主模型", accuracy: data.model.metrics.accuracy, macro_f1: data.model.metrics.f1_macro, weighted_f1: data.model.metrics.f1_weighted, macro_recall: data.model.metrics.macro_recall },
    { model: "Fallback", accuracy: fallback.accuracy, macro_f1: fallback.f1_macro, weighted_f1: fallback.f1_weighted, macro_recall: fallback.macro_recall },
  ];
  const keys = ["model", "accuracy", "macro_f1", "weighted_f1", "macro_recall"];
  thead.innerHTML = `<tr>${keys.map((key) => `<th>${key}</th>`).join("")}</tr>`;
  tbody.innerHTML = rows
    .map((row) => `<tr>${keys.map((key) => `<td>${adminMetric(row[key])}</td>`).join("")}</tr>`)
    .join("");
}

function renderKeyValue(containerId, values) {
  const container = document.getElementById(containerId);
  container.innerHTML = Object.entries(values)
    .map(
      ([key, value]) => `
        <div class="kv-row">
          <span>${key}</span>
          <strong>${value}</strong>
        </div>
      `,
    )
    .join("");
}

function renderCaptureStatus(status) {
  document.getElementById("adminCaptureStats").innerHTML = [
    ["运行状态", status.running ? "运行中" : "未启动"],
    ["已处理包", status.packets_seen || 0],
    ["活跃流", status.active_flows || 0],
    ["预测结果", status.results_total || 0],
  ]
    .map(([label, value]) => `<article><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
  const message = status.last_error
    ? `错误：${status.last_error}`
    : status.running
      ? `正在监听接口 ${status.interface}，运行 ${Math.round(status.uptime_seconds || 0)} 秒。`
      : "实时抓包未启动。";
  document.getElementById("adminCaptureMessage").textContent = message;
}

async function refreshInterfaces() {
  const table = document.getElementById("interfaceTable");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");
  thead.innerHTML = "<tr><th>id</th><th>name</th><th>raw</th></tr>";
  tbody.innerHTML = "<tr><td colspan='3'>正在读取网卡...</td></tr>";
  try {
    const response = await fetch("/api/capture/interfaces");
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "读取网卡失败");
    tbody.innerHTML = data.interfaces
      .map((item) => `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.raw}</td></tr>`)
      .join("");
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan='3'>${error.message}</td></tr>`;
  }
}

async function stopCapture() {
  const response = await fetch("/api/capture/stop", { method: "POST" });
  const data = await response.json();
  if (!response.ok) {
    alert(data.detail || "停止抓包失败");
    return;
  }
  renderCaptureStatus(data);
  await loadAdminSummary();
}

async function quickPredict() {
  const result = document.getElementById("quickPredictResult");
  result.textContent = "测试中...";
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        records: [{ transport: "TCP", sequence_text: "" }],
        include_probabilities: false,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "预测测试失败");
    const prediction = data.predictions[0];
    result.innerHTML = `
      <span>预测类别</span><br />
      <strong>${prediction.predicted_label}</strong>
      <p>置信度：${adminMetric(prediction.confidence)}</p>
      <p>使用模型：${prediction.model_used}</p>
      <p>输入类型：${prediction.input_profile}</p>
      <p>缺失字段数：${prediction.missing_numeric_features?.length ?? 0}</p>
    `;
  } catch (error) {
    result.textContent = error.message;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadAdminSummary();
  refreshInterfaces();
  document.getElementById("refreshAdminBtn").addEventListener("click", loadAdminSummary);
  document.getElementById("adminRefreshInterfacesBtn").addEventListener("click", refreshInterfaces);
  document.getElementById("adminStopCaptureBtn").addEventListener("click", stopCapture);
  document.getElementById("quickPredictBtn").addEventListener("click", quickPredict);
});
