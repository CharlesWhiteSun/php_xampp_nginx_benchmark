# 🚀 快速參考 - 菜單系統使用指南

## 執行菜單系統

### ✅ 推薦方式（Windows 用戶）
```
直接雙擊 start_benchmark.bat
```

### 📝 PowerShell 方式
```powershell
.\start_benchmark.ps1
```

---

## 菜單操作

### 1️⃣ 選擇測試模式
```
  1. Quick Test (3 minutes)
  2. Standard Test (10 minutes) [RECOMMENDED]
  3. Long-term Test (30 minutes)
  4. Ultra-long Test (1 hour)
  5. Custom Parameters
  0. Exit
```

輸入對應數字並按 Enter

---

## 操作技巧

### 🎯 確認提示
```
Confirm to start? (Y/N) [Press Enter for Yes]:
```

**操作方式**:
- **直接按 Enter** ← 🌟 **推薦** 👍（預設為 Yes）
- 輸入 `Y` 或 `y` 後按 Enter（確認）
- 輸入 `N` 或 `n` 後按 Enter（取消並退出）

### 📊 進度顯示  
運行中會顯示:
```
  Progress: [=========================   ] 85% | Elapsed: 153s | Remaining: 27s
```

### 📖 報告打開確認
```
Open report in browser? (Y/N) [Press Enter for Yes]:
```

**操作方式**:
- **直接按 Enter** ← 🌟 **推薦** 👍（自動打開報告）
- 輸入 `Y` 或 `y` 後按 Enter（打開報告）
- 輸入 `N` 或 `n` 後按 Enter（跳過打開）

---

## ⚡ 快速命令參考

### 3 分鐘測試（快速驗證）
```powershell
.\start_benchmark.ps1  # 選項 1
```

### 10 分鐘測試（推薦日常使用）
```powershell
.\start_benchmark.ps1  # 選項 2
```

### 30 分鐘測試（穩定性觀察）
```powershell
.\start_benchmark.ps1  # 選項 3
```

### 1 小時測試（極限壓力）
```powershell
.\start_benchmark.ps1  # 選項 4
```

### 自訂參數測試
```powershell
.\start_benchmark.ps1  # 選項 5
# 輸入自訂時長和連線數
```

---

## 📋 配置摘要示例

```
========================================
   Configuration Summary
========================================

  Selected Mode: Standard Test (10 minutes) [RECOMMENDED]

  Parameters:
    * Duration: 600 seconds (10.0 minutes)
    * Connections: 100

Confirm to start? (Y/N) [Press Enter for Yes]:
```

---

## 🔄 完整流程示例

```
1. 雙擊 start_benchmark.bat
   ↓
2. 菜單出現，選擇 2（標準 10 分鐘測試）
   ↓
3. 配置摘要顯示，直接按 Enter 確認
   ↓
4. 進度條實時更新（自動更新每秒）
   📊 Progress: [=============================>] 100% | Elapsed: 600s | Remaining: 0s
   ↓
5. [SUCCESS] Benchmark completed!
   ↓
6. 提示打開報告，直接按 Enter 打開
   ↓
7. 瀏覽器自動打開報告分析結果
```

---

## ⚠️ 常見問題

### Q: 為什麼菜單後直接按 Enter 會執行？
A: 這是新的默認行為。按 Enter 等同於輸入 Y，方便快速確認。

### Q: 取消後會怎樣？
A: 輸入 N 後會立即退出整個程序，無法返回菜單。

### Q: 進度條時間不準確？
A: 進度條基於預估時間和已用時間計算，±數秒偏差是正常的。

### Q: 如何停止正在運行的測試？
A: 按 Ctrl+C 強制中止程序。

---

## 📊 結果查看

測試完成後會自動：
1. ✅ 生成 HTML 報告
2. 📁 將結果保存到 `results/[時間戳]/` 目錄
3. 🖥️ 可選擇自動打開報告
4. 📈 報告包含詳細的圖表和分析

---

## 💡 最佳實踐

1. **日常測試**：使用選項 2（10 分鐘）
2. **快速驗證**：使用選項 1（3 分鐘）
3. **重要決策**：使用選項 3 或 4（更長時間以確保數據穩定）
4. **調試問題**：使用自訂參數（選項 5）進行針對性測試

---

**版本**: 2.0 - 2026年2月15日  
**語言**: 繁體中文 (Traditional Chinese)
