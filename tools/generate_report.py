#!/usr/bin/env python3
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TEXTS = {
    "en": {
        "lang": "en",
        "title": "PHP Benchmark Report",
        "meta_generated": "Generated",
        "meta_source": "Source",
        "formulas_title": "Formulas",
        "formula_throughput": "Throughput: $R = \\frac{N}{T}$, where $N$ is total requests and $T$ is test duration.",
        "formula_percentile": "Percentile latency: $P_{90}$ means 90% of requests complete in $\\le P_{90}$.",
        "formula_delta": "Throughput delta: $\\Delta\\% = \\frac{R_{xampp} - R_{nginx}}{R_{nginx}} \\times 100\\%$.",
        "chart_requests": "Requests/sec by Endpoint",
        "desc_requests": "Shows throughput per endpoint across two systems. Compare XAMPP (constrained) and NGINX-Multi (unlimited cores) to see throughput differences.",
        "chart_latency": "Latency (ms) by Endpoint",
        "desc_latency": "Shows average response time across both systems. Lower bars are better. NGINX-Multi demonstrates multi-core potential; XAMPP is single-process control.",
        "chart_transfer": "Transfer (KB/sec) by Endpoint",
        "desc_transfer": "Shows output bandwidth per endpoint. Higher bars indicate more data served per second, useful for payload-heavy endpoints.",
        "chart_pctl": "Latency Percentiles (ms)",
        "desc_pctl": "Shows tail latency across both systems. Use P90 and P99 to understand worst-case behavior; lower values mean fewer slow requests.",
        "pctl_missing": "Percentile data is missing. Re-run the benchmark with latency percentiles enabled.",
        "chart_dist": "Requests/sec Distribution",
        "desc_dist": "Shows the spread of throughput across endpoints and systems. The violin width indicates density; compare central tendency between servers.",
        "chart_delta": "Throughput Comparison",
        "desc_delta": "Two system comparison: XAMPP (orange) and NGINX Multi-core (blue). Compare performance across all test endpoints.",
        "insights_title": "Insights",
        "interpretation_title": "Interpretation",
        "raw_title": "Raw Results",
        "th_timestamp": "Timestamp",
        "th_server": "Server",
        "th_endpoint": "Endpoint",
        "th_req": "Req/sec",
        "th_latency": "Latency",
        "th_p50": "P50",
        "th_p90": "P90",
        "th_p99": "P99",
        "th_transfer": "Transfer/sec",
        "th_winner_throughput": "Throughput Winner",
        "th_delta": "Delta (%)",
        "th_winner_latency": "Latency Winner",
        "th_latency_delta": "Latency Delta (%)",
        "delta_yaxis": "Delta % (XAMPP vs NGINX Multi)",
        "no_pctl_chart": "No percentile series available.",
        "interp_intro": "Use throughput and latency together to avoid a misleading single-metric conclusion.",
        "interp_compare": "Throughput favors {req_winner}; latency favors {lat_winner}.",
        "interp_tradeoff": "If your workload is batch or high concurrency, pick the throughput winner. If it is interactive, pick the latency winner.",
        "interp_consistent": "Both key metrics favor {winner}; it is the safer default for this workload.",
        "interp_tail": "High P99 indicates some requests will be significantly slower. If your application prioritizes response time (e.g., API or frontend services), consider choosing a setup with lower tail latency.",
        "interp_p99_missing": "P99 is missing; rerun benchmark with latency percentiles to validate tail behavior.",
        "endpoints_title": "Benchmark Endpoints & Methodology",
        "endpoints_intro": "This benchmark uses three carefully selected PHP endpoints to simulate real-world application scenarios. Each endpoint exercises different server capabilities to provide a comprehensive performance assessment.",
        "endpoint_cpu_title": "CPU Endpoint: Computational Workload",
        "endpoint_cpu_desc": "Purpose: Measures pure computational throughput and CPU efficiency. This endpoint performs intensive mathematical calculations without I/O operations. Use case: Suitable for applications with heavy data processing, analytics, or algorithmic computation (e.g., image processing, encryption, scientific computing). Metric insight: Reveals how well each server architecture handles CPU-bound tasks and optimization.",
        "endpoint_io_title": "I/O Endpoint: Disk/Database Operations",
        "endpoint_io_desc": "Purpose: Simulates real-world I/O patterns including file reads, database queries, and network requests. This endpoint introduces latency variability from external systems. Use case: Typical for web applications that interact with databases, file systems, or external APIs (e.g., content management systems, user authentication, data retrieval). Metric insight: Demonstrates server behavior under I/O wait conditions and how efficiently requests are queued and processed.",
        "endpoint_json_title": "JSON Endpoint: Data Serialization & Transfer",
        "endpoint_json_desc": "Purpose: Tests JSON encoding/decoding performance and payload handling—a common operation in modern REST APIs and AJAX applications. This endpoint balances CPU work with memory operations. Use case: Reflects modern web service patterns where responses are serialized to JSON (e.g., REST APIs, real-time data feeds, SPA backends). Metric insight: Indicates how efficiently the server can generate dynamic content and handle medium-to-large payloads.",
        "theme_label": "Theme:",
    },
    "zh": {
        "lang": "zh-Hant",
        "title": "PHP 壓測報告",
        "meta_generated": "產生時間",
        "meta_source": "來源",
        "formulas_title": "公式",
        "formula_throughput": "吞吐量：$R = \\frac{N}{T}$，其中 $N$ 為總請求數，$T$ 為測試時間。",
        "formula_percentile": "延遲分位數：$P_{90}$ 表示 90% 的請求在 $\\le P_{90}$ 內完成。",
        "formula_delta": "吞吐差異：$\\Delta\\% = \\frac{R_{xampp} - R_{nginx}}{R_{nginx}} \\times 100\\%$。",
        "chart_requests": "每端點 Requests/sec",
        "desc_requests": "顯示各端點的吞吐量。透過兩個系統比較：XAMPP（受限）、NGINX-Multi（無限核心）來看吞吐量差異。",
        "chart_latency": "每端點延遲 (ms)",
        "desc_latency": "顯示平均回應時間，越低越好。NGINX-Multi 展示多核潛力；XAMPP 為單進程控制。",
        "chart_transfer": "每端點傳輸量 (KB/sec)",
        "desc_transfer": "顯示每秒傳輸量，回應較大的端點會更高。",
        "chart_pctl": "延遲分位數 (ms)",
        "desc_pctl": "顯示兩個系統的尾端延遲；P90/P99 可觀察最慢請求的風險，越低越好。",
        "pctl_missing": "缺少分位數資料，請重新跑壓測以啟用延遲分位數模式。",
        "chart_dist": "Requests/sec 分佈",
        "desc_dist": "顯示各系統吞吐量分佈，寬度代表密度；可比較三者穩定性。",
        "chart_delta": "吞吐量對比",
        "desc_delta": "兩系統對比：XAMPP（橘）、NGINX 多核（藍）。比較各端點效能差異。",
        "insights_title": "重點整理",
        "interpretation_title": "解讀建議",
        "raw_title": "原始結果",
        "th_timestamp": "時間",
        "th_server": "服務",
        "th_endpoint": "端點",
        "th_req": "Req/sec",
        "th_latency": "延遲",
        "th_p50": "P50",
        "th_p90": "P90",
        "th_p99": "P99",
        "th_transfer": "傳輸量/sec",
        "th_winner_throughput": "吞吐勝出",
        "th_delta": "差異 (%)",
        "th_winner_latency": "延遲勝出",
        "th_latency_delta": "延遲差異 (%)",
        "delta_yaxis": "差異 % (XAMPP 相對 NGINX)",
        "no_pctl_chart": "沒有分位數資料。",
        "interp_intro": "建議同時看吞吐與延遲，避免只用單一指標做判斷。",
        "interp_compare": "吞吐偏向 {req_winner}；延遲偏向 {lat_winner}。",
        "interp_tradeoff": "若是批次或高併發工作，偏向吞吐勝出；若是互動型工作，偏向延遲勝出。",
        "interp_consistent": "兩項指標都偏向 {winner}，可作為此工作負載的優先選擇。",
        "interp_tail": "P99 明顯偏高，代表部分請求的延遲會特別久。若你的應用對響應速度要求高（如API/前端服務），應選擇尾端延遲更低的方案。",
        "interp_p99_missing": "缺少 P99，請重新跑壓測以確認尾端延遲。",
        "endpoints_title": "壓測端點與設計方法",
        "endpoints_intro": "本壓測使用三個精心選擇的 PHP 端點來模擬真實應用場景。每個端點各自對伺服器的不同能力進行壓力測試，以提供全面的效能評估。",
        "endpoint_cpu_title": "CPU 端點：運算密集型工作",
        "endpoint_cpu_desc": "用途：測量純運算吞吐量與 CPU 效率。此端點執行密集的數學計算，不涉及 I/O 操作。應用場景：適用於數據處理、分析或演算法運算型應用（例如影像處理、加密、科學計算）。指標意義：揭示各伺服器架構在 CPU 密集任務與最佳化上的表現。",
        "endpoint_io_title": "I/O 端點：磁碟與資料庫操作",
        "endpoint_io_desc": "用途：模擬真實的 I/O 模式，包括檔案讀取、資料庫查詢與網路請求。此端點引入來自外部系統的延遲變異性。應用場景：典型的網路應用會與資料庫、檔案系統或外部 API 互動（例如內容管理系統、使用者認證、資料檢索）。指標意義：展示伺服器在 I/O 等待條件下的行為，以及請求佇列與處理的效率。",
        "endpoint_json_title": "JSON 端點：資料序列化與傳輸",
        "endpoint_json_desc": "用途：測試 JSON 編碼/解碼效能與 payload 處理—這是現代 REST API 與 AJAX 應用的常見操作。此端點平衡了 CPU 工作與記憶體操作。應用場景：反映現代網路服務的典型模式，其中回應被序列化為 JSON（例如 REST API、即時數據饋送、SPA 後端）。指標意義：指示伺服器産生動態內容與處理中等到大型 payload 的效率。",
        "theme_label": "佈景主題:",
    }
}
def load_csv(csv_path: Path):
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def parse_latency_ms(value: str) -> float:
    if value.endswith("us"):
        return float(value[:-2]) / 1000.0
    if value.endswith("ms"):
        return float(value[:-2])
    if value.endswith("s"):
        return float(value[:-1]) * 1000.0
    return float(value)


