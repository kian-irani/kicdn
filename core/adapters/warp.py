"""WARP/WireGuard adapter — config for warp-cli or wireguard-go."""
from ..models import Config


def generate(cfg: Config) -> dict:
    return {
        "warp": {
            "mode": "warp+",
            "endpoint": f"{cfg.server.host}:{cfg.server.port or 2408}",
            "routing": cfg.routing,
            "dns": "1.1.1.1",
        },
        "wireguard": {
            "private_key": cfg.credentials.password or "",
            "public_key": cfg.credentials.public_key or "",
            "peer_endpoint": f"{cfg.server.host}:{cfg.server.port or 2408}",
            "allowed_ips": (
                "0.0.0.0/0, ::/0"
                if cfg.routing == "full_tunnel"
                else "0.0.0.0/1, 128.0.0.0/1"
            ),
        },
        "fallback": "direct",
        "_kicdn_meta": {
            "protocol": "warp",
            "profile": cfg.profile_name,
            "routing": cfg.routing,
        },
    }
