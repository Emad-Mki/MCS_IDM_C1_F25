# MCS_IDM_C1_F25 - California Housing ML Project

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
