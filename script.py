
import os, json
os.makedirs('output/california_housing_project', exist_ok=True)
base = 'output/california_housing_project'

# ==================== 1. requirements.txt ====================
requirements = """pandas
numpy
scikit-learn
matplotlib
seaborn
streamlit
scipy
pyngrok
plotly
joblib
"""
with open(f'{base}/requirements.txt', 'w') as f: f.write(requirements)

# ==================== 2. .gitignore ====================
gitignore = """__pycache__/
.ipynb_checkpoints/
artifacts/
*.log
"""
with open(f'{base}/.gitignore', 'w') as f: f.write(gitignore)

# ==================== 3. project_report_template.md ====================
report_template = """# California Housing Project Report

## 1. Introduction
اكتب هنا مقدمة المشروع والهدف منه.

## 2. Dataset
- المصدر: sklearn.datasets.fetch_california_housing
- عدد الصفوف: 20,640
- عدد الميزات: 8
- العمود الهدف: MedHouseVal

## 3. Regression
- نتائج Linear Regression (RMSE, MAE, R²)
- مقارنة Ridge و Lasso
- تحليل Polynomial Features

## 4. Classification
- التصنيف الثنائي (Expensive / Affordable)
- التصنيف متعدد الفئات (4 أرباع)

## 5. Clustering
- KMeans لـ k=3,4,5
- Hierarchical Clustering (Bonus)
- تحليل الخريطة الجغرافية

## 6. Comparative Analysis
- مقارنة التعلم المُشرف وغير المُشرف
- أبرز 3 نتائج

## 7. Bonus
- GridSearchCV
- Hierarchical Clustering
- Streamlit Dashboard
"""
with open(f'{base}/project_report_template.md', 'w', encoding='utf-8') as f: f.write(report_template)

# ==================== 4. run_colab_ngrok.py ====================
run_ngrok = """import os
import time
import subprocess
from pyngrok import ngrok, conf

token = os.environ.get('NGROK_AUTHTOKEN', '')
if not token:
    raise ValueError('Please set NGROK_AUTHTOKEN environment variable before running.')

conf.get_default().auth_token = token

proc = subprocess.Popen(
    ['streamlit', 'run', 'app.py',
     '--server.port', '8501',
     '--server.address', 'localhost',
     '--server.headless', 'true'],
    stdout=open('/content/streamlit.log', 'w'),
    stderr=subprocess.STDOUT
)

print("Streamlit starting, waiting 10 seconds...")
time.sleep(10)

tunnel = ngrok.connect(8501)
print('=' * 50)
print('Public URL:', tunnel.public_url)
print('=' * 50)
"""
with open(f'{base}/run_colab_ngrok.py', 'w') as f: f.write(run_ngrok)

# ==================== 5. README.md ====================
readme = """# MCS_IDM_C1_F25 - California Housing ML Project

مشروع تحليل بيانات إسكان كاليفورنيا باستخدام تقنيات Regression و Classification و Clustering.

## هيكل الملفات
```
california_housing_project/
├── california_housing_project.ipynb   ← الدفتر الرئيسي
├── app.py                              ← لوحة Streamlit التفاعلية
├── run_colab_ngrok.py                  ← تشغيل Streamlit عبر ngrok في Colab
├── requirements.txt                    ← المكتبات المطلوبة
├── project_report_template.md          ← قالب التقرير
└── .gitignore
```

## Dataset
- المصدر: `sklearn.datasets.fetch_california_housing`
- 20,640 عينة، 8 ميزات إدخال، الهدف: قيمة المنزل الوسيطة (MedHouseVal)

## خطوات تشغيل المشروع على Google Colab

### الطريقة السريعة:
1. اذهب إلى [colab.research.google.com](https://colab.research.google.com)
2. File → Open notebook → GitHub
3. الصق رابط الـ repository وافتح `california_housing_project.ipynb`
4. شغّل الخلايا بالترتيب من الأعلى للأسفل

### تشغيل Streamlit Dashboard:
```python
# الخلية 1: تثبيت المكتبات
!pip install -q streamlit pyngrok

# الخلية 2: ضبط ngrok token
import os
os.environ['NGROK_AUTHTOKEN'] = 'YOUR_TOKEN_HERE'

# الخلية 3: تشغيل التطبيق
!python run_colab_ngrok.py
```
انسخ الرابط الذي يظهر بعد `Public URL:` وافتحه في المتصفح.

## الأجزاء
| الجزء | الموضوع | النقاط |
|-------|---------|--------|
| Part 1 | Introduction & Setup | 5 |
| Part 2 | Regression | 30 |
| Part 3 | Classification | 30 |
| Part 4 | Clustering | 25 |
| Part 5 | Comparative Analysis | 10 |
| Bonus | Hierarchical, GridSearchCV, Streamlit | +10 |

## ملاحظات
- تأكد أن `app.py` موجود في نفس مجلد الدفتر
- artifacts/ تُنشأ تلقائياً عند تشغيل الدفتر
- عند إعادة تشغيل Runtime في Colab أعد تنفيذ خلايا التثبيت
"""
with open(f'{base}/README.md', 'w', encoding='utf-8') as f: f.write(readme)

print("Files 1-5 created successfully.")
print(os.listdir(base))
