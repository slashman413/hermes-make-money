#!/usr/bin/env python3
"""
Income Tracker — 實際收入記錄系統
每筆收入依日期排序，自動生成報表與圖表。

Usage:
  python income.py add --date 2026-06-28 --amount 12.50 --source "博客來聯盟行銷" --notes "勵志書訂單"
  python income.py add --amount 3.50 --source "AdSense" --notes "今日廣告收入" (--date預設今天)
  python income.py list                       # 最新10筆
  python income.py report                     # 本月統計
  python income.py report --month 2026-06     # 指定月份
  python income.py dashboard                  # 產出 HTML 儀表板
  python income.py verify                     # 驗證數據一致性
"""
import os, sys, json, csv
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Optional

DATA_DIR = Path(__file__).parent / "data"
INCOME_FILE = DATA_DIR / "income.json"
CSV_FILE = DATA_DIR / "income.csv"
DASHBOARD_FILE = Path(__file__).parent.parent / "INCOME.md"

def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not INCOME_FILE.exists():
        _save([])

def _load() -> list[dict]:
    if not INCOME_FILE.exists():
        return []
    import json
    with open(INCOME_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(records: list[dict]):
    import json
    with open(INCOME_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    # Also write CSV
    if records:
        with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=["date","amount","source","category","notes","created_at"])
            w.writeheader()
            for r in sorted(records, key=lambda x: x["date"]):
                w.writerow(r)

def add_entry(date_str: str, amount: float, source: str, notes: str = "", category: str = "其他"):
    """Add an income entry. 自動寫入 income.json + 追加到 CSV"""
    ensure_dirs()
    records = _load()
    
    entry = {
        "date": date_str,
        "amount": round(amount, 2),
        "source": source,
        "category": category,
        "notes": notes,
        "created_at": datetime.now().isoformat()
    }
    records.append(entry)
    _save(records)
    
    total = sum(r["amount"] for r in records)
    print(f"✅ 已記錄: ${amount:.2f} from {source} on {date_str}")
    print(f"📊 累計總收入: ${total:.2f} ({len(records)} 筆)")
    return entry

def list_entries(limit: int = 10):
    """列出最近 N 筆收入，依日期排序"""
    records = _load()
    if not records:
        print("📭 尚無收入記錄")
        return
    
    sorted_recs = sorted(records, key=lambda x: x["date"], reverse=True)
    print(f"\n📋 最新 {limit} 筆收入（共 {len(records)} 筆）：")
    print(f"{'日期':<12} {'金額':>8} {'來源':<20} {'備註'}")
    print("-" * 60)
    for r in sorted_recs[:limit]:
        print(f"{r['date']:<12} ${r['amount']:>6.2f} {r['source']:<20} {r['notes'][:30]}")
    print(f"\n💰 總收入: ${sum(r['amount'] for r in records):.2f}")

def monthly_report(month_str: Optional[str] = None):
    """月報表：本月收入統計"""
    records = _load()
    if not records:
        print("📭 尚無收入記錄")
        return
    
    today = date.today()
    if month_str:
        year, month = int(month_str[:4]), int(month_str[5:7])
    else:
        year, month = today.year, today.month
    
    # Filter by month
    month_recs = [r for r in records if r["date"].startswith(f"{year}-{month:02d}")]
    if not month_recs:
        print(f"📭 {year}-{month:02d} 無收入")
        return
    
    total = sum(r["amount"] for r in month_recs)
    by_source = {}
    by_category = {}
    for r in month_recs:
        by_source[r["source"]] = by_source.get(r["source"], 0) + r["amount"]
        by_category[r.get("category","其他")] = by_category.get(r.get("category","其他"), 0) + r["amount"]
    
    print(f"\n📊 {year}-{month:02d} 月報表")
    print(f"總收入: ${total:.2f} ({len(month_recs)} 筆)")
    print()
    print("📂 分類統計：")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat}: ${amt:.2f}")
    print()
    print("📎 來源統計：")
    for src, amt in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {src}: ${amt:.2f}")