def parse_transfer_kb(value: str) -> float:
    if value.endswith("MB"):
        return float(value[:-2]) * 1024.0
    if value.endswith("KB"):
        return float(value[:-2])
    if value.endswith("B"):
        return float(value[:-1]) / 1024.0
    return float(value)


def normalize_rows(rows):
    utc_plus_8 = timezone(timedelta(hours=8))
    normalized = []
    for row in rows:
        p50 = row.get("latency_p50", "")
        p75 = row.get("latency_p75", "")
        p90 = row.get("latency_p90", "")
        p99 = row.get("latency_p99", "")
        
        # Convert timestamp to UTC+8 format
        timestamp_str = row["timestamp"]
        try:
            if timestamp_str.endswith("Z"):
                dt_utc = datetime.fromisoformat(timestamp_str[:-1] + "+00:00")
            else:
                dt_utc = datetime.fromisoformat(timestamp_str)
            dt_plus8 = dt_utc.astimezone(utc_plus_8)
            timestamp_display = dt_plus8.strftime("%Y-%m-%d %H:%M:%S")
        except:
            timestamp_display = timestamp_str
        
        normalized.append(
            {
                "timestamp": timestamp_display,
                "server": row["server"],
                "endpoint": row["endpoint"],
                "requests_sec": float(row["requests_sec"]),
                "latency_ms": parse_latency_ms(row["latency_avg"]),
                "latency_p50_ms": parse_latency_ms(p50) if p50 else None,
                "latency_p75_ms": parse_latency_ms(p75) if p75 else None,
                "latency_p90_ms": parse_latency_ms(p90) if p90 else None,
                "latency_p99_ms": parse_latency_ms(p99) if p99 else None,
                "transfer_kb_sec": parse_transfer_kb(row["transfer_sec"]),
                "latency_avg": row["latency_avg"],
                "latency_p50": p50,
                "latency_p75": p75,
                "latency_p90": p90,
                "latency_p99": p99,
                "transfer_sec": row["transfer_sec"],
            }
        )
    return normalized


