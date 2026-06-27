import os
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
