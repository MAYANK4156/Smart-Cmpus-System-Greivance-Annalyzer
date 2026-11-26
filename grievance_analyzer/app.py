import os, re
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import ai_engine

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grievance.db"
db = SQLAlchemy(app)

ADMIN_EMAIL = "admin@campus.edu"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
LOCATIONS = ["Hostel", "Library", "Canteen", "Main Block", "Computer Lab", "Sports Ground", "Parking Area", "Admin Building", "Auditorium", "Workshop"]
CATEGORIES = ["Water", "Electricity", "Waste", "Cleanliness", "Infrastructure", "Green Space", "Unclassified"]
PRIORITIES = ["High", "Medium", "Low"]
STATUSES = ["Pending", "In Progress", "Resolved"]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="student")      # student | admin

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    text = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(30))
    priority = db.Column(db.String(10))
    status = db.Column(db.String(20), default="Pending")
    duplicate_of = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- access control ----------
def login_required(f):
    @wraps(f)
    def wrapper(*a, **k):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*a, **k)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*a, **k):
        if session.get("role") != "admin":
            flash("Admin access required.", "warning")
            return redirect(url_for("login"))
        return f(*a, **k)
    return wrapper

@app.context_processor
def inject():
    return dict(is_admin=session.get("role") == "admin", user_name=session.get("name"),
                logged_in=bool(session.get("user_id")),
                STATUSES=STATUSES, CATEGORIES=CATEGORIES, PRIORITIES=PRIORITIES)

# ---------- authentication ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        pw, pw2 = request.form.get("password", ""), request.form.get("confirm", "")
        if not name or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Enter your name and a valid email.", "danger")
        elif len(pw) < 6 or pw != pw2:
            flash("Password must be at least 6 characters and match the confirmation.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("This email is already registered.", "danger")
        else:
            u = User(name=name, email=email, password_hash=generate_password_hash(pw), role="student")
            db.session.add(u); db.session.commit()
            session.update(user_id=u.id, role=u.role, name=u.name)
            flash("Registration successful. Welcome!", "success")
            return redirect(url_for("submit"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = User.query.filter_by(email=request.form.get("email", "").strip().lower()).first()
        if u and check_password_hash(u.password_hash, request.form.get("password", "")):
            session.clear()
            session.update(user_id=u.id, role=u.role, name=u.name)
            return redirect(url_for("dashboard" if u.role == "admin" else "submit"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------- complaints ----------
@app.route("/", methods=["GET", "POST"])
@login_required
def submit():
    if request.method == "POST":
        text, location = request.form.get("text", "").strip(), request.form.get("location", "")
        if len(text) < 10 or location not in LOCATIONS:
            flash("Enter a valid location and a description of at least 10 characters.", "danger")
            return redirect(url_for("submit"))
        existing = [(c.id, c.text) for c in Complaint.query.all()]
        category, priority, dup = ai_engine.analyze(text, existing)
        if dup:                                   # always point to the original complaint
            parent = db.session.get(Complaint, dup)
            dup = parent.duplicate_of or parent.id
        c = Complaint(user_id=session["user_id"], text=text, location=location,
                      category=category, priority=priority, duplicate_of=dup)
        db.session.add(c); db.session.commit()
        msg = f"Complaint #{c.id} submitted. Category: {category}, Priority: {priority}."
        if dup: msg += f" Similar to existing complaint #{dup}."
        flash(msg, "success")
        return redirect(url_for("my_complaints"))
    return render_template("submit.html", locations=LOCATIONS)

@app.route("/my-complaints")
@login_required
def my_complaints():
    items = Complaint.query.filter_by(user_id=session["user_id"]).order_by(Complaint.created_at.desc()).all()
    return render_template("my_complaints.html", items=items)

@app.route("/complaints")
def complaints():
    q = Complaint.query
    for field in ("category", "status", "priority"):
        v = request.args.get(field)
        if v: q = q.filter(getattr(Complaint, field) == v)
    return render_template("complaints.html", items=q.order_by(Complaint.created_at.desc()).all())

# ---------- admin ----------
@app.route("/admin/update/<int:cid>", methods=["POST"])
@admin_required
def update(cid):
    c = db.get_or_404(Complaint, cid)
    for field, allowed in (("status", STATUSES), ("category", CATEGORIES), ("priority", PRIORITIES)):
        v = request.form.get(field)
        if v in allowed: setattr(c, field, v)
    db.session.commit()
    flash(f"Complaint #{cid} updated.", "success")
    return redirect(request.referrer or url_for("complaints"))

@app.route("/dashboard")
@admin_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/stats")
@admin_required
def stats():
    items = Complaint.query.all()
    def count(attr, keys):
        return {k: sum(1 for c in items if getattr(c, attr) == k) for k in keys}
    dups = [{"id": c.id, "original": c.duplicate_of, "location": c.location, "text": c.text} for c in items if c.duplicate_of]
    return jsonify(total=len(items), duplicates=dups, ai_mode=ai_engine.MODE,
                   by_category=count("category", CATEGORIES), by_priority=count("priority", PRIORITIES),
                   by_location=count("location", LOCATIONS), by_status=count("status", STATUSES))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(role="admin").first():       # seed default admin
        db.session.add(User(name="Administrator", email=ADMIN_EMAIL,
                            password_hash=generate_password_hash(ADMIN_PASSWORD), role="admin"))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
