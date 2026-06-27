#!/usr/bin/env python3
"""
Auto Skill Generator — when an experiment shows positive results,
this script generates a structured skill markdown file and saves
it to the skills/ directory with proper categorization.

Usage:
  python auto_skill.py generate --experiment exp-001 --revenue 12.50 --traffic 150
  python auto_skill.py list                     # List all generated skills
  python auto_skill.py status                    # Show experiment results overview
"""

import os
import sys
import json
import datetime
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"
RESULTS_DIR = Path(__file__).parent.parent / "results"


def ensure_dirs():
    SKILLS_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)
    for cat in ["monetization", "traffic", "conversion", "automation"]:
        (SKILLS_DIR / cat).mkdir(exist_ok=True)


def get_experiment_meta(exp_id: str) -> dict:
    """Load experiment metadata from its README."""
    exp_dir = Path(__file__).parent.parent / "experiments" / exp_id
    readme = exp_dir / "README.md"
    meta = {"id": exp_id, "name": exp_id.replace("-", " ").title(), "dir": str(exp_dir)}
    if readme.exists():
        content = readme.read_text()
        lines = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                meta["name"] = line.replace("# ", "").strip()
    return meta


def generate_skill_md(experiment: str, revenue: float, traffic: int, conversions: int, notes: str = "") -> str:
    """Generate a structured skill markdown file."""
    meta = get_experiment_meta(experiment)
    today = datetime.date.today().isoformat()

    # Determine category based on experiment type
    if "adsense" in experiment or "affiliate" in experiment:
        category = "monetization"
    elif "traffic" in experiment or "seo" in experiment:
        category = "traffic"
    elif "sponsor" in experiment or "premium" in experiment:
        category = "conversion"
    else:
        category = "automation"

    # Determine tier based on results
    if revenue >= 100:
        tier = "platinum"
        emoji = "💎"
    elif revenue >= 30:
        tier = "gold"
        emoji = "🥇"
    elif revenue >= 10:
        tier = "silver"
        emoji = "🥈"
    elif revenue > 0:
        tier = "bronze"
        emoji = "🥉"
    else:
        tier = "testing"
        emoji = "🔬"

    content = f"""---
title: "{meta['name']}"
category: {category}
tier: {tier}
revenue: {revenue}
traffic: {traffic}
conversions: {conversions}
date_achieved: {today}
experiment: {experiment}
---

# {emoji} {meta['name']}

## 成效摘要

| 指標 | 數值 |
|------|------|
| 收入 | ${revenue:.2f} |
| 流量增加 | {traffic} |
| 轉換次數 | {conversions} |
| 達成日期 | {today} |

## 方法回顧

{notes or "待補充分法細節"}

## 可複製步驟

1. 設定實驗環境
2. 執行實驗腳本
3. 監控 KPI 指標
4. 優化轉換率
5. 規模化

## 技術棧

- GitHub Actions
- {meta.get('tech_stack', '待補充')}

## 下一步

- [ ] 擴大流量來源
- [ ] A/B 測試優化
- [ ] 自動化更多環節
"""
    return content


def generate_skill(experiment: str, revenue: float = 0, traffic: int = 0,
                   conversions: int = 0, notes: str = ""):
    """Generate and save a skill markdown file."""
    ensure_dirs()
    meta = get_experiment_meta(experiment)

    if "adsense" in experiment:
        category_dir = "monetization"
    elif "affiliate" in experiment:
        category_dir = "monetization"
    elif "sponsor" in experiment:
        category_dir = "conversion"
    elif "premium" in experiment:
        category_dir = "conversion"
    elif "saas" in experiment:
        category_dir = "monetization"
    else:
        category_dir = "automation"

    skill_content = generate_skill_md(experiment, revenue, traffic, conversions, notes)
    skill_path = SKILLS_DIR / category_dir / f"{experiment}.md"
    skill_path.write_text(skill_content, encoding="utf-8")

    # Save result to results/
    result = {
        "experiment": experiment,
        "date": datetime.date.today().isoformat(),
        "revenue": revenue,
        "traffic": traffic,
        "conversions": conversions,
        "tier": "bronze" if revenue > 0 else "testing",
        "skill_file": str(skill_path),
    }
    result_file = RESULTS_DIR / f"{experiment}_result.json"
    result_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def list_skills():
    """List all generated skills."""
    ensure_dirs()
    for category_dir in sorted(SKILLS_DIR.iterdir()):
        if category_dir.is_dir():
            for skill_file in sorted(category_dir.glob("*.md")):
                print(f"  [{category_dir.name}] {skill_file.stem}")


def show_status():
    """Show overall experiment results."""
    ensure_dirs()
    total_revenue = 0
    results = []
    for result_file in sorted(RESULTS_DIR.glob("*_result.json")):
        data = json.loads(result_file.read_text())
        results.append(data)
        total_revenue += data.get("revenue", 0)

    print(f"\n💰 總收入: ${total_revenue:.2f}")
    print(f"📊 活躍實驗: {len(results)}")
    print()
    for r in results:
        print(f"  {r['experiment']}: ${r['revenue']:.2f} | {r['traffic']} traffic | {r['conversions']} conversions")
    print()


if __name__ == "__main__":
    ensure_dirs()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "generate":
        exp = sys.argv[sys.argv.index("--experiment") + 1] if "--experiment" in sys.argv else "unknown"
        rev = float(sys.argv[sys.argv.index("--revenue") + 1]) if "--revenue" in sys.argv else 0
        traf = int(sys.argv[sys.argv.index("--traffic") + 1]) if "--traffic" in sys.argv else 0
        conv = int(sys.argv[sys.argv.index("--conversions") + 1]) if "--conversions" in sys.argv else 0
        notes = sys.argv[sys.argv.index("--notes") + 1] if "--notes" in sys.argv else ""
        generate_skill(exp, rev, traf, conv, notes)

    elif action == "list":
        list_skills()

    elif action == "status":
        show_status()

    else:
        print(f"Unknown action: {action}")
        print(__doc__)
