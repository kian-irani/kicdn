"""VPS installer — continuation of kian_v2ray install.sh logic, driven over SSH."""
from .ssh_client import SSH

def install(ssh: SSH, payload_b64: str, raw_base: str) -> int:
    """Run the one-line installer with a generated payload (KIAN_PAYLOAD env)."""
    cmd = (f"export KIAN_PAYLOAD='{payload_b64}'\n"
           f"curl -fsSL {raw_base}/install.sh -o /tmp/kicdn.sh && bash /tmp/kicdn.sh")
    code, out, err = ssh.run(cmd, timeout=900)
    return code
