#!/usr/bin/env python3
"""ClawTweaks 汉化 — 字符串抽取工具。

从上游源码抽取可翻译的 UI 字面串，生成英文源文目录（catalog）。
确定性、幂等：上游更新后直接对新快照重跑，得到最新目录，供翻译词典
维护与覆盖率统计使用。目录是后续 apply / coverage 的输入。

用法:
  python3 tools/extract.py \
      --root     .work/upstream/<snapshot-dir> \
      --out-xml  catalog/en.xaml.json \
      --out-cs   catalog/en.cs.json
"""
import argparse
import glob
import json
import os
import re

# XAML 中承载用户可见文本的属性（正则按此展开，忽略大小写场景极少，保持精确）
_XAML_ATTR_RE = (
    r'(?P<name>Text|Content|Header|PlaceholderText|ToolTipService\.ToolTip|Title|Description|AutomationProperties\.Name)'
    r'\s*=\s*(?P<q>["\'])(?P<val>(?:[^"\'\\]|\\.)*?)(?P=q)'
)
_ATTR_PAT = re.compile(_XAML_ATTR_RE)

_CS_LITERAL_PAT = re.compile(r'"((?:[^"\\]|\\.)*?)"')


def is_translatable(value: str) -> bool:
    """粗略判断：含英文字母才视为可翻译文本；纯数字/符号/实体/绑定跳过。"""
    v = value.strip()
    if not v:
        return False
    # 绑定/资源引用不是字面文案
    if v.startswith("{") and ("Binding" in v or "StaticResource" in v or "x:Bind" in v or "TemplateBinding" in v):
        return False
    return bool(re.search(r"[A-Za-z]", v))


def scan_xaml(root: str) -> dict:
    catalog: dict = {}
    for f in glob.glob(os.path.join(root, "**", "*.xaml"), recursive=True):
        rel = os.path.relpath(f, root)
        s = open(f, encoding="utf-8", errors="replace").read()
        for m in _ATTR_PAT.finditer(s):
            v = m.group("val")
            if is_translatable(v):
                catalog.setdefault(v, set()).add(rel)
    return {k: sorted(v) for k, v in catalog.items()}


def scan_cs_candidates(root: str) -> dict:
    """C# 字符串字面量候选，仅供人工筛选确认后手动加入 cs 词典；不会自动应用。"""
    out: dict = {}
    for f in glob.glob(os.path.join(root, "**", "*.cs"), recursive=True):
        rel = os.path.relpath(f, root)
        s = open(f, encoding="utf-8", errors="replace").read()
        for m in _CS_LITERAL_PAT.finditer(s):
            v = m.group(1)
            if is_translatable(v):
                out.setdefault(v, set()).add(rel)
    return {k: sorted(v) for k, v in out.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out-xml", required=True)
    ap.add_argument("--out-cs", required=True)
    a = ap.parse_args()

    xaml = scan_xaml(a.root)
    cs = scan_cs_candidates(a.root)

    os.makedirs(os.path.dirname(a.out_xml), exist_ok=True)
    os.makedirs(os.path.dirname(a.out_cs), exist_ok=True)
    json.dump(xaml, open(a.out_xml, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    json.dump(cs, open(a.out_cs, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)

    print(f"XAML 可翻译字面串（唯一）: {len(xaml)}")
    print(f"C#  候选字面量（唯一）  : {len(cs)}")
    print(f"目录 -> {a.out_xml} / {a.out_cs}")


if __name__ == "__main__":
    main()