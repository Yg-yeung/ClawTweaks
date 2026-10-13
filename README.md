# ClawTweaks 汉化镜像

对 [enterTheVoidCode/ClawTweaks](https://github.com/enterTheVoidCode/ClawTweaks) 的中文（zh-CN）汉化镜像。
持续追踪作者更新：作者每次更新后，重新抽取字符串、增量更新翻译词典、重新生成译文源码树。

## 目录结构

- `tools/extract.py` — 从上游源码抽取可翻译字符串 → `catalog/`
- `tools/apply.py` — 把词典应用到上游源码副本 → `build/zh-CN/`
- `tools/sync.py` — 检测上游分支 HEAD 是否变化，变化则拉取新快照
- `tools/coverage.py` — 统计翻译覆盖率，列出未翻译串
- `catalog/` — 英文源文目录（`en.xaml.json` / `en.cs.json`）
- `translations/` — 词典：`zh-CN.xaml.json`（en→zh）、`zh-CN.cs.json`（人工筛选的 C# 字面量）
- `state/upstream.json` — 已同步的上游 SHA 与快照路径
- `build/zh-CN/` — 生成的译后源码（可随时重建重建，默认 gitignore）

## 工作流（作者更新 → 更新汉化）

```bash
# 1. 检测上游；有更新则下载新快照
python3 tools/sync.py

# 2. 对新快照重跑抽取（得到最新英文源文目录）
python3 tools/extract.py \
    --root "$(python3 -c "import json;print(json.load(open('state/upstream.json'))['snapshot_dir'])")" \
    --out-xml catalog/en.xaml.json \
    --out-cs  catalog/en.cs.json

# 3. 增量增补/修订 translations/zh-CN.xaml.json（en→zh）

# 4. 重新生成译后源码树
python3 tools/apply.py \
    --src  "$(python3 -c "import json;print(json.load(open('state/upstream.json'))['snapshot_dir'])")" \
    --out  build/zh-CN \
    --xml-dict translations/zh-CN.xaml.json \
    --cs-dict  translations/zh-CN.cs.json

# 5. 查看覆盖率与未翻译清单
python3 tools/coverage.py
```

## 汉化策略

- 上游是 UWP「Xbox Game Bar」组件，仅可在 Windows + Visual Studio 2022 + Windows SDK 10.0.26100 构建（见 `BUILDING.md`）。
  因此本仓库做**源码级汉化**，不做（也无法在此环境做）二进制打包。
- XAML：对 `Text/Content/Header/PlaceholderText/ToolTip/Title/Description` 等属性的**整个属性值做精确替换**，确定性、幂等。
- C# 字面量：仅替换 `translations/zh-CN.cs.json` 中**人工确认**的条目，避免误伤 IPC/枚举/协议/日志串。
- 「词典 + 重生成」：每次从**全新上游快照**重新生成，天然规避与上游的合并冲突；词典是唯一需要长期维护、随作者更新而增量的来源。

## 许可

上游采用 GNU AGPL v3.0（见 `LICENSE`）。本镜像延续该许可并保留上游声明。