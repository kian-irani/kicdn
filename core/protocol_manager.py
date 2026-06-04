"""Protocol manager — plugin registry for tunnel engines (V2Ray, MHRV, WARP, SNI)."""
_REGISTRY = {}

def register(name):
    def deco(fn): _REGISTRY[name] = fn; return fn
    return deco

def available(): return sorted(_REGISTRY)

def get(name):
    if name not in _REGISTRY: raise KeyError(f"no adapter for {name}")
    return _REGISTRY[name]
