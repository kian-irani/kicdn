#!/usr/bin/env python3
"""KICDN Windows GUI — PySide6, دو‌زبانه EN/FA, dark theme (TASK-020)."""
import sys, json, queue
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit,
    QGroupBox, QMessageBox,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.models import Config, Server, Credentials, ApiKeys
from core import config_generator

APP_VERSION = "0.1.0"

# ── palette ──────────────────────────────────────────────────────────────────
BG   = "#0c1118"; CARD = "#131c27"; ACC = "#2ee6a6"
TXT  = "#e7eef5"; MUT  = "#8ba0b4"; ERR = "#ff6b6b"
FONT = "Segoe UI"; MONO = "Consolas"

QSS = f"""
QMainWindow, QWidget     {{ background:{BG}; color:{TXT}; font-family:{FONT}; font-size:10pt; }}
QTabWidget::pane         {{ border:1px solid #283a4d; }}
QTabBar::tab             {{ background:{CARD}; color:{MUT}; padding:8px 18px; }}
QTabBar::tab:selected    {{ background:{ACC}; color:#04130d; font-weight:bold; }}
QGroupBox                {{ border:1px solid #283a4d; border-radius:4px; margin-top:10px; color:{MUT}; }}
QGroupBox::title         {{ subcontrol-origin:margin; left:8px; padding:0 4px; color:{ACC}; }}
QLineEdit                {{ background:{CARD}; border:1px solid #283a4d; border-radius:3px;
                            color:{TXT}; padding:4px 8px; }}
QLineEdit:focus          {{ border-color:{ACC}; }}
QComboBox                {{ background:{CARD}; border:1px solid #283a4d; border-radius:3px;
                            color:{TXT}; padding:4px 8px; }}
QComboBox QAbstractItemView {{ background:{CARD}; color:{TXT}; selection-background-color:{ACC}; }}
QTextEdit                {{ background:#080c11; border:1px solid #283a4d;
                            color:#bfe9d8; font-family:{MONO}; font-size:9pt; }}
QPushButton              {{ background:#1e3a4a; border:1px solid #283a4d; border-radius:3px;
                            color:{TXT}; padding:6px 18px; }}
QPushButton:hover        {{ background:#25495e; }}
QPushButton#accent       {{ background:{ACC}; color:#04130d; font-weight:bold; border:none; }}
QPushButton#accent:hover {{ background:#22d3ee; }}
QPushButton#danger       {{ background:#7f1d1d; color:{TXT}; border:none; }}
QPushButton#danger:hover {{ background:#991b1b; }}
QLabel#ok  {{ color:{ACC}; font-weight:bold; }}
QLabel#err {{ color:{ERR}; font-weight:bold; }}
"""

PROTOCOLS = ["reality", "mhrv", "warp", "ss"]
ROUTING   = ["bypass_ir", "full_tunnel", "custom"]

