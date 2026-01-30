# راهنمای استفاده

## شروع سریع

### نصب

```bash
pip install iran-encoding
```

### کدگذاری/رمزگشایی اولیه

```python
from iran_encoding import encode, decode

# کدگذاری متن فارسی
text = "سلام دنیا"
encoded_bytes = encode(text)
print(f"کدگذاری شده (هگز): {encoded_bytes.hex()}")

# رمزگشایی مجدد به متن
decoded_text = decode(encoded_bytes)
print(f"رمزگشایی شده: {decoded_text}")
```

## تشخیص محل

کتابخانه به طور خودکار تشخیص می‌دهد که متن شما عمدتاً فارسی یا انگلیسی است و اعداد را متناسب با آن مدیریت می‌کند:

```python
from iran_encoding import encode, detect_locale

# متن غالب فارسی
fa_text = "سلام 123"  # شامل فارسی و اعداد
locale = detect_locale(fa_text)
print(f"محل شناسایی شده: {locale}")  # خروجی: 'fa'

encoded = encode(fa_text)
# اعداد '123' به ارقام فارسی '۱۲۳' تبدیل خواهد شد

# متن غالب انگلیسی
en_text = "Hello 123"  # شامل انگلیسی و اعداد
locale = detect_locale(en_text)
print(f"محل شناسایی شده: {locale}")  # خروجی: 'en'

encoded = encode(en_text)
# اعداد '123' به عنوان ASCII باقی خواهد ماند
```

## گزینه‌های پیشرفته

### چیدمان دیداری در مقابل منطقی

به طور پیش‌فرض، کدگذار از چیدمان دیداری استفاده می‌کند که برای سیستم ایران معمول است:

```python
# چیدمان دیداری (پیش‌فرض)
encoded_visual = encode("سلام", visual_ordering=True)

# چیدمان منطقی (برای موارد خاص کاربردی)
encoded_logical = encode("سلام", visual_ordering=False)
```

### پیکربندی سفارشی

می‌توانید پیکربندی اضافی را به شکل‌دهنده عربی منتقل کنید:

```python
config = {
    # گزینه‌های شکل‌دهی سفارشی می‌تواند اینجا منتقل شود
}

encoded = encode("سلام دنیا", configuration=config)
```

## رابط خط فرمان

بسته شامل یک رابط خط فرمان برای استفاده آسان است:

### کدگذاری

```bash
# کدگذاری متن به هگز سیستم ایران
iran-encoding encode "سلام دنیا"

# کدگذاری با چیدمان منطقی
iran-encoding encode --logical "سلام دنیا"

# کدگذاری با پیکربندی سفارشی (فرمت JSON)
iran-encoding encode --config '{"rtl_shaping_type": "general"}' "سلام دنیا"
```

### رمزگشایی

```bash
# رمزگشایی رشته هگز به متن
iran-encoding decode-hex "a8f391f4"

# رمزگشایی رشته بایت به متن
iran-encoding decode "b'\\xa8\\xf3\\x91\\xf4'"
```

## مثال‌های یکپارچه‌سازی

### یکپارچه‌سازی برنامه وب

```python
from flask import Flask, request, jsonify
from iran_encoding import encode, decode

app = Flask(__name__)

@app.route('/encode', methods=['POST'])
def api_encode():
    data = request.json
    text = data.get('text', '')
    encoded = encode(text)
    return jsonify({
        'input': text,
        'encoded': encoded.hex(),
        'encoded_bytes': list(encoded)
    })

@app.route('/decode', methods=['POST'])
def api_decode():
    data = request.json
    hex_string = data.get('hex', '')
    try:
        decoded = decode(bytes.fromhex(hex_string))
        return jsonify({
            'hex': hex_string,
            'decoded': decoded
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

### پردازش فایل

```python
def process_text_file(input_file, output_file):
    """تبدیل فایل متنی از یونی‌کد به کدگذاری سیستم ایران"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    encoded_bytes = encode(content)
    
    with open(output_file, 'wb') as f:
        f.write(encoded_bytes)

def read_iran_system_file(file_path):
    """خواندن فایل کدگذاری شده سیستم ایران و تبدیل به یونی‌کد"""
    with open(file_path, 'rb') as f:
        iran_system_bytes = f.read()
    
    decoded_text = decode(iran_system_bytes)
    return decoded_text
```

## مدیریت خطا

```python
from iran_encoding import encode, decode

try:
    # تلاش برای کدگذاری متن
    encoded = encode("نمونه متن")
    decoded = decode(encoded)
    print(f"موفقیت: {decoded}")
except Exception as e:
    print(f"کدگذاری/رمزگشایی ناموفق: {e}")

# رمزگشایی ایمن هگز
def safe_decode_hex(hex_string):
    try:
        return decode_hex(hex_string)
    except ValueError as e:
        print(f"رشته هگز نامعتبر: {e}")
        return None
```

## نکات عملکردی

- نمونه‌های کدگذار/رمزگشای را در صورت پردازش متون زیاد ذخیره کنید
- هنگام تبدیل چندین فایل از پردازش دسته‌ای استفاده کنید
- در هنگام پردازش متون بزرگ به طور مکرر، سربار تشخیص محل را در نظر بگیرید