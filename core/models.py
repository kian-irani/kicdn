"""KICDN shared data models. Pure Python, no deps."""
from dataclasses import dataclass, field
from typing import Optional

PROTOCOLS = ("reality", "mhrv", "warp", "sni_spoof", "ss", "tls")
ROUTING = ("full_tunnel", "bypass_ir", "custom")

@dataclass
class Server:
    host: str
    port: int = 443
    domain: str = ""          # for TLS / SNI

@dataclass
class Credentials:
    uuid: str = ""
    public_key: str = ""
    short_id: str = ""
    password: str = ""        # ss / trojan

@dataclass
class ApiKeys:
    cloudflare: str = ""
    groq: str = ""
    gdrive: str = ""
    vercel: str = ""
    netlify: str = ""

@dataclass
class Config:
    profile_name: str
    protocol: str                       # one of PROTOCOLS
    server: Server
    credentials: Credentials = field(default_factory=Credentials)
    routing: str = "bypass_ir"          # one of ROUTING
    api_keys: ApiKeys = field(default_factory=ApiKeys)

    def validate(self) -> None:
        if self.protocol not in PROTOCOLS:
            raise ValueError(f"unknown protocol: {self.protocol}")
        if self.routing not in ROUTING:
            raise ValueError(f"unknown routing: {self.routing}")
