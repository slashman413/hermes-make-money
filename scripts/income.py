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
HTML_FILE = Path(__file__).parent.parent / "docs" / "index.html"

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

def generate_html():
    """Generate docs/index.html — a self-contained income dashboard for GitHub Pages.

    Data is baked in at build time (no client-side fetch), so the page works
    on GitHub Pages with zero dependencies.
    """
    import html as _html

    records = _load()
    sorted_recs = sorted(records, key=lambda x: x["date"])
    total = sum(r["amount"] for r in records)

    # Monthly / category / source aggregates
    monthly, by_category, by_source = {}, {}, {}
    for r in sorted_recs:
        ym = r["date"][:7]
        monthly[ym] = monthly.get(ym, 0) + r["amount"]
        cat = r.get("category", "其他")
        by_category[cat] = by_category.get(cat, 0) + r["amount"]
        by_source[r["source"]] = by_source.get(r["source"], 0) + r["amount"]

    n_months = max(len(monthly), 1)
    avg_month = total / n_months
    best_month_amt = max(monthly.values()) if monthly else 0.0
    best_month = max(monthly, key=monthly.get) if monthly else "—"
    updated = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    def esc(s):
        return _html.escape(str(s))

    def money(v):
        return f"${v:,.2f}"

    # Monthly bars
    max_monthly = best_month_amt if best_month_amt > 0 else 1
    month_bars = ""
    for ym in sorted(monthly.keys()):
        amt = monthly[ym]
        pct = min(100, amt / max_monthly * 100)
        month_bars += (
            f'<div class="bar-row"><span class="bar-label">{esc(ym)}</span>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%"></div></div>'
            f'<span class="bar-val">{money(amt)}</span></div>\n'
        )
    if not month_bars:
        month_bars = '<p class="empty">尚無月份資料</p>'

    # Category chips
    cat_chips = ""
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        cat_chips += f'<span class="chip">{esc(cat)} · {money(amt)}</span>'
    if not cat_chips:
        cat_chips = '<span class="chip empty">尚無分類</span>'

    # Entries table (newest first)
    rows = ""
    for r in sorted(records, key=lambda x: x["date"], reverse=True):
        rows += (
            "<tr>"
            f"<td class='nowrap'>{esc(r['date'])}</td>"
            f"<td class='amt'>{money(r['amount'])}</td>"
            f"<td>{esc(r['source'])}</td>"
            f"<td><span class='tag'>{esc(r.get('category','其他'))}</span></td>"
            f"<td class='notes'>{esc(r.get('notes',''))}</td>"
            "</tr>\n"
        )
    if not rows:
        rows = "<tr><td colspan='5' class='empty'>📭 尚無收入記錄</td></tr>"

    doc = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>💰 收入儀表板 · hermes-make-money</title>
<meta name="description" content="hermes-make-money 每日自動更新的收入儀表板">
<style>
  :root {{ --bg:#0b0f17; --card:#151b26; --line:#232c3b; --txt:#e6ecf5; --dim:#8b98ad; --accent:#3ddc97; --accent2:#4d8dff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,"Segoe UI",Roboto,"Noto Sans TC",sans-serif; background:var(--bg); color:var(--txt); line-height:1.5; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:32px 20px 64px; }}
  header h1 {{ margin:0 0 4px; font-size:1.7rem; }}
  header .sub {{ color:var(--dim); font-size:.9rem; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; margin:24px 0; }}
  .stat {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:18px; }}
  .stat .k {{ color:var(--dim); font-size:.8rem; letter-spacing:.03em; text-transform:uppercase; }}
  .stat .v {{ font-size:1.8rem; font-weight:700; margin-top:6px; }}
  .stat .v.green {{ color:var(--accent); }}
  section {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; margin:18px 0; }}
  section h2 {{ margin:0 0 16px; font-size:1.1rem; }}
  .bar-row {{ display:flex; align-items:center; gap:12px; margin:8px 0; font-size:.9rem; }}
  .bar-label {{ width:64px; color:var(--dim); flex:none; }}
  .bar-track {{ flex:1; background:#0d1420; border-radius:6px; height:14px; overflow:hidden; }}
  .bar-fill {{ height:100%; background:linear-gradient(90deg,var(--accent2),var(--accent)); border-radius:6px; min-width:2px; }}
  .bar-val {{ width:90px; text-align:right; flex:none; }}
  .chips {{ display:flex; flex-wrap:wrap; gap:8px; }}
  .chip {{ background:#0d1420; border:1px solid var(--line); border-radius:999px; padding:5px 12px; font-size:.85rem; }}
  table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
  th,td {{ text-align:left; padding:10px 8px; border-bottom:1px solid var(--line); vertical-align:top; }}
  th {{ color:var(--dim); font-weight:600; font-size:.78rem; text-transform:uppercase; letter-spacing:.03em; }}
  td.amt {{ color:var(--accent); font-weight:600; white-space:nowrap; }}
  td.nowrap {{ white-space:nowrap; color:var(--dim); }}
  .tag {{ background:#0d1420; border:1px solid var(--line); border-radius:6px; padding:2px 8px; font-size:.78rem; }}
  .notes {{ color:var(--dim); max-width:320px; }}
  .empty {{ color:var(--dim); text-align:center; padding:20px; }}
  footer {{ color:var(--dim); font-size:.82rem; text-align:center; margin-top:28px; }}
  a {{ color:var(--accent2); }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>💰 收入儀表板</h1>
    <div class="sub">hermes-make-money · 目標：每日 $500 被動收入 · 最後更新 {esc(updated)}</div>
  </header>

  <div class="grid">
    <div class="stat"><div class="k">總收入</div><div class="v green">{money(total)}</div></div>
    <div class="stat"><div class="k">總筆數</div><div class="v">{len(records)}</div></div>
    <div class="stat"><div class="k">月均收入</div><div class="v">{money(avg_month)}</div></div>
    <div class="stat"><div class="k">最高月收入</div><div class="v">{money(best_month_amt)}<span style="font-size:.9rem;color:var(--dim)"> ({esc(best_month)})</span></div></div>
  </div>

  <section>
    <h2>📅 月份收入</h2>
    {month_bars}
  </section>

  <section>
    <h2>📂 分類統計</h2>
    <div class="chips">{cat_chips}</div>
  </section>

  <section>
    <h2>📋 逐筆收入（最新在上）</h2>
    <table>
      <thead><tr><th>日期</th><th>金額</th><th>來源</th><th>分類</th><th>備註</th></tr></thead>
      <tbody>
{rows}      </tbody>
    </table>
  </section>

  <footer>
    🔄 由 GitHub Actions 每日自動更新（UTC 06:00）·
    <a href="https://github.com/slashman413/hermes-make-money">原始碼</a>
  </footer>
</div>
</body>
</html>
"""

    HTML_FILE.parent.mkdir(parents=True, exist_ok=True)
    HTML_FILE.write_text(doc, encoding="utf-8")
    print(f"✅ docs/index.html generated ({len(records)} entries, {money(total)} total)")
    return doc

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
        generate_html()
    
    elif cmd == "list":
        limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 10
        list_entries(limit)
    
    elif cmd == "report":
        month = sys.argv[sys.argv.index("--month") + 1] if "--month" in sys.argv else None
        monthly_report(month)
    
    elif cmd == "dashboard":
        generate_markdown(full=True)
        generate_html()

    elif cmd == "html":
        generate_html()

    elif cmd == "verify":
        verify()
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