L = {
    "en": dict(
        title="KICDN — Censorship Circumvention",
        tab_setup="Setup", tab_connect="Connect", tab_logs="Logs",
        grp_server="Server", grp_creds="Credentials", grp_api="API Keys (optional)",
        host="Host / IP", port="Port", domain="Domain (SNI)",
        protocol="Protocol", routing="Routing",
        uuid="UUID", pubkey="Public Key", shortid="Short ID", password="Password",
        cf="Cloudflare Token", groq="Groq API Key",
        gdrive="GDrive Folder ID", vercel="Vercel Token", netlify="Netlify Token",
        profile="Profile Name", btn_gen="Generate Config",
        btn_connect="Connect", btn_disconnect="Disconnect", btn_clear="Clear Logs",
        st_ready="● Ready", st_ok="● Connected", st_err="● Disconnected",
        cfg_hint="Generated config (JSON) will appear here",
    ),
    "fa": dict(
        title="KiCDN — دور زدن فیلتر",
        tab_setup="تنظیمات", tab_connect="اتصال", tab_logs="لاگ",
        grp_server="سرور", grp_creds="احراز هویت", grp_api="کلیدهای API (اختیاری)",
        host="آدرس / IP", port="پورت", domain="دامنه (SNI)",
        protocol="پروتکل", routing="مسیریابی",
        uuid="UUID", pubkey="کلید عمومی", shortid="Short ID", password="رمز",
        cf="توکن Cloudflare", groq="کلید Groq",
        gdrive="شناسه GDrive", vercel="توکن Vercel", netlify="توکن Netlify",
        profile="نام پروفایل", btn_gen="ساخت کانفیگ",
        btn_connect="اتصال", btn_disconnect="قطع", btn_clear="پاک کردن لاگ",
        st_ready="● آماده", st_ok="● متصل", st_err="● قطع",
        cfg_hint="کانفیگ ساخته‌شده (JSON) اینجا نمایش داده می‌شود",
    ),
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = "fa"
        self._lq: queue.Queue = queue.Queue()
        self._connected = False
        self._cfg_json = ""
        self._build_ui()
        QTimer(self, timeout=self._drain_log, interval=100).start()

    # ── build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        t = L[self.lang]
        self.setWindowTitle(f"{t['title']}  v{APP_VERSION}")
        self.resize(920, 660)
        self.setStyleSheet(QSS)

        root = QWidget(); self.setCentralWidget(root)
        vlay = QVBoxLayout(root); vlay.setContentsMargins(8, 8, 8, 4)

        top = QHBoxLayout()
        self.lbl_st = QLabel(t["st_err"]); self.lbl_st.setObjectName("err")
        top.addWidget(self.lbl_st); top.addStretch()
        btn_lang = QPushButton("EN / فا"); btn_lang.setFixedWidth(72)
        btn_lang.clicked.connect(self._toggle_lang); top.addWidget(btn_lang)
        vlay.addLayout(top)

        self.tabs = QTabWidget()
        vlay.addWidget(self.tabs)
        self._build_setup(); self._build_connect(); self._build_logs()

    def _build_setup(self):
        t = L[self.lang]; page = QWidget(); lay = QVBoxLayout(page)

        g1 = QGroupBox(t["grp_server"]); f1 = QFormLayout(g1)
        self.e_host   = QLineEdit(); self.e_host.setPlaceholderText("1.2.3.4")
        self.e_port   = QLineEdit("443"); self.e_port.setFixedWidth(80)
        self.e_domain = QLineEdit(); self.e_domain.setPlaceholderText("vpn.example.com")
        self.cb_proto = QComboBox(); self.cb_proto.addItems(PROTOCOLS)
        self.cb_route = QComboBox(); self.cb_route.addItems(ROUTING)
        for lbl, w in [(t["host"], self.e_host), (t["port"], self.e_port),
                       (t["domain"], self.e_domain), (t["protocol"], self.cb_proto),
                       (t["routing"], self.cb_route)]:
            f1.addRow(lbl, w)
        lay.addWidget(g1)

        g2 = QGroupBox(t["grp_creds"]); f2 = QFormLayout(g2)
        self.e_uuid   = QLineEdit(); self.e_uuid.setPlaceholderText("auto if empty")
        self.e_pubkey = QLineEdit()
        self.e_sid    = QLineEdit()
        self.e_pass   = QLineEdit(); self.e_pass.setEchoMode(QLineEdit.Password)
        for lbl, w in [(t["uuid"], self.e_uuid), (t["pubkey"], self.e_pubkey),
                       (t["shortid"], self.e_sid), (t["password"], self.e_pass)]:
            f2.addRow(lbl, w)
        lay.addWidget(g2)

        g3 = QGroupBox(t["grp_api"]); f3 = QFormLayout(g3)
        self.e_cf      = QLineEdit(); self.e_cf.setEchoMode(QLineEdit.Password)
        self.e_groq    = QLineEdit(); self.e_groq.setEchoMode(QLineEdit.Password)
        self.e_gdrive  = QLineEdit()
        self.e_vercel  = QLineEdit(); self.e_vercel.setEchoMode(QLineEdit.Password)
        self.e_netlify = QLineEdit(); self.e_netlify.setEchoMode(QLineEdit.Password)
        for lbl, w in [(t["cf"], self.e_cf), (t["groq"], self.e_groq),
                       (t["gdrive"], self.e_gdrive), (t["vercel"], self.e_vercel),
                       (t["netlify"], self.e_netlify)]:
            f3.addRow(lbl, w)
        lay.addWidget(g3)

        bot = QHBoxLayout()
        self.e_profile = QLineEdit("default"); self.e_profile.setFixedWidth(140)
        bot.addWidget(QLabel(t["profile"])); bot.addWidget(self.e_profile)
        bot.addStretch()
        self.btn_gen = QPushButton(t["btn_gen"]); self.btn_gen.setObjectName("accent")
        self.btn_gen.clicked.connect(self._generate); bot.addWidget(self.btn_gen)
        lay.addLayout(bot)

        self.txt_cfg = QTextEdit(); self.txt_cfg.setReadOnly(True)
        self.txt_cfg.setPlaceholderText(t["cfg_hint"]); self.txt_cfg.setFixedHeight(150)
        lay.addWidget(self.txt_cfg)

        self.tabs.addTab(page, t["tab_setup"])

    def _build_connect(self):
        t = L[self.lang]; page = QWidget(); lay = QVBoxLayout(page)
        lay.setAlignment(Qt.AlignTop)

        grp = QGroupBox("Connection"); g_lay = QVBoxLayout(grp)
        self.lbl_st2 = QLabel(t["st_err"]); self.lbl_st2.setObjectName("err")
        self.lbl_st2.setAlignment(Qt.AlignCenter)
        self.lbl_st2.setFont(QFont(FONT, 14, QFont.Bold))
        g_lay.addWidget(self.lbl_st2)

        row = QHBoxLayout()
        self.btn_con = QPushButton(t["btn_connect"]); self.btn_con.setObjectName("accent")
        self.btn_con.setFixedHeight(44); self.btn_con.clicked.connect(self._connect)
        self.btn_dis = QPushButton(t["btn_disconnect"]); self.btn_dis.setObjectName("danger")
        self.btn_dis.setFixedHeight(44); self.btn_dis.setEnabled(False)
        self.btn_dis.clicked.connect(self._disconnect)
        row.addWidget(self.btn_con); row.addWidget(self.btn_dis)
        g_lay.addLayout(row)
        lay.addWidget(grp)

        self.txt_con_info = QTextEdit(); self.txt_con_info.setReadOnly(True)
        self.txt_con_info.setPlaceholderText("Generate a config in Setup tab first.")
        lay.addWidget(self.txt_con_info)
        self.tabs.addTab(page, t["tab_connect"])

    def _build_logs(self):
        t = L[self.lang]; page = QWidget(); lay = QVBoxLayout(page)
        self.txt_log = QTextEdit(); self.txt_log.setReadOnly(True)
        lay.addWidget(self.txt_log)
        btn_clr = QPushButton(t["btn_clear"]); btn_clr.clicked.connect(self.txt_log.clear)
        lay.addWidget(btn_clr)
        self.tabs.addTab(page, t["tab_logs"])

    # ── actions ───────────────────────────────────────────────────────────────

    def _generate(self):
        try:
            port = int(self.e_port.text().strip() or "443")
        except ValueError:
            port = 443

        cfg = Config(
            profile_name=self.e_profile.text().strip() or "default",
            protocol=self.cb_proto.currentText(),
            server=Server(
                host=self.e_host.text().strip(),
                port=port,
                domain=self.e_domain.text().strip(),
            ),
            credentials=Credentials(
                uuid=self.e_uuid.text().strip(),
                public_key=self.e_pubkey.text().strip(),
                short_id=self.e_sid.text().strip(),
                password=self.e_pass.text().strip(),
            ),
            routing=self.cb_route.currentText(),
            api_keys=ApiKeys(
                cloudflare=self.e_cf.text().strip(),
                groq=self.e_groq.text().strip(),
                gdrive=self.e_gdrive.text().strip(),
                vercel=self.e_vercel.text().strip(),
                netlify=self.e_netlify.text().strip(),
            ),
        )
        try:
            result = config_generator.generate(cfg)
            self._cfg_json = json.dumps(result, ensure_ascii=False, indent=2)
            self.txt_cfg.setPlainText(self._cfg_json)
            self.txt_con_info.setPlainText(self._cfg_json)
            self._log(f"[KICDN] Config generated — protocol={cfg.protocol} routing={cfg.routing}")
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
            self._log(f"[ERROR] {exc}")

    def _connect(self):
        if not self._cfg_json:
            QMessageBox.warning(self, "", "Generate a config first / ابتدا کانفیگ بساز")
            return
        self._connected = True
        self._set_status("ok")
        self.btn_con.setEnabled(False); self.btn_dis.setEnabled(True)
        self._log("[KICDN] Connect — tunnel engine wired in TASK-021")

    def _disconnect(self):
        self._connected = False
        self._set_status("err")
        self.btn_con.setEnabled(True); self.btn_dis.setEnabled(False)
        self._log("[KICDN] Disconnected")

    def _set_status(self, obj: str):
        t = L[self.lang]
        text = t["st_ok"] if obj == "ok" else t["st_err"]
        for lbl in (self.lbl_st, self.lbl_st2):
            lbl.setText(text); lbl.setObjectName(obj)
            lbl.style().unpolish(lbl); lbl.style().polish(lbl)

    # ── logging ───────────────────────────────────────────────────────────────

    def _log(self, msg: str):
        self._lq.put(msg)

    def _drain_log(self):
        try:
            while True:
                self.txt_log.append(self._lq.get_nowait())
        except queue.Empty:
            pass

    # ── language ──────────────────────────────────────────────────────────────

    def _toggle_lang(self):
        self.lang = "en" if self.lang == "fa" else "fa"
        QMessageBox.information(
            self, "Language / زبان",
            "Restart to apply.\nبرای اعمال، برنامه را مجدد اجرا کنید.",
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
