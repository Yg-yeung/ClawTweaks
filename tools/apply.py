#!/usr/bin/env python3
"""ClawTweaks 汉化 — 应用翻译词典到上游源码副本。

- XAML：对指定属性整值精确替换（确定性、幂等）。
- C# ：仅替换「赋值给 UI 属性 / 通知方法」的字面量（Text=、SetText( 等），
       避免误伤 IPC/枚举/协议/日志串。

每轮从全新上游快照重新生成；词典是唯一长期维护、随上游增量演进的来源。

用法:
  python3 tools/apply.py \
      --src SRC --out OUT \
      --xml-dict translations/zh-CN.xaml.json \
      --cs-dict  translations/zh-CN.cs.json
"""
import argparse
import glob
import json
import os
import re
import shutil

_XAML_PAT = re.compile(
    r"(?P<name>Text|Content|Header|PlaceholderText|ToolTipService\.ToolTip|Title|Description|AutomationProperties\.Name)"
    r"\s*=\s*(?P<q>[\"'])(?P<val>(?:[^\"'\\]|\\.)*?)(?P=q)"
)

_CS_UI_PROP = (
    r"(?:Text|Content|Header|Title|PlaceholderText|StatusText|LabelText|Caption|Message)"
)
_CS_ASSIGN_PAT = re.compile(
    r"(\b" + _CS_UI_PROP + r'\s*=\s*")((?:[^"\\]|\\.)*?)(")'
)
_CS_CALL_PAT = re.compile(
    r'(\b(?:SetText|SetToolTip|NotifyUser|Notify|SetStatusText)\s*\(\s*")((?:[^"\\]|\\.)*?)(")'
)


def apply_xaml(root: str, xml_map: dict) -> int:
    total = 0
    for f in glob.glob(os.path.join(root, "**", "*.xaml"), recursive=True):
        s = open(f, encoding="utf-8", errors="replace").read()

        def repl(m, _c=[0]):
            v = m.group("val")
            if v in xml_map:
                _c[0] += 1
                return f'{m.group("name")}={m.group("q")}{xml_map[v]}{m.group("q")}'
            return m.group(0)

        s2 = _XAML_PAT.sub(repl, s)
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            total += repl.__defaults__[0][0]
    return total


def apply_cs(root: str, cs_map: dict) -> int:
    """仅替换赋值给 UI 属性/通知方法里的字面量，避免误伤协议/枚举/日志。"""
    if not cs_map:
        return 0
    count = 0
    for f in glob.glob(os.path.join(root, "**", "*.cs"), recursive=True):
        s = open(f, encoding="utf-8", errors="replace").read()

        def repl(m, _c=[0]):
            v = m.group(2)
            if v in cs_map:
                _c[0] += 1
                return m.group(1) + cs_map[v] + m.group(3)
            return m.group(0)

        s2 = s
        for pat in (_CS_ASSIGN_PAT, _CS_CALL_PAT):
            s2 = pat.sub(repl, s2)
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            count += repl.__defaults__[0][0]
    return count


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--xml-dict", required=True)
    ap.add_argument("--cs-dict", required=False, default="")
    a = ap.parse_args()

    xml_map = json.load(open(a.xml_dict, encoding="utf-8"))
    cs_map = {}
    if a.cs_dict and os.path.exists(a.cs_dict):
        cs_map = json.load(open(a.cs_dict, encoding="utf-8"))

    if os.path.abspath(a.out) == os.path.abspath(a.src):
        root = a.src
    else:
        shutil.rmtree(a.out, ignore_errors=True)
        shutil.copytree(a.src, a.out)
        root = a.out

    xml_repl = apply_xaml(root, xml_map)
    cs_repl = apply_cs(root, cs_map)

    print(f"XAML 属性值替换次数: {xml_repl}")
    print(f"C#  UI 赋值/通知替换次数: {cs_repl}")
    print(f"输出 -> {root}")


if __name__ == "__main__":
    main()