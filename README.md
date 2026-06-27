# hermes-make-money 💰

> **目標：每日 $500 美金被動收入**
> 使用 GitHub Actions + GitHub Pages 自動化

## 📊 即時進度

[![Revenue Dashboard](https://img.shields.io/badge/📊-Dashboard-blue)](https://slashman413.github.io/hermes-pro/)
[![GitHub](https://img.shields.io/badge/GitHub-hermes--pro-181717?logo=github)](https://github.com/slashman413/hermes-pro)

**當前狀態**：請查看 [hermes-pro 儀表板](https://slashman413.github.io/hermes-pro/) 取得即時收入數據

## 🎯 產品組合（7 條收入線）

```
hermes-make-money          ← 🧠 策略總部 + 收入儀表板
├── pixabay-shorts-bot     ← 🎬 YouTube Shorts 自動生成（聯盟行銷已上線）
├── hermes-shortsgen       ← 🚀 SaaS 產品：ShortsGen Pro ($29-499/月)
├── hermes-deal-finder     ← 🛒 聯盟行銷比價站（Amazon 2.5-10%）
├── hermes-seo-farm        ← 📝 SEO內容農場（AdSense + 訂閱）
├── hermes-lead-magnet     ← 📧 Email名單收集（lead value ~$0.50/個）
├── hermes-content-recycle ← ♻️ 舊內容跨平台變現
└── hermes-pro             ← 🎯 中樞儀表板
```

## 🚀 行銷策略

### 1. 免費 → 付費漏斗
```
工具站訪客 → 免費工具 → 升級 Pro → 月費$29
YouTube觀眾 → Shorts → 描述連結 → 訂閱$9-$29
SEO搜尋 → 文章 → AdSense + 聯盟連結
```

### 2. 自動化行銷（GitHub Actions）
- 每日自動生成 SEO 內容 → 增加自然流量
- Shorts 自動上傳 → Description 放產品連結
- 每 4 小時更新收入儀表板 → 即時追蹤

### 3. 定價策略
| 產品 | 免費版 | Pro | Business | Enterprise |
|------|--------|-----|----------|------------|
| ShortsGen | 5/月 | $29/月 (60/月) | $99/月 (無限) | $499/月 |
| Deal Finder | 基本 | $9/月 (即時通知) | $29/月 (API) | — |
| SEO Farm | 文章 | $19/月 (自訂主題) | — | — |
| Lead Magnet | 基本 | $9/月 (自動化) | — | — |

### 4. 客戶獲取管道
| 管道 | 成本 | 預計轉換率 | 每月獲取量 |
|------|------|-----------|-----------|
| YouTube Shorts | 0 | 0.5% | 50+ |
| GitHub 自然流量 | 0 | 1% | 20+ |
| SEO 搜尋 | 0 | 0.3% | 30+ |
| 工具站導流 | 0 | 0.8% | 15+ |

## 📈 $500/天目標拆解

### 方案 A：SaaS 訂閱（最穩定）

| 方案 | 用戶數 | 單價 | 月收入 |
|------|-------|------|--------|
| ShortsGen Pro | 165 | $29 | $4,785 |
| ShortsGen Business | 50 | $99 | $4,950 |
| ShortsGen Enterprise | 15 | $499 | $7,485 |
| Deal Finder Pro | 300 | $9 | $2,700 |
| SEO Farm Pro | 200 | $19 | $3,800 |
| Lead Magnet Pro | 500 | $9 | $4,500 |
| **總計** | **1,230** | | **$28,220/月 ≈ $940/天** |

### 方案 B：混合模式

| 來源 | 月收入 |
|------|--------|
| SaaS 訂閱 (ShortsGen+Deals+SEO+Lead) | $8,000 |
| 聯盟行銷 (Amazon + 博客來) | $2,000 |
| AdSense (工具站 + SEO站) | $1,500 |
| GitHub Sponsors | $500 |
| 一次性銷售 (模板/課程) | $3,000 |
| **總計** | **$15,000/月 = $500/天** |

## 🧪 實驗狀態

| # | 實驗 | 狀態 | 啟動日期 | 首次收入 |
|---|------|------|---------|---------|
| 001 | Shorts 聯盟行銷 | 🟢 已上線 | 2026-06-27 | ⏳ 待YouTube有觀看數 |
| 002 | 工具站 AdSense | 🔧 腳本就緒 | ⏳ 待申請 | ⏳ |
| 003 | GitHub Sponsors | 📝 已設定 | 2026-06-27 | ⏳ |
| 004 | TWSE Premium | 📊 規劃中 | ⏳ | ⏳ |
| 005 | SaaS模板銷售 | 🏗️ 規劃中 | ⏳ | ⏳ |
| 006 | ShortsGen SaaS | 🟢 已上線 | 2026-06-28 | ⏳ 首個客戶 |
| 007 | 內容回收 | 🟢 已上線 | 2026-06-28 | ⏳ |
| 008 | SEO Farm | 🟢 已上線 | 2026-06-28 | ⏳ AdSense核准後 |
| 009 | Deal Finder | 🟢 已上線 | 2026-06-28 | ⏳ 首筆聯盟訂單 |

## 💳 如何記錄收入

```bash
# 有任何收入就記一筆
cd /d/Hermes-Agent/hermes-make-money
python scripts/income.py add \
  --amount 29.00 \
  --source "ShortsGen Pro 訂閱" \
  --category "SaaS" \
  --notes "customer@email.com - pro plan"

# 查看進度
python scripts/income.py report
python scripts/income.py dashboard
```

## 🔗 相關 Repos

| Repo | 用途 | 連結 |
|------|------|------|
| hermes-pro | 🎯 中央儀表板 | [GitHub](https://github.com/slashman413/hermes-pro) |
| hermes-shortsgen | 🎬 Shorts SaaS | [GitHub](https://github.com/slashman413/hermes-shortsgen) |
| hermes-deal-finder | 🛒 聯盟行銷 | [GitHub](https://github.com/slashman413/hermes-deal-finder) |
| hermes-seo-farm | 📝 SEO內容 | [GitHub](https://github.com/slashman413/hermes-seo-farm) |
| hermes-lead-magnet | 📧 名單收集 | [GitHub](https://github.com/slashman413/hermes-lead-magnet) |
| hermes-content-recycle | ♻️ 內容回收 | [GitHub](https://github.com/slashman413/hermes-content-recycle) |
| pixabay-shorts-bot | 🎬 Shorts引擎 | [GitHub](https://github.com/slashman413/pixabay-shorts-bot) |
