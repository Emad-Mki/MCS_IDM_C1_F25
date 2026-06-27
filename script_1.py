
base = 'output/california_housing_project'

# ==================== 6. app.py (Streamlit Dashboard - FULL) ====================
app_py = '''import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import fetch_california_housing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

st.set_page_config(page_title="California Housing ML Project", layout="wide", page_icon="🏠")
st.title("🏠 California Housing ML Project Dashboard")
st.caption("Regression | Classification | Clustering | Comparative Analysis — IDM Project")

@st.cache_data
def load_data():
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.copy()
    target_col = (housing.target.name
                  if hasattr(housing.target, "name") and housing.target.name in df.columns
                  else "MedHouseVal")
    return df, target_col

@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df, target_col = load_data()
feature_cols = [c for c in df.columns if c != target_col]

st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to", [
    "📊 Overview",
    "📈 Regression",
    "🏷️ Classification",
    "🔵 Clustering",
    "🔮 Prediction",
    "📋 Comparative Analysis"
])

# ─── OVERVIEW ───────────────────────────────────────────────────────────────
if section == "📊 Overview":
    st.subheader("Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Input Features", len(feature_cols))
    c3.metric("Target", target_col)
    c4.metric("Missing Values", int(df.isnull().sum().sum()))

    st.markdown("### Feature Description")
    desc = {
        "MedInc": "Median income in block group",
        "HouseAge": "Median house age in block group",
        "AveRooms": "Average number of rooms per household",
        "AveBedrms": "Average number of bedrooms per household",
        "Population": "Block group population",
        "AveOccup": "Average number of household members",
        "Latitude": "Block group latitude",
        "Longitude": "Block group longitude",
        "MedHouseVal": "Median house value (target, in $100k)"
    }
    st.table(pd.DataFrame({"Feature": list(desc.keys()), "Description": list(desc.values())}))

    st.markdown("### Statistical Summary")
    st.dataframe(df.describe().round(3), use_container_width=True)

    if "MedInc" in df.columns:
        fig = px.scatter(
            df.sample(min(3000, len(df)), random_state=42),
            x="MedInc", y=target_col, color="HouseAge",
            title="Median Income vs House Value (colored by House Age)",
            labels={"MedInc": "Median Income", target_col: "House Value ($100k)"}
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Correlation Heatmap")
    corr = df.corr(numeric_only=True)
    fig2 = px.imshow(corr, text_auto=".2f", aspect="auto",
                     title="Feature Correlation Matrix", color_continuous_scale="RdBu_r")
    st.plotly_chart(fig2, use_container_width=True)

# ─── REGRESSION ─────────────────────────────────────────────────────────────
elif section == "📈 Regression":
    st.subheader("Regression Results")
    reg = load_csv("artifacts/regression_results.csv")
    feat = load_csv("artifacts/feature_importance.csv")

    if reg is not None:
        st.markdown("#### Model Comparison")
        st.dataframe(reg.round(4), use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(reg, x="Model", y="R2", color="Model",
                         title="R² Score by Model", text_auto=".3f")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig2 = px.bar(reg, x="Model", y="RMSE", color="Model",
                          title="RMSE by Model", text_auto=".3f")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ Run the notebook first to generate regression artifacts.")

    if feat is not None:
        st.markdown("#### Feature Importance (Linear Regression Coefficients)")
        fig = px.bar(feat.head(10), x="Feature", y="AbsCoefficient",
                     color="AbsCoefficient", title="Top Features by Coefficient Magnitude")
        st.plotly_chart(fig, use_container_width=True)

# ─── CLASSIFICATION ──────────────────────────────────────────────────────────
elif section == "🏷️ Classification":
    st.subheader("Classification Results")
    binary = load_csv("artifacts/classification_binary_results.csv")
    multi  = load_csv("artifacts/classification_multiclass_results.csv")

    if binary is not None:
        st.markdown("### Binary Classification (Expensive / Affordable)")
        st.dataframe(binary.round(4), use_container_width=True)
        metrics = [c for c in binary.columns if c != "Model"]
        fig = px.bar(binary.melt(id_vars="Model", value_vars=metrics),
                     x="Model", y="value", color="variable", barmode="group",
                     title="Binary Classification Metrics")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Binary classification artifacts not found. Run the notebook.")

    if multi is not None:
        st.markdown("### Multi-class Classification (4 Quartiles)")
        st.dataframe(multi.round(4), use_container_width=True)
    else:
        st.warning("⚠️ Multi-class classification artifacts not found.")

# ─── CLUSTERING ──────────────────────────────────────────────────────────────
elif section == "🔵 Clustering":
    st.subheader("Clustering Results")
    scores = load_csv("artifacts/clustering_scores.csv")
    hier   = load_csv("artifacts/hierarchical_scores.csv")

    if scores is not None:
        st.markdown("#### KMeans Metrics (k = 3, 4, 5)")
        st.dataframe(scores.round(4), use_container_width=True)
        fig = px.line(scores, x="k", y=["Inertia_SSE", "Silhouette"],
                      markers=True, title="KMeans Inertia & Silhouette by k")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Clustering artifacts not found. Run the notebook.")

    if hier is not None:
        st.markdown("#### Hierarchical Clustering (Bonus)")
        st.dataframe(hier.round(4), use_container_width=True)

    if "Longitude" in df.columns and "Latitude" in df.columns:
        st.markdown("#### California Map — House Values")
        fig_map = px.scatter(
            df.sample(min(5000, len(df)), random_state=42),
            x="Longitude", y="Latitude", color=target_col,
            color_continuous_scale="plasma",
            title="California Map Colored by Median House Value",
            labels={target_col: "House Value ($100k)"},
            opacity=0.6
        )
        st.plotly_chart(fig_map, use_container_width=True)

    cluster_df = load_csv("artifacts/kmeans_clusters.csv")
    if cluster_df is not None:
        st.markdown("#### KMeans Clusters on California Map (k=4)")
        fig_cl = px.scatter(
            cluster_df.sample(min(5000, len(cluster_df)), random_state=42),
            x="Longitude", y="Latitude",
            color=cluster_df.sample(min(5000, len(cluster_df)), random_state=42)["Cluster"].astype(str),
            title="KMeans Clusters (k=4) on California Map",
            labels={"color": "Cluster"}
        )
        st.plotly_chart(fig_cl, use_container_width=True)

# ─── PREDICTION ──────────────────────────────────────────────────────────────
elif section == "🔮 Prediction":
    st.subheader("Single House Value Prediction")
    st.info("Fill in the feature values below and click Predict.")

    defaults = df[feature_cols].median()
    values = {}
    cols_ui = st.columns(2)
    for i, f in enumerate(feature_cols):
        values[f] = cols_ui[i % 2].number_input(f, value=float(defaults[f]), format="%.4f")

    model_name = st.selectbox("Select Regression Model", [
        "linear_regression_model.joblib",
        "ridge_model.joblib",
        "polynomial_ridge_model.joblib"
    ])
    model_path = os.path.join("artifacts", model_name)

    if st.button("🔮 Predict House Value"):
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            X_input = pd.DataFrame([values])
            pred = model.predict(X_input)[0]
            st.success(f"✅ Predicted {target_col}: **{pred:.4f}** (≈ ${pred*100_000:,.0f})")
        else:
            st.error("❌ Model file not found. Run the notebook first to train models.")

# ─── COMPARATIVE ANALYSIS ────────────────────────────────────────────────────
elif section == "📋 Comparative Analysis":
    st.subheader("Comparative Analysis")
    st.markdown("""
    ### Supervised vs Unsupervised Learning

    | Aspect | Supervised (Regression/Classification) | Unsupervised (Clustering) |
    |--------|----------------------------------------|---------------------------|
    | Labels needed | ✅ Yes | ❌ No |
    | Goal | Predict a target value or class | Discover hidden patterns |
    | Evaluation | RMSE, R², Accuracy, F1 | Inertia (SSE), Silhouette |
    | Example here | Predict house value / Expensive? | Group similar neighborhoods |

    ### Key Takeaways
    1. **MedInc is the strongest predictor** — median income has the highest correlation with house value.
    2. **Polynomial features improved regression** — degree-2 features for MedInc & HouseAge reduced RMSE.
    3. **KMeans clusters align with geography** — clusters roughly correspond to coastal vs inland regions.

    ### Model Summary
    """)
    reg = load_csv("artifacts/regression_results.csv")
    binary = load_csv("artifacts/classification_binary_results.csv")
    scores = load_csv("artifacts/clustering_scores.csv")

    if reg is not None:
        st.markdown("**Regression**")
        st.dataframe(reg.round(4), use_container_width=True)
    if binary is not None:
        st.markdown("**Classification (Binary)**")
        st.dataframe(binary.round(4), use_container_width=True)
    if scores is not None:
        st.markdown("**Clustering**")
        st.dataframe(scores.round(4), use_container_width=True)
'''

with open(f'{base}/app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("app.py created:", os.path.getsize(f'{base}/app.py'), "bytes")
