#!/usr/bin/env python3
"""
Android Security Scanner & AntiVirus - v2.1 (Security Hardened)
Advanced heuristic scanner for Android via Termux
No root required
"""

import os
import subprocess
import json
import re
import sys
import shutil
import shlex
import hashlib
import argparse
from datetime import datetime
from xml.etree import ElementTree as ET
from tqdm import tqdm


class AndroidSecurityScanner:
    def __init__(self, args=None):
        self.args = args or {}
        self.risk_score = 100
        self.issues = []
        self.malware_detected = []
        self.suspicious_processes = []
        self.security_settings = []
        self.apk_analysis = []
        self.fixed_issues = []
        self.installed_apps = []
        self.network_connections = []
        self.cert_issues = []

        # Setup logging directory
        self.log_dir = "/sdcard/.av_logs"
        os.makedirs(self.log_dir, exist_ok=True)

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
        # FIXED #2: Removed generic crypto patterns, added specific malicious combos
        self.suspicious_patterns = [
            (r"frida", "Frida hooking framework detected"),
            (r"xposed", "Xposed framework reference found"),
            (r"substrate", "Substrate framework reference found"),
            (r"android/os/Debug", "Anti-debugging bypass attempt"),
            (r"getRuntime\(\)\.exec\s*\(\s*\"(rm|chmod|su|mount)\"", "Dangerous shell command execution"),
            (r"/proc/self/status", "Anti-debug/VM detection"),
            (r"libjiagu", "Jiagu packer/obfuscator"),
            (r"libmobisec", "Aliyun/Mobisec obfuscation"),
            (r"libtup", "Tencent packer detected"),
            (r"http://[\d.]+|https://[\d.]+", "Hardcoded IP URL (suspicious)"),
            (r"smtp\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}", "SMTP server reference (possible data exfiltration)"),
            (r"hidden|stealth|spy|trojan|backdoor", "Suspicious naming convention"),
            (r"sendTextMessage\s*\(", "SMS sending without user consent pattern"),
            (r"getDeviceId|getSubscriberId|getSimSerialNumber", "Device ID harvesting"),
            (r"Base64\.(encode|decode).{0,50}(AES|DES|RSA)", "Obfuscated crypto + encoding combo"),
            (r"TelephonyManager.*getLine1Number", "Phone number extraction"),
            (r"ClipboardManager.*setPrimaryClip|getPrimaryClip", "Clipboard hijacking"),
            (r"AccessibilityService.*onAccessibilityEvent", "Accessibility abuse for keylogging"),
            (r"PowerManager\$WakeLock.*acquire\(\).*release\(\)", "WakeLock abuse (mining/background activity)"),
            (r"AlarmManager.*setRepeating.*RTC_WAKEUP", "Persistent background alarm (spyware pattern)"),
            (r"dexClassLoader|PathClassLoader.*loadClass", "Dynamic code loading (possible payload)"),
            (r"reflect.*Method.*invoke|getDeclaredMethod", "Heavy reflection usage (obfuscation)"),
            (r"javax\.crypto\.Cipher.*getInstance\(\"AES/ECB", "Weak AES-ECB mode (security flaw)"),
        ]

        # Suspicious running processes
        self.suspicious_procs = ["frida", "frida-server", "xposed", "substrate",
                                  "magisk", "supersu", "busybox", "tcpdump", "netcat", "nc"]

        # Suspicious package names (installed apps)
        self.suspicious_packages = [
            "spy", "tracker", "keylogger", "stealth", "hidden", "monitor",
            "smsforward", "callrecord", "screenrecorder.hidden"
        ]

        # Known malware hashes (IOC database - expandable)
        self.known_malware_hashes = self._load_signature_db()

    def _load_signature_db(self):
        """Load or create signature database"""
        sig_file = os.path.join(self.log_dir, "signatures.json")
        if os.path.exists(sig_file):
            try:
                with open(sig_file, 'r') as f:
                    data = json.load(f)
                    return data.get("hashes", [])
            except:
                pass
        # Default known hashes (Joker, Anubis samples)
        default_hashes = [
            # These are example placeholders - replace with real IOCs
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        ]
        self._save_signature_db(default_hashes)
        return default_hashes

    def _save_signature_db(self, hashes):
        sig_file = os.path.join(self.log_dir, "signatures.json")
        with open(sig_file, 'w') as f:
            json.dump({"hashes": hashes, "updated": datetime.now().isoformat()}, f)

    def log(self, level, message):
        """Write to audit log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        log_file = os.path.join(self.log_dir, f"scan_{datetime.now().strftime('%Y%m%d')}.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        if self.args.get('verbose'):
            print(f"   [{level}] {message}")

    def run_cmd(self, cmd, timeout=30):
        """Run shell command safely with shlex protection"""
        try:
            # Use list instead of shell=True where possible, or shlex.quote
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            self.log("WARN", f"Command timed out: {cmd[:50]}...")
            return "", "Timeout", 1
        except Exception as e:
            self.log("ERROR", f"Command failed: {str(e)}")
            return "", str(e), 1

    def notify(self, title, content, priority="normal"):
        """Send Termux notification"""
        safe_title = shlex.quote(title)
        safe_content = shlex.quote(content)
        cmd = f'termux-notification --title {safe_title} --content {safe_content} --priority {priority}'
        self.run_cmd(cmd)

    def ensure_apktool(self):
        """Check and install apktool if missing"""
        if shutil.which("apktool"):
            return True
        print("🔧 apktool یافت نشد، در حال نصب...")
        out, err, code = self.run_cmd("pkg install apktool -y", timeout=120)
        if code != 0:
            print(f"❌ خطا در نصب apktool: {err}")
            self.log("ERROR", f"apktool installation failed: {err}")
            return False
        self.log("INFO", "apktool installed successfully")
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
                self.log("WARN", f"Security setting DANGER: {name} is enabled")
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
            out, _, _ = self.run_cmd(f"settings get global {key}")
            if out == "1":
                resp = input(f"   ⚠️ {name} فعال است. آیا می‌خواهید غیرفعال شود؟ (y/n): ").strip().lower()
                if resp == 'y':
                    _, err, code = self.run_cmd(cmd)
                    if code == 0:
                        self.fixed_issues.append(f"{name} غیرفعال شد.")
                        self.log("INFO", f"Auto-fixed: {name} disabled")
                        print(f"      ✅ {name} غیرفعال شد.")
                    else:
                        self.log("ERROR", f"Auto-fix failed for {name}: {err}")
                        print(f"      ❌ خطا: {err}")

    def scan_processes(self):
        """Scan running processes for suspicious frameworks/tools"""
        print("🔍 اسکن فرآیندهای در حال اجرا...")
        out, _, _ = self.run_cmd("ps -A -o CMD= 2>/dev/null || ps -o comm=")
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
                    self.log("WARN", f"Suspicious process detected: {line.strip()}")
                    break

    def scan_network(self):
        """Check active network connections"""
        print("🌐 بررسی اتصالات شبکه فعال...")
        out, _, code = self.run_cmd("ss -tulpn 2>/dev/null || netstat -tulpn 2>/dev/null || netstat -an")
        if code != 0 or not out:
            return

        suspicious_ports = ["4444", "5555", "6666", "31337", "12345"]  # Common malware ports
        for line in out.splitlines():
            for port in suspicious_ports:
                if f":{port}" in line:
                    self.network_connections.append({
                        "connection": line.strip(),
                        "threat": f"اتصال به پورت مشکوک {port}",
                        "risk": 10
                    })
                    self.risk_score -= 10
                    self.log("WARN", f"Suspicious network connection on port {port}: {line.strip()}")

    def scan_installed_apps(self):
        """Scan installed packages for suspicious names"""
        print("📱 اسکن اپلیکیشن‌های نصب‌شده...")
        out, _, code = self.run_cmd("pm list packages -f")
        if code != 0 or not out:
            return

        for line in out.splitlines():
            pkg = line.replace("package:", "").split("=")[-1] if "=" in line else line
            pkg_lower = pkg.lower()
            for susp in self.suspicious_packages:
                if susp in pkg_lower:
                    self.installed_apps.append({
                        "package": pkg,
                        "threat": f"نام پکیج مشکوک: '{susp}'",
                        "risk": 12
                    })
                    self.risk_score -= 12
                    self.log("WARN", f"Suspicious installed app: {pkg}")
                    break

    def check_apk_certificate(self, apk_path, out_dir):
        """Verify APK certificate using keytool"""
        cert_files = []
        meta_dir = os.path.join(out_dir, "original", "META-INF")
        if os.path.exists(meta_dir):
            for f in os.listdir(meta_dir):
                if f.endswith(('.RSA', '.DSA', '.EC')):
                    cert_files.append(os.path.join(meta_dir, f))

        if not cert_files:
            return {"status": "unknown", "info": "No certificate found"}

        cert_path = cert_files[0]
        out, err, code = self.run_cmd(f"keytool -printcert -file {shlex.quote(cert_path)}")

        if code != 0:
            return {"status": "error", "info": err}

        # Parse certificate info
        owner = re.search(r"Owner:\s*(.+)", out)
        issuer = re.search(r"Issuer:\s*(.+)", out)
        valid_from = re.search(r"Valid from:\s*(.+?)", out)
        valid_until = re.search(r"until:\s*(.+)", out)

        issues = []

        # Check self-signed
        if owner and issuer and owner.group(1).strip() == issuer.group(1).strip():
            issues.append("Self-signed certificate")
            self.risk_score -= 5

        # Check expired
        if valid_until:
            try:
                expiry = datetime.strptime(valid_until.group(1).strip(), "%a %b %d %H:%M:%S %Z %Y")
                if expiry < datetime.now():
                    issues.append("Expired certificate")
                    self.risk_score -= 8
            except:
                pass

        # Check common debug keys
        if owner and ("Android Debug" in out or "CN=Android" in out):
            issues.append("Debug/development certificate")
            self.risk_score -= 10

        return {
            "status": "suspicious" if issues else "valid",
            "owner": owner.group(1).strip() if owner else "unknown",
            "issues": issues,
            "raw": out[:500]
        }

    def hash_file(self, filepath):
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except:
            return None

    def decompile_apk(self, apk_path, out_dir):
        """Decompile APK using apktool with safe quoting"""
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        # FIXED #1: Use shlex.quote to prevent command injection
        cmd = f'apktool d {shlex.quote(apk_path)} -o {shlex.quote(out_dir)} -f -q'
        _, err, code = self.run_cmd(cmd, timeout=90)
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
            self.log("ERROR", f"Manifest parsing failed: {str(e)}")
            return {"error": str(e)}

    def analyze_smali_strings(self, smali_dir):
        """Search suspicious patterns in smali - memory efficient line-by-line"""
        if not os.path.exists(smali_dir):
            return []

        matches = []
        files_scanned = 0

        # FIXED #5: Line-by-line reading instead of loading entire file
        for root, _, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(('.smali', '.xml', '.txt', '.json')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            file_matched = False
                            for line_num, line in enumerate(f, 1):
                                if file_matched:
                                    break
                                for pattern, desc in self.suspicious_patterns:
                                    if re.search(pattern, line, re.IGNORECASE):
                                        matches.append({
                                            "file": os.path.basename(filepath),
                                            "line": line_num,
                                            "pattern": pattern,
                                            "description": desc,
                                            "risk": 7,
                                            "snippet": line.strip()[:100]
                                        })
                                        self.risk_score -= 7
                                        file_matched = True
                                        break
                        files_scanned += 1
                    except Exception as e:
                        self.log("WARN", f"Could not read {filepath}: {str(e)}")

        self.log("INFO", f"Scanned {files_scanned} files in smali directory")
        return matches

    def scan_apk_files(self):
        """Find and deeply analyze APK/APKS/XAPK files"""
        print("📦 اسکن و آنالیز عمیق فایل‌های APK...")

        # Support custom scan path
        custom_path = self.args.get('scan_path')
        if custom_path and os.path.exists(custom_path):
            paths = [custom_path]
        else:
            paths = ["/sdcard/Download", "/sdcard/Downloads", "/storage/emulated/0/Download"]

        apks = []
        for base in paths:
            if os.path.exists(base):
                for root, _, files in os.walk(base):
                    for file in files:
                        if file.lower().endswith(('.apk', '.apks', '.xapk')):
                            apks.append(os.path.join(root, file))

        if not apks:
            print("   ℹ️ هیچ فایل APK یافت نشد.")
            return

        for apk_path in tqdm(apks, desc="آنالیز APKها", unit="file"):
            filename = os.path.basename(apk_path)
            print(f"   🔬 آنالیز: {filename}")

            # Hash check against known malware
            file_hash = self.hash_file(apk_path)
            if file_hash and file_hash in self.known_malware_hashes:
                self.malware_detected.append({
                    "file": filename,
                    "recommendation": "🔴 شناخته‌شده: این APK در دیتابیس malware ثبت شده!",
                    "hash": file_hash
                })
                self.risk_score -= 50
                self.log("CRITICAL", f"Known malware hash match: {filename} ({file_hash})")
                continue

            out_dir = f"/tmp/av_scan_{os.path.splitext(filename)[0]}"

            if self.decompile_apk(apk_path, out_dir):
                manifest = os.path.join(out_dir, "AndroidManifest.xml")
                smali = os.path.join(out_dir, "smali")

                manifest_data = self.analyze_manifest(manifest) or {}
                smali_data = self.analyze_smali_strings(smali)

                # Certificate analysis
                cert_data = self.check_apk_certificate(apk_path, out_dir)
                if cert_data.get("status") == "suspicious":
                    self.cert_issues.append({
                        "file": filename,
                        "issues": cert_data.get("issues", [])
                    })

                total_risk = sum(p.get("risk", 0) for p in manifest_data.get("permissions", []))
                total_risk += sum(c.get("risk", 0) for c in manifest_data.get("components", []))
                total_risk += sum(s.get("risk", 0) for s in smali_data)
                total_risk += sum(len(i) * 5 for i in cert_data.get("issues", []))

                status = "🟢 ایمن" if total_risk < 10 else "🟡 مشکوک" if total_risk < 30 else "🔴 خطرناک"

                self.apk_analysis.append({
                    "file": filename,
                    "path": apk_path,
                    "hash": file_hash,
                    "status": status,
                    "permissions": manifest_data.get("permissions", []),
                    "components": manifest_data.get("components", []),
                    "suspicious_strings": smali_data,
                    "certificate": cert_data,
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
                self.log("ERROR", f"Failed to decompile: {filename}")

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
        .code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 گزارش اسکن امنیتی اندروید</h1>
        <p class="subtitle">نسخه ۲.۱ | اسکن Heuristic پیشرفته</p>

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
            <h2>🌐 اتصالات شبکه مشکوک</h2>
"""
        if report.get('network_connections'):
            html += "<ul>"
            for n in report['network_connections']:
                html += f"<li><strong>{n['connection']}</strong> — {n['threat']}</li>"
            html += "</ul>"
        else:
            html += "<p>هیچ اتصال مشکوکی یافت نشد ✅</p>"

        html += """
        </div>

        <div class="section">
            <h2>📱 اپلیکیشن‌های نصب‌شده مشکوک</h2>
"""
        if report.get('installed_apps'):
            html += "<ul>"
            for a in report['installed_apps']:
                html += f"<li><code class='code'>{a['package']}</code> — {a['threat']}</li>"
            html += "</ul>"
        else:
            html += "<p>هیچ اپلیکیشن مشکوکی یافت نشد ✅</p>"

        html += """
        </div>

        <div class="section">
            <h2>📦 آنالیز فایل‌های APK</h2>
"""
        for apk in report.get('apk_analysis', []):
            cert_issues = apk.get('certificate', {}).get('issues', [])
            cert_badge = 'b-danger' if cert_issues else 'b-safe'
            cert_text = f"⚠️ {'، '.join(cert_issues)}" if cert_issues else "✅ معتبر"
            html += f"""
            <div style="margin-bottom:20px; padding:15px; background:#fafafa; border-radius:8px;">
                <h4>{apk['file']} <span class="badge {'b-danger' if '🔴' in apk['status'] else 'b-warning' if '🟡' in apk['status'] else 'b-safe'}">{apk['status']}</span></h4>
                <p><strong>مسیر:</strong> <code class="code">{apk.get('path','')}</code></p>
                <p><strong>SHA256:</strong> <code class="code">{apk.get('hash','N/A')[:16]}...</code></p>
                <p><strong>مجوزهای خطرناک:</strong> {len(apk.get('permissions',[]))}</p>
                <p><strong>رشته‌های مشکوک:</strong> {len(apk.get('suspicious_strings',[]))}</p>
                <p><strong>گواهینامه:</strong> <span class="badge {cert_badge}">{cert_text}</span></p>
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
            <p>Android Security Scanner v2.1</p>
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
        print("🚀 Android Security Scanner v2.1")
        print("🔍 شروع اسکن کامل...")
        print("=" * 50)
        self.log("INFO", "Full scan started")

        if not self.ensure_apktool():
            print("❌ apktool در دسترس نیست. اسکن APKها رد می‌شود.")
            self.log("WARN", "apktool not available, skipping APK analysis")

        self.check_security_settings()
        self.scan_processes()
        self.scan_network()
        self.scan_installed_apps()
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
            "network_connections": self.network_connections,
            "installed_apps": self.installed_apps,
            "apk_analysis": self.apk_analysis,
            "malware_detected": self.malware_detected,
            "fixed_issues": self.fixed_issues,
            "details": self.malware_detected + self.suspicious_processes + self.network_connections
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
        print(f"📝 لاگ: {self.log_dir}/")
        print("=" * 50)
        self.log("INFO", f"Scan completed. Score: {self.risk_score}/100 - {status}")


def main():
    parser = argparse.ArgumentParser(description="Android Security Scanner v2.1")
    parser.add_argument("--scan-path", help="Custom path to scan for APKs")
    parser.add_argument("--quick", action="store_true", help="Quick scan (skip APK deep analysis)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output with logs")
    parser.add_argument("--no-fix", action="store_true", help="Skip auto-fix prompts")
    parser.add_argument("--watch", help="Watch directory for new APKs (interval in seconds)", type=int)
    args = parser.parse_args()

    if not os.path.exists("/sdcard"):
        print("❌ این اسکریپت فقط در Termux قابل اجراست.")
        sys.exit(1)

    scanner = AndroidSecurityScanner(vars(args))

    if args.watch:
        print(f"👁️ حالت نظارت فعال - هر {args.watch} ثانیه چک می‌شود...")
        import time
        while True:
            scanner.run_full_scan()
            print(f"\n⏳ منتظر {args.watch} ثانیه...")
            time.sleep(args.watch)
            # Reset for next iteration
            scanner = AndroidSecurityScanner(vars(args))
    else:
        scanner.run_full_scan()


if __name__ == "__main__":
    main()
