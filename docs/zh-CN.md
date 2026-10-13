# zh-CN (简体中文) Localization Reference

> This file is a **documentation-only** contribution. It describes a Simplified Chinese 
> localization mirror of ClawTweaks and serves as a notice + translation reference for the maintainer.

## Notice / 告知

Hello! A community-maintained **Simplified Chinese (zh-CN) localization** of ClawTweaks is maintained at:

- **Fork:** https://github.com/Yg-yeung/ClawTweaks  · branch `zh-CN`
- **Coverage:** XAML UI 915/1058 (86.5%), C# runtime UI 145/171 (84.8%).
  Remaining strings are intentionally untranslated (units like `1200 MHz`, button combos like `Menu + ←`, glyphs, font/brand names).
- **Approach:** source-level dictionary + regeneration pipeline (`tools/`), does not modify the source tree; terminology fixed in `translations/GLOSSARY.md`.
- **Sync:** re-extracted and incrementally updated on every upstream release.

The maintainer is invited to:
1. consider official multi-language support (zh-CN, possibly zh-TW); and/or
2. take the translations in whatever format is preferred (`.resw` / `.po` / JSON).

No pressure — this can stay a standalone mirror. Thanks for ClawTweaks!

---

## Terminology glossary (节选 / excerpt)

| English | 中文 |
|---|---|
| controller | 手柄 |
| emulation / backend | 模拟 / 后端 |
| virtual | 虚拟 |
| firmware | 固件 |
| helper | 助手程序（Helper） |
| tile | 磁贴 |
| hotkey | 热键 |
| widget | 组件 |
| overlay | 覆盖层 |
| on-screen overlay / OSD | 覆盖显示（OSD） |
| per-game | 每游戏 |
| profile | 配置 |
| preset | 预设 |
| boost | 加速 |
| frame | 帧 |
| frame generation | 帧生成 |
| FPS limiter | FPS 限制器 |
| gyro | 陀螺仪 |
| yaw / roll / pitch | 偏航 / 翻滚 / 俯仰 |
| stick | 摇杆 |
| trigger | 扳机 |
| bumper | 肩键 |
| D-Pad | 方向键 |
| deadzone | 死区 |
| anti-deadzone | 反死区 |
| rumble / vibration | 振动 |
| haptic | 触觉 |
| touchpad | 触摸板 |
| fan curve | 风扇曲线 |
| RPM | 转速（RPM） |
| charge limit | 充电限制 |
| enable / disable | 启用 / 停用 |
| on / off | 开 / 关 |
| save / apply | 保存 / 应用 |
| reset / restore | 重置 / 恢复 |
| default / custom | 默认 / 自定义 |
| resolution | 分辨率 |
| refresh rate | 刷新率 |
| V-Sync | 垂直同步 |
| scaling | 缩放 |
| iGPU | 核显 |
| P-Core / E-Core | P 核 / E 核 |
| undervolt / overvolt | 降压 / 加压 |
| handheld | 掌机 |
| posture | 持机姿态 |

## Sample translations (样例 / sample)

| English | 中文 |
|---|---|
| TDP Mode | TDP 模式 |
| Fan Curve | 风扇曲线 |
| Charge Limit | 充电限制 |
| Deadzone | 死区 |
| Button Remapping | 按键重映射 |
| Performance Mode | 性能模式 |
| Virtual Controller | 虚拟手柄 |
| Factory Reset | 恢复出厂设置 |
| Disconnected | 未连接 |
| Coming soon | 即将推出 |
