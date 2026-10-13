#!/usr/bin/env python3
"""ClawTweaks 汉化 — 把本地镜像推送到用户的 GitHub fork。

本环境 git 无 HTTPS 传输，改用纯 Python 的 dulwich 走 smart-HTTP 推送。
Token 仅作一次性推送凭据，绝不写入提交；优先从环境变量读取，其次 .gh-token 文件（已 gitignore）。

用法:
  GH_TOKEN=github_pat_xxx python3 tools/push.py                      # 推 main -> zh-CN
  python3 tools/push.py --token github_pat_xxx --branch zh-CN       # 指定分支
"""
import argparse
import os
import sys


def load_token(cli_token: str) -> str:
    if cli_token:
        return cli_token
    env = os.environ.get("GH_TOKEN", "")
    if env:
        return env
    if os.path.exists(".gh-token"):
        return open(".gh-token", encoding="utf-8").read().strip()
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--remote", default="Yg-yeung/ClawTweaks")
    ap.add_argument("--branch", default="zh-CN")
    ap.add_argument("--local-branch", default="main")
    ap.add_argument("--token", default="")
    a = ap.parse_args()

    token = load_token(a.token)
    if not token:
        print("缺少 token：请设 GH_TOKEN 环境变量、--token 参数，或写入 .gh-token 文件",
              file=sys.stderr)
        return 2

    from dulwich import porcelain

    url = f"https://x-access-token:{token}@github.com/{a.remote}.git"
    refspec = f"refs/heads/{a.local_branch}:refs/heads/{a.branch}"
    print(f"push {a.local_branch} -> github.com/{a.remote}@{a.branch} ...")

    try:
        result = porcelain.push(".", url, refspec)
    except Exception as exc:  # noqa: BLE001
        print(f"push 失败: {exc}", file=sys.stderr)
        return 1

    print("push 返回:", result)
    return 0


if __name__ == "__main__":
    sys.exit(main())