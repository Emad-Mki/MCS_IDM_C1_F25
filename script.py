import os, json, textwrap
base='output/mcs_idm_ngrok_only'
os.makedirs(base, exist_ok=True)

readme = '''# MCS_IDM_C1_F25 - California Housing Project (ngrok only)

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

مجموعة California Housing تُحمّل عبر `fetch_california_housing(as_frame=True)`، والهدف هو قيمة المنزل الوسيطة، وعدد العينات 20,640 مع 8 ميزات إدخال وفق توثيق scikit-learn.'''  # [web:7][web:23][web:32][web:40][web:37]
with open(f'{base}/README.md','w',encoding='utf-8') as f: f.write(readme)

with open(f'{base}/.gitignore','w',encoding='utf-8') as f: f.write('__pycache__/\n.ipynb_checkpoints/\nartifacts/\n*.log\n')

with open(f'{base}/requirements.txt','w',encoding='utf-8') as f:
    f.write('pandas\nnumpy\nscikit-learn\nmatplotlib\nseaborn\nstreamlit\nscipy\npyngrok\nplotly\njoblib\n')

app = '''import os
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.datasets import fetch_california_housing

st.set_page_config(page_title='California Housing ML Project', layout='wide')
st.title('California Housing ML Project Dashboard')
st.caption('Regression, Classification, Clustering, and Comparative Analysis')

@st.cache_data
def load_data():
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.copy()
    target_col = housing.target.name if hasattr(housing.target, 'name') and housing.target.name in df.columns else 'MedHouseVal'
    return df, target_col

@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


df, target_col = load_data()
feature_cols = [c for c in df.columns if c != target_col]

st.sidebar.header('Navigation')
section = st.sidebar.radio('Go to', ['Overview', 'Regression', 'Classification', 'Clustering', 'Prediction'])

if section == 'Overview':
    st.subheader('Dataset Overview')
    c1, c2, c3 = st.columns(3)
    c1.metric('Rows', f"{df.shape[0]:,}")
    c2.metric('Input Features', len(feature_cols))
    c3.metric('Target', target_col)
    st.dataframe(df.head(), use_container_width=True)
    if 'MedInc' in df.columns:
        fig = px.scatter(df.sample(min(3000, len(df)), random_state=42), x='MedInc', y=target_col, color='HouseAge', title='MedInc vs Target')
        st.plotly_chart(fig, use_container_width=True)

elif section == 'Regression':
    st.subheader('Regression Results')
    reg = load_csv('artifacts/regression_results.csv')
    feat = load_csv('artifacts/feature_importance.csv')
    if reg is not None:
        st.dataframe(reg, use_container_width=True)
        st.plotly_chart(px.bar(reg, x='Model', y='R2', title='R² by Regression Model'), use_container_width=True)
    else:
        st.warning('Run the notebook first to generate regression artifacts.')
    if feat is not None:
        st.plotly_chart(px.bar(feat.head(8), x='Feature', y='AbsCoefficient', title='Strongest Features'), use_container_width=True)

elif section == 'Classification':
    st.subheader('Classification Results')
    b = load_csv('artifacts/classification_binary_results.csv')
    m = load_csv('artifacts/classification_multiclass_results.csv')
    if b is not None:
        st.markdown('### Binary Classification')
        st.dataframe(b, use_container_width=True)
        st.plotly_chart(px.bar(b, x='Model', y='F1', title='Binary F1 Score'), use_container_width=True)
    else:
        st.warning('Binary classification artifacts not found.')
    if m is not None:
        st.markdown('### Multi-class Classification')
        st.dataframe(m, use_container_width=True)
    else:
        st.warning('Multi-class classification artifacts not found.')

elif section == 'Clustering':
    st.subheader('Clustering Results')
    c = load_csv('artifacts/clustering_scores.csv')
    if c is not None:
        st.dataframe(c, use_container_width=True)
        st.plotly_chart(px.line(c, x='k', y=['Inertia_SSE','Silhouette'], markers=True, title='KMeans Metrics by k'), use_container_width=True)
    else:
        st.warning('Clustering artifacts not found.')
    if 'Longitude' in df.columns and 'Latitude' in df.columns:
        fig = px.scatter(df.sample(min(4000, len(df)), random_state=42), x='Longitude', y='Latitude', color=target_col, title='California Coordinates Colored by Target')
        st.plotly_chart(fig, use_container_width=True)

elif section == 'Prediction':
    st.subheader('Single Prediction')
    defaults = df[feature_cols].median()
    values = {}
    cols = st.columns(2)
    for i, f in enumerate(feature_cols):
        values[f] = cols[i % 2].number_input(f, value=float(defaults[f]))
    model_name = st.selectbox('Regression model', ['linear_regression_model.joblib','ridge_model.joblib','polynomial_ridge_model.joblib'])
    model_path = os.path.join('artifacts', model_name)
    if st.button('Predict house value'):
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            X_input = pd.DataFrame([values])
            pred = model.predict(X_input)[0]
            st.success(f'Predicted {target_col}: {pred:.4f} (in $100,000 units)')
        else:
            st.error('Model file not found. Run california_housing_project.ipynb first.')
'''
with open(f'{base}/app.py','w',encoding='utf-8') as f: f.write(app)

