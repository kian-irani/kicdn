"""Thin SSH wrapper — same contract as kian_v2ray/kv2m/core.py SSH (paramiko).
Reused so KICDN can install on the user's VPS from the GUI.
"""
class SSH:
    def __init__(self): self.client = None; self.host = None
    def connect(self, host, port=22, username="root", password=None, key_path=None, timeout=15):
        import paramiko
        c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        kw = dict(hostname=host, port=int(port), username=username, timeout=timeout,
                  allow_agent=False, look_for_keys=False)
        if key_path: kw["key_filename"] = key_path
        if password: kw["password"] = password
        c.connect(**kw); self.client = c; self.host = host; return self
    def run(self, command, timeout=180):
        if not self.client: raise RuntimeError("SSH not connected")
        _, out, err = self.client.exec_command(command, timeout=timeout)
        return out.channel.recv_exit_status(), out.read().decode("utf-8","replace"), err.read().decode("utf-8","replace")
    def close(self):
        if self.client:
            try: self.client.close()
            except Exception: pass
            self.client = None
