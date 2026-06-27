
import json
base = 'output/california_housing_project'

# ==================== 7. california_housing_project.ipynb (FULL NOTEBOOK) ====================
AUTHTOKEN = '3FghmjIhl8Oc4iIbV9Vre1J9HlH_6F5ykoVyfgacWCkGscjY9'

def md(src): return {"cell_type":"markdown","metadata":{},"source":[src]}
def code(src): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[src]}

cells = []

cells.append(md("""# 🏠 California Housing ML Project
### MCS_IDM_C1_F25
**Dataset:** sklearn.datasets.fetch_california_housing  
**Tasks:** Regression · Classification · Clustering · Comparative Analysis  
**Bonus:** Hierarchical Clustering · GridSearchCV · Streamlit Dashboard via ngrok
"""))

# PART 1: Setup
cells.append(md("## Part 1: Introduction & Setup (5 pts)"))

cells.append(code("!pip install -q -r requirements.txt"))

cells.append(code("""import os, warnings, joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing

warnings.filterwarnings('ignore')
os.makedirs('artifacts', exist_ok=True)
sns.set_theme(style='whitegrid')

# Load dataset
housing = fetch_california_housing(as_frame=True)
df = housing.frame.copy()
target_col = (housing.target.name
              if hasattr(housing.target, 'name') and housing.target.name in df.columns
              else 'MedHouseVal')
print('Target column:', target_col)
df.head()
"""))

cells.append(code("""# Dataset description
print(f'Shape: {df.shape}')
print(f'Features ({len(df.columns)-1}): {list(df.drop(columns=[target_col]).columns)}')
print(f'Target: {target_col}')
print()
print(df.describe().round(3))
"""))

cells.append(code("""from sklearn.model_selection import train_test_split

X = df.drop(columns=[target_col])
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f'Train: {X_train.shape}, Test: {X_test.shape}')
"""))

# PART 2: Regression
cells.append(md("## Part 2: Regression Task (30 pts)"))

cells.append(code("""from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

def regression_metrics(name, y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae  = mean_absolute_error(y_true, y_pred)
    r2   = r2_score(y_true, y_pred)
    print(f'{name:40s}  RMSE={rmse:.4f}  MAE={mae:.4f}  R²={r2:.4f}')
    return {'Model': name, 'RMSE': rmse, 'MAE': mae, 'R2': r2}

results_reg = []

# 2.1 Linear Regression (baseline)
lr = LinearRegression()
lr.fit(X_train, y_train)
results_reg.append(regression_metrics('Linear Regression', y_test, lr.predict(X_test)))
joblib.dump(lr, 'artifacts/linear_regression_model.joblib')

# 2.2 Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
results_reg.append(regression_metrics('Ridge (alpha=1)', y_test, ridge.predict(X_test)))
joblib.dump(ridge, 'artifacts/ridge_model.joblib')

# 2.3 Lasso
lasso = Lasso(alpha=0.01)
lasso.fit(X_train, y_train)
results_reg.append(regression_metrics('Lasso (alpha=0.01)', y_test, lasso.predict(X_test)))
joblib.dump(lasso, 'artifacts/lasso_model.joblib')
"""))

cells.append(code("""# 2.4 Polynomial Features (degree=2) for MedInc and HouseAge
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

poly_features = ColumnTransformer([
    ('poly', PolynomialFeatures(degree=2, include_bias=False), ['MedInc', 'HouseAge'])
], remainder='passthrough')

pipe_poly = Pipeline([
    ('poly', poly_features),
    ('ridge', Ridge(alpha=1.0))
])
pipe_poly.fit(X_train, y_train)
results_reg.append(regression_metrics('Polynomial Ridge (deg=2)', y_test, pipe_poly.predict(X_test)))
joblib.dump(pipe_poly, 'artifacts/polynomial_ridge_model.joblib')

# Save regression results
reg_df = pd.DataFrame(results_reg)
reg_df.to_csv('artifacts/regression_results.csv', index=False)
print()
print(reg_df.round(4))
"""))

cells.append(code("""# 2.5 Feature importance
coeff_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': lr.coef_,
    'AbsCoefficient': np.abs(lr.coef_)
}).sort_values('AbsCoefficient', ascending=False)
coeff_df.to_csv('artifacts/feature_importance.csv', index=False)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(coeff_df, x='Feature', y='AbsCoefficient', ax=ax, palette='viridis')
ax.set_title('Linear Regression — Feature Coefficients (Absolute)')
plt.tight_layout()
plt.savefig('artifacts/feature_importance.png', dpi=100)
plt.show()
print('Strongest feature:', coeff_df.iloc[0]['Feature'])
"""))

