import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

# --- 1. Load Data ---
try:
    df = pd.read_csv('Salary Prediction of Data Professions.csv')
except FileNotFoundError:
    print("❌ Error: Dataset not found.")
    exit()

print("\n✅ --- Data Loaded ---")
print(df.head())

# --- 2. Clean & Rename Columns ---
df.columns = df.columns.str.strip().str.lower().str.replace('-', '_')

# --- 3. Preprocess Target Variable ---
df['income'] = df['income'].str.strip()
df['income'] = df['income'].map({'<=50K': 0, '>50K': 1})

# --- 4. Define Features and Target ---
X = df.drop('income', axis=1)
y = df['income']

# Split column types
categorical_cols = X.select_dtypes(include='object').columns.tolist()
numerical_cols = X.select_dtypes(include=np.number).columns.tolist()

print(f"\n🔍 Categorical Columns: {categorical_cols}")
print(f"🔢 Numerical Columns: {numerical_cols}")

# --- 5. Build Preprocessing Pipeline ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]
)

# --- 6. Define Models ---
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

results = {}

# --- 7. Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 8. Train and Evaluate All Models ---
for name, clf in models.items():
    print(f"\n🚀 Training: {name}")
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', clf)
    ])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    results[name] = acc
    print(f"✅ Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

# --- 9. Save the Best Model ---
best_model_name = max(results, key=results.get)
best_accuracy = results[best_model_name]
print(f"\n🏆 Best Model: {best_model_name} with Accuracy: {best_accuracy:.4f}")

# Train final pipeline on full dataset
final_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', models[best_model_name])
])
final_pipeline.fit(X, y)

joblib.dump(final_pipeline, 'salary_prediction_model.joblib')
print("💾 Final model saved as 'salary_prediction_model.joblib'")
