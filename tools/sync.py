#!/usr/bin/env python3
"""ClawTweaks 汉化 — 上游同步工具。

检测上游分支 HEAD 是否变化；若变化则下载 tarball 并解压为快照，
更新 state/upstream.json。不含支出敏感时段的重试；按需手动/定时运行。

用法:
  python3 tools/sync.py [--branch release/v0.3.98.0] [--state state/upstream.json] [--workdir .work]
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import tarfile
import urllib.request

REPO = "enterTheVoidCode/ClawTweaks"
DEFAULT_BRANCH = "release/v0.3.98.0"


def api(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "dsh-agent"})
    return urllib.request.urlopen(req, timeout=90).read()


def get_head_sha(branch: str) -> str:
    data = json.loads(api(f"https://api.github.com/repos/{REPO}/branches?per_page=100"))
    for b in data:
        if b["name"] == branch:
            return b["commit"]["sha"]
    raise SystemExit(f"branch {branch} not found")


def download_tarball(sha: str, out: str) -> None:
    url = f"https://codeload.github.com/{REPO}/tar.gz/{sha}"
    tmp = out + ".part"
    with urllib.request.urlopen(url, timeout=600) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)
    os.replace(tmp, out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", default=DEFAULT_BRANCH)
    ap.add_argument("--state", default="state/upstream.json")
    ap.add_argument("--workdir", default=".work")
    a = ap.parse_args()

    sha = get_head_sha(a.branch)
    os.makedirs(os.path.dirname(a.state) or ".", exist_ok=True)

    prev = {}
    if os.path.exists(a.state):
        prev = json.load(open(a.state, encoding="utf-8"))

    if prev.get("sha") == sha:
        print(f"NO CHANGE  sha={sha[:12]}  ({prev.get('created_at', '')})")
        return 0

    os.makedirs(a.workdir, exist_ok=True)
    tgz = os.path.join(a.workdir, f"upstream-{sha[:12]}.tar.gz")
    download_tarball(sha, tgz)

    snap = os.path.join(a.workdir, "upstream", sha[:12])
    shutil.rmtree(snap, ignore_errors=True)
    os.makedirs(snap, exist_ok=True)
    with tarfile.open(tgz, "r:gz") as t:
        t.extractall(snap)

    top = [d for d in os.listdir(snap) if os.path.isdir(os.path.join(snap, d))]
    state = {
        "repo": REPO,
        "branch": a.branch,
        "sha": sha,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "snapshot_dir": os.path.join(snap, top[0]) if top else snap,
        "prev_sha": prev.get("sha"),
    }
    json.dump(state, open(a.state, "w", encoding="utf-8"), indent=1)
    print(f"UPDATED  sha={sha[:12]}  prev={str(prev.get('sha'))[:12]}")
    print(f"snapshot -> {state['snapshot_dir']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())