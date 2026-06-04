---
title: "🛰️ KICDN — Kian Integrated CDN / Censorship-circumvention app"
tags: [project, kicdn, readme, active]
date: 2026-06-03
status: active
project: kicdn
---

# 🛰️ KICDN — Kian Integrated CDN / Censorship-circumvention app

اپ یکپارچهٔ دور زدن فیلترینگ که پروژه‌های kianv2ray / mhrv / zyrln را در یک هسته جمع می‌کند.
روی **Windows** و **Android** (بعداً Linux/Mac). با وارد کردن API key (Cloudflare/Groq/GDrive/Vercel/Netlify) خودکار کانفیگ می‌سازد.

فناوری‌ها: MHRV · ZRLYN · V2Ray · WARP · WireGuard · SNI-Spoofing · XHTTP

> دستورالعمل کامل ایجنت و backlog در ریشهٔ workspace: [`KICDN.md`](../../KICDN.md)

## ساختار
```
core/      هستهٔ مشترک Python (models, config_generator, protocol_manager, ssh_client, vps_installer)
windows/   اپ ویندوز (فاز اول Python GUI — قالب kv2m)
android/   اپ اندروید (Kotlin + Jetpack Compose + VpnService)
scripts/   نصب/آپدیت روی VPS
docs/      مستندات FA/EN
.github/   workflowهای build اندروید و ویندوز
```

## وضعیت
اسکلت آماده است (stubها compile می‌شوند). برای ساخت repo: `git init && git remote add ... && git push`.
جزئیات backlog و چه‌کاری‌بعدی در [`STATUS.md`](STATUS.md).
