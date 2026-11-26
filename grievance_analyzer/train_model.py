"""Trains category and priority classifiers (TF-IDF + Logistic Regression)."""
import sys, pandas as pd, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report

DATA = sys.argv[1] if len(sys.argv) > 1 else "data/complaints.csv"
df = pd.read_csv(DATA)
print("Training on", DATA, "|", len(df), "rows")
for target in ["category", "priority"]:
    X_tr, X_te, y_tr, y_te = train_test_split(df["text"], df[target], test_size=0.2, random_state=42, stratify=df[target])
    model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), stop_words="english"), LogisticRegression(max_iter=1000))
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    print(f"\n=== {target.upper()} | accuracy: {accuracy_score(y_te, pred):.2%} ===")
    print(classification_report(y_te, pred, zero_division=0))
    model.fit(df["text"], df[target])          # retrain on all data for deployment
    joblib.dump(model, f"models/{target}.pkl")
print("Models saved in models/")
