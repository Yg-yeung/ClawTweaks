#!/usr/bin/env python3
"""ClawTweaks 汉化 — 抽取 C# 中赋值给 UI 属性/通知方法的字符串。

只抽高置信 UI 文案：Text/Content/Header/Title/... = "..." 与 SetText/NotifyUser( 等，
输出 catalog/en.cs_ui.json（供翻译与覆盖率参考）。避开全量 C# 字面量（含日志/协议/枚举）。

用法:
  python3 tools/extract_cs_ui.py --root .work/upstream/<snap> --out catalog/en.cs_ui.json
"""
import argparse
import glob
import json
import os
import re

_PROP = r"(?:Text|Content|Header|Title|PlaceholderText|StatusText|LabelText|Caption|Message)"
_ASSIGN = re.compile(r"\b" + _PROP + r'\s*=\s*"((?:[^"\\]|\\.)*?)"')
_CALL = re.compile(r"\b(?:SetText|SetToolTip|NotifyUser|Notify|SetStatusText)\s*\(\s*" r'"((?:[^"\\]|\\.)*?)"')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    cat: dict = {}
    for f in glob.glob(os.path.join(a.root, "**", "*.cs"), recursive=True):
        rel = os.path.relpath(f, a.root)
        s = open(f, encoding="utf-8", errors="replace").read()
        for pat in (_ASSIGN, _CALL):
            for m in pat.finditer(s):
                v = m.group(1)
                if v.strip():
                    cat.setdefault(v, set()).add(rel)

    out = {k: sorted(v) for k, v in cat.items()}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print(f"C# UI 赋值/通知唯一字符串: {len(out)} -> {a.out}")


if __name__ == "__main__":
    main()