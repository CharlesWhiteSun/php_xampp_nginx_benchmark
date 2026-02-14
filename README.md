# PHP XAMPP NGINX 性能基準測試

一個全面的性能基準測試工具，用於比較 XAMPP 和 NGINX 在 PHP 應用上的性能表現。該工具生成交互式的視覺化報告，幫助開發者和運維人員做出最佳的伺服器選擇。

[English](#english) | [中文](#chinese)

## 功能特性 🚀

- ✅ **三個測試端點**：CPU 密集型、I/O 密集型、JSON 處理
- ✅ **完整的性能指標**：吞吐量、延遲、傳輸率、百分位數
- ✅ **交互式視覺化報告**：Plotly.js 驅動的圖表
- ✅ **可折叠/展開功能**：靈活地組織報告內容
- ✅ **多語言支援**：繁體中文 & English
- ✅ **標準化 Y 軸**：統一使用 'k' 格式（千位標記）
- ✅ **詳細的分析**：自動生成洞察和解讀建議

## 項目結構 📁

```
php_xampp_nginx_benchmark/
├── README.md                    # 本文件
├── .gitignore                   # Git 忽略規則
├── benchmarks/                  # PHP 測試業務邏輯
│   ├── cpu.php                  # CPU 密集型測試端點
│   ├── io.php                   # I/O 密集型測試端點
│   └── json.php                 # JSON 處理測試端點
├── tools/
│   ├── run_benchmark.sh         # 基準測試執行腳本
│   └── generate_report.py       # 報告生成工具
├── results/                     # 測試結果數據（CSV 格式）
└── reports/                     # 生成的 HTML 報告
    └── report.html              # 最新的基準測試報告
```

## 快速開始 🚀

### 前置需求

- **PHP 7.4+**（XAMPP 和/或 NGINX 配置）
- **Python 3.7+**（用於報告生成）
- **Apache Bench (ab)** 或 **wrk**（用於壓測）
- **Git**（版本控制）

### 安裝步驟

1. **克隆倉庫**
```bash
git clone https://github.com/CharlesWhiteSun/php_xampp_nginx_benchmark.git
cd php_xampp_nginx_benchmark
```

2. **配置 XAMPP 和 NGINX**
   - 將 `benchmarks/` 目錄部署到 XAMPP web root 和 NGINX root
   - 確保兩個伺服器都已正確配置並運行

3. **安裝 Python 依賴**（如果有 requirements.txt）
```bash
pip install -r requirements.txt
```

## 使用方法 📊

### 執行基準測試

```bash
# 運行基準測試（生成 CSV 結果）
bash tools/run_benchmark.sh
```

此腳本將：
- 對 XAMPP 和 NGINX 各執行壓測
- 測試三個端點：cpu, io, json
- 保存結果到 `results/` 目錄

### 生成報告

```bash
# 使用 Python 腳本生成 HTML 報告
python tools/generate_report.py
```

報告將生成到 `reports/report.html`

### 查看報告

在瀏覽器中打開 `reports/report.html`：
```bash
# Windows
start reports/report.html

# macOS
open reports/report.html

# Linux
xdg-open reports/report.html
```

## 測試端點說明 🔍

### 1. **CPU 端點** (`/benchmarks/cpu.php`)
- **用途**：測試伺服器 CPU 計算能力
- **方案**：執行密集的數學運算
- **場景**：適用於計算密集型應用

### 2. **I/O 端點** (`/benchmarks/io.php`)
- **用途**：測試伺服器文件系統性能
- **方案**：大量文件讀寫操作
- **場景**：適用於文件處理應用

### 3. **JSON 端點** (`/benchmarks/json.php`)
- **用途**：測試 JSON 序列化/反序列化和資料庫操作
- **方案**：生成和處理大型 JSON 數據集
- **場景**：適用於 RESTful API 應用

## 報告功能 📈

### 圖表類型

| 圖表 | 說明 |
|------|------|
| **Requests/sec** | 每秒請求數對比（吞吐量） |
| **Latency (ms)** | 平均延遲對比 |
| **Transfer (KB/sec)** | 數據傳輸速率 |
| **Latency Percentiles** | P50/P90/P99 延遲分佈 |
| **Distribution** | 吞吐量分佈（小提琴圖） |
| **Throughput Comparison** | XAMPP vs NGINX 吞吐量趨勢 |

### 交互特性

- ✅ **可折叠部分**：點擊 ▼/▶ 按鈕展開/隱藏內容
- ✅ **懸停提示**：將鼠標懸停在圖表上查看詳細值
- ✅ **語言切換**：上方選擇 繁體中文 或 English
- ✅ **Y 軸標準化**：所有圖表 Y 軸使用 `k` 後綴（例：1.5k = 1500）

## 報告結構 📋

報告包含以下部分：

1. **壓測端點與設計方法** - 解釋三個端點的選擇原因
2. **公式** - 性能計算公式的定義
3. **性能圖表** - 6 個交互式可視化圖表
4. **重點整理** - 每個端點的勝負對比
5. **解讀建議** - 自動生成的性能分析
6. **原始結果** - 詳細的測試數據（XAMPP & NGINX 分組）

## 數據格式 📄

### 結果 CSV 格式

```csv
timestamp,server,endpoint,requests_sec,latency_avg,latency_p50,latency_p90,latency_p99,transfer_sec
2026-02-14T19:30:00+08:00,xampp,cpu,1234.5,0.81,0.75,0.90,1.10,2.5MB/sec
```

### 計算公式

- **吞吐量**：R = N/T （N 為總請求數，T 為測試持續時間）
- **延遲百分位**：P90 表示 90% 的請求在 ≤ 該值 內完成
- **吞吐量差異**：Δ% = (R_xampp - R_nginx)/R_nginx × 100%

## 配置說明 ⚙️

### 修改測試參數

編輯 `tools/run_benchmark.sh` 中的以下參數：

```bash
CONCURRENCY=10          # 並發連接數
REQUESTS=1000          # 總請求數
XAMPP_URL=...          # XAMPP 基礎 URL
NGINX_URL=...          # NGINX 基礎 URL
```

### 自定義報告語言

編輯 `tools/generate_report.py` 中的 `TEXTS` 字典以添加新語言或修改現有文本。

## 常見問題 ❓

**Q: 如何修改測試端點的邏輯？**
A: 編輯 `benchmarks/` 目錄中的 PHP 文件即可。確保返回有效的 HTTP 響應。

**Q: 報告在哪裡查看？**
A: 執行 `python tools/generate_report.py` 後，報告位於 `reports/report.html`

**Q: 如何添加新的測試端點？**
A: 
1. 在 `benchmarks/` 創建新 PHP 文件
2. 修改 `tools/run_benchmark.sh` 添加對應壓測命令
3. 修改 `tools/generate_report.py` 中的數據處理邏輯

**Q: 支持哪些伺服器？**
A: 目前專注於 XAMPP（Apache + PHP）和 NGINX + PHP-FPM

## 效能優化建議 💡

基於測試結果，考慮以下優化：

1. **NGINX 更快時**：考慮遷移到 NGINX + PHP-FPM
2. **XAMPP 更快時**：優化 Apache 模塊配置
3. **I/O 瓶頸**：檢查磁盤子系統和文件系統
4. **CPU 瓶頸**：考慮垂直擴展或優化代碼效率
5. **記憶體使用**：調整 PHP-FPM 或 Apache worker 進程數

## 技術棧 🛠️

| 組件 | 技術 |
|------|------|
| **後端** | PHP 7.4+, Python 3.7+ |
| **前端** | HTML5, CSS3, JavaScript |
| **圖表** | Plotly.js 2.27.0 |
| **數學展示** | KaTeX 0.16.9 |
| **版本控制** | Git |

## 貢獻指南 🤝

1. Fork 本倉庫
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 許可證 📄

本項目採用 MIT 許可證。詳見 [LICENSE](LICENSE) 文件。

## 作者 👤

**CharlesWhiteSun**
- GitHub: [@CharlesWhiteSun](https://github.com/CharlesWhiteSun)

## 致謝 🙏

感謝所有貢獻者和使用此工具的開發人員！

---

# English

# PHP XAMPP NGINX Performance Benchmark

A comprehensive performance benchmarking tool for comparing XAMPP and NGINX performance on PHP applications. This tool generates interactive visual reports to help developers and DevOps engineers make the best server choices.

## Features 🚀

- ✅ **Three Test Endpoints**: CPU-intensive, I/O-intensive, JSON processing
- ✅ **Complete Performance Metrics**: Throughput, latency, transfer rate, percentiles
- ✅ **Interactive Visualization Reports**: Plotly.js-powered charts
- ✅ **Collapse/Expand Functionality**: Flexibly organize report content
- ✅ **Multi-Language Support**: Traditional Chinese & English
- ✅ **Normalized Y-Axis**: Unified 'k' format (thousand notation)
- ✅ **Detailed Analysis**: Auto-generated insights and recommendations

## Quick Start 🚀

### Prerequisites

- **PHP 7.4+** (XAMPP and/or NGINX configuration)
- **Python 3.7+** (for report generation)
- **Apache Bench (ab)** or **wrk** (for load testing)
- **Git** (version control)

### Installation

```bash
git clone https://github.com/CharlesWhiteSun/php_xampp_nginx_benchmark.git
cd php_xampp_nginx_benchmark
```

### Running Benchmarks

```bash
# Run benchmark tests
bash tools/run_benchmark.sh

# Generate HTML report
python tools/generate_report.py

# View report in browser
start reports/report.html
```

## Test Endpoints 🔍

| Endpoint | Purpose | Use Case |
|----------|---------|----------|
| **/cpu** | CPU computation | Compute-intensive applications |
| **/io** | File system operations | File processing applications |
| **/json** | JSON serialization & data handling | RESTful APIs |

## Report Features 📈

- **6 Interactive Charts**: Requests/sec, Latency, Transfer, Percentiles, Distribution, Throughput Comparison
- **Multi-language Interface**: Chinese & English support
- **Standardized Y-Axis**: All charts use 'k' suffix notation (e.g., 1.5k = 1500)
- **Collapsible Sections**: Click ▼/▶ buttons to expand/collapse content
- **Detailed Analysis**: Auto-generated insights and performance recommendations

## Project Structure 📁

```
php_xampp_nginx_benchmark/
├── benchmarks/          # PHP test endpoints
├── tools/              # Testing and report generation scripts
├── results/            # CSV result data
└── reports/            # Generated HTML reports
```

## License 📄

MIT License - see [LICENSE](LICENSE) file for details

## Author 👤

**CharlesWhiteSun** - [GitHub](https://github.com/CharlesWhiteSun)
