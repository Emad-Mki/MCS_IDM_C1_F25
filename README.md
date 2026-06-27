# 🏠 California Housing ML Project - MCS_IDM_C1_F25

## نظرة عامة على المشروع

مشروع شامل لتحليل بيانات إسكان كاليفورنيا باستخدام تقنيات التعلم الآلي المختلفة:
- **Regression**: التنبؤ بقيمة المنازل
- **Classification**: تصنيف المنازل كـ "غالية" أو "معقولة"
- **Clustering**: تجميع المناطق المتشابهة جغرافياً وديموغرافياً
- **Comparative Analysis**: مقارنة النتائج واستخلاص الاستنتاجات

## هيكل الملفات

```
california_housing_project/
├── california_housing_project.ipynb    ← الدفتر الرئيسي (Google Colab)
├── app.py                               ← لوحة Streamlit التفاعلية
├── run_colab_ngrok.py                   ← تشغيل Streamlit عبر ngrok
├── requirements.txt                     ← المكتبات المطلوبة
├── project_report_template.md           ← قالب التقرير
├── .gitignore                          ← ملف تجاهل Git
└── README.md                           ← هذا الملف
```

## مجموعة البيانات (Dataset)

- **المصدر**: `sklearn.datasets.fetch_california_housing`
- **عدد العينات**: 20,640 عينة
- **الميزات (Features)**: 8 ميزات إدخال
  - `MedInc`: متوسط الدخل في المجموعة
  - `HouseAge`: متوسط عمر المنزل
  - `AveRooms`: متوسط عدد الغرف
  - `AveBedrms`: متوسط عدد غرف النوم
  - `Population`: السكان في المجموعة
  - `AveOccup`: متوسط عدد أفراد الأسرة
  - `Latitude`: خط العرض
  - `Longitude`: خط الطول
- **الهدف (Target)**: `MedHouseVal` - قيمة المنزل الوسيطة (بآلاف الدولارات)

## خطوات التشغيل على Google Colab

### الطريقة السريعة (Recommended):

1. **افتح Google Colab**: اذهب إلى [colab.research.google.com](https://colab.research.google.com)

2. **افتح الدفتر**:
   - File → Open notebook → GitHub
   - الصق رابط الـ repository الخاص بك
   - اختر `california_housing_project.ipynb`

3. **شغّل الخلايا بالترتيب**:
   - Runtime → Run all (أو اضغط Shift+Enter لكل خلية)

4. **لتشغيل Streamlit Dashboard**:
   ```python
   # الخلية 1: تثبيت المكتبات
   !pip install -q streamlit pyngrok plotly

   # الخلية 2: ضبط ngrok token
   import os
   os.environ['NGROK_AUTHTOKEN'] = '3FghmjIhl8Oc4iIbV9Vre1J9HlH_6F5ykoVyfgacWCkGscjY9'

   # الخلية 3: تشغيل التطبيق
   !python run_colab_ngrok.py
   ```

5. **انسخ الرابط**: بعد التشغيل، سيظهر رابط عام (Public URL) - انسخه وافتحه في المتصفح

## أجزاء المشروع والتقييم

| الجزء | الموضوع | النقاط |
|-------|---------|--------|
| Part 1 | Introduction & Setup | 5 pts |
| Part 2 | Regression Task | 30 pts |
| Part 3 | Classification Task | 30 pts |
| Part 4 | Clustering Task | 25 pts |
| Part 5 | Comparative Analysis | 10 pts |
| **Bonus** | Hierarchical + GridSearchCV + Streamlit | +10 pts |
| **المجموع** | | **100 + 10** |

## تفاصيل كل جزء

### Part 1: Introduction & Setup (5 pts)
- تحميل البيانات باستخدام `fetch_california_housing(as_frame=True)`
- تحويل البيانات إلى DataFrame
- وصف البيانات (عدد الصفوف، الميزات، الهدف)
- تقسيم البيانات إلى train/test (80/20)

### Part 2: Regression Task (30 pts)
- تدريب Linear Regression كخط أساس
- التقييم باستخدام RMSE, MAE, R²
- تدريب Ridge و Lasso ومقارنتها
- إضافة Polynomial Features (degree=2) لـ MedInc و HouseAge
- تحديد أقوى الميزات ومناقشة أفضل نموذج

### Part 3: Classification Task (30 pts)
- إنشاء تسمية ثنائية: Expensive إذا كانت MedHouseValue > الوسيط
- تدريب Logistic Regression و Decision Tree
- التقارير: Accuracy, Precision, Recall, F1, Confusion Matrix
- التصنيف متعدد الفئات باستخدام quartiles
- مقارنة النتائج بين الثنائي ومتعدد الفئات

### Part 4: Clustering Task (25 pts)
- توحيد الميزات (Standardization)
- تقليل الأبعاد إلى 2D باستخدام PCA
- تطبيق KMeans مع k=4
- التقييم باستخدام Inertia (SSE) و Silhouette Score
- مقارنة k=3, k=4, k=5
- تصور clusters في فضاء PCA وعلى خريطة كاليفورنيا
- مناقشة تطابق clusters مع المناطق الجغرافية

### Part 5: Comparative Analysis (10 pts)
- ملخص نتائج Regression و Classification و Clustering
- مقارنة التعلم المُشرف vs غير المُشرف
- 3 استنتاجات رئيسية من المشروع

### Bonus (+10 pts)
- تجربة Hierarchical Clustering ومقارنتها مع KMeans
- ضبط المعلمات باستخدام GridSearchCV
- بناء Streamlit Dashboard للتفاعل مع النموذج

## المخرجات (Artifacts)

بعد تشغيل الدفتر، سيتم إنشاء مجلد `artifacts/` يحتوي على:

| الملف | الوصف |
|-------|-------|
| `regression_results.csv` | نتائج نماذج الانحدار |
| `classification_binary_results.csv` | نتائج التصنيف الثنائي |
| `classification_multiclass_results.csv` | نتائج التصنيف متعدد الفئات |
| `clustering_scores.csv` | نتائج KMeans لقيم k المختلفة |
| `hierarchical_scores.csv` | مقارنة KMeans و Hierarchical |
| `feature_importance.csv` | أهمية الميزات في الانحدار |
| `kmeans_clusters.csv` | تسميات clusters مع إحداثيات PCA |
| `*.joblib` | النماذج المدربة المحفوظة |
| `*.png` | الرسوم البيانية والصور |

## متطلبات النظام

- Python 3.8+
- Google Colab (موصى به) أو بيئة محلية مع Jupyter

## المكتبات المطلوبة

```bash
pandas
numpy
scikit-learn
matplotlib
seaborn
streamlit
scipy
pyngrok
plotly
joblib
```

## استكشاف الأخطاء

### مشكلة: ngrok لا يعمل
- تأكد من صحة token
- أعد تثبيت pyngrok: `!pip install --upgrade pyngrok`

### مشكلة: Streamlit لا يظهر
- انتظر 10-15 ثانية بعد التشغيل
- تحقق من logs: `!cat /content/streamlit.log`

### مشكلة: الملفات المفقودة
- شغّل جميع خلايا الدفتر بالترتيب
- تأكد من وجود `app.py` في نفس المجلد

## روابط مفيدة

- [Google Colab](https://colab.research.google.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [ngrok Documentation](https://ngrok.com/docs)
- [Scikit-learn California Housing](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html)

## الترخيص

هذا المشروع لأغراض تعليمية كجزء من دورة Intelligent Data Mining (IDM).

---

**تم التطوير بواسطة**: MCS_IDM_C1_F25  
**التاريخ**: 2025
