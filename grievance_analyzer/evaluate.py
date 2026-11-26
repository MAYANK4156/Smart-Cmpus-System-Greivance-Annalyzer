"""Evaluates the AI module on hand-written data (not the training set).
Run after train_model.py:  python evaluate.py [data/test_set.csv]
Input : data/test_set.csv, data/duplicate_pairs.csv
Output: printed results + data/test_results.csv"""
import sys, os, pandas as pd, joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import ai_engine

TEST = sys.argv[1] if len(sys.argv) > 1 else "data/test_set.csv"
df = pd.read_csv(TEST)
print(f"Test file: {TEST} | size: {len(df)} complaints")
for target in ["category", "priority"]:
    model = joblib.load(f"models/{target}.pkl")
    pred = model.predict(df["text"])
    df[f"{target}_predicted"] = pred
    print(f"\n=== {target.upper()} accuracy: {accuracy_score(df[target], pred):.2%} ===")
    print(classification_report(df[target], pred, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(df[target], pred))
df.to_csv("data/" + os.path.splitext(os.path.basename(TEST))[0] + "_results.csv", index=False)

wrong = df[(df.category != df.category_predicted) | (df.priority != df.priority_predicted)]
print(f"\n=== MISCLASSIFIED ({len(wrong)} of {len(df)}) ===")
for _, r in wrong.iterrows():
    print(f"- {r.text}\n    actual: {r.category}/{r.priority} | predicted: {r.category_predicted}/{r.priority_predicted}")

pairs = pd.read_csv("data/duplicate_pairs.csv")
pairs["predicted"] = [ai_engine.analyze(b, [(1, a)])[2] is not None
                      for a, b in zip(pairs.text_a, pairs.text_b)]
dup, non = pairs[pairs.is_duplicate == 1], pairs[pairs.is_duplicate == 0]
print(f"\n=== DUPLICATE DETECTION (mode: {ai_engine.MODE}, threshold {ai_engine.THRESHOLD}) ===")
print(f"Duplicates detected : {int(dup.predicted.sum())} of {len(dup)}")
print(f"False alarms        : {int(non.predicted.sum())} of {len(non)}")
