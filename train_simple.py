"""
Simple Training Script for Azure ML
No arguments needed - finds dataset automatically
Logs metrics to Azure ML Studio
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from xgboost import XGBClassifier
import os
import pickle
import json
import glob
import mlflow

print("="*70)
print("SIMPLE AZURE ML TRAINING")
print("="*70)

# Enable Azure ML logging
mlflow.autolog(disable=True)  # Disable autolog to have full control
print("✅ MLflow logging enabled")

# Find the dataset automatically
print("\n1. Looking for dataset...")
possible_paths = [
    "cleaned_support_tickets - with context.csv",
    "data/cleaned_support_tickets - with context.csv",
    "/tmp/tmp*/cleaned_support_tickets - with context.csv"
]

# Also search for any CSV files
csv_files = glob.glob("**/*.csv", recursive=True)
if csv_files:
    data_path = csv_files[0]
    print(f"   Found dataset: {data_path}")
else:
    print("   ERROR: No CSV files found!")
    exit(1)

# Load data
df = pd.read_csv(data_path)
print(f"   Loaded {df.shape[0]} rows, {df.shape[1]} columns")

# Simple feature selection - use all numeric columns except target
target = 'priority_cat'
features = [col for col in df.columns if col != target and df[col].dtype in ['int64', 'float64']]
print(f"\n2. Using {len(features)} features")

# Prepare data
X = df[features].fillna(0)
y = df[target]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   Train: {len(X_train)}, Test: {len(X_test)}")

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# ITERATION 1: Random Forest
print("\n3. Training Iteration 1: Random Forest")
model1 = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model1.fit(X_train, y_train)

y_pred1 = model1.predict(X_test)
metrics1 = {
    'test_accuracy': float(accuracy_score(y_test, y_pred1)),
    'test_f1': float(f1_score(y_test, y_pred1, average='weighted')),
    'test_precision': float(precision_score(y_test, y_pred1, average='weighted')),
    'test_recall': float(recall_score(y_test, y_pred1, average='weighted'))
}

print(f"   Accuracy: {metrics1['test_accuracy']:.4f}")
print(f"   F1 Score: {metrics1['test_f1']:.4f}")

# Log to Azure ML
mlflow.log_metric("iteration_1_accuracy", metrics1['test_accuracy'])
mlflow.log_metric("iteration_1_f1_score", metrics1['test_f1'])
mlflow.log_metric("iteration_1_precision", metrics1['test_precision'])
mlflow.log_metric("iteration_1_recall", metrics1['test_recall'])

# Save iteration 1
with open("outputs/iteration_1_model.pkl", "wb") as f:
    pickle.dump(model1, f)
with open("outputs/iteration_1_metrics.json", "w") as f:
    json.dump(metrics1, f, indent=2)

# ITERATION 2: XGBoost
print("\n4. Training Iteration 2: XGBoost")

# Remap target to 0,1,2 for XGBoost
y_train_xgb = y_train - 1
y_test_xgb = y_test - 1

model2 = XGBClassifier(n_estimators=100, random_state=42, max_depth=6, learning_rate=0.1)
model2.fit(X_train, y_train_xgb)

y_pred2 = model2.predict(X_test)
# Remap predictions back to 1,2,3
y_pred2_remapped = y_pred2 + 1

metrics2 = {
    'test_accuracy': float(accuracy_score(y_test, y_pred2_remapped)),
    'test_f1': float(f1_score(y_test, y_pred2_remapped, average='weighted')),
    'test_precision': float(precision_score(y_test, y_pred2_remapped, average='weighted')),
    'test_recall': float(recall_score(y_test, y_pred2_remapped, average='weighted'))
}

print(f"   Accuracy: {metrics2['test_accuracy']:.4f}")
print(f"   F1 Score: {metrics2['test_f1']:.4f}")

# Log to Azure ML
mlflow.log_metric("iteration_2_accuracy", metrics2['test_accuracy'])
mlflow.log_metric("iteration_2_f1_score", metrics2['test_f1'])
mlflow.log_metric("iteration_2_precision", metrics2['test_precision'])
mlflow.log_metric("iteration_2_recall", metrics2['test_recall'])

# Calculate and log improvement
improvement = (metrics2['test_f1'] - metrics1['test_f1']) / metrics1['test_f1'] * 100
mlflow.log_metric("f1_improvement_percent", improvement)

# Save iteration 2
with open("outputs/iteration_2_model.pkl", "wb") as f:
    pickle.dump(model2, f)
with open("outputs/iteration_2_metrics.json", "w") as f:
    json.dump(metrics2, f, indent=2)

print("\n" + "="*70)
print("TRAINING COMPLETE")
print("="*70)
print(f"✅ Iteration 1 saved: outputs/iteration_1_model.pkl")
print(f"✅ Iteration 2 saved: outputs/iteration_2_model.pkl")
print(f"✅ Metrics logged to Azure ML Studio")
print(f"📈 F1 Score Improvement: {improvement:.2f}%")
print("="*70)