def to_plot_data(rows):
    by_endpoint = defaultdict(list)
    for row in rows:
        by_endpoint[row["endpoint"]].append(row)

    endpoints = sorted(by_endpoint.keys())
    labels = [e.replace(".php", "") for e in endpoints]

    charts = {
        "requests_sec": {"labels": [], "xampp": [], "nginx_multi": []},
        "latency_ms": {"labels": [], "xampp": [], "nginx_multi": []},
        "transfer_kb_sec": {"labels": [], "xampp": [], "nginx_multi": []},
        "latency_pctl": {
            "labels": [],
            "xampp": {"p50": [], "p75": [], "p90": [], "p99": []},
            "nginx_multi": {"p50": [], "p75": [], "p90": [], "p99": []},
        },
        "throughput_delta_pct": {"labels": [], "values": []},
    }

    for endpoint, label in zip(endpoints, labels):
        x = next((r for r in by_endpoint[endpoint] if r["server"] == "xampp"), None)
        nm = next((r for r in by_endpoint[endpoint] if r["server"] == "nginx_multi"), None)

        charts["requests_sec"]["labels"].append(label)
        charts["requests_sec"]["xampp"].append(x["requests_sec"] if x else None)
        charts["requests_sec"]["nginx_multi"].append(nm["requests_sec"] if nm else None)

        charts["latency_ms"]["labels"].append(label)
        charts["latency_ms"]["xampp"].append(x["latency_ms"] if x else None)
        charts["latency_ms"]["nginx_multi"].append(nm["latency_ms"] if nm else None)

        charts["transfer_kb_sec"]["labels"].append(label)
        charts["transfer_kb_sec"]["xampp"].append(x["transfer_kb_sec"] if x else None)
        charts["transfer_kb_sec"]["nginx_multi"].append(nm["transfer_kb_sec"] if nm else None)

        charts["latency_pctl"]["labels"].append(label)
        if x:
            charts["latency_pctl"]["xampp"]["p50"].append(x["latency_p50_ms"])
            charts["latency_pctl"]["xampp"]["p75"].append(x["latency_p75_ms"])
            charts["latency_pctl"]["xampp"]["p90"].append(x["latency_p90_ms"])
            charts["latency_pctl"]["xampp"]["p99"].append(x["latency_p99_ms"])
        if nm:
            charts["latency_pctl"]["nginx_multi"]["p50"].append(nm["latency_p50_ms"])
            charts["latency_pctl"]["nginx_multi"]["p75"].append(nm["latency_p75_ms"])
            charts["latency_pctl"]["nginx_multi"]["p90"].append(nm["latency_p90_ms"])
            charts["latency_pctl"]["nginx_multi"]["p99"].append(nm["latency_p99_ms"])

        delta = None
        if nm and nm["requests_sec"] > 0:
            delta = (x["requests_sec"] - nm["requests_sec"]) / nm["requests_sec"] * 100.0 if x else None
        charts["throughput_delta_pct"]["labels"].append(label)
        charts["throughput_delta_pct"]["values"].append(delta)

    return charts, endpoints


def histogram_data(rows, key):
    return {
        "xampp": [r[key] for r in rows if r["server"] == "xampp"],
        "nginx_multi": [r[key] for r in rows if r["server"] == "nginx_multi"],
    }


