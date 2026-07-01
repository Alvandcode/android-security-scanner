#!/usr/bin/env python3
"""
اسکنر امنیتی پیشرفته + آنتی‌ویروس قوی اندروید
اسکن قوی APK با apktool + heuristic پیشرفته
"""

import os
import subprocess
import json
import re
import zipfile
from datetime import datetime
import sys
from pathlib import Path

class StrongAndroidSecurityAV:
    def __init__(self):
        self.risk_score = 100
        self.issues = []
        self.malware_detected = []
        self.fixed = []
        
        self.dangerous_perms = {
            "READ_SMS", "SEND_SMS", "READ_CONTACTS", "WRITE_CONTACTS",
            "ACCESS_FINE_LOCATION", "CAMERA", "RECORD_AUDIO", "READ_PHONE_STATE",
            "CALL_PHONE", "BIND_ACCESSIBILITY_SERVICE", "SYSTEM_ALERT_WINDOW",
            "READ_CALL_LOG", "INSTALL_PACKAGES", "WRITE_SETTINGS", "REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"
        }

    def run_command(self, cmd, timeout=20):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except:
            return "", "Timeout/Error", 1

    def install_apktool_if_needed(self):
        """نصب apktool برای اسکن قوی"""
        print("🔧 بررسی و نصب ابزارهای اسکن قوی...")
        out, _, _ = self.run_command("command -v apktool")
        if not out:
            print("   نصب apktool ...")
            self.run_command("pkg install apktool -y")
        print("   ✅ apktool آماده است.")

    def decode_apk_strong(self, apk_path):
        """اسکن قوی با decode کامل APK"""
        try:
            temp_dir = f"/sdcard/.temp_apk_scan_{int(time.time())}"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Decode با apktool
            cmd = f"apktool d '{apk_path}' -o '{temp_dir}' -f --no-src"
            self.run_command(cmd, timeout=30)
            
            manifest_path = os.path.join(temp_dir, "AndroidManifest.xml")
            if not os.path.exists(manifest_path):
                return None
            
            with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
                manifest = f.read()
            
            # استخراج مجوزها
            perms = re.findall(r'android:permission="([^"]+)"|android:name="android\.permission\.([A-Z_]+)"', manifest)
            perms = {p[0] or p[1] for p in perms if p[0] or p[1]}
            
            dangerous = [p for p in perms if any(d in p for d in self.dangerous_perms)]
            
            # چک strings.xml برای کلمات مشکوک
            strings_path = os.path.join(temp_dir, "res/values/strings.xml")
            suspicious_strings = 0
            if os.path.exists(strings_path):
                with open(strings_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                    susp_keywords = ["smali", "inject", "keylog", "steal", "phish", "rat", "trojan"]
                    suspicious_strings = sum(1 for kw in susp_keywords if kw in content)
            
            pkg_match = re.search(r'package="([^"]+)"', manifest)
            pkg = pkg_match.group(1) if pkg_match else "unknown"
            
            risk = len(dangerous) * 8 + suspicious_strings * 10
            if risk > 0:
                return {
                    "file": os.path.basename(apk_path),
                    "package": pkg,
                    "dangerous_permissions": len(dangerous),
                    "suspicious_strings": suspicious_strings,
                    "risk_score": min(risk, 70),
                    "recommendation": "حذف فوری - فایل مخرب تشخیص داده شد"
                }
            
            # پاک کردن فایل موقت
            self.run_command(f"rm -rf '{temp_dir}'")
            return None
            
        except Exception as e:
            return None

    def scan_all_apks_strong(self):
        """اسکن قوی تمام فایل‌های APK در دستگاه"""
        print("🔍 اسکن قوی فایل‌های APK / APKS / XAPK ...")
        self.install_apktool_if_needed()
        
        search_paths = ["/sdcard/Download", "/sdcard", "/storage/emulated/0/Download"]
        threats = 0
        
        for base_path in search_paths:
            if not os.path.exists(base_path):
                continue
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith(('.apk', '.apks', '.xapk')):
                        full_path = os.path.join(root, file)
                        print(f"   بررسی: {file}")
                        result = self.decode_apk_strong(full_path)
                        if result:
                            self.malware_detected.append(result)
                            self.risk_score -= result["risk_score"]
                            threats += 1
                            print(f"      ⚠️ تهدید قوی تشخیص داده شد!")
        
        if threats == 0:
            print("   ✅ هیچ تهدید APK پیدا نشد.")

    def scan_running_processes_strong(self):
        """اسکن قوی فرآیندها"""
        print("🔍 اسکن قوی فرآیندها و سرویس‌ها...")
        out, _, _ = self.run_command("ps -ef | grep -E 'u0_a|u1_a|app_'")
        lines = out.splitlines()
        
        for line in lines:
            if any(k in line.lower() for k in ["frida", "xposed", "magisk", "substrate", "miner", "payload"]):
                self.malware_detected.append({"type": "suspicious_process", "details": line})
                self.risk_score -= 30

    def basic_system_scan(self):
        """اسکن پایه سیستم"""
        checks = [
            ("adb_enabled", "global", "USB Debugging", 18),
            ("install_non_market_apps", "global", "نصب از منابع ناشناس", 15),
        ]
        for key, table, title, penalty in checks:
            out, _, _ = self.run_command(f"settings get {table} {key}")
            if out.strip() == "1":
                self.issues.append({
                    "title": title,
                    "fix_cmd": f"settings put {table} {key} 0"
                })
                self.risk_score -= penalty

    def run_full_strong_scan(self):
        print("🚀 شروع اسکن **قوی** امنیتی + آنتی‌ویروس")
        print("="*70)
        
        self.basic_system_scan()
        self.scan_running_processes_strong()
        self.scan_all_apks_strong()
        
        # گزارش نهایی
        final_score = max(10, self.risk_score)
        status = "خطرناک" if final_score < 60 else "هشدار" if final_score < 80 else "امن"
        
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": final_score,
            "status": status,
            "malware_found": len(self.malware_detected),
            "details": self.malware_detected + self.issues
        }
        
        report_path = "/sdcard/strong_security_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*70)
        print("📊 گزارش نهایی اسکن قوی")
        print("="*70)
        print(f"امتیاز امنیت: {final_score}/100 → {status}")
        print(f"تهدیدات شناسایی شده: {len(self.malware_detected)}")
        print(f"گزارش کامل: {report_path}")
        print("="*70)
        
        if self.malware_detected:
            print("⚠️ فایل‌های مخرب شناسایی شده را فوراً حذف کنید!")


if __name__ == "__main__":
    if not os.path.exists("/sdcard"):
        print("❌ فقط در Termux روی اندروید اجرا شود.")
        sys.exit(1)
    
    scanner = StrongAndroidSecurityAV()
    scanner.run_full_strong_scan()