def generate_markdown(full: bool = False):
    """Generate INCOME.md with income sorted by date"""
    records = _load()
    if not records:
        content = "# 💰 收入儀表板\n\n📭 尚無收入記錄\n"
        DASHBOARD_FILE.write_text(content, encoding="utf-8")
        return
    
    sorted_recs = sorted(records, key=lambda x: x["date"])
    total = sum(r["amount"] for r in records)
    
    # Calculate monthly totals
    monthly = {}
    for r in sorted_recs:
        ym = r["date"][:7]
        monthly[ym] = monthly.get(ym, 0) + r["amount"]
    
    lines = [
        "# 💰 收入儀表板",
        "",
        f"> 最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 📊 總覽",
        "",
        f"| 指標 | 數值 |",
        "|------|------|",
        f"| **總收入** | **${total:.2f}** |",
        f"| **總筆數** | {len(records)} |",
        f"| **月均收入** | **${total / max(len(monthly),1):.2f}** |",
        f"| **最高月收入** | **${max(monthly.values()):.2f}** ({max(monthly, key=monthly.get)}) |" if monthly else "",
        "",
        "## 📅 月份收入",
        "",
        "| 月份 | 收入 | 趨勢 |",
        "|------|------|------|",
    ]
    
    max_monthly = max(monthly.values()) if monthly else 1
    if max_monthly == 0:
        max_monthly = 1
    for ym in sorted(monthly.keys()):
        amt = monthly[ym]
        bar_len = int(amt / max_monthly * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        lines.append(f"| {ym} | ${amt:.2f} | {bar} |")
    
    lines += [
        "",
        "## 📋 逐筆收入（依日期排序）",
        "",
        "| 日期 | 金額 | 來源 | 分類 | 備註 |",
        "|------|------|------|------|------|",
    ]
    
    for r in sorted_recs:
        lines.append(f"| {r['date']} | ${r['amount']:.2f} | {r['source']} | {r.get('category','其他')} | {r['notes'][:50]} |")
    
    lines += [
        "",
        "---",
        "",
        "🔄 自動更新：GitHub Actions 每日 UTC 06:00",
    ]
    
    content = "\n".join(lines)
    DASHBOARD_FILE.write_text(content, encoding="utf-8")
    print(f"✅ INCOME.md generated ({len(sorted_recs)} entries, ${total:.2f} total)")
    return content

def verify():
    """Verify data integrity"""
    records = _load()
    issues = []
    
    for i, r in enumerate(records):
        if "date" not in r:
            issues.append(f"Entry {i}: missing date")
        if "amount" not in r or not isinstance(r["amount"], (int, float)):
            issues.append(f"Entry {i}: invalid amount")
        if "source" not in r:
            issues.append(f"Entry {i}: missing source")
    
    if issues:
        print(f"⚠️ Found {len(issues)} issues:")
        for issue in issues:
            print(f"  • {issue}")
        return False
    
    total = sum(r["amount"] for r in records)
    print(f"✅ Data verified: {len(records)} entries, ${total:.2f} total")
    return True

if __name__ == "__main__":
    ensure_dirs()
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        date_str = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else date.today().isoformat()
        amount = float(sys.argv[sys.argv.index("--amount") + 1])
        source = sys.argv[sys.argv.index("--source") + 1]
        notes = sys.argv[sys.argv.index("--notes") + 1] if "--notes" in sys.argv else ""
        category = sys.argv[sys.argv.index("--category") + 1] if "--category" in sys.argv else "其他"
        add_entry(date_str, amount, source, notes, category)
        generate_markdown()
    
    elif cmd == "list":
        limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 10
        list_entries(limit)
    
    elif cmd == "report":
        month = sys.argv[sys.argv.index("--month") + 1] if "--month" in sys.argv else None
        monthly_report(month)
    
    elif cmd == "dashboard":
        generate_markdown(full=True)
    
    elif cmd == "verify":
        verify()
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
