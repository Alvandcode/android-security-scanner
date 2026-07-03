# 📚 نمونه‌های استفاده و خروجی

## 🚀 نمونه اول: اسکن ساده

```bash
$ python3 strong_security_av_improved.py

2024-01-15 10:30:00 - SecurityAV - INFO - ============================================================
2024-01-15 10:30:00 - SecurityAV - INFO - 🔒 شروع اسکن امنیتی اندروید
2024-01-15 10:30:00 - SecurityAV - INFO - ============================================================
2024-01-15 10:30:00 - SecurityAV - INFO - شروع اسکن: /root/storage/downloads
2024-01-15 10:30:00 - SecurityAV - INFO - بررسی فرآیندهای در حال اجرا...
2024-01-15 10:30:02 - SecurityAV - INFO - پیدا شد 0 تهدید در فرآیندهای در حال اجرا
2024-01-15 10:30:02 - SecurityAV - INFO - پیدا شد 8 فایل APK
2024-01-15 10:30:02 - SecurityAV - INFO - اسکن APK: |████████████████████| 100%
2024-01-15 10:30:45 - SecurityAV - INFO - ============================================================
2024-01-15 10:30:45 - SecurityAV - INFO - 📊 خلاصه نتایج:
2024-01-15 10:30:45 - SecurityAV - INFO -   - کل تهدیدات: 5
2024-01-15 10:30:45 - SecurityAV - INFO -   - امتیاز ریسک: 32.5/100
2024-01-15 10:30:45 - SecurityAV - INFO -   - امتیاز امنیتی: 74.0/100
2024-01-15 10:30:45 - SecurityAV - INFO -   - مدت اسکن: 43.25 ثانیه
2024-01-15 10:30:45 - SecurityAV - INFO - ============================================================
2024-01-15 10:30:45 - SecurityAV - INFO - ✅ گزارش JSON: /sdcard/Download/security_report_20240115_103045.json
2024-01-15 10:30:45 - SecurityAV - INFO - ✅ گزارش HTML: /sdcard/Download/security_report_20240115_103045.html
```

---

## 🔍 نمونه دوم: اسکن تفصیلی (DEBUG)

```bash
$ python3 strong_security_av_improved.py --log DEBUG --path /sdcard/Download

2024-01-15 10:31:00 - SecurityAV - INFO - ============================================================
2024-01-15 10:31:00 - SecurityAV - INFO - 🔒 شروع اسکن امنیتی اندروید
2024-01-15 10:31:00 - SecurityAV - INFO - ============================================================
2024-01-15 10:31:00 - SecurityAV - INFO - شروع اسکن: /sdcard/Download
2024-01-15 10:31:00 - SecurityAV - INFO - بررسی فرآیندهای در حال اجرا...
2024-01-15 10:31:00 - SecurityAV - DEBUG - یافت شد process: zygote با PID 123
2024-01-15 10:31:00 - SecurityAV - DEBUG - یافت شد process: system_server با PID 456
2024-01-15 10:31:00 - SecurityAV - DEBUG - بررسی الگوهای مشکوک در frida...
2024-01-15 10:31:00 - SecurityAV - DEBUG - بررسی الگوهای مشکوک در xposed...
2024-01-15 10:31:00 - SecurityAV - INFO - پیدا شد 0 تهدید در فرآیندهای در حال اجرا
2024-01-15 10:31:00 - SecurityAV - INFO - پیدا شد 3 فایل APK
2024-01-15 10:31:00 - SecurityAV - INFO - اسکن APK: |████████████████████| 100%
2024-01-15 10:31:01 - SecurityAV - DEBUG - اسکن: /sdcard/Download/Instagram.apk (8.5 MB)
2024-01-15 10:31:01 - SecurityAV - DEBUG - استخراج شده 48 مجوز از com.instagram.android
2024-01-15 10:31:01 - SecurityAV - DEBUG - مجوز خطرناک: android.permission.CAMERA (risk=8)
2024-01-15 10:31:01 - SecurityAV - DEBUG - مجوز خطرناک: android.permission.RECORD_AUDIO (risk=8)
2024-01-15 10:31:01 - SecurityAV - DEBUG - مجوز خطرناک: android.permission.ACCESS_FINE_LOCATION (risk=8)
2024-01-15 10:31:02 - SecurityAV - DEBUG - استخراج 2150 رشته از APK
2024-01-15 10:31:02 - SecurityAV - DEBUG - اسکن: /sdcard/Download/WhatsApp.apk (65.2 MB)
2024-01-15 10:31:05 - SecurityAV - DEBUG - استخراج شده 25 مجوز از com.whatsapp
2024-01-15 10:31:05 - SecurityAV - DEBUG - مجوز خطرناک: android.permission.READ_CONTACTS (risk=8)
2024-01-15 10:31:05 - SecurityAV - DEBUG - استخراج 4820 رشته از APK
2024-01-15 10:31:10 - SecurityAV - INFO - ============================================================
2024-01-15 10:31:10 - SecurityAV - INFO - 📊 خلاصه نتایج:
2024-01-15 10:31:10 - SecurityAV - INFO -   - کل تهدیدات: 7
2024-01-15 10:31:10 - SecurityAV - INFO -   - امتیاز ریسک: 48.0/100
2024-01-15 10:31:10 - SecurityAV - INFO -   - امتیاز امنیتی: 61.6/100
2024-01-15 10:31:10 - SecurityAV - INFO -   - مدت اسکن: 10.15 ثانیه
2024-01-15 10:31:10 - SecurityAV - INFO - ============================================================
```

