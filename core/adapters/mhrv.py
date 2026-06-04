"""MHRV (MasterHttpRelayVPN) adapter — HTTP relay tunnel config."""
from ..models import Config


def generate(cfg: Config) -> dict:
    return {
        "relay": {
            "server": cfg.server.host,
            "port": cfg.server.port,
            "domain": cfg.server.domain or cfg.server.host,
            "auth_key": cfg.credentials.password or "",
            "tunnel_type": "http",
        },
        "client": {
            "listen_port": 10808,
            "routing": cfg.routing,
        },
        "_kicdn_meta": {
            "protocol": "mhrv",
            "profile": cfg.profile_name,
            "routing": cfg.routing,
        },
    }
