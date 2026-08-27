#!/usr/bin/env python3
"""
Android Security Scanner & AntiVirus - v2.0 (Rebuilt)
Advanced heuristic scanner for Android via Termux
No root required
"""

import os
import subprocess
import json
import re
import sys
import shutil
from datetime import datetime
from xml.etree import ElementTree as ET
from tqdm import tqdm


class AndroidSecurityScanner:
    def __init__(self):
        self.risk_score = 100
        self.issues = []
        self.malware_detected = []
        self.suspicious_processes = []
        self.security_settings = []
        self.apk_analysis = []
        self.fixed_issues = []

        # Dangerous permissions mapped to risk deduction
        self.dangerous_perms = {
            "READ_SMS": 5, "SEND_SMS": 8, "RECEIVE_SMS": 5,
            "READ_CONTACTS": 3, "WRITE_CONTACTS": 4,
            "ACCESS_FINE_LOCATION": 4, "ACCESS_COARSE_LOCATION": 2,
            "CAMERA": 3, "RECORD_AUDIO": 5,
            "READ_PHONE_STATE": 4, "CALL_PHONE": 6,
            "BIND_ACCESSIBILITY_SERVICE": 10,
            "SYSTEM_ALERT_WINDOW": 6,
            "WRITE_EXTERNAL_STORAGE": 2,
            "REQUEST_INSTALL_PACKAGES": 7,
            "BIND_DEVICE_ADMIN": 8
        }

        # Suspicious strings/patterns in decompiled code
        self.suspicious_patterns = [
            (r"frida", "Frida hooking framework detected"),
            (r"xposed", "Xposed framework reference found"),
            (r"substrate", "Substrate framework reference found"),
            (r"android/os/Debug", "Anti-debugging bypass attempt"),
            (r"getRuntime\(\)\.exec", "Shell command execution"),
            (r"/proc/self/status", "Anti-debug/VM detection"),
            (r"libjiagu", "Jiagu packer/obfuscator"),
            (r"libmobisec", "Aliyun/Mobisec obfuscation"),
            (r"libtup", "Tencent packer detected"),
            (r"http://[\d.]+|https://[\d.]+", "Hardcoded IP URL (suspicious)"),
            (r"smtp\.|ftp\.|telnet", "Suspicious network protocol"),
            (r"encrypt|decrypt|AES|RSA|DES", "Crypto operations (review needed)"),
            (r"hidden|stealth|spy|trojan", "Suspicious naming convention"),
        ]

        # Suspicious running processes
        self.suspicious_procs = ["frida", "frida-server", "xposed", "substrate",
                                  "magisk", "supersu", "busybox", "tcpdump"]

    def run_cmd(self, cmd, timeout=30):
        """Run shell command safely"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Timeout", 1
        except Exception as e:
            return "", str(e), 1

    def notify(self, title, content, priority="normal"):
        """Send Termux notification"""
        cmd = f'termux-notification --title "{title}" --content "{content}" --priority {priority}'
        self.run_cmd(cmd)

    def ensure_apktool(self):
        """Check and install apktool if missing"""
        if shutil.which("apktool"):
            return True
        print("🔧 apktool یافت نشد، در حال نصب...")
        out, err, code = self.run_cmd("pkg install apktool -y", timeout=120)
        if code != 0:
            print(f"❌ خطا در نصب apktool: {err}")
            return False
        return True

    def check_security_settings(self):
        """Scan critical Android security settings via settings global/secure"""
        print("🔐 بررسی تنظیمات امنیتی سیستم...")
        checks = [
            ("settings get global adb_enabled", "USB Debugging (ADB)", "1"),
            ("settings get global install_non_market_apps", "Unknown Sources", "1"),
            ("settings get global development_settings_enabled", "Developer Options", "1"),
            ("settings get secure lockscreen_disabled", "Lockscreen Disabled", "1"),
        ]

        for cmd, name, bad_value in checks:
            out, _, _ = self.run_cmd(cmd)
            if out == bad_value:
                self.security_settings.append({
                    "type": name,
                    "status": "خطر",
                    "value": out,
                    "recommendation": f"{name} فعال است. توصیه: غیرفعال کنید."
                })
                self.risk_score -= 8
            else:
                self.security_settings.append({
                    "type": name,
                    "status": "ایمن",
                    "value": out or "0",
                    "recommendation": "OK"
                })

    def fix_security_settings(self):
        """Auto-fix common security issues with user confirmation"""
        print("🔧 بررسی فیکس خودکار...")
        fixes = [
            ("settings put global adb_enabled 0", "USB Debugging", "adb_enabled"),
            ("settings put global install_non_market_apps 0", "Unknown Sources", "install_non_market_apps"),
            ("settings put global development_settings_enabled 0", "Developer Options", "development_settings_enabled"),
        ]

        for cmd, name, key in fixes:
            # Check if currently enabled
            out, _, _ = self.run_cmd(f"settings get global {key}")
            if out == "1":
                resp = input(f"   ⚠️ {name} فعال است. آیا می‌خواهید غیرفعال شود؟ (y/n): ").strip().lower()
                if resp == 'y':
                    _, err, code = self.run_cmd(cmd)
                    if code == 0:
                        self.fixed_issues.append(f"{name} غیرفعال شد.")
                        print(f"      ✅ {name} غیرفعال شد.")
                    else:
                        print(f"      ❌ خطا: {err}")

    def scan_processes(self):
        """Scan running processes for suspicious frameworks/tools"""
        print("🔍 اسکن فرآیندهای در حال اجرا...")
        out, _, _ = self.run_cmd("ps -A -o CMD= || ps -o comm=")
        if not out:
            return

        lines = out.lower().splitlines()
        for proc in self.suspicious_procs:
            for line in lines:
                if proc in line:
                    self.suspicious_processes.append({
                        "process": line.strip(),
                        "threat": f"ابزار/فریمورک {proc.upper()} در حال اجراست",
                        "risk": 15
                    })
                    self.risk_score -= 15
                    break

    def decompile_apk(self, apk_path, out_dir):
        """Decompile APK using apktool"""
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        cmd = f'apktool d "{apk_path}" -o "{out_dir}" -f -q'
        _, err, code = self.run_cmd(cmd, timeout=60)
        return code == 0

    def analyze_manifest(self, manifest_path):
        """Extract and score dangerous permissions from AndroidManifest.xml"""
        if not os.path.exists(manifest_path):
            return

        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            ns = {'android': 'http://schemas.android.com/apk/res/android'}

            perms = root.findall(".//uses-permission")
            found_perms = []

            for p in perms:
                attr = p.get('{http://schemas.android.com/apk/res/android}name')
                if attr:
                    # Extract simple name
                    perm_name = attr.split('.')[-1]
                    if perm_name in self.dangerous_perms:
                        found_perms.append({
                            "permission": perm_name,
                            "risk": self.dangerous_perms[perm_name],
                            "description": f"مجوز خطرناک: {perm_name}"
                        })
                        self.risk_score -= self.dangerous_perms[perm_name]

            # Check for suspicious receivers/services
            components = []
            for tag in ['receiver', 'service', 'activity']:
                for elem in root.findall(f".//{tag}"):
                    name = elem.get('{http://schemas.android.com/apk/res/android}name', '')
                    exported = elem.get('{http://schemas.android.com/apk/res/android}exported', 'false')
                    if exported == 'true' and any(k in name.lower() for k in ['download', 'admin', 'accessibility', 'sms']):
                        components.append({
                            "component": name,
                            "type": tag,
                            "risk": 5,
                            "description": f"{tag} exported با نام مشکوک: {name}"
                        })
                        self.risk_score -= 5

            return {"permissions": found_perms, "components": components}
        except Exception as e:
            return {"error": str(e)}

    def analyze_smali_strings(self, smali_dir):
        """Search suspicious patterns in smali and resources"""
        if not os.path.exists(smali_dir):
            return []

        matches = []
        files_scanned = 0

        for root, _, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(('.smali', '.xml', '.txt', '.json')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern, desc in self.suspicious_patterns:
                                if re.search(pattern, content, re.IGNORECASE):
                                    matches.append({
                                        "file": os.path.basename(filepath),
                                        "pattern": pattern,
                                        "description": desc,
                                        "risk": 7
                                    })
                                    self.risk_score -= 7
                                    break  # One match per file is enough
                        files_scanned += 1
                    except:
                        pass
        return matches

    def scan_apk_files(self):
        """Find and deeply analyze APK/APKS/XAPK files"""
        print("📦 اسکن و آنالیز عمیق فایل‌های APK...")
        paths = ["/sdcard/Download", "/sdcard/Downloads", "/storage/emulated/0/Download"]
        apks = []

        for base in paths:
            if os.path.exists(base):
                for root, _, files in os.walk(base):
                    for file in files:
                        if file.lower().endswith(('.apk', '.apks', '.xapk')):
                            apks.append(os.path.join(root, file))

        if not apks:
            return

        for apk_path in tqdm(apks, desc="آنالیز APKها", unit="file"):
            filename = os.path.basename(apk_path)
            print(f"   🔬 آنالیز: {filename}")

            out_dir = f"/tmp/av_scan_{os.path.splitext(filename)[0]}"

            if self.decompile_apk(apk_path, out_dir):
                manifest = os.path.join(out_dir, "AndroidManifest.xml")
                smali = os.path.join(out_dir, "smali")

                manifest_data = self.analyze_manifest(manifest) or {}
                smali_data = self.analyze_smali_strings(smali)

                total_risk = sum(p.get("risk", 0) for p in manifest_data.get("permissions", []))
                total_risk += sum(c.get("risk", 0) for c in manifest_data.get("components", []))
                total_risk += sum(s.get("risk", 0) for s in smali_data)

                status = "🟢 ایمن" if total_risk < 10 else "🟡 مشکوک" if total_risk < 30 else "🔴 خطرناک"

                self.apk_analysis.append({
                    "file": filename,
                    "path": apk_path,
                    "status": status,
                    "permissions": manifest_data.get("permissions", []),
                    "components": manifest_data.get("components", []),
                    "suspicious_strings": smali_data,
                    "total_risk": total_risk
                })

                if total_risk >= 15:
                    self.malware_detected.append({
                        "file": filename,
                        "recommendation": f"{status} - امتیاز ریسک: {total_risk}"
                    })

                # Cleanup
                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir)
            else:
                self.apk_analysis.append({
                    "file": filename,
                    "path": apk_path,
                    "status": "⚠️ خطا در آنالیز",
                    "error": "apktool failed"
                })

    def generate_html_report(self, report):
        """Generate a rich HTML report"""
        score = max(0, min(100, report['risk_score']))
        score_class = 'safe' if score >= 80 else 'warning' if score >= 50 else 'danger'
        score_text = '✅ ایمن' if score >= 80 else '⚠️ نیاز به بررسی' if score >= 50 else '🔴 خطرناک'

        html = f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>گزارش اسکن امنیتی اندروید</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; color: #333; }}
        .container {{ max-width: 900px; margin: auto; background: #fff; border-radius: 16px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        h1 {{ text-align: center; color: #1a237e; margin-bottom: 10px; }}
        .subtitle {{ text-align: center; color: #666; margin-bottom: 30px; }}
        .score-box {{ text-align: center; padding: 25px; border-radius: 12px; margin-bottom: 30px; }}
        .safe {{ background: #e8f5e9; color: #2e7d32; }}
        .warning {{ background: #fff3e0; color: #ef6c00; }}
        .danger {{ background: #ffebee; color: #c62828; }}
        .score-num {{ font-size: 56px; font-weight: bold; display: block; }}
        .score-label {{ font-size: 20px; margin-top: 5px; display: block; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #1a237e; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 12px; border: 1px solid #e0e0e0; text-align: right; }}
        th {{ background: #3f51b5; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .badge {{ padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        .b-danger {{ background: #ffcdd2; color: #b71c1c; }}
        .b-warning {{ background: #ffe0b2; color: #e65100; }}
        .b-safe {{ background: #c8e6c9; color: #1b5e20; }}
        .footer {{ text-align: center; margin-top: 30px; color: #999; font-size: 13px; }}
        ul {{ padding-right: 20px; }}
        li {{ margin-bottom: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 گزارش اسکن امنیتی اندروید</h1>
        <p class="subtitle">نسخه ۲.۰ | اسکن Heuristic پیشرفته</p>

        <div class="score-box {score_class}">
            <span class="score-num">{score}/100</span>
            <span class="score-label">{score_text}</span>
        </div>

        <div class="section">
            <h2>⚙️ تنظیمات امنیتی سیستم</h2>
            <table>
                <tr><th>تنظیم</th><th>وضعیت</th><th>توصیه</th></tr>
"""
        for item in report.get('security_settings', []):
            status_badge = 'b-danger' if item['status'] == 'خطر' else 'b-safe'
            html += f"<tr><td>{item['type']}</td><td><span class='badge {status_badge}'>{item['status']}</span></td><td>{item['recommendation']}</td></tr>"

        html += """
            </table>
        </div>

        <div class="section">
            <h2>🔍 فرآیندهای مشکوک</h2>
"""
        if report.get('suspicious_processes'):
            html += "<ul>"
            for p in report['suspicious_processes']:
                html += f"<li><strong>{p['process']}</strong> — {p['threat']}</li>"
            html += "</ul>"
        else:
            html += "<p>هیچ فرآیند مشکوکی یافت نشد ✅</p>"

        html += """
        </div>

        <div class="section">
            <h2>📦 آنالیز فایل‌های APK</h2>
"""
        for apk in report.get('apk_analysis', []):
            html += f"""
            <div style="margin-bottom:20px; padding:15px; background:#fafafa; border-radius:8px;">
                <h4>{apk['file']} <span class="badge {'b-danger' if '🔴' in apk['status'] else 'b-warning' if '🟡' in apk['status'] else 'b-safe'}">{apk['status']}</span></h4>
                <p><strong>مسیر:</strong> {apk.get('path','')}</p>
                <p><strong>مجوزهای خطرناک:</strong> {len(apk.get('permissions',[]))}</p>
                <p><strong>رشته‌های مشکوک:</strong> {len(apk.get('suspicious_strings',[]))}</p>
            </div>
            """

        html += """
        </div>

        <div class="section">
            <h2>🔧 فیکس‌های خودکار اعمال‌شده</h2>
"""
        if report.get('fixed_issues'):
            html += "<ul>"
            for fix in report['fixed_issues']:
                html += f"<li>✅ {fix}</li>"
            html += "</ul>"
        else:
            html += "<p>موردی فیکس نشده یا نیازی نبود.</p>"

        html += f"""
        </div>

        <div class="footer">
            <p>زمان اسکن: {report['timestamp']}</p>
            <p>Android Security Scanner v2.0</p>
        </div>
    </div>
</body>
</html>
"""
        report_path = "/sdcard/Android_Security_Report.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)
        return report_path

    def run_full_scan(self):
        print("=" * 50)
        print("🚀 Android Security Scanner v2.0")
        print("🔍 شروع اسکن کامل...")
        print("=" * 50)

        if not self.ensure_apktool():
            print("❌ apktool در دسترس نیست. اسکن APKها رد می‌شود.")

        self.check_security_settings()
        self.scan_processes()
        self.scan_apk_files()

        # Auto-fix prompt
        self.fix_security_settings()

        # Final score clamp
        self.risk_score = max(0, min(100, self.risk_score))

        status = "ایمن" if self.risk_score >= 80 else "هشدار" if self.risk_score >= 50 else "خطرناک"

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": self.risk_score,
            "status": status,
            "security_settings": self.security_settings,
            "suspicious_processes": self.suspicious_processes,
            "apk_analysis": self.apk_analysis,
            "malware_detected": self.malware_detected,
            "fixed_issues": self.fixed_issues,
            "details": self.malware_detected + self.suspicious_processes
        }

        # Save JSON
        json_path = "/sdcard/Android_Security_Report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # Save HTML
        html_path = self.generate_html_report(report)

        # Notify
        self.notify("اسکن امنیتی تکمیل شد", f"امتیاز: {self.risk_score} — {status}", "high")

        print("\n" + "=" * 50)
        print(f"📊 امتیاز نهایی: {self.risk_score}/100 — {status}")
        print(f"📄 گزارش HTML: {html_path}")
        print(f"📄 گزارش JSON: {json_path}")
        print(f"🦠 تهدیدات شناسایی‌شده: {len(self.malware_detected)}")
        print(f"⚙️ تنظیمات خطرناک: {sum(1 for s in self.security_settings if s['status']=='خطر')}")
        print("=" * 50)


if __name__ == "__main__":
    if not os.path.exists("/sdcard"):
        print("❌ این اسکریپت فقط در Termux قابل اجراست.")
        sys.exit(1)

    scanner = AndroidSecurityScanner()
    scanner.run_full_scan()
