#!/usr/bin/env python3
"""ClawTweaks 汉化 — 应用翻译词典到上游源码副本。

输入：上游源码目录 + 词典 JSON（en -> zh）。
- XAML：对指定属性的整个属性值做精确替换（确定性、幂等）。
- .cs ：仅替换词典中显式收录的字面量（zh-CN.cs.json，需人工筛选用）。

输出：翻译后的源码树。每次从全新上游快照重新生成，避免与上游合并冲突；
词典本身是唯一需要持续维护的、可随作者更新而增量的来源。

用法:
  python3 tools/apply.py \
      --src      .work/upstream/<snapshot-dir> \
      --out      build/zh-CN \
      --xml-dict translations/zh-CN.xaml.json \
      --cs-dict  translations/zh-CN.cs.json
"""
import argparse
import glob
import json
import os
import re
import shutil

_XAML_NAME = r"(?:Text|Content|Header|PlaceholderText|ToolTipService\.ToolTip|Title|Description|AutomationProperties\.Name)"
_XAML_PAT = re.compile(
    r"(?P<name>" + _XAML_NAME + r')\s*=\s*(?P<q>["\'])(?P<val>(?:[^"\'\\]|\\.)*?)(?P=q)'
)
_CS_PAT = re.compile(r'"((?:[^"\\]|\\.)*?)"')


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
    if not cs_map:
        return 0
    count = 0
    for f in glob.glob(os.path.join(root, "**", "*.cs"), recursive=True):
        s = open(f, encoding="utf-8", errors="replace").read()

        def repl(m, _c=[0]):
            v = m.group(1)
            if v in cs_map:
                _c[0] += 1
                return cs_map[v]
            return m.group(0)

        s2 = _CS_PAT.sub(repl, s)
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
    if cs_map:
        print(f"C#  字面量替换次数: {cs_repl}")
    print(f"输出 -> {root}")


if __name__ == "__main__":
    main()