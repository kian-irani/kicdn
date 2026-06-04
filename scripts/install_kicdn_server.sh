#!/usr/bin/env bash
# KICDN server installer (skeleton). Rules: starts with dpkg fix, no set -e, single heredoc-safe.
dpkg --configure -a 2>/dev/null || true
echo "[kicdn] installer skeleton — wire to kian_v2ray install.sh logic (vps_installer.py)."
# TODO: docker + xray + warp + caddy (reuse kian_v2ray/install.sh)
