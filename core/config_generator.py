"""Config generator — dispatches a Config to the matching protocol adapter."""
from .models import Config
from . import protocol_manager as _pm
from .adapters import reality, mhrv, warp, ss

_pm._REGISTRY.update({
    "reality": reality.generate,
    "mhrv":    mhrv.generate,
    "warp":    warp.generate,
    "ss":      ss.generate,
})


def generate(cfg: Config) -> dict:
    cfg.validate()
    return _pm.get(cfg.protocol)(cfg)


def available_protocols() -> list:
    return _pm.available()
