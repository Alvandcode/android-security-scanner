# Android Security Scanner & Antivirus

[![Stars](https://img.shields.io/github/stars/Alvandcode/android-security-scanner?style=flat-square)](https://github.com/Alvandcode/android-security-scanner/stargazers) [![License](https://img.shields.io/github/license/Alvandcode/android-security-scanner?style=flat-square)](./LICENSE) [![Last commit](https://img.shields.io/github/last-commit/Alvandcode/android-security-scanner?style=flat-square)](https://github.com/Alvandcode/android-security-scanner/commits)

> Heuristic Android security scanner & antivirus (no root, Termux-ready) with APK analysis and risk scoring.

<div dir="rtl">

## اسکنر امنیتی و آنتی‌ویروس اندروید

اسکنر امنیتی و آنتی‌ویروس هیوریستیک اندروید بدون نیاز به روت، مخصوص ترموکس؛ همراه با تحلیل فایل APK و امتیازدهی به ریسک امنیتی.

</div>

---

# ðŸ”’ Android Security Scanner & AntiVirus

[![Stars](https://img.shields.io/github/stars/Alvandcode/android-security-scanner?style=flat-square)](https://github.com/Alvandcode/android-security-scanner/stargazers)
[![License](https://img.shields.io/github/license/Alvandcode/android-security-scanner?style=flat-square)](./LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/Alvandcode/android-security-scanner?style=flat-square)](https://github.com/Alvandcode/android-security-scanner/commits)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](./requirements.txt)

> Heuristic Android security scanner & antivirus (no root, Termux-ready) with APK analysis and risk scoring.

Checks device settings (USB debugging, unknown sources, developer options), scans running processes for suspicious tools (Frida, Xposed, miners), deep-scans APK/APKS/XAPK files via `apktool`, and produces a 0â€“100 risk score + full JSON report with auto-fix for common issues.

## âœ¨ Features

- âœ… Device security checks (USB debugging, unknown sources, dev options)
- âœ… Running-process scan with suspicious-tool detection
- âœ… APK/APKS/XAPK static analysis (dangerous permissions, strings, packages)
- âœ… Heuristic 0â€“100 risk scoring
- âœ… JSON report + auto-fix for common issues
- âœ… No root required, Termux-ready

## ðŸ“¸ Demo

> TODO: add 1 screenshot or GIF to `docs/` â€” e.g. terminal output. Example:
> `docs/demo.png`

```text
Risk Score: 23/100 (Low)
[!] USB Debugging enabled
[!] 2 APKs request SEND_SMS + READ_CONTACTS
Report saved: /sdcard/strong_security_report.json
```

## ðŸš€ Quick Start

### Requirements

- Python 3.10+
- Termux (F-Droid build recommended) or Linux
- `apktool` (script checks/installs automatically)

### Install

```bash
pkg update && pkg upgrade -y
pkg install python apktool -y
git clone https://github.com/Alvandcode/android-security-scanner.git
cd android-security-scanner
pip install -r requirements.txt
```

### Run

```bash
python strong_security_av.py
# allow storage for full scan:
termux-setup-storage
```

Report: `/sdcard/strong_security_report.json`

## âš™ï¸ Options

| Option | Description |
|---|---|
| (interactive prompts) | choose scan type: quick / full APK scan / auto-fix |

## ðŸ“‚ Project Structure

```text
android-security-scanner/
â”œâ”€â”€ strong_security_av.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ docs/
â”œâ”€â”€ LICENSE
â””â”€â”€ README.md
```

## âš ï¸ Limitations

Heuristic tool â€” not a replacement for professional AVs like Malwarebytes. Large scans may take minutes. Malware removal is manual.

## ðŸ¤ Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Issues and PRs welcome!

## ðŸ”’ Security

See [SECURITY.md](./SECURITY.md).

## ðŸ“ License

MIT â€” see [LICENSE](./LICENSE).

---

â­ If useful: https://github.com/Alvandcode/android-security-scanner

---

## Contributing / مشارکت

- EN: Issues and Pull Requests are welcome. Please see `CONTRIBUTING.md`.
- FA: برای گزارش مشکل یا پیشنهاد قابلیت جدید، لطفا ایشو یا پول‌ریکوئست ثبت کنید.

## License / لایسنس

MIT — see [LICENSE](./LICENSE).

## Contact / ارتباط

- Telegram: https://t.me/a_c_official
- Website: https://alvandcode.github.io
