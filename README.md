# MCS_IDM_C1_F25 - California Housing Project (ngrok only)

هذا الإصدار معدّل ليعمل عبر **ngrok فقط** بدل LocalTunnel.

## الملفات
- `california_housing_project.ipynb` : الدفتر الرئيسي للتنفيذ والتشغيل.
- `app.py` : تطبيق Streamlit.
- `requirements.txt` : الحزم المطلوبة.
- `run_colab_ngrok.py` : تشغيل التطبيق في Colab عبر ngrok.
- `project_report_template.md` : قالب تقرير.
- `.gitignore` : تجاهل الملفات المؤقتة.

## التشغيل على Colab

1. افتح `california_housing_project.ipynb` من GitHub في Colab.
2. شغّل خلايا التحليل والتدريب.
3. في قسم تشغيل Streamlit عبر ngrok، نفّذ الخلايا التالية بالترتيب:
   - تثبيت `streamlit` و `pyngrok`
   - ضبط `NGROK_AUTHTOKEN`
   - تشغيل `!python run_colab_ngrok.py`
4. انسخ الرابط الذي يظهر بعد `Public URL:` وافتحه في المتصفح.

## ملاحظات
- هذا الإصدار لا يحتوي على LocalTunnel.
- تأكد أن `app.py` موجود في نفس المجلد الذي تشغّل منه الدفتر.
- إذا أعدت تشغيل Runtime في Colab، أعد تنفيذ التثبيت وضبط التوكن وتشغيل النفق.

مجموعة California Housing تُحمّل عبر `fetch_california_housing(as_frame=True)`، والهدف هو قيمة المنزل الوسيطة، وعدد العينات 20,640 مع 8 ميزات إدخال وفق توثيق scikit-learn.