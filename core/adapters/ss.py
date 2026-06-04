"""Shadowsocks adapter — single-user format compatible with xray-core."""
import secrets
from ..models import Config


def generate(cfg: Config) -> dict:
    password = cfg.credentials.password or secrets.token_hex(16)
    return {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "tag": "ss-in",
                "port": cfg.server.port,
                "protocol": "shadowsocks",
                "settings": {
                    "method": "chacha20-ietf-poly1305",
                    "password": password,
                    "network": "tcp,udp",
                },
                "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
            }
        ],
        "outbounds": [{"protocol": "freedom", "tag": "direct"}],
        "_kicdn_meta": {
            "protocol": "ss",
            "profile": cfg.profile_name,
            "routing": cfg.routing,
            "ss_uri": (
                f"ss://chacha20-ietf-poly1305:{password}"
                f"@{cfg.server.host}:{cfg.server.port}"
            ),
        },
    }