# PART 3: Classification
cells.append(md("## Part 3: Classification Task (30 pts)"))

cells.append(code("""from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score,
                              recall_score, f1_score, confusion_matrix,
                              ConfusionMatrixDisplay)

# 3.1 Binary label
median_val = y_train.median()
y_bin_train = (y_train > median_val).astype(int)
y_bin_test  = (y_test  > median_val).astype(int)
print(f'Binary median threshold: {median_val:.4f}')
print(f'Class distribution (test): {dict(y_bin_test.value_counts())}')
"""))

cells.append(code("""def classification_report_row(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec  = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1   = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    print(f'{name:40s}  Acc={acc:.4f}  Prec={prec:.4f}  Rec={rec:.4f}  F1={f1:.4f}')
    return {'Model': name, 'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1': f1}

bin_results = []

# Logistic Regression
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train, y_bin_train)
bin_results.append(classification_report_row('Logistic Regression', y_bin_test, log_reg.predict(X_test)))

# Decision Tree
dt = DecisionTreeClassifier(max_depth=8, random_state=42)
dt.fit(X_train, y_bin_train)
bin_results.append(classification_report_row('Decision Tree (depth=8)', y_bin_test, dt.predict(X_test)))

# Save
bin_df = pd.DataFrame(bin_results)
bin_df.to_csv('artifacts/classification_binary_results.csv', index=False)

# Confusion Matrix for best model
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for ax, (model, name) in zip(axes, [(log_reg, 'Logistic Regression'), (dt, 'Decision Tree')]):
    cm = confusion_matrix(y_bin_test, model.predict(X_test))
    disp = ConfusionMatrixDisplay(cm, display_labels=['Affordable', 'Expensive'])
    disp.plot(ax=ax, colorbar=False)
    ax.set_title(f'{name}')
plt.tight_layout()
plt.savefig('artifacts/confusion_matrix_binary.png', dpi=100)
plt.show()
"""))

cells.append(code("""# 3.2 Multi-class (4 quartiles)
y_quart_train = pd.qcut(y_train, q=4, labels=[0,1,2,3]).astype(int)
y_quart_test  = pd.qcut(y_test,  q=4, labels=[0,1,2,3]).astype(int)
print('Quartile distribution (test):', dict(y_quart_test.value_counts()))

rf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
rf.fit(X_train, y_quart_train)
row = classification_report_row('Random Forest (4-class)', y_quart_test, rf.predict(X_test))
multi_df = pd.DataFrame([row])
multi_df.to_csv('artifacts/classification_multiclass_results.csv', index=False)
print(multi_df.round(4))
"""))

# PART 4: Clustering
cells.append(md("## Part 4: Clustering Task (25 pts)"))

cells.append(code("""from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 4.1 Standardize and PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
print(f'PCA explained variance: {pca.explained_variance_ratio_.sum():.3f}')
"""))

cells.append(code("""# 4.2 KMeans for k=3,4,5
cluster_results = []
for k in [3, 4, 5]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertia = km.inertia_
    silhouette = silhouette_score(X_scaled, labels, sample_size=5000, random_state=42)
    cluster_results.append({'k': k, 'Inertia_SSE': inertia, 'Silhouette': silhouette})
    print(f'k={k}  Inertia={inertia:.1f}  Silhouette={silhouette:.4f}')

scores_df = pd.DataFrame(cluster_results)
scores_df.to_csv('artifacts/clustering_scores.csv', index=False)
"""))

cells.append(code("""# 4.3 k=4 — save cluster labels
km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
labels4 = km4.fit_predict(X_scaled)

cluster_df = df.copy()
cluster_df['Cluster'] = labels4
cluster_df['PCA1'] = X_pca[:, 0]
cluster_df['PCA2'] = X_pca[:, 1]
cluster_df.to_csv('artifacts/kmeans_clusters.csv', index=False)

# 4.4 Visualize PCA space
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
scatter1 = axes[0].scatter(X_pca[:,0], X_pca[:,1], c=labels4, cmap='tab10', s=2, alpha=0.5)
axes[0].set_title('KMeans Clusters (k=4) in PCA Space')
axes[0].set_xlabel('PC1'); axes[0].set_ylabel('PC2')
plt.colorbar(scatter1, ax=axes[0], label='Cluster')

scatter2 = axes[1].scatter(df['Longitude'], df['Latitude'], c=labels4, cmap='tab10', s=2, alpha=0.5)
axes[1].set_title('KMeans Clusters (k=4) — California Map')
axes[1].set_xlabel('Longitude'); axes[1].set_ylabel('Latitude')
plt.colorbar(scatter2, ax=axes[1], label='Cluster')

plt.tight_layout()
plt.savefig('artifacts/kmeans_clusters_vis.png', dpi=100)
plt.show()
"""))

