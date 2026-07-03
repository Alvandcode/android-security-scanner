# 🔒 اسکنر امنیتی اندروید بهبود‌یافته

## نسخه بهبود‌یافته ۲.۰

یک اسکنر امنیتی **پیشرفته و تحت تأثیر هوشمند** برای اندروید، بدون نیاز به روت.

---

## 🚀 بهبودی‌های اصلی نسبت به نسخه قدیمی

### 1. **تحلیل APK واقعی** ✅
- **قبل**: فقط نام فایل را لیست می‌کرد
- **بعد**: استفاده از `apktool` برای decompile و استخراج واقعی `AndroidManifest.xml`
- استخراج دقیق تمام مجوزها (permissions)
- شناسایی نام بسته نرم‌افزاری (package name)

### 2. **امتیازدهی هوشمند و پویا** ✅
- **قبل**: امتیاز همیشه `100` ثابت بود!
- **بعد**: امتیاز پویا بر اساس:
  - تعداد تهدیدات
  - شدت تهدیدات (critical/high/medium/low)
  - نوع تهدید (مجوز، رشته، فرآیند، نام فایل)
  - نرمال‌سازی صحیح (۰-۱۰۰)

### 3. **بررسی فرآیندهای در حال اجرا** ✅
شناسایی ابزارهای آزمایش و بدافزارهای معروف:
- 🚫 **Frida** - Dynamic instrumentation framework
- 🚫 **Xposed** - System modification framework
- 🚫 **Magisk** - Root management
- 🚫 **Crypto Mining** - فرآیندهای استخراج ارز دیجیتال

### 4. **جستجوی رشته‌های مشکوک** ✅
- الگوهای Regex برای شناسایی:
  - دامنه‌های C2 (Command & Control)
  - Payloads کدگذاری‌شده (Base64)
  - الگوهای بدافزارهای بانکی
  - تزریق‌های کد پویا
  - دسترسی‌های نامشروع (IMEI, Device ID)

### 5. **دیتابیس تهدیدات کامل** ✅
- **۱۶ مجوز خطرناک** با طبقه‌بندی دقیق:
  - موقعیت‌یابی (Location)
  - تماس‌ها (Contacts)
  - پیامک (SMS)
  - دوربین (Camera)
  - میکروفن (Audio)
  - فایل‌ها (Storage)
  - و بیشتر...

- **۲۰+ الگوی مشکوک** برای شناسایی:
  - دامنه‌های خطرناک
  - کد‌های بدافزار معروف
  - تکنیک‌های سرقت داده

- **نام‌های بسته و فایل مشکوک** (Suspicious Package Names)

### 6. **صحیح‌سازی کامل HTML** ✅
- **قبل**: HTML injection شامل مقادیر escape نشده
- **بعد**: تمام مقادیر با `html.escape()` محافظت‌شده
- امنیت از XSS محلی
- نمایش صحیح کاراکترهای خاص و unicode

### 7. **بهبود مدیریت خطا** ✅
- **قبل**: `except: pass` (خطاها قورت می‌خوردند!)
- **بعد**: Logging صحیح با سطح‌های مختلف:
  - DEBUG برای اطلاعات تفصیلی
  - INFO برای وقایع مهم
  - WARNING برای هشدارها
  - ERROR برای خطاهای جدی

### 8. **حذف استفاده نادرست از shell** ✅
- **قبل**: `subprocess.run(..., shell=True)` خطرناک
- **بعد**: استفاده از لیست‌های تفصیل‌یافته (اجرای مستقیم)
- ایمنی از command injection

### 9. **رابط خط فرمان کامل (CLI)** ✅
```bash
python3 strong_security_av_improved.py --help

# مثال‌های استفاده:
python3 strong_security_av_improved.py                      # اسکن پیش‌فرض
python3 strong_security_av_improved.py --path /sdcard/Downloads
python3 strong_security_av_improved.py --json-only          # فقط JSON
python3 strong_security_av_improved.py --html-only          # فقط HTML
python3 strong_security_av_improved.py --no-notify          # بدون اعلان Termux
python3 strong_security_av_improved.py --log DEBUG          # لاگ تفصیلی
python3 strong_security_av_improved.py --output /path/to/file
```

### 10. **گزارش‌های حرفه‌ای** ✅

#### گزارش JSON:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "device": {
    "android_version": "12",
    "brand": "Samsung",
    "model": "Galaxy S20"
  },
  "summary": {
    "total_apks": 25,
    "total_threats": 12,
    "risk_score": 45.5,
    "security_score": 81.2,
    "scan_duration_seconds": 23.45
  },
  "threat_breakdown": {
    "critical": 2,
    "high": 5,
    "medium": 4,
    "low": 1
  },
  "findings": [...]
}
```

#### گزارش HTML:
- ✨ رابط کاربری زیبا و مدرن
- 📊 دیاگرام‌های تصویری
- 🎨 کدهای رنگی براساس شدت خطر
- ➡️ پشتیبانی کامل RTL (فارسی)
- 📱 Responsive برای موبایل

### 11. **مدل‌های داده مناسب** ✅
```python
@dataclass
class Permission      # نمایندگی مجوز
class ThreatFinding   # نمایندگی تهدید
class ScanResult      # نتیجه اسکن کامل
```

### 12. **Type Hints** ✅
- `List[str]`, `Dict`, `Optional[str]` و غیره
- IDE auto-completion بهتر
- کد قابل‌فهم‌تر

### 13. **Progress Bar اختیاری** ✅
- اگر `tqdm` نصب باشد، Progress bar نمایش می‌دهد
- اگر نه، بدون خطا کار می‌کند

### 14. **نوتیفیکیشن Termux** ✅
- اطلاع رسانی خودکار پس از اتمام اسکن
- قابل غیرفعال‌کردن با `--no-notify`

---

## 📦 نصب و راه‌اندازی

### در Termux:

```bash
# نصب وابستگی‌های سیستم
apt update
apt install -y python3 apktool git

