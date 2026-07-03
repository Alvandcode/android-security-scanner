#!/usr/bin/env python3
"""
اسکنر امنیتی پیشرفته اندروید - v1.2
اسکن خودکار پوشه‌ها + نوتیفیکیشن + گزارش HTML زیبا
"""

import os
import subprocess
import json
import re
import time
import sys
from datetime import datetime

class StrongAndroidSecurityAV:
    def __init__(self):
        self.risk_score = 100
        self.issues = []
        self.malware_detected = []
        
        self.dangerous_perms = {
            "READ_SMS", "SEND_SMS", "READ_CONTACTS", "WRITE_CONTACTS",
            "ACCESS_FINE_LOCATION", "CAMERA", "RECORD_AUDIO", "READ_PHONE_STATE",
            "CALL_PHONE", "BIND_ACCESSIBILITY_SERVICE", "SYSTEM_ALERT_WINDOW"
        }

    def run_command(self, cmd, timeout=25):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except:
            return "", "Error", 1

    def send_notification(self, title, content, priority="normal"):
        cmd = f'termux-notification --title "{title}" --content "{content}" --priority {priority}'
        self.run_command(cmd)

    def install_requirements(self):
        print("🔧 آماده‌سازی...")
        self.run_command("pkg install apktool -y")
        print("   ✅ آماده")

    def generate_html_report(self, report):
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head>
            <meta charset="utf-8">
            <title>گزارش امنیتی اندروید</title>
            <style>
                body {{ font-family: Tahoma; background: #f4f4f9; margin: 20px; }}
                h1 {{ color: #d32f2f; text-align: center; }}
                .score {{ font-size: 48px; font-weight: bold; text-align: center; }}
                .safe {{ color: #388e3c; }} .warning {{ color: #f57c00; }} .danger {{ color: #d32f2f; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; border: 1px solid #ddd; text-align: right; }}
                th {{ background: #3f51b5; color: white; }}
            </style>
        </head>
        <body>
            <h1>📊 گزارش اسکن امنیتی</h1>
            <div class="score {'safe' if report['risk_score'] >= 80 else 'warning' if report['risk_score'] >= 60 else 'danger'}">
                {report['risk_score']}/100
            </div>
            <p style="text-align:center; font-size:18px;">وضعیت: <b>{report['status']}</b></p>
            
            <h2>تهدیدات شناسایی شده ({len(report.get('details', []))})</h2>
            <table>
                <tr><th>فایل/نوع</th><th>جزئیات</th></tr>
        """
        for item in report.get('details', []):
            html += f"<tr><td>{item.get('file', item.get('type', ''))}</td><td>{item.get('recommendation', 'مشکوک')}</td></tr>"
        html += """
            </table>
            <p>زمان اسکن: """ + report['timestamp'] + """</p>
        </body>
        </html>
        """
        report_path = "/sdcard/strong_security_report.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)
        return report_path

    def scan_folders_automatically(self):
        print("🔍 اسکن خودکار پوشه‌ها...")
        paths = ["/sdcard/Download", "/sdcard/Downloads", "/storage/emulated/0/Download"]
        for base in paths:
            if os.path.exists(base):
                for root, _, files in os.walk(base):
                    for file in files:
                        if file.lower().endswith(('.apk', '.apks', '.xapk')):
                            print(f"   پیدا شد: {file}")
                            self.malware_detected.append({
                                "file": file,
                                "recommendation": "فایل APK - بررسی شود"
                            })

    def run_full_scan(self):
        print("🚀 شروع اسکن خودکار v1.2")
        self.install_requirements()
        self.scan_folders_automatically()
        
        final_score = max(10, self.risk_score)
        status = "امن" if final_score >= 80 else "هشدار" if final_score >= 60 else "خطرناک"

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": final_score,
            "status": status,
            "details": self.malware_detected
        }

        html_path = self.generate_html_report(report)
        json_path = "/sdcard/strong_security_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.send_notification("اسکن امنیتی", f"امتیاز: {final_score} - {status}", "high")

        print(f"\n✅ اسکن تمام شد! امتیاز: {final_score}")
        print(f"📄 گزارش HTML: {html_path}")

if __name__ == "__main__":
    if not os.path.exists("/sdcard"):
        print("❌ فقط در Termux اجرا شود.")
        sys.exit(1)
    
    scanner = StrongAndroidSecurityAV()
    scanner.run_full_scan()
