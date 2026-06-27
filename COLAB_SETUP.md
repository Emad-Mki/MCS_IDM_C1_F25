# 🚀 دليل التشغيل السريع على Google Colab

## مشكلة ngrok وحلها

إذا ظهرت لك رسالة الخطأ **ERR_NGROK_3200** أو أي خطأ متعلق بـ ngrok، فاتبع الخطوات التالية:

### الطريقة الأولى (الموصى بها): استخدام pyngrok مباشرة في Colab

```python
# الخلية 1: تثبيت المكتبات
!pip install -q streamlit pyngrok plotly scikit-learn pandas numpy matplotlib seaborn

# الخلية 2: تشغيل Streamlit مع ngrok مباشرة
from pyngrok import ngrok
import subprocess
import time

# ضبط token الخاص بك
ngrok.set_auth_token('3FghmjIhl8Oc4iIbV9Vre1J9HlH_6F5ykoVyfgacWCkGscjY9')

# تشغيل Streamlit في الخلفية
proc = subprocess.Popen(
    ['streamlit', 'run', 'app.py', 
     '--server.port', '8501',
     '--server.address', 'localhost',
     '--server.headless', 'true']
)

time.sleep(5)  # انتظر حتى يبدأ Streamlit

# إنشاء النفق
tunnel = ngrok.connect(8501)
print('=' * 60)
print(f'🔗 افتح الرابط التالي: {tunnel.public_url}')
print('=' * 60)

# إبقاء الخلية تعمل
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\nإيقاف...')
    ngrok.disconnect()
    proc.terminate()
```

### الطريقة الثانية: استخدام ملف run_colab_ngrok.py

```python
# الخلية 1: تثبيت المكتبات
!pip install -q streamlit pyngrok

# الخلية 2: تحميل الملف (إذا لم يكن موجوداً)
!wget https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/run_colab_ngrok.py -O run_colab_ngrok.py

# الخلية 3: تشغيل الملف
!python run_colab_ngrok.py
```

## خطوات التشغيل الكاملة

### 1. فتح المشروع على Colab

1. اذهب إلى [Google Colab](https://colab.research.google.com)
2. اختر **File → Open notebook → GitHub**
3. أدخل اسم المستخدم واسم المستودع
4. اختر `california_housing_project.ipynb`

### 2. تشغيل الخلايا

1. **Runtime → Run all** لتشغيل جميع الخلايا
2. أو اضغط **Shift+Enter** لكل خلية على حدة

### 3. تشغيل Dashboard التفاعلي

بعد تشغيل جميع خلايا الدفتر، شغّل الخلايا الخاصة بـ Streamlit في النهاية.

## استكشاف الأخطاء الشائعة

### ❌ خطأ: ERR_NGROK_3200

**السبب**: النفق غير متصل أو الـ token غير صحيح

**الحل**:
```python
# تأكد من ضبط token بشكل صحيح
from pyngrok import ngrok
ngrok.set_auth_token('3FghmjIhl8Oc4iIbV9Vre1J9HlH_6F5ykoVyfgacWCkGscjY9')
```

### ❌ خطأ: SyntaxError في GridSearchCV

**السبب**: صيغة print خاطئة

**الحل**: تأكد من استخدام f-string:
```python
# ✅ الصحيح
print(f'Best F1: {grid_dt.best_score_:.4f}')

# ❌ الخطأ
print('Best F1:', grid_dt.best_score_:.4f)
```

### ❌ خطأ: ModuleNotFoundError

**الحل**: ثبّت جميع المكتبات:
```python
!pip install -q streamlit pyngrok scikit-learn pandas numpy matplotlib seaborn plotly joblib
```

## روابط مفيدة

- [لوحة تحكم ngrok](https://dashboard.ngrok.com)
- [توثيق Streamlit](https://docs.streamlit.io)
- [توثيق pyngrok](https://pyngrok.readthedocs.io)

---

**تم التحديث**: 2025