# نصب وابستگی‌های Python (اختیاری)
pip install -r requirements.txt

# اجرای اسکنر
python3 strong_security_av_improved.py
```

### در سیستم لینوکس معمولی:

```bash
# نصب apktool
sudo apt install -y apktool

# اجرای اسکنر
python3 strong_security_av_improved.py --path ~/Downloads
```

---

## 🔧 معماری کد

### کلاس‌های اصلی:

```
StrongAndroidSecurityAV          # مدیر اصلی اسکن
  ├── ThreatDatabase              # دیتابیس تهدیدات
  ├── APKAnalyzer                 # تحلیل‌گر APK
  ├── ProcessScanner              # اسکنر فرآیندها
  └── ReportGenerator             # تولید گزارش
```

### جریان اسکن:

```
شروع اسکن
  ↓
1. بررسی فرآیندهای در حال اجرا
  ↓
2. جستجوی فایل‌های APK
  ↓
3. برای هر APK:
   ├── استخراج مجوزها
   ├── بررسی نام بسته
   ├── بررسی نام فایل
   └── اسکن رشته‌های مشکوک
  ↓
4. محاسبه امتیاز‌ها
  ↓
5. تولید گزارش‌ها
  ↓
پایان و اعلان
```

---

## 📊 مثال خروجی

```
============================================================
🔒 شروع اسکن امنیتی اندروید
============================================================

بررسی فرآیندهای در حال اجرا...
پیدا شد 25 فایل APK
اسکن APK: |████████████████████| 100%

============================================================
📊 خلاصه نتایج:
  - کل تهدیدات: 12
  - امتیاز ریسک: 45.5/100
  - امتیاز امنیتی: 81.2/100
  - مدت اسکن: 23.45 ثانیه
============================================================

✅ گزارش JSON: /sdcard/Download/security_report_20240115_103000.json
✅ گزارش HTML: /sdcard/Download/security_report_20240115_103000.html
```

---

## 🛡️ نکات امنیتی

1. **بدون نیاز به روت**: همه‌جا از API‌های عمومی استفاده می‌کند
2. **محلی**: تمام داده‌ها در دستگاه پردازش می‌شود، بدون ارسال به سرور
3. **HTML Escape**: از تمام تزریق‌های HTML محافظت می‌کند
4. **بدون Shell Injection**: از `subprocess.run()` با لیست استفاده می‌کند

---

## 🎯 امکانات آینده

- [ ] اتصال به پایگاه داده آنلاین (VirusTotal API)
- [ ] کش‌کردن نتایج اسکن برای سرعت بیشتر
- [ ] پانل مدیریت وب
- [ ] آپدیت خودکار دیتابیس تهدیدات
- [ ] تست‌های واحد (Unit Tests)
- [ ] اسکن بسته‌های نصب‌شده سیستم
- [ ] یکپارچگی با فریم‌ورک‌های امنیتی دیگر

---

## 🐛 رفع شده‌ی مشکلات

| مشکل | وضعیت قبل | وضعیت بعد |
|------|----------|----------|
| تحلیل APK واقعی | ❌ وجود ندارد | ✅ استفاده از apktool |
| امتیازدهی پویا | ❌ همیشه 100 | ✅ بر اساس تهدیدات |
| بررسی فرآیندها | ❌ وجود ندارد | ✅ شامل 4 نوع تهدید |
| جستجوی رشته | ❌ وجود ندارد | ✅ 20+ الگو |
| HTML Escape | ❌ نه | ✅ بلی |
| مدیریت خطا | ❌ Silent | ✅ Logging مناسب |
| Shell Safety | ❌ shell=True | ✅ Subprocess List |
| CLI Arguments | ❌ Hard-coded | ✅ argparse کامل |
| Type Hints | ❌ نه | ✅ بلی |
| Logging | ❌ نه | ✅ logging module |

---

## 📝 نمونه دستور

```bash
# اسکن کامل با لاگ DEBUG
python3 strong_security_av_improved.py \
  --path /sdcard/Download \
  --log DEBUG

# فقط JSON، بدون اعلان
python3 strong_security_av_improved.py \
  --json-only \
  --no-notify \
  --output ~/report.json

# اسکن HTML تنها
python3 strong_security_av_improved.py \
  --html-only \
  --output ~/security_report.html
```

---

## 📄 لایسنس

Open Source - استفاده آزاد

---

## 👨‍💻 توسعه‌دهندگان

- نسخه اصلی: Alvandcode
- بهبودی‌ها و رفع نقاط ضعف: نسخه ۲.۰

---

**نکته مهم**: این ابزار برای شناسایی تهدیدات بالقوه طراحی شده است. برای بررسی تمام‌تر، از ابزارهای تخصصی مثل `APKiD`، `MobSF`، و `VirusTotal` نیز استفاده کنید.
