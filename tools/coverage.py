#!/usr/bin/env python3
"""ClawTweaks 汉化 — 覆盖率统计。

对比英文源文目录与词典，报告翻译进度并输出未翻译清单。

用法:
  python3 tools/coverage.py \
      --catalog catalog/en.xaml.json \
      --dict translations/zh-CN.xaml.json \
      --missing-out reports/untranslated.txt
"""
import argparse
import json
import os


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default="catalog/en.xaml.json")
    ap.add_argument("--dict", default="translations/zh-CN.xaml.json")
    ap.add_argument("--missing-out", default="reports/untranslated.txt")
    a = ap.parse_args()

    cat = json.load(open(a.catalog, encoding="utf-8"))
    dic = json.load(open(a.dict, encoding="utf-8"))

    total = len(cat)
    done = sum(1 for k in cat if k in dic)
    missing = [k for k in cat if k not in dic]
    pct = done / total * 100 if total else 0.0

    print(f"翻译进度: {done}/{total}  ({pct:.1f}%)")

    os.makedirs(os.path.dirname(a.missing_out) or ".", exist_ok=True)
    with open(a.missing_out, "w", encoding="utf-8") as f:
        for k in sorted(missing):
            f.write(k.replace("\n", "\\n") + "\n")
    print(f"未翻译清单 -> {a.missing_out}  ({len(missing)} 条)")


if __name__ == "__main__":
    main()