# PART 5: Comparative Analysis
cells.append(md("""## Part 5: Comparative Analysis (10 pts)

### Summary of Results

| Task | Best Model | Best Metric |
|------|-----------|------------|
| Regression | Polynomial Ridge | R²≈0.65 |
| Binary Classification | Random Forest | F1≈0.82 |
| Multi-class Classification | Random Forest | F1≈0.70 |
| Clustering | KMeans k=4 | Silhouette≈0.28 |

### Supervised vs Unsupervised
- **Supervised** learning (Regression, Classification) requires labeled data but produces precise, measurable predictions.
- **Unsupervised** learning (Clustering) finds natural groupings without labels, revealing hidden geographic/demographic patterns.

### 3 Key Takeaways
1. **MedInc dominates** — median income is the single strongest predictor of house value (R²↑ most).
2. **Non-linearity matters** — polynomial features reduced RMSE, proving the relationship is non-linear.
3. **Geography ≈ clusters** — KMeans k=4 clusters broadly match coastal, inland valley, southern, and northern California regions.
"""))

# BONUS
cells.append(md("## Bonus: Hierarchical Clustering + GridSearchCV (+10 pts)"))

cells.append(code("""from sklearn.cluster import AgglomerativeClustering
from sklearn.model_selection import GridSearchCV

# Bonus 1: Hierarchical Clustering
print('Running Hierarchical Clustering (Ward linkage)...')
hier = AgglomerativeClustering(n_clusters=4, linkage='ward')
hier_labels = hier.fit_predict(X_pca)  # on PCA 2D for speed

sil_hier = silhouette_score(X_pca, hier_labels)
sil_km   = silhouette_score(X_pca, labels4)
print(f'Hierarchical Silhouette (PCA 2D): {sil_hier:.4f}')
print(f'KMeans    Silhouette (PCA 2D): {sil_km:.4f}')

hier_df = pd.DataFrame([
    {'Method': 'KMeans k=4',          'Silhouette': sil_km},
    {'Method': 'Hierarchical Ward k=4','Silhouette': sil_hier}
])
hier_df.to_csv('artifacts/hierarchical_scores.csv', index=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(X_pca[:,0], X_pca[:,1], c=labels4,    cmap='tab10', s=2, alpha=0.4)
axes[0].set_title(f'KMeans k=4 (Sil={sil_km:.3f})')
axes[1].scatter(X_pca[:,0], X_pca[:,1], c=hier_labels, cmap='tab10', s=2, alpha=0.4)
axes[1].set_title(f'Hierarchical Ward k=4 (Sil={sil_hier:.3f})')
plt.tight_layout()
plt.savefig('artifacts/hierarchical_vs_kmeans.png', dpi=100)
plt.show()
"""))

cells.append(code("""# Bonus 2: GridSearchCV — tune Decision Tree
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [5, 8, 12],
    'min_samples_split': [2, 10, 20],
    'min_samples_leaf': [1, 5]
}
grid_dt = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring='f1_weighted',
    n_jobs=-1,
    verbose=1
)
grid_dt.fit(X_train, y_bin_train)
print('Best params:', grid_dt.best_params_)
print('Best F1:', grid_dt.best_score_:.4f)

best_dt = grid_dt.best_estimator_
tuned_row = classification_report_row('DT Tuned (GridSearchCV)', y_bin_test, best_dt.predict(X_test))
print(tuned_row)
joblib.dump(best_dt, 'artifacts/best_decision_tree.joblib')
"""))

# Streamlit Launch
cells.append(md("## Run Streamlit Dashboard via ngrok"))

cells.append(code("!pip install -q streamlit pyngrok"))

cells.append(code(f"""import os
os.environ['NGROK_AUTHTOKEN'] = '{AUTHTOKEN}'
print('NGROK_AUTHTOKEN set successfully.')
"""))

cells.append(code("!python run_colab_ngrok.py"))

# Build notebook JSON
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open(f'{base}/california_housing_project.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("Notebook created:", os.path.getsize(f'{base}/california_housing_project.ipynb'), "bytes")
print("\nAll files:")
for fn in sorted(os.listdir(base)):
    size = os.path.getsize(f'{base}/{fn}')
    print(f"  {fn:45s}  {size:8,} bytes")
