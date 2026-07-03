# 🚀 شروع سریع (Quick Start)

## 5 دقیقه برای شروع!

### مرحله 1️⃣: نصب وابستگی‌ها

#### اگر در **Termux** هستید:

```bash
# باز کنید Termux و این دستورات را اجرا کنید:

# آپدیت مخازن
apt update

# نصب Python و apktool
apt install -y python3 apktool git

# (اختیاری) نصب tqdm برای progress bar
pip install tqdm
```

#### اگر در **لینوکس** (Ubuntu/Debian) هستید:

```bash
# آپدیت مخازن
sudo apt update

# نصب Python و apktool
sudo apt install -y python3 python3-pip apktool

# (اختیاری) نصب tqdm
pip3 install tqdm
```

#### اگر در **macOS** هستید:

```bash
# نصب Homebrew اگر ندارید
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# نصب
brew install python apktool

# (اختیاری)
pip install tqdm
```

---

### مرحله 2️⃣: دانلود کد

```bash
# تمام فایل‌های زیر را دانلود کنید:
# - strong_security_av_improved.py (کد اصلی)
# - requirements.txt (وابستگی‌ها)

# اگر git دارید:
git clone <repo-url>

# یا دستی دانلود کنید و در پوشه قرار دهید
```

---

### مرحله 3️⃣: اجرای اول (تست)

#### اگر به شدت عجله دارید:

```bash
cd /path/to/downloaded/files
python3 strong_security_av_improved.py
```

**خروجی مورد انتظار:**
```
============================================================
🔒 شروع اسکن امنیتی اندروید
============================================================
...
✅ گزارش JSON: /sdcard/Download/security_report_20240115_103000.json
✅ گزارش HTML: /sdcard/Download/security_report_20240115_103000.html
```

---

### مرحله 4️⃣: آزمایش گزینه‌های مختلف

#### 📊 صرفاً گزارش JSON:

```bash
python3 strong_security_av_improved.py --json-only
```

#### 🌐 صرفاً گزارش HTML:

```bash
python3 strong_security_av_improved.py --html-only
```

#### 🔍 اسکن تفصیلی (DEBUG):

```bash
python3 strong_security_av_improved.py --log DEBUG
```

#### 📁 اسکن مسیر خاص:

```bash
python3 strong_security_av_improved.py --path /path/to/apk/folder
```

#### 🔇 بدون اعلان Termux:

```bash
python3 strong_security_av_improved.py --no-notify
```

---

### مرحله 5️⃣: مشاهده نتایج

#### 📄 گزارش JSON:
```bash
# باز کردن فایل JSON
cat /sdcard/Download/security_report_*.json | less

# یا با JSON pretty-printer
python3 -m json.tool /sdcard/Download/security_report_*.json
```

#### 🌐 گزارش HTML:
```bash
# باز کردن در مرورگر
# در Termux: من پیشنهاد می‌کنم از "Termux:GUI" استفاده کنید
# یا فایل را منتقل کنید و در فایل منیجر دوبار کلیک کنید
```

---

## 🎯 سناریوهای متداول

### سناریو ۱: اسکن سریع پوشه Downloads

```bash
python3 strong_security_av_improved.py \
  --path ~/Downloads \
  --no-notify
```

**⏱️ مدت زمان:** 10-30 ثانیه

---

### سناریو ۲: اسکن کامل با لاگ تفصیلی

```bash
python3 strong_security_av_improved.py \
  --path /sdcard/Download \
  --log DEBUG \
  --html-only
```

**⏱️ مدت زمان:** 20-60 ثانیه

---

### سناریو ۳: اسکن و ذخیره در مسیر خاص

```bash
python3 strong_security_av_improved.py \
  --output ~/my_reports/security_$(date +%Y%m%d).json \
  --json-only
```

---

### سناریو ۴: Automation - اسکن روزانه

#### ایجاد اسکریپت (`daily_scan.sh`):

```bash
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="/sdcard/Download/security_reports"

mkdir -p "$OUTPUT_DIR"

python3 strong_security_av_improved.py \
  --path ~/Downloads \
  --output "$OUTPUT_DIR/report_$DATE.json" \
  --json-only \
  --no-notify

echo "✅ اسکن تمام شد: $OUTPUT_DIR/report_$DATE.json"
```

#### اجرا:

```bash
chmod +x daily_scan.sh
./daily_scan.sh
```

---

## ⚠️ مشکلات و راه‌حل

### مشکل 1: "apktool command not found"

```bash
# Termux:
apt install -y apktool

# Ubuntu/Debian:
sudo apt install -y apktool

# macOS:
brew install apktool
```

### مشکل 2: "Permission denied"

```bash
chmod +x strong_security_av_improved.py

# یا اجرا با python3 به جای باینری
python3 strong_security_av_improved.py
```