def build_insights(rows, endpoints):
    by_endpoint = defaultdict(list)
    for row in rows:
        by_endpoint[row["endpoint"]].append(row)

    insights = []
    for endpoint in endpoints:
        x = next((r for r in by_endpoint[endpoint] if r["server"] == "xampp"), None)
        nm = next((r for r in by_endpoint[endpoint] if r["server"] == "nginx_multi"), None)

        # Find throughput winner among available systems
        req_values = {}
        if x: req_values["xampp"] = x["requests_sec"]
        if nm: req_values["nginx_multi"] = nm["requests_sec"]
        req_winner = max(req_values, key=req_values.get) if req_values else "N/A"

        # Find latency winner among available systems
        lat_values = {}
        if x: lat_values["xampp"] = x["latency_ms"]
        if nm: lat_values["nginx_multi"] = nm["latency_ms"]
        lat_winner = min(lat_values, key=lat_values.get) if lat_values else "N/A"

        req_delta = 0.0
        if nm and nm["requests_sec"] > 0 and x:
            req_delta = (x["requests_sec"] - nm["requests_sec"]) / nm["requests_sec"] * 100.0

        lat_delta = 0.0
        if nm and nm["latency_ms"] > 0 and x:
            lat_delta = (x["latency_ms"] - nm["latency_ms"]) / nm["latency_ms"] * 100.0

        insights.append(
            {
                "endpoint": endpoint,
                "req_winner": req_winner,
                "req_delta": req_delta,
                "lat_winner": lat_winner,
                "lat_delta": lat_delta,
            }
        )

    return insights


def build_interpretations(rows, endpoints, lang_key):
    t = TEXTS[lang_key]
    by_endpoint = defaultdict(list)
    for row in rows:
        by_endpoint[row["endpoint"]].append(row)

    notes = []
    for endpoint in endpoints:
        label = endpoint.replace(".php", "")
        x = next((r for r in by_endpoint[endpoint] if r["server"] == "xampp"), None)
        nm = next((r for r in by_endpoint[endpoint] if r["server"] == "nginx_multi"), None)

        # Find throughput winner
        req_values = {}
        if x: req_values["XAMPP"] = x["requests_sec"]
        if nm: req_values["NGINX (Multi-core)"] = nm["requests_sec"]
        req_winner = max(req_values, key=req_values.get) if req_values else "N/A"

        # Find latency winner
        lat_values = {}
        if x: lat_values["XAMPP"] = x["latency_ms"]
        if nm: lat_values["NGINX (Multi-core)"] = nm["latency_ms"]
        lat_winner = min(lat_values, key=lat_values.get) if lat_values else "N/A"

        parts = []
        parts.append(t["interp_compare"].format(req_winner=req_winner, lat_winner=lat_winner))

        if req_winner != lat_winner:
            parts.append(t["interp_tradeoff"])
        else:
            parts.append(t["interp_consistent"].format(winner=req_winner))

        p99_values = []
        if x and x["latency_p99_ms"] is not None: p99_values.append(x["latency_p99_ms"])
        if nm and nm["latency_p99_ms"] is not None: p99_values.append(nm["latency_p99_ms"])
        
        if p99_values:
            p99_max = max(p99_values)
            if p99_max >= 1000.0:
                parts.append(t["interp_tail"])
        else:
            parts.append(t["interp_p99_missing"])

        notes.append({"endpoint": label, "text": " ".join(parts)})

    return notes


def has_percentiles(rows):
    for row in rows:
        if row.get("latency_p50_ms") is not None:
            return True
        if row.get("latency_p75_ms") is not None:
            return True
        if row.get("latency_p90_ms") is not None:
            return True
        if row.get("latency_p99_ms") is not None:
            return True
    return False


def csv_has_percentiles(csv_path: Path) -> bool:
    try:
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, [])
        return "latency_p50" in header and "latency_p99" in header
    except OSError:
        return False


def find_latest_results_csv():
    if not RESULTS_DIR.exists():
        return None
    candidates = sorted((p for p in RESULTS_DIR.glob("*/results.csv") if p.is_file()), reverse=True)
    if not candidates:
        return None

    with_percentiles = [p for p in candidates if csv_has_percentiles(p)]
    return with_percentiles[0] if with_percentiles else candidates[0]