---

## 📋 نمونه سوم: فقط JSON

```bash
$ python3 strong_security_av_improved.py --json-only

2024-01-15 10:32:00 - SecurityAV - INFO - ============================================================
2024-01-15 10:32:00 - SecurityAV - INFO - 🔒 شروع اسکن امنیتی اندروید
2024-01-15 10:32:00 - SecurityAV - INFO - ============================================================
2024-01-15 10:32:00 - SecurityAV - INFO - شروع اسکن: /root/storage/downloads
...
2024-01-15 10:32:30 - SecurityAV - INFO - ✅ گزارش JSON: /sdcard/Download/security_report_20240115_103230.json
```

**خروجی JSON:**

```json
{
  "timestamp": "2024-01-15T10:32:30.123456",
  "device": {
    "release": "12",
    "brand": "Samsung",
    "model": "Galaxy S21"
  },
  "summary": {
    "total_apks": 8,
    "total_threats": 7,
    "risk_score": 48.0,
    "security_score": 61.6,
    "scan_duration_seconds": 30.45
  },
  "threat_breakdown": {
    "critical": 0,
    "high": 7,
    "medium": 0,
    "low": 0
  },
  "findings": [
    {
      "file_path": "/sdcard/Download/Instagram.apk",
      "threat_type": "suspicious_perm",
      "threat_name": "android.permission.CAMERA",
      "severity": "high",
      "description": "مجوز خطرناک: CAMERA",
      "evidence": "android.permission.CAMERA"
    },
    {
      "file_path": "/sdcard/Download/Instagram.apk",
      "threat_type": "suspicious_perm",
      "threat_name": "android.permission.RECORD_AUDIO",
      "severity": "high",
      "description": "مجوز خطرناک: AUDIO",
      "evidence": "android.permission.RECORD_AUDIO"
    },
    {
      "file_path": "/sdcard/Download/WhatsApp.apk",
      "threat_type": "suspicious_perm",
      "threat_name": "android.permission.READ_CONTACTS",
      "severity": "high",
      "description": "مجوز خطرناک: CONTACTS",
      "evidence": "android.permission.READ_CONTACTS"
    }
  ]
}
```

---

## 🌐 نمونه چهارم: گزارش HTML

```bash
$ python3 strong_security_av_improved.py --html-only \
  --output ~/my_security_report.html

2024-01-15 10:33:00 - SecurityAV - INFO - ============================================================
2024-01-15 10:33:00 - SecurityAV - INFO - 🔒 شروع اسکن امنیتی اندروید
...
2024-01-15 10:33:30 - SecurityAV - INFO - ✅ گزارش HTML: /home/user/my_security_report.html
```

**نمایش HTML:**

```html
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <title>گزارش امنیتی اندروید</title>
</head>
<body>
    <header>
        <h1>🔒 گزارش امنیتی اندروید</h1>
        <p>اسکنر امنیتی پیشرفته | Strong Security AV</p>
    </header>
    
    <div class="summary">
        <div class="card">
            <h3>امتیاز امنیتی</h3>
            <div class="score">61.6/100</div>
        </div>
        <div class="card">
            <h3>تعداد تهدیدات</h3>
            <div class="value">7</div>
        </div>
        <div class="card">
            <h3>فایل‌های APK</h3>
            <div class="value">8</div>
        </div>
        <div class="card">
            <h3>مدت اسکن</h3>
            <div class="value">30.5s</div>
        </div>
    </div>
    
    <div class="findings">
        <h2>📊 تفصیل تهدیدات</h2>
        <table>
            <thead>
                <tr>
                    <th>فایل</th>
                    <th>نوع</th>
                    <th>نام تهدید</th>
                    <th>شدت</th>
                    <th>توضیح</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>/sdcard/Download/Instagram.apk</td>
                    <td>suspicious_perm</td>
                    <td>android.permission.CAMERA</td>
                    <td><span style="color: #fd7e14;">HIGH</span></td>
                    <td>مجوز خطرناک: CAMERA</td>
                </tr>
                <!-- ... ردیف‌های بیشتر ... -->
            </tbody>
        </table>
    </div>
</body>
</html>
```