### مشکل 3: "ModuleNotFoundError: No module named 'logging'"

**یادداشت:** `logging` بخش استاندارد Python است و نباید نصب کنید. اگر خطا دارید:

```bash
# Python را دوباره نصب کنید:
# Ubuntu:
sudo apt install --reinstall python3

# Termux:
apt install --reinstall python
```

### مشکل 4: "No such file or directory"

```bash
# بررسی کنید مسیر درست است:
ls -la /path/to/apk/folder

# یا مسیر را تصحیح کنید:
python3 strong_security_av_improved.py --path ~/Downloads
```

### مشکل 5: "tqdm not found"

```bash
# tqdm اختیاری است. اگر خطا دارید:
pip install tqdm

# یا بدون آن اجرا کنید (بدون progress bar)
```

---

## 📝 ویرایش دستی (Advanced)

### اگر می‌خواهید مجوزهای خطرناک اضافه کنید:

```python
# فایل را باز کنید و این قسمت را پیدا کنید:

class ThreatDatabase:
    DANGEROUS_PERMISSIONS = {
        'android.permission.EXISTING': {'level': 'dangerous', 'category': 'cat', 'risk': 8},
        
        # اینجا اضافه کنید:
        'android.permission.YOUR_CUSTOM': {'level': 'dangerous', 'category': 'custom', 'risk': 9},
    }
```

### اگر می‌خواهید الگوی جدید اضافه کنید:

```python
SUSPICIOUS_PATTERNS = {
    r'(your|pattern|here)': 'Your Pattern Name',
    # الگوهای دیگر...
}
```

---

## 💡 نکات مفید

### 1. **پایه‌های داده را به‌روز نگاه دارید**

اگر می‌خواهید الگوهای جدید اضافه کنید:

```bash
# فایل را ویرایش کنید (Termux):
nano strong_security_av_improved.py

# و مجوزها/الگوها را اضافه کنید
```

### 2. **گزارش‌ها را ذخیره کنید**

```bash
# ایجاد پوشه برای ذخیره
mkdir -p ~/security_reports

# اسکن و ذخیره
python3 strong_security_av_improved.py --output ~/security_reports/report.json
```

### 3. **مقایسه نتایج**

```bash
# اسکن دو بار و مقایسه
python3 strong_security_av_improved.py --json-only \
  --output report_1.json

# بعداً:
python3 strong_security_av_improved.py --json-only \
  --output report_2.json

# مقایسه:
diff <(jq -S . report_1.json) <(jq -S . report_2.json)
```

---

## 🧪 آزمایش سریع

### ایجاد دایرکتوری تست:

```bash
mkdir -p ~/test_apks
cd ~/test_apks

# دانلود یک APK برای تست (مثلاً از اینجا):
# https://www.apkmirror.com/
# یا استفاده از یک APK موجود

# سپس:
python3 strong_security_av_improved.py --path ~/test_apks
```

---

## 📊 فهمیدن نتایج

### امتیاز امنیتی (Security Score):

```
90-100  ✅ بسیار ایمن
70-89   ⚠️  نسبتاً ایمن
50-69   ⚠️  نیاز به بررسی
0-49    🚨 خطر بالا
```

### شدت تهدیدات:

```
Critical (قرمز) 🔴  - اقدام فوری لازم
High (نارنجی) 🟠    - بررسی ضروری
Medium (زرد) 🟡     - نظارت داشته باشید
Low (سبز) 🟢        - اطلاعات
```

---

## 🔗 لینک‌های مفید

- [Android Permissions](https://developer.android.com/guide/topics/permissions/overview)
- [apktool Documentation](https://ibotpeaches.github.io/Apktool/)
- [Python logging](https://docs.python.org/3/library/logging.html)

---

## ✅ چک‌لیست تیم‌های

- [ ] apktool نصب شده
- [ ] Python 3 نصب شده
- [ ] فایل قابل اجرا است (`chmod +x`)
- [ ] مسیر صحیح مشخص شد
- [ ] تست اول موفق بود
- [ ] گزارش‌ها تولید شدند
- [ ] نتایج منطقی به نظر می‌رسد

---

## 🆘 کمک بیشتر

اگر مشکل دارید:

1. **Help را مشاهده کنید:**
   ```bash
   python3 strong_security_av_improved.py --help
   ```

2. **با DEBUG لاگ دنبال کنید:**
   ```bash
   python3 strong_security_av_improved.py --log DEBUG
   ```

3. **فایل لاگ را بررسی کنید**

4. **README_IMPROVEMENTS.md را بخوانید**

---

**حالا آماده‌اید! 🎉**

سوال دارید؟ `--help` را اجرا کنید!

```bash
python3 strong_security_av_improved.py --help
```