def generate_html(rows, csv_path: Path, output_path: Path):
    charts, endpoints = to_plot_data(rows)
    hist_requests = histogram_data(rows, "requests_sec")
    insights = build_insights(rows, endpoints)
    interpretations = {
        "en": build_interpretations(rows, endpoints, "en"),
        "zh": build_interpretations(rows, endpoints, "zh"),
    }
    pctl_available = has_percentiles(rows)

    utc_plus_8 = timezone(timedelta(hours=8))
    generated_at_local = datetime.now(timezone.utc).astimezone(utc_plus_8)
    generated_at_str = generated_at_local.strftime("%Y-%m-%d %H:%M:%S")
    source_name = f"results/{csv_path.parent.name}/results.csv"

    payload = {
        "meta": {
            "generated_at": generated_at_str,
            "source": source_name,
        },
        "endpoints": endpoints,
        "charts": charts,
        "hist_requests": hist_requests,
        "insights": insights,
        "interpretations": interpretations,
        "has_pctl": pctl_available,
        "rows": rows,
    }

    html = f"""<!DOCTYPE html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>PHP Benchmark Report</title>
  <script src=\"https://cdn.plot.ly/plotly-2.27.0.min.js\"></script>
  <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css\">
  <script defer src=\"https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js\"></script>
  <script defer src=\"https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js\"></script>
  <style>
    :root {{
      --bg: #0f1b1e;
      --panel: #13262a;
      --text: #e7f4f2;
      --muted: #a7c8c2;
      --accent: #f2b264;
      --accent2: #6dd3b6;
    }}
    body {{
      margin: 0;
      font-family: "Noto Serif TC", "Source Han Serif TC", "PMingLiU", serif;
      background: radial-gradient(1200px 800px at 20% -10%, #1f3c3f, transparent), var(--bg);
      color: var(--text);
    }}
    body.light-theme {{
      --bg: #f5f5f5;
      --panel: #ffffff;
      --text: #1a1a1a;
      --muted: #666666;
      --accent: #f2b264;
      --accent2: #6dd3b6;
      background: radial-gradient(1200px 800px at 20% -10%, #e8f0ef, transparent), var(--bg);
    }}
    body.dark-theme {{
      --bg: #000000;
      --panel: #0a0a0a;
      --text: #d0d0d0;
      --muted: #888888;
      --accent: #f2b264;
      --accent2: #6dd3b6;
      background: var(--bg);
    }}
    header {{
      padding: 32px 24px;
      border-bottom: 1px solid #1f3c3f;
      background: linear-gradient(120deg, rgba(18, 47, 50, 0.8), rgba(13, 27, 30, 0.8));
    }}
    .header-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}
    h1 {{
      margin: 0 0 8px 0;
      font-size: 28px;
      letter-spacing: 0.5px;
    }}
    .lang-switch {{
      display: flex;
      gap: 8px;
    }}
    .lang-btn {{
      border: 1px solid #1f3c3f;
      background: transparent;
      color: var(--muted);
      padding: 6px 10px;
      border-radius: 999px;
      cursor: pointer;
      font-size: 12px;
    }}
    .lang-btn.active {{
      border-color: var(--accent);
      color: var(--accent);
    }}
    footer {{
      background: var(--panel);
      border-top: 1px solid #1f3c3f;
      padding: 24px;
      margin-top: 40px;
      text-align: center;
    }}
    .theme-switch {{
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
    }}
    .theme-label {{
      color: var(--muted);
      font-size: 13px;
      margin-right: 8px;
    }}
    .theme-btn {{
      border: 2px solid #1f3c3f;
      background: transparent;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      cursor: pointer;
      transition: all 0.3s ease;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0;
    }}
    .theme-btn::after {{
      content: '\u25cf';
      font-size: 9px;
      color: var(--muted);
      opacity: 0;
      transition: all 0.3s ease;
    }}
    .theme-btn:hover {{
      border-color: var(--muted);
    }}
    .theme-btn.active {{
      border-color: var(--accent);
    }}
    .theme-btn.active::after {{
      opacity: 1;
      color: var(--accent);
    }}
    .meta {{
      color: var(--muted);
      font-size: 14px;
    }}
    .container {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 24px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid #1f3c3f;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }}
    .card h2 {{
      margin: 0 0 8px 0;
      font-size: 18px;
      color: var(--accent);
    }}
    .plot {{
      height: 320px;
    }}
    .desc {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
      margin: 8px 0 0 0;
    }}
    .formula {{
      display: grid;
      gap: 6px;
      margin: 0;
      padding-left: 18px;
    }}
    .formula li {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }}
    .interpretation {{
      display: grid;
      gap: 8px;
      margin: 0;
      padding-left: 18px;
    }}
    .interpretation li {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid #1f3c3f;
      padding: 8px;
      text-align: left;
    }}
    th {{
      color: var(--muted);
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <header>
    <div class=\"header-row\">
      <div>
        <h1 data-i18n=\"title\"></h1>
        <div class="meta"><span data-i18n="meta_generated"></span>: <span id="meta-generated"></span></div>
      </div>
      <div class=\"lang-switch\">
        <button class=\"lang-btn\" data-lang=\"en\">English</button>
        <button class=\"lang-btn\" data-lang=\"zh\">繁體中文</button>
      </div>
    </div>
  </header>
  <div class=\"container\">
    <div class=\"card\" style=\"margin-bottom: 16px;\">
      <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
        <h2 data-i18n=\"endpoints_title\" style=\"margin: 0;\"></h2>
        <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
      </div>
      <div class=\"card-content\">
        <p class=\"desc\" data-i18n=\"endpoints_intro\"></p>
        <div style=\"margin-top: 16px; display: grid; gap: 12px;\">
          <div style=\"border-left: 4px solid #f2b264; padding-left: 12px; padding-top: 8px; padding-bottom: 8px;\">
            <h3 style=\"margin: 0 0 6px 0; font-size: 14px; color: #f2b264;\" data-i18n=\"endpoint_cpu_title\"></h3>
            <p style=\"margin: 0; font-size: 13px; color: var(--muted); line-height: 1.6;\" data-i18n=\"endpoint_cpu_desc\"></p>
          </div>
          <div style=\"border-left: 4px solid #6dd3b6; padding-left: 12px; padding-top: 8px; padding-bottom: 8px;\">
            <h3 style=\"margin: 0 0 6px 0; font-size: 14px; color: #6dd3b6;\" data-i18n=\"endpoint_io_title\"></h3>
            <p style=\"margin: 0; font-size: 13px; color: var(--muted); line-height: 1.6;\" data-i18n=\"endpoint_io_desc\"></p>
          </div>
          <div style=\"border-left: 4px solid #a7c8c2; padding-left: 12px; padding-top: 8px; padding-bottom: 8px;\">
            <h3 style=\"margin: 0 0 6px 0; font-size: 14px; color: #a7c8c2;\" data-i18n=\"endpoint_json_title\"></h3>
            <p style=\"margin: 0; font-size: 13px; color: var(--muted); line-height: 1.6;\" data-i18n=\"endpoint_json_desc\"></p>
          </div>
        </div>
      </div>
    </div>

    <div class=\"card\" style=\"margin-bottom: 16px;\">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="formulas_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <ul class="formula">
          <li data-i18n="formula_throughput"></li>
          <li data-i18n="formula_percentile"></li>
          <li data-i18n="formula_delta"></li>
        </ul>
      </div>
    </div>
    <div class=\"grid\">
      <div class=\"card\">
        <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
          <h2 data-i18n=\"chart_requests\" style=\"margin: 0;\"></h2>
          <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
        </div>
        <p class=\"desc\" data-i18n=\"desc_requests\" style=\"margin-bottom: 12px; margin-top: 0;\"></p>
        <div class=\"card-content\">
          <div id=\"chart-req\" class=\"plot\"></div>
        </div>
      </div>
      <div class=\"card\">
        <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
          <h2 data-i18n=\"chart_latency\" style=\"margin: 0;\"></h2>
          <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
        </div>
        <p class=\"desc\" data-i18n=\"desc_latency\" style=\"margin-bottom: 12px; margin-top: 0;\"></p>
        <div class=\"card-content\">
          <div id=\"chart-lat\" class=\"plot\"></div>
        </div>
      </div>
      <div class=\"card\">
        <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
          <h2 data-i18n=\"chart_transfer\" style=\"margin: 0;\"></h2>
          <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
        </div>
        <p class=\"desc\" data-i18n=\"desc_transfer\" style=\"margin-bottom: 12px; margin-top: 0;\"></p>
        <div class=\"card-content\">
          <div id=\"chart-xfer\" class=\"plot\"></div>
        </div>
      </div>
      <div class=\"card\">
        <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
          <h2 data-i18n=\"chart_pctl\" style=\"margin: 0;\"></h2>
          <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
        </div>
        <p class=\"desc\" data-i18n=\"desc_pctl\" style=\"margin-bottom: 12px; margin-top: 0;\"></p>
        <div class=\"card-content\">
          <div id=\"chart-pctl\" class=\"plot\"></div>
          <p class=\"desc\" id=\"pctl-note\" style=\"margin-top: 8px; margin-bottom: 0;\"></p>
        </div>
      </div>
      <div class=\"card\">
        <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
          <h2 data-i18n=\"chart_dist\" style=\"margin: 0;\"></h2>
          <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
        </div>
        <p class=\"desc\" data-i18n=\"desc_dist\" style=\"margin-bottom: 12px; margin-top: 0;\"></p>
        <div class=\"card-content\">
          <div id=\"chart-hist\" class=\"plot\"></div>
        </div>
      </div>
      <div class=\"card\">
        <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
          <h2 data-i18n=\"chart_delta\" style=\"margin: 0;\"></h2>
          <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
        </div>
        <p class=\"desc\" data-i18n=\"desc_delta\" style=\"margin-bottom: 12px; margin-top: 0;\"></p>
        <div class=\"card-content\">
          <div id=\"chart-delta\" class=\"plot\"></div>
        </div>
      </div>
    </div>

    <div class=\"card\" style=\"margin-top: 16px;\">
      <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
        <h2 data-i18n=\"insights_title\" style=\"margin: 0;\"></h2>
        <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
      </div>
      <div class=\"card-content\">
        <table>
          <thead>
            <tr>
              <th data-i18n=\"th_endpoint\"></th>
              <th data-i18n=\"th_winner_throughput\"></th>
              <th data-i18n=\"th_delta\"></th>
              <th data-i18n=\"th_winner_latency\"></th>
              <th data-i18n=\"th_latency_delta\"></th>
            </tr>
          </thead>
          <tbody>
            {"" .join([f"<tr><td>{i['endpoint'].replace('.php', '')}</td><td>{i['req_winner']}</td><td>{i['req_delta']:.1f}</td><td>{i['lat_winner']}</td><td>{i['lat_delta']:.1f}</td></tr>" for i in insights])}
          </tbody>
        </table>
      </div>
    </div>

    <div class=\"card\" style=\"margin-top: 16px; background: rgba(242, 178, 100, 0.15); border-color: rgba(242, 178, 100, 0.3);\">
      <p style=\"color: var(--accent); margin: 0; line-height: 1.6;\"><strong data-i18n=\"interp_intro\"></strong></p>
    </div>

    <div class=\"card\" style=\"margin-top: 16px;\">
      <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
        <h2 data-i18n=\"interpretation_title\" style=\"margin: 0;\"></h2>
        <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
      </div>
      <div class=\"card-content\">
        <ul class=\"interpretation\" id=\"interpretation-list\"></ul>
      </div>
    </div>

    <div class=\"card\" style=\"margin-top: 16px;\">
      <div style=\"display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;\">
        <h2 data-i18n=\"raw_title\" style=\"margin: 0;\"></h2>
        <button class=\"collapse-btn\" onclick=\"this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';\" style=\"background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;\">▼</button>
      </div>
      
      <div class=\"card-content\">
        <div style=\"margin-bottom: 24px;\">
          <h3 style=\"margin: 0 0 12px 0; font-size: 16px; color: #f2b264;\">XAMPP</h3>
          <table>
            <thead>
              <tr>
                <th data-i18n=\"th_endpoint\"></th>
                <th data-i18n=\"th_req\"></th>
                <th data-i18n=\"th_latency\"></th>
                <th data-i18n=\"th_p50\"></th>
                <th data-i18n=\"th_p90\"></th>
                <th data-i18n=\"th_p99\"></th>
                <th data-i18n=\"th_transfer\"></th>
              </tr>
            </thead>
            <tbody>
              {"".join([f"<tr><td>{r['endpoint'].replace('.php', '')}</td><td>{r['requests_sec']:.2f}</td><td>{r['latency_avg']}</td><td>{r['latency_p50']}</td><td>{r['latency_p90']}</td><td>{r['latency_p99']}</td><td>{r['transfer_sec']}</td></tr>" for r in rows if r['server'] == 'xampp'])}
            </tbody>
          </table>
        </div>

        <div style=\"margin-top: 24px;\">
          <h3 style=\"margin: 0 0 12px 0; font-size: 16px; color: #64b5f6;\">NGINX (Multi-core)</h3>
          <table>
            <thead>
              <tr>
                <th data-i18n=\"th_endpoint\"></th>
                <th data-i18n=\"th_req\"></th>
                <th data-i18n=\"th_latency\"></th>
                <th data-i18n=\"th_p50\"></th>
                <th data-i18n=\"th_p90\"></th>
                <th data-i18n=\"th_p99\"></th>
                <th data-i18n=\"th_transfer\"></th>
              </tr>
            </thead>
            <tbody>
              {"".join([f"<tr><td>{r['endpoint'].replace('.php', '')}</td><td>{r['requests_sec']:.2f}</td><td>{r['latency_avg']}</td><td>{r['latency_p50']}</td><td>{r['latency_p90']}</td><td>{r['latency_p99']}</td><td>{r['transfer_sec']}</td></tr>" for r in rows if r['server'] == 'nginx_multi'])}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <footer>
    <div class=\"theme-switch\">
      <span class=\"theme-label\" data-i18n=\"theme_label\"></span>
      <button class=\"theme-btn\" data-theme=\"light\" title=\"Light Theme\"></button>
      <button class=\"theme-btn\" data-theme=\"default\" title=\"Default/Dark Theme\"></button>
      <button class=\"theme-btn\" data-theme=\"dark\" title=\"Pure Dark Theme\"></button>
    </div>
  </footer>

  <script>
    const payload = {json.dumps(payload)};
    const TEXTS = {json.dumps(TEXTS)};

    // Format numbers with 'k' suffix (thousand) to 1 decimal place
    const kFormatter = (v) => {{
      if (v >= 1000) {{
        return (v / 1000).toFixed(1) + 'k';
      }}
      return v.toFixed(1);
    }};

    const reqData = [
      {{ type: 'bar', name: 'XAMPP', x: payload.charts.requests_sec.labels, y: payload.charts.requests_sec.xampp, marker: {{ color: '#f2b264' }} }},
      {{ type: 'bar', name: 'NGINX (Multi)', x: payload.charts.requests_sec.labels, y: payload.charts.requests_sec.nginx_multi, marker: {{ color: '#64b5f6' }} }},
    ];
    Plotly.newPlot('chart-req', reqData, {{ barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: {{ color: '#e7f4f2' }}, yaxis: {{ tickformat: '.1f', ticksuffix: 'k' }} }});

    const latData = [
      {{ type: 'bar', name: 'XAMPP', x: payload.charts.latency_ms.labels, y: payload.charts.latency_ms.xampp, marker: {{ color: '#f2b264' }} }},
      {{ type: 'bar', name: 'NGINX (Multi)', x: payload.charts.latency_ms.labels, y: payload.charts.latency_ms.nginx_multi, marker: {{ color: '#64b5f6' }} }},
    ];
    Plotly.newPlot('chart-lat', latData, {{ barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: {{ color: '#e7f4f2' }}, yaxis: {{ tickformat: '.1f', ticksuffix: 'k' }} }});

    const xferData = [
      {{ type: 'bar', name: 'XAMPP', x: payload.charts.transfer_kb_sec.labels, y: payload.charts.transfer_kb_sec.xampp, marker: {{ color: '#f2b264' }} }},
      {{ type: 'bar', name: 'NGINX (Multi)', x: payload.charts.transfer_kb_sec.labels, y: payload.charts.transfer_kb_sec.nginx_multi, marker: {{ color: '#64b5f6' }} }},
    ];
    Plotly.newPlot('chart-xfer', xferData, {{ barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: {{ color: '#e7f4f2' }}, yaxis: {{ tickformat: '.1f', ticksuffix: 'k' }} }});

    const pctlData = [
      {{ type: 'bar', name: 'XAMPP p50', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.xampp.p50, marker: {{ color: 'rgba(242,178,100,0.65)' }} }},
      {{ type: 'bar', name: 'XAMPP p90', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.xampp.p90, marker: {{ color: 'rgba(242,178,100,0.85)' }} }},
      {{ type: 'bar', name: 'XAMPP p99', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.xampp.p99, marker: {{ color: 'rgba(242,178,100,1.0)' }} }},
      {{ type: 'bar', name: 'NGINX Multi p50', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.nginx_multi.p50, marker: {{ color: 'rgba(100,181,246,0.65)' }} }},
      {{ type: 'bar', name: 'NGINX Multi p90', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.nginx_multi.p90, marker: {{ color: 'rgba(100,181,246,0.85)' }} }},
      {{ type: 'bar', name: 'NGINX Multi p99', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.nginx_multi.p99, marker: {{ color: 'rgba(100,181,246,1.0)' }} }},
    ];
    if (payload.has_pctl) {{
      Plotly.newPlot('chart-pctl', pctlData, {{ barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: {{ color: '#e7f4f2' }}, yaxis: {{ tickformat: '.1f', ticksuffix: 'k' }} }});
    }} else {{
      const el = document.getElementById('chart-pctl');
      if (el) {{
        el.innerHTML = '<div class="desc">No percentile series available.</div>';
      }}
    }}

    const histData = [
      {{
        type: 'violin',
        name: 'XAMPP',
        y: payload.hist_requests.xampp,
        box: {{ visible: true }},
        meanline: {{ visible: true }},
        fillcolor: 'rgba(242, 178, 100, 0.45)',
        line: {{ color: '#f2b264' }},
      }},
      {{
        type: 'violin',
        name: 'NGINX (Multi)',
        y: payload.hist_requests.nginx_multi,
        box: {{ visible: true }},
        meanline: {{ visible: true }},
        fillcolor: 'rgba(100, 181, 246, 0.45)',
        line: {{ color: '#64b5f6' }},
      }},
    ];
    Plotly.newPlot('chart-hist', histData, {{
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: {{ color: '#e7f4f2' }},
      yaxis: {{ title: 'Req/sec', tickformat: '.1f', ticksuffix: 'k' }},
    }});

    const deltaData = [
      {{
        type: 'scatter',
        mode: 'lines+markers',
        name: 'XAMPP',
        x: payload.charts.requests_sec.labels,
        y: payload.charts.requests_sec.xampp,
        line: {{ color: '#f2b264', width: 3 }},
        marker: {{ size: 8 }}
      }},
      {{
        type: 'scatter',
        mode: 'lines+markers',
        name: 'NGINX (Multi)',
        x: payload.charts.requests_sec.labels,
        y: payload.charts.requests_sec.nginx_multi,
        line: {{ color: '#64b5f6', width: 3 }},
        marker: {{ size: 8 }}
      }}
    ];
    Plotly.newPlot('chart-delta', deltaData, {{
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: {{ color: '#e7f4f2' }},
      yaxis: {{ title: 'Requests/sec', tickformat: '.1f', ticksuffix: 'k' }},
      hovermode: 'x unified'
    }});

    function updateChartsTheme(fontColor) {{
      const chartIds = ['chart-req', 'chart-lat', 'chart-xfer', 'chart-pctl', 'chart-hist', 'chart-delta'];
      const layoutUpdate = {{
        font: {{ color: fontColor }},
        xaxis: {{ tickfont: {{ color: fontColor }}, titlefont: {{ color: fontColor }} }},
        yaxis: {{ tickfont: {{ color: fontColor }}, titlefont: {{ color: fontColor }} }}
      }};
      chartIds.forEach(id => {{
        const elem = document.getElementById(id);
        if (elem && elem.data && elem.data.length > 0) {{
          Plotly.relayout(id, layoutUpdate);
        }}
      }});
    }}

    function applyTheme(theme) {{
      document.body.classList.remove('light-theme', 'dark-theme');
      let fontColor = '#e7f4f2';
      
      if (theme === 'light') {{
        document.body.classList.add('light-theme');
        fontColor = '#1a1a1a';
      }} else if (theme === 'dark') {{
        document.body.classList.add('dark-theme');
        fontColor = '#d0d0d0';
      }}
      
      updateChartsTheme(fontColor);
      window.localStorage.setItem('report_theme', theme);
      document.querySelectorAll('.theme-btn').forEach((btn) => {{
        btn.classList.toggle('active', btn.dataset.theme === theme);
      }});
    }}

    function applyLang(lang) {{
      const t = TEXTS[lang];
      document.documentElement.lang = t.lang;
      document.querySelectorAll('[data-i18n]').forEach((el) => {{
        const key = el.dataset.i18n;
        if (t[key]) {{
          el.innerHTML = t[key];
        }}
      }});
      document.getElementById('meta-generated').textContent = payload.meta.generated_at;

      const note = document.getElementById('pctl-note');
      if (payload.has_pctl) {{
        note.textContent = '';
        note.style.display = 'none';
      }} else {{
        note.textContent = t.pctl_missing;
        note.style.display = 'block';
      }}

      const list = document.getElementById('interpretation-list');
      list.innerHTML = payload.interpretations[lang]
        .map((item) => `<li><strong>${{item.endpoint}}</strong>: ${{item.text}}</li>`)
        .join('');

      document.querySelectorAll('.lang-btn').forEach((btn) => {{
        btn.classList.toggle('active', btn.dataset.lang === lang);
      }});

      if (window.renderMathInElement) {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{ left: '$', right: '$', display: false }},
            {{ left: '$$', right: '$$', display: true }},
          ],
        }});
      }}
    }}

    window.addEventListener('load', () => {{
      const saved = window.localStorage.getItem('report_lang') || 'zh';
      applyLang(saved);
      document.querySelectorAll('.lang-btn').forEach((btn) => {{
        btn.addEventListener('click', () => {{
          window.localStorage.setItem('report_lang', btn.dataset.lang);
          applyLang(btn.dataset.lang);
        }});
      }});
      
      const savedTheme = window.localStorage.getItem('report_theme') || 'default';
      applyTheme(savedTheme);
      document.querySelectorAll('.theme-btn').forEach((btn) => {{
        btn.addEventListener('click', () => {{
          applyTheme(btn.dataset.theme);
        }});
      }});
    }});
  </script>
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")


def main():
    csv_path = find_latest_results_csv()
    if csv_path is None:
        raise SystemExit("No results.csv found under results/")

    rows = normalize_rows(load_csv(csv_path))

    generate_html(rows, csv_path, REPORTS_DIR / "report.html")
    print(f"Report generated: {REPORTS_DIR / 'report.html'}")


if __name__ == "__main__":
    main()
