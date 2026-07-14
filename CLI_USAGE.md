# CLI Usage Guide - Smart Text Matcher 🚀

دليل شامل لاستخدام واجهة سطر الأوامر (Command Line Interface) للأداة

---

## 📋 جدول المحتويات

1. [البدء السريع](#البدء-السريع)
2. [التثبيت والإعدادات](#التثبيت-والإعدادات)
3. [الأوامر الأساسية](#الأوامر-الأساسية)
4. [الوسائط والخيارات](#الوسائط-والخيارات)
5. [أمثلة عملية](#أمثلة-عملية)
6. [قراءة النتائج](#قراءة-النتائج)
7. [معالجة الأخطاء](#معالجة-الأخطاء)
8. [نصائح متقدمة](#نصائح-متقدمة)

---

## البدء السريع

### التشغيل الأساسي

```bash
# استخراج جميع الأنماط من نص مباشر
python main.py --text "Contact: test@example.com"

# استخراج الإيميلات من ملف
python main.py --file data.txt --mode emails

# عرض المساعدة
python main.py --help
```

---

## التثبيت والإعدادات

### المتطلبات

- Python 3.7 أو أحدث
- مكتبات المشروع (مثبتة بالفعل)

### تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### التحقق من التثبيت

```bash
python main.py --version
```

**النتيجة:**
```
smart-text-matcher 1.0.0
```

---

## الأوامر الأساسية

### البنية العامة

```bash
python main.py [OPTIONS] --file FILE | --text TEXT
```

### المتطلبات الأساسية

يجب تحديد **مصدر الإدخال** (واحد فقط):
- `--file` أو `-f`: قراءة من ملف
- `--text` أو `-t`: نص مباشر

---

## الوسائط والخيارات

### 1️⃣ خيارات الإدخال (مطلوبة - واحدة منهما فقط)

#### `--file FILE` أو `-f FILE`
قراءة محتوى من ملف نصي

```bash
python main.py --file path/to/file.txt --mode emails
```

**الميزات:**
- يدعم المسارات المطلقة والنسبية
- يقرأ ملفات UTF-8
- يعرض حجم الملف عند استخدام `--verbose`

#### `--text TEXT` أو `-t TEXT`
معالجة نص مباشر

```bash
python main.py --text "Your text here" --mode emails
```

---

### 2️⃣ خيار نمط المطابقة (اختياري)

#### `--mode MODE` أو `-m MODE`
نوع الأنماط المراد البحث عنها

**القيم المتاحة:**

| القيمة | الوصف | الاستخدام |
|--------|-------|----------|
| `emails` | البريد الإلكتروني | البحث عن عناوين بريد فقط |
| `phones` | أرقام الهواتف | استخراج أرقام الهواتف |
| `urls` | روابط الويب | البحث عن URLs |
| `keywords` | كلمات مفتاحية | البحث عن كلمات محددة |
| `regex` | نمط Regex مخصص | استخدام تعبير نمطي مخصص |
| `all` | جميع الأنماط (افتراضي) | البحث عن كل شيء |

**الافتراضي:** `all`

```bash
python main.py --text "Email: test@example.com" --mode emails
```

---

### 3️⃣ خيارات إضافية (اختيارية)

#### `--pattern PATTERN` أو `-p PATTERN`
تعبير نمطي مخصص (يُستخدم مع `--mode regex`)

```bash
python main.py --text "Numbers: 123 456 789" --mode regex --pattern "\d{3}"
```

#### `--keywords KEYWORD [KEYWORD ...]` أو `-k`
قائمة الكلمات المراد البحث عنها (يُستخدم مع `--mode keywords`)

```bash
python main.py --text "Python Java C++ JavaScript" --mode keywords --keywords Python Java
```

#### `--international`
استخدام صيغة E.164 العالمية لأرقام الهواتف

```bash
python main.py --text "+1234567890 +441234567890" --mode phones --international
```

#### `--case-sensitive`
تفعيل المطابقة حساسة لحالة الأحرف

```bash
python main.py --text "Python python" --mode keywords --keywords Python --case-sensitive
```

**بدون هذا الخيار:** المطابقة غير حساسة لحالة الأحرف (افتراضي)

#### `--format FORMAT` أو `-o FORMAT`
صيغة المخرجات

**القيم المتاحة:**

| الصيغة | الوصف |
|-------|-------|
| `text` | نص منسق (افتراضي) |
| `json` | JSON structured |
| `csv` | ملف CSV |

```bash
python main.py --text "test@example.com" --mode emails --format json
```

#### `--output FILE` أو `-O FILE`
حفظ النتائج في ملف

```bash
python main.py --file data.txt --mode emails --output results.txt
```

#### `--verbose` أو `-v`
تفعيل الإخراج المفصل

```bash
python main.py --text "test@example.com" --mode emails --verbose
```

**المعلومات الإضافية:**
- حجم الملف المحمل
- عدد الأحرف المعالجة
- إعدادات المطابقة المستخدمة

---

## أمثلة عملية

### مثال 1️⃣: استخراج الإيميلات من ملف

```bash
python main.py --file contacts.txt --mode emails
```

**الملف `contacts.txt`:**
```
Contact us at support@example.com
Sales: sales@company.co.uk
Info: info@domain.net
```

**النتيجة:**
```
======================================================================
🎯 SMART TEXT MATCHER - RESULTS
======================================================================

📋 Type: Emails
✅ Total Matches: 3

📍 Details:
   1. support@example.com
      Position: 15
      Type: email

   2. sales@company.co.uk
      Position: 35
      Type: email

   3. info@domain.net
      Position: 65
      Type: email

======================================================================
```

---

### مثال 2️⃣: البحث عن أرقام الهواتف

```bash
python main.py --text "Call (555) 123-4567 or 555.987.6543" --mode phones
```

**النتيجة:**
```
======================================================================
🎯 SMART TEXT MATCHER - RESULTS
======================================================================

📋 Type: Phone Numbers
✅ Total Matches: 2

📍 Details:
   1. (555) 123-4567
      Position: 5
      Type: phone

   2. 555.987.6543
      Position: 23
      Type: phone

======================================================================
```

---

### مثال 3️⃣: استخراج جميع الأنماط

```bash
python main.py --text "Email: test@example.com, Phone: (555) 123-4567, Website: https://example.com" --mode all
```

**النتيجة:**
```
======================================================================
🎯 SMART TEXT MATCHER - RESULTS
======================================================================

📧 EMAILS: 1 found
   1. test@example.com (pos: 7)

📧 PHONES: 1 found
   1. (555) 123-4567 (pos: 36)

📧 URLS: 1 found
   1. https://example.com (pos: 65)

======================================================================
```

---

## قراءة النتائج

### فهم مخرجات النصوص

#### 🎯 رأس النتيجة
يظهر في أعلى كل مخرجات النصوص ويشير إلى بدء النتائج

```
======================================================================
🎯 SMART TEXT MATCHER - RESULTS
======================================================================
```

#### 📋 نوع المطابقة
يوضح نوع الأنماط التي تم البحث عنها

```
📋 Type: Emails
```

#### 📊 إجمالي المطابقات
عدد العناصر المكتشفة

```
✅ Total Matches: 3
```

#### 📍 التفاصيل
معلومات كاملة عن كل مطابقة:
- **النص المطابق**: القيمة الفعلية المكتشفة
- **الموضع**: رقم الحرف في النص
- **النوع**: نوع المطابقة
- **الثقة**: درجة الثقة (من 0 إلى 1)

```
📍 Details:
   1. test@example.com
      Position: 15
      Type: email
```

---

## معالجة الأخطاء

### ❌ خطأ: لم يتم تحديد الإدخال

```bash
python main.py --mode emails
```

**الرسالة:**
```
usage: smart-text-matcher [-h] (--file FILE | --text TEXT) ...
error: one of the arguments --file -f --text -t is required
```

**الحل:**
```bash
python main.py --file data.txt --mode emails
```

---

### ❌ خطأ: الملف غير موجود

```bash
python main.py --file missing.txt --mode emails
```

**الرسالة:**
```
❌ Error: File not found: missing.txt
```

**الحل:**
تحقق من المسار وتأكد من وجود الملف

---

## نصائح متقدمة

### 💡 معالجة ملفات كبيرة

```bash
python main.py --file large_file.txt --mode emails --verbose
```

---

### 💡 حفظ النتائج في ملف

```bash
python main.py --file data.txt --mode emails --output results.txt
```

---

### 💡 استخدام صيغة JSON

```bash
python main.py --text "test@example.com" --mode emails --format json
```

---

### 💡 أنماط Regex متقدمة

```bash
python main.py --text "123 4567 89012" --mode regex --pattern "\d{3,5}"
```

---

## الخلاصة

**Smart Text Matcher CLI** توفر طريقة قوية وسهلة الاستخدام لمعالجة النصوص واستخراج الأنماط مباشرة من سطر الأوامر. 

للمزيد من المعلومات، راجع [README.md](README.md) الرئيسي.

---

**آخر تحديث:** 2026 | الإصدار: 1.0.0