run_ngrok = '''import os
import time
import subprocess
from pyngrok import ngrok

token = os.environ.get('NGROK_AUTHTOKEN')
if not token:
    raise ValueError('Please set NGROK_AUTHTOKEN in environment variables before running.')

ngrok.set_auth_token(token)

subprocess.Popen([
    'streamlit', 'run', 'app.py',
    '--server.port', '8501',
    '--server.address', 'localhost',
    '--server.headless', 'true'
], stdout=open('/content/streamlit.log', 'w'), stderr=subprocess.STDOUT)

time.sleep(8)
public_url = ngrok.connect(8501)
print('Public URL:', public_url)
'''
with open(f'{base}/run_colab_ngrok.py','w',encoding='utf-8') as f: f.write(run_ngrok)

report = '''# California Housing Project Report

## 1. Introduction
## 2. Dataset
## 3. Regression
## 4. Classification
## 5. Clustering
## 6. Comparative Analysis
## 7. Bonus
'''
with open(f'{base}/project_report_template.md','w',encoding='utf-8') as f: f.write(report)

nb = {
 "cells": [],
 "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.10"}},
 "nbformat": 4,
 "nbformat_minor": 5
}

cells=[]
cells.append({"cell_type":"markdown","metadata":{},"source":["# California Housing ML Project\n","نسخة جاهزة للتشغيل عبر ngrok فقط."]})
cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":["!pip install -q -r requirements.txt"]})
cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":["import os, warnings, joblib\n","warnings.filterwarnings('ignore')\n","import numpy as np\n","import pandas as pd\n","from sklearn.datasets import fetch_california_housing\n","from sklearn.model_selection import train_test_split\n","os.makedirs('artifacts', exist_ok=True)\n","housing = fetch_california_housing(as_frame=True)\n","df = housing.frame.copy()\n","target_col = housing.target.name if hasattr(housing.target, 'name') and housing.target.name in df.columns else 'MedHouseVal'\n","print('Target column used:', target_col)\n","df.head()"]})
cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":["print('Rows, Columns:', df.shape)\n","print('Columns:', df.columns.tolist())\n","print('Features:', list(df.drop(columns=[target_col]).columns))\n","print('Target:', target_col)\n","df.describe()"]})
cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":["X = df.drop(columns=[target_col])\n","y = df[target_col]\n","X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n","print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)"]})
cells.append({"cell_type":"markdown","metadata":{},"source":["## 13/14. Streamlit via ngrok\n","LocalTunnel removed. Use ngrok only."]})
cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":["!pip install -q streamlit pyngrok"]})
cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":["import os\n","os.environ['NGROK_AUTHTOKEN'] = '3FghmjIhl8Oc4iIbV9Vre1J9HlH_6F5ykoVyfgacWCkGscjY9'\n","print('NGROK_AUTHTOKEN set.')"]})
cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":["!python run_colab_ngrok.py"]})
nb['cells']=cells
with open(f'{base}/california_housing_project.ipynb','w',encoding='utf-8') as f: json.dump(nb,f,ensure_ascii=False,indent=2)

print(base, os.listdir(base))