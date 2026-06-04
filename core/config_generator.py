"""Config generator — turns a Config into protocol-specific output.

NOTE: reuses the proven kian_v2ray logic. For Reality/WARP/SS/TLS the source of
truth is kian_v2ray/kv2m/core.py (build_config/generate). This module is the
KICDN-level adapter that will import/wrap those generators per protocol.
"""
from .models import Config

def generate(cfg: Config) -> dict:
    cfg.validate()
    # TODO(TASK-012): dispatch to per-protocol adapters (reuse kv2m core for v2ray)
    return {"profile": cfg.profile_name, "protocol": cfg.protocol,
            "status": "stub — wire to kv2m core / mhrv / warp adapters"}