---

## 🎯 نمونه پنجم: استفاده برنامه‌ای (Python Code)

```python
#!/usr/bin/env python3
from strong_security_av_improved import StrongAndroidSecurityAV, setup_logging

# راه‌اندازی
logger = setup_logging("INFO")
scanner = StrongAndroidSecurityAV(scan_path="/sdcard/Download", logger=logger)

# اجرای اسکن
result = scanner.scan()

# استفاده از نتایج
print(f"امتیاز: {result.final_score:.1f}/100")
print(f"تهدیدات: {len(result.findings)}")

# بررسی تهدیدات
critical_threats = [f for f in result.findings if f.severity == 'critical']
if critical_threats:
    print(f"\n⚠️  {len(critical_threats)} تهدید حیاتی!")
    for threat in critical_threats:
        print(f"  - {threat.threat_name} در {threat.file_path}")

# تولید گزارش
json_report = scanner.generate_json_report(result)
html_report = scanner.generate_html_report(result)

# ذخیره
with open('report.json', 'w') as f:
    f.write(json_report)

with open('report.html', 'w') as f:
    f.write(html_report)
```

---

## 🔐 نمونه ششم: اسکن مسیر خاص (تست)

```bash
# اسکن فقط یک بار، بدون Termux notification
$ python3 strong_security_av_improved.py \
  --path /tmp/test_apks \
  --no-notify \
  --log INFO \
  --json-only

# خروجی:
# ✅ گزارش JSON: /sdcard/Download/security_report_20240115_103500.json
```

---

## 📊 جدول مقایسه شدت‌ها

| شدت | رنگ | معنی | مثال |
|-----|-----|------|------|
| **Critical** | 🔴 قرمز | خطر فوری | Frida، Xposed |
| **High** | 🟠 نارنجی | خطر قابل‌توجه | مجوزهای خطرناک |
| **Medium** | 🟡 زرد | هشدار | نام فایل مشکوک |
| **Low** | 🟢 سبز | اطلاعات | اندازه بزرگ APK |

---

## ⚡ نکات سریع

### ✅ زمان‌های متوقع اجرا:
- اسکن فایل‌های کم (< 5 APK): **5-15 ثانیه**
- اسکن متوسط (5-20 APK): **15-45 ثانیه**
- اسکن بزرگ (> 20 APK): **45+ ثانیه**

### 📁 مسیرهای پیش‌فرض:
- Termux: `~/storage/downloads` (مع~ = `/root/storage/downloads`)
- لینوکس: `~/Downloads`

### 🚨 معنی امتیاز‌ها:
- **90-100**: تقریباً ایمن ✅
- **70-89**: نسبتاً ایمن ⚠️
- **50-69**: نیاز به بررسی دقیق
- **0-49**: خطر زیاد 🚨

---

## 🔧 رفع‌کردن مشکلات

### مشکل: "apktool not found"

```bash
# Termux:
apt install -y apktool

# لینوکس (Ubuntu/Debian):
sudo apt install -y apktool

# macOS:
brew install apktool
```

### مشکل: "Permission denied"

```bash
chmod +x strong_security_av_improved.py
```

### مشکل: "No module named 'tqdm'"

```bash
# اختیاری است، اما برای progress bar بهتر:
pip install tqdm
```

---

## 📞 راهنمایی بیشتر

```bash
# مشاهده تمام گزینه‌ها
python3 strong_security_av_improved.py --help

# خروجی:
# usage: strong_security_av_improved.py [-h] [--path PATH] [--json-only] 
#        [--html-only] [--output OUTPUT] [--no-notify] [--log {DEBUG,INFO,WARNING,ERROR}]
#
# اسکنر امنیتی اندروید پیشرفته
# 
# optional arguments:
#   -h, --help            نمایش این پیام و خروج
#   --path PATH           مسیر پوشه‌ای برای اسکن
#   --json-only           صرفاً گزارش JSON
#   --html-only           صرفاً گزارش HTML
#   --output OUTPUT       مسیر فایل خروجی
#   --no-notify           بدون نوتیفیکیشن Termux
#   --log {DEBUG,INFO...} سطح لاگ‌گیری
```

---

## 🎓 نکات آموزشی

اگر می‌خواهید **کد بهتر یادگیری کنید**:

1. **Logging**: ببینید چطور `logging` module استفاده می‌شود
2. **Type Hints**: مثال‌های خوب `List`, `Dict`, `Optional` و غیره
3. **Dataclasses**: استفاده از `@dataclass` برای مدل‌ها
4. **subprocess**: بهترین روش برای اجرای برنامه‌های خارجی
5. **HTML Escaping**: چطور از XSS جلوگیری کنیم

---

**موفق باشید! 🚀**
