"""VLESS + Reality adapter — generates xray-core inbound config."""
import uuid as _uuid
from ..models import Config


def generate(cfg: Config) -> dict:
    uid = cfg.credentials.uuid or str(_uuid.uuid4())
    return {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "tag": "vless-reality",
                "port": cfg.server.port,
                "protocol": "vless",
                "settings": {
                    "clients": [
                        {
                            "id": uid,
                            "flow": "xtls-rprx-vision",
                            "level": 0,
                        }
                    ],
                    "decryption": "none",
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "reality",
                    "realitySettings": {
                        "show": False,
                        "dest": f"{cfg.server.domain or 'www.google.com'}:443",
                        "xver": 0,
                        "serverNames": [cfg.server.domain or "www.google.com"],
                        "privateKey": cfg.credentials.password or "",
                        "shortIds": [cfg.credentials.short_id or ""],
                    },
                },
                "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
            }
        ],
        "outbounds": [{"protocol": "freedom", "tag": "direct"}],
        "_kicdn_meta": {
            "protocol": "reality",
            "profile": cfg.profile_name,
            "routing": cfg.routing,
        },
    }
