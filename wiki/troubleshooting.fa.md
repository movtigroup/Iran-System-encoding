# راهنمای عیب‌یابی

## مشکلات رایج

### 1. نمایش نادرست کاراکترها

**مشکل**: کاراکترها پس از کدگذاری/رمزگشایی به درستی نمایش داده نمی‌شوند.

**راه‌حل**:
- اطمینان حاصل کنید که از کدگذاری صحیح هنگام نمایش متن استفاده می‌کنید
- برخی برنامه‌ها ممکن است نیاز به پشتیبانی فونت خاص برای کاراکترهای فارسی داشته باشند
- بررسی کنید که ترمینال/ویرایشگر شما از رندر کردن متن فارسی پشتیبانی می‌کند

### 2. مشکلات مدیریت اعداد

**مشکل**: اعداد طبق محل به صورت مورد انتظار تبدیل نمی‌شوند.

**راه‌حل**:
- الگوریتم تشخیص محل فراوانی کاراکتر را تحلیل می‌کند
- متن مختلط با تعداد برابر کاراکترهای فارسی و انگلیسی به صورت پیش‌فرض به 'en' تبدیل می‌شود
- برای رفتار یکنواخت، اطمینان حاصل کنید که متن دارای غالب بودن واضح زبان است

### 3. مشکلات تبدیل دوطرفه

**مشکل**: کدگذاری و سپس رمزگشایی متن اصلی را بازمی‌گرداند.

**راه‌حل**:
- سیستم ایران از چیدمان دیداری استفاده می‌کند، که برخی اطلاعات منطقی را از دست می‌دهد
- برخی توالی‌های یونی‌کد ممکن است چندین نمایش سیستم ایران داشته باشند
- این مربوط به طراحی کدگذاری سیستم ایران است

### 4. وابستگی‌های گم شده

**مشکل**: خطاهای وارد کردن مربوط به `arabic_reshaper` یا `python-bidi`.

**راه‌حل**:
- اطمینان حاصل کنید که تمام وابستگی‌ها نصب شده‌اند: `pip install -r requirements.txt`
- بررسی کنید که نسخه پایتون شما سازگار است (3.7+)

## نکات اشکال‌زدایی

### فعال‌سازی لاگ‌های مفصل

اضافه کردن اطلاعات اشکال‌زدایی برای درک فرآیند تبدیل:

```python
from iran_encoding import encode, decode, detect_locale

# اشکال‌زدایی تشخیص محل
text = "Your text here"
locale = detect_locale(text)
print(f"Text: {repr(text)}")
print(f"Detected locale: {locale}")

# اشکال‌زدایی فرآیند کدگذاری
encoded = encode(text)
print(f"Encoded bytes: {encoded}")
print(f"Encoded as hex: {encoded.hex()}")

# اشکال‌زدایی فرآیند رمزگشایی
decoded = decode(encoded)
print(f"Decoded text: {repr(decoded)}")
```

### آزمایش کاراکترهای خاص

اگر مشکلی با کاراکترهای خاص دارید، آن‌ها را به صورت جداگانه آزمایش کنید:

```python
# آزمایش کاراکترهای جداگانه
test_chars = ['ا', 'ب', 'پ', 'ت', 'س', 'ش', '۰', '۱', '۲', '0', '1', '2']

for char in test_chars:
    try:
        encoded = encode(char)
        decoded = decode(encoded)
        print(f"'{char}' -> {encoded.hex()} -> '{decoded}' (Match: {char == decoded})")
    except Exception as e:
        print(f"Error with '{char}': {e}")
```

## مشکلات عملکردی

### پردازش آهسته

اگر کدگذاری/رمزگشایی آهسته است:

- متون بزرگ زمان بیشتری برای پردازش تشخیص محل می‌گیرند
- در نظر بگیرید متون را در تکه‌های کوچکتر پردازش کنید
- نتایج را ذخیره کنید اگر همان متون را به طور مکرر پردازش می‌کنید

### مصرف حافظه

برای فایل‌های بزرگ، در نظر بگیرید جریان دادن:

```python
def process_large_file(input_path, output_path):
    """Process large files in chunks to manage memory"""
    chunk_size = 1024  # Process in 1KB chunks
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'wb') as outfile:
        
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break
                
            encoded_chunk = encode(chunk)
            outfile.write(encoded_chunk)
```

## مسائل خاص پلتفرم

### ویندوز

- اطمینان حاصل کنید که کنسول شما از UTF-8 پشتیبانی می‌کند: `chcp 65001`
- برخی نسخه‌های قدیمی ویندوز ممکن است مشکلات رندر فونت داشته باشند

### لینوکس/مک

- پشتیبانی فونت معمولاً بهتر است اما ممکن است هنوز نیاز به نصب فونت‌های فارسی داشته باشید
- کدگذاری ترمینال باید UTF-8 باشد

## آزمایش نصب شما

تأیید اینکه همه چیز به درستی کار می‌کند:

```python
from iran_encoding import encode, decode, detect_locale

def test_setup():
    print("Testing Iran System Encoding setup...")
    
    # Test basic functionality
    test_text = "سلام"
    encoded = encode(test_text)
    decoded = decode(encoded)
    
    print(f"Original: {test_text}")
    print(f"Encoded: {encoded.hex()}")
    print(f"Decoded: {decoded}")
    print(f"Round-trip successful: {test_text == decoded or test_text in decoded}")
    
    # Test locale detection
    fa_text = "سلام 123"
    en_text = "Hello 123"
    
    print(f"Persian text '{fa_text}' locale: {detect_locale(fa_text)}")
    print(f"English text '{en_text}' locale: {detect_locale(en_text)}")
    
    print("Setup test complete!")

if __name__ == "__main__":
    test_setup()
```

## دریافت کمک

اگر با مشکلاتی مواجه می‌شوید که اینجا پوشش داده نشده است:

1. بررسی کنید که آیا مشکلات موجود گیت‌هاب وجود دارد: https://github.com/movtigroup/Iran-System-encoding/issues
2. اجرای مجموعه تست برای تأیید عملکرد پایه: `python -m pytest tests/`
3. ایجاد یک مثال قابل تکرار حداقلی هنگام گزارش مشکلات