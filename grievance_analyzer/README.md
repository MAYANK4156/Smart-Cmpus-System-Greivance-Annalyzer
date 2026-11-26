# Smart Campus Sustainability Grievance Analyzer
1. pip install -r requirements.txt
2. python make_dataset.py
3. python train_model.py
4. python app.py  -> http://127.0.0.1:5000
Students: register at /register. Admin: admin@campus.edu / admin123 (set ADMIN_PASSWORD env var to change).
Optional embeddings for duplicate detection: set USE_EMBEDDINGS=1.
NOTE: delete instance/grievance.db after upgrading from an older version (schema changed).
