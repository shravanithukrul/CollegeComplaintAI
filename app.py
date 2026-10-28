"""
Smart AI-Based College Complaint Management & Priority System
Flask Application Controller with Role-Based Authentication
"""

import os
import sqlite3
import time
import json
import urllib.request
import threading
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from ai_model import (
    analyze_complaint,
    find_similar_complaints,
    check_recurring_issue,
    CATEGORY_DEPARTMENT_MAP
)

app = Flask(__name__)
app.secret_key = "college_care_ai_institutional_secret_key_2026"
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
DB_PATH = "complaints.db"
FIREBASE_PROJECT_ID = "collegecare-ai"


def format_firestore_fields(data: dict) -> dict:
    fields = {}
    for k, v in data.items():
        if v is None:
            fields[k] = {"nullValue": None}
        elif isinstance(v, bool):
            fields[k] = {"booleanValue": v}
        elif isinstance(v, int):
            fields[k] = {"integerValue": str(v)}
        elif isinstance(v, float):
            fields[k] = {"doubleValue": v}
        else:
            fields[k] = {"stringValue": str(v)}
    return fields


def sync_to_firestore_async(complaint_dict: dict):
    """Syncs a complaint document to Firebase Cloud Firestore in a non-blocking background thread."""
    def _worker():
        try:
            cid = complaint_dict.get("id")
            doc_id = f"ticket_{cid}" if cid else f"ticket_{int(time.time())}"
            url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/complaints/{doc_id}"

            payload_data = {
                "id": complaint_dict.get("id", 0),
                "name": complaint_dict.get("name", "Student"),
                "category": complaint_dict.get("category", ""),
                "priority": complaint_dict.get("priority", "Medium"),
                "priority_reason": complaint_dict.get("priority_reason", ""),
                "location": complaint_dict.get("location", ""),
                "description": complaint_dict.get("description", ""),
                "department": complaint_dict.get("department", ""),
                "status": complaint_dict.get("status", "Pending"),
                "admin_remarks": complaint_dict.get("admin_remarks", "") or "",
                "image_path": complaint_dict.get("image_path", "") or "",
                "is_recurring": bool(complaint_dict.get("is_recurring", False)),
                "created_at": complaint_dict.get("created_at") or time.strftime("%Y-%m-%d %H:%M:%S")
            }

            payload = json.dumps({"fields": format_firestore_fields(payload_data)}).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="PATCH"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"[Firebase Firestore Sync]: Successfully stored ticket #{cid} in Firestore.")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"[Firebase Firestore Sync HTTP {e.code}]: {err_body}")
        except Exception as e:
            print(f"[Firebase Firestore Sync Notice]: {e}")

    threading.Thread(target=_worker, daemon=True).start()


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Authentication Decorators & Privacy Helpers
# ---------------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in or register to submit a complaint. Guests can only view existing complaints.", "warning")
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash("Administrator credentials required to access the Administrative Board.", "warning")
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def mask_complaint_for_viewer(c: dict) -> dict:
    """
    Privacy Rule:
    The student's name / ID is ONLY viewable by:
    1. Administrators (session.role == 'admin')
    2. The specific user who submitted the complaint (owner)
    For all other users and unauthenticated guests, the student's name is masked.
    """
    row = dict(c)
    current_uid = session.get("user_id")
    is_admin = session.get("role") == "admin"
    current_name = (session.get("full_name") or "").strip().lower()
    complaint_name = (row.get("name") or "").strip().lower()

    is_owner = False
    if current_uid and row.get("user_id") and row.get("user_id") == current_uid:
        is_owner = True
    elif current_name and complaint_name and current_name == complaint_name:
        is_owner = True

    if is_admin or is_owner:
        row["is_identity_visible"] = True
    else:
        row["is_identity_visible"] = False
        row["real_name"] = row.get("name")
        row["name"] = "🔒 Student Identity Protected"

    return row


# ---------------------------------------------------------------------------
# Database Initialization & Seeding
# ---------------------------------------------------------------------------
def init_db():
    """Initializes and migrates the database schema safely."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # 1. Complaints Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Medium',
                location TEXT NOT NULL DEFAULT 'Campus',
                description TEXT NOT NULL,
                image_path TEXT,
                status TEXT DEFAULT 'Pending',
                department TEXT,
                is_recurring INTEGER DEFAULT 0,
                parent_id INTEGER,
                related_count INTEGER DEFAULT 1,
                priority_reason TEXT,
                admin_remarks TEXT,
                created_at TEXT
            )
        """)

        # Migration helper for complaints
        cursor.execute("PRAGMA table_info(complaints)")
        existing_cols = [col[1] for col in cursor.fetchall()]

        column_defs = {
            "priority": "TEXT NOT NULL DEFAULT 'Medium'",
            "location": "TEXT NOT NULL DEFAULT 'Campus'",
            "image_path": "TEXT",
            "department": "TEXT",
            "is_recurring": "INTEGER DEFAULT 0",
            "parent_id": "INTEGER",
            "related_count": "INTEGER DEFAULT 1",
            "priority_reason": "TEXT",
            "admin_remarks": "TEXT",
            "created_at": "TEXT",
            "user_id": "INTEGER"
        }

        for col, col_type in column_defs.items():
            if col not in existing_cols:
                try:
                    cursor.execute(f"ALTER TABLE complaints ADD COLUMN {col} {col_type}")
                except Exception as e:
                    print(f"Column migration warning ({col}): {e}")

        cursor.execute("UPDATE complaints SET created_at = datetime('now', 'localtime') WHERE created_at IS NULL")

        # 2. Users Table for Authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Seed default users if users table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            seed_default_users(cursor)

        # Seed sample complaints if table has minimal records
        cursor.execute("SELECT COUNT(*) FROM complaints")
        if cursor.fetchone()[0] <= 2:
            seed_demo_data(cursor)

        conn.commit()


def seed_default_users(cursor):
    """Seeds default admin and student test accounts."""
    default_users = [
        ("admin", generate_password_hash("admin123"), "Campus Administrator", "admin"),
        ("student", generate_password_hash("student123"), "Rahul Sharma", "student")
    ]
    for u in default_users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        """, u)


def seed_demo_data(cursor):
    """Seeds realistic campus grievances to demonstrate all AI features."""
    sample_records = [
        (
            "Aarav Mehta", "IT & Lab Facilities", "Medium", "Room 115",
            "Projector is not turning on and display cable is damaged in Room 115.",
            None, "Pending", "IT Support & Computing Systems", 1, None, 4,
            "Flagged Medium Priority due to disruption indicator: 'not working'.",
            "IT technician scheduled for inspection."
        ),
        (
            "Rohan Sharma", "Electrical & Power", "High", "Classroom 204",
            "Sparks coming out of the switchboard near the back door! Exposed wires danger.",
            None, "Pending", "Electrical & Maintenance Dept", 0, None, 1,
            "Flagged High Priority due to critical safety/operational hazard: 'spark'.",
            "Power breaker tripped for safety."
        ),
        (
            "Sneha Patil", "Water Supply", "High", "Main Building 2nd Floor",
            "Water tap leaking continuously and flooding the restroom floor.",
            None, "In Progress", "Plumbing & Water Services", 1, None, 2,
            "Flagged High Priority due to critical utility (Water Supply) disruption.",
            "Plumber dispatched to replace valve."
        ),
        (
            "Kavita Verma", "Cleanliness & Sanitation", "Medium", "Central Library",
            "Dustbins overflowing with plastic cups and wrappers near study tables.",
            None, "Resolved", "Housekeeping & Sanitation", 0, None, 1,
            "Routine cleanliness requirement.",
            "Housekeeping staff cleaned the reading hall."
        ),
        (
            "Ananya Deshmukh", "Classroom Facilities", "Low", "Room 102",
            "Two wooden benches are broken and rocking slightly.",
            None, "Pending", "Estate & Campus Facilities", 0, None, 1,
            "Routine furniture repair request.",
            None
        ),
        (
            "Vikram Singhania", "Infrastructure & Campus", "Medium", "Main College Entrance",
            "Large pothole in the pathway right after the entrance gate.",
            None, "In Progress", "Civil Works & Infrastructure", 0, None, 1,
            "Campus accessibility and vehicle disruption.",
            "Civil work team requested quotation."
        ),
        (
            "Rahul Joshi", "IT & Lab Facilities", "Medium", "Computer Lab 1",
            "Five computers are showing network disconnection and cannot access server.",
            None, "Pending", "IT Support & Computing Systems", 1, None, 2,
            "Flagged Medium Priority due to computer lab disruption.",
            None
        )
    ]

    for rec in sample_records:
        cursor.execute("""
            INSERT INTO complaints 
            (name, category, priority, location, description, image_path, status, department, is_recurring, parent_id, related_count, priority_reason, admin_remarks, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
        """, rec)


# ---------------------------------------------------------------------------
# Authentication Routes (/login, /register, /logout)
# ---------------------------------------------------------------------------
@app.route("/api/google_login", methods=["POST"])
def api_google_login():
    """Authenticates or registers users via Firebase Google Sign-In."""
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    full_name = data.get("name", "").strip() or email.split("@")[0]
    next_url = data.get("next_url")

    if not email:
        return jsonify({"error": "No email provided"}), 400

    username = email.split("@")[0]

    with get_db_connection() as conn:
        cursor = conn.cursor()
        user = conn.execute(
            "SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(username) = ?",
            (username, email)
        ).fetchone()

        if not user:
            # Create user account for Google sign-in
            random_pwd_hash = generate_password_hash(f"google_oauth_{email}_{int(time.time())}")
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, 'student')
            """, (username, random_pwd_hash, full_name))
            user_id = cursor.lastrowid
            conn.commit()
            role = "student"
        else:
            user_id = user["id"]
            role = user["role"]
            full_name = user["full_name"]

    session["user_id"] = user_id
    session["username"] = username
    session["full_name"] = full_name
    session["role"] = role

    flash(f"Signed in via Google as {full_name}.", "success")
    redirect_target = next_url if (next_url and next_url.startswith("/")) else (url_for("admin") if role == "admin" else url_for("home"))

    return jsonify({"success": True, "redirect": redirect_target})


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles campus authentication for students and administrators."""
    next_url = request.args.get("next")

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please provide both username and password.", "danger")
            return render_template("login.html", next_url=next_url)

        with get_db_connection() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE LOWER(username) = ?",
                (username.lower(),)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            # Establish session
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]

            flash(f"Welcome back, {user['full_name']}!", "success")

            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            if user["role"] == "admin":
                return redirect(url_for("admin"))
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials. Please verify username and password.", "danger")
            return render_template("login.html", next_url=next_url)

    if "user_id" in session:
        if session.get("role") == "admin":
            return redirect(url_for("admin"))
        return redirect(url_for("home"))

    return render_template("login.html", next_url=next_url)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Allows students and faculty to create campus accounts."""
    next_url = request.args.get("next")

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        role = request.form.get("role", "student").strip()
        password = request.form.get("password", "")

        if not full_name or not username or not password:
            flash("All registration fields are required.", "danger")
            return render_template("register.html", next_url=next_url)

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html", next_url=next_url)

        with get_db_connection() as conn:
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if existing:
                flash("Username is already taken. Please choose another.", "danger")
                return render_template("register.html", next_url=next_url)

            hashed = generate_password_hash(password)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            """, (username, hashed, full_name, role))
            user_id = cursor.lastrowid
            conn.commit()

        # Automatically log in the new user
        session["user_id"] = user_id
        session["username"] = username
        session["full_name"] = full_name
        session["role"] = role

        flash(f"Account registered successfully! Welcome to CollegeCare AI, {full_name}.", "success")
        if next_url and next_url.startswith("/"):
            return redirect(next_url)
        return redirect(url_for("home"))

    return render_template("register.html", next_url=next_url)


@app.route("/logout")
def logout():
    """Logs the user out and clears session state."""
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/my_complaints")
@login_required
def my_complaints():
    """Portal for logged-in students to view all their personal grievances."""
    user_name = session.get("full_name", "")
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM complaints WHERE LOWER(name) LIKE ? ORDER BY id DESC",
            (f"%{user_name.lower()}%",)
        ).fetchall()
        complaints = [dict(r) for r in rows]

    return render_template("my_complaints.html", complaints=complaints)


# ---------------------------------------------------------------------------
# Core Campus Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    """Landing page with system highlights and live status."""
    with get_db_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Pending'").fetchone()[0]
        resolved = conn.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'").fetchone()[0]
        urgent = conn.execute("SELECT COUNT(*) FROM complaints WHERE priority = 'High' AND status != 'Resolved'").fetchone()[0]

    return render_template("index.html", stats={
        "total": total,
        "pending": pending,
        "resolved": resolved,
        "urgent": urgent
    })


@app.route("/complaint", methods=["GET", "POST"])
@login_required
def complaint():
    """Handles complaint submission and real-time AI processing. Requires student or user sign-in."""
    if request.method == "POST":
        user_id = session.get("user_id")
        name = session.get("full_name") or request.form.get("name", "").strip() or session.get("username", "Student")
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not location or not description:
            return render_template("complaint.html", error="Please fill in all required fields.")

        # Handle optional image upload
        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename != "" and allowed_file(file.filename):
                safe_name = secure_filename(file.filename)
                unique_name = f"{int(time.time())}_{safe_name}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                image_filename = unique_name

        # 1. AI Analysis: Category, Priority, Department
        ai_result = analyze_complaint(description)
        category = ai_result["category"]
        priority = ai_result["priority"]
        priority_reason = ai_result["priority_reason"]
        department = ai_result["department"]

        # 2. AI Duplicate / Similarity Detection against unresolved complaints
        with get_db_connection() as conn:
            active_rows = conn.execute(
                "SELECT id, description, location, category, parent_id, related_count FROM complaints WHERE status != 'Resolved'"
            ).fetchall()
            active_list = [dict(row) for row in active_rows]

        similar_match = find_similar_complaints(description, location, active_list)
        parent_id = None
        related_count = 1
        parent_info = None

        with get_db_connection() as conn:
            cursor = conn.cursor()

            if similar_match:
                parent_id = similar_match["parent_id"]
                cursor.execute(
                    "UPDATE complaints SET related_count = related_count + 1 WHERE id = ?",
                    (parent_id,)
                )
                cursor.execute(
                    "SELECT related_count, priority FROM complaints WHERE id = ?",
                    (parent_id,)
                )
                parent_info = cursor.fetchone()
                if parent_info and parent_info["related_count"] >= 3 and parent_info["priority"] == "Low":
                    cursor.execute("UPDATE complaints SET priority = 'Medium' WHERE id = ?", (parent_id,))

            # 3. AI Recurring Issue Detection
            is_recurring, hist_count, recurring_msg = check_recurring_issue(
                location=location,
                category=category,
                threshold=2
            )

            # Insert new complaint with user_id
            cursor.execute("""
                INSERT INTO complaints 
                (name, category, priority, location, description, image_path, status, department, is_recurring, parent_id, related_count, priority_reason, created_at, user_id)
                VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?, ?, ?, ?, ?, datetime('now', 'localtime'), ?)
            """, (
                name, category, priority, location, description, image_filename,
                department, 1 if is_recurring else 0, parent_id, related_count, priority_reason, user_id
            ))
            complaint_id = cursor.lastrowid
            conn.commit()

        complaint_data = {
            "id": complaint_id,
            "name": name,
            "category": category,
            "priority": priority,
            "priority_reason": priority_reason,
            "location": location,
            "description": description,
            "department": department,
            "status": "Pending",
            "image_path": image_filename,
            "similar_info": similar_match,
            "related_count": (parent_info["related_count"] if similar_match and parent_info else 1),
            "is_recurring": is_recurring
        }

        # Asynchronously store in Firebase Cloud Firestore
        sync_to_firestore_async(complaint_data)

        return render_template(
            "complaint_success.html",
            complaint=complaint_data,
            recurring_message=recurring_msg
        )

    default_name = session.get("full_name") or session.get("username", "")
    return render_template("complaint.html", default_name=default_name)


@app.route("/track")
def track():
    """Allows students & guests to check complaint resolution status and browse campus reports."""
    search_query = request.args.get("id", "").strip()
    complaints = []
    searched = bool(search_query)

    with get_db_connection() as conn:
        if searched:
            if search_query.isdigit():
                rows = conn.execute(
                    "SELECT * FROM complaints WHERE id = ?",
                    (int(search_query),)
                ).fetchall()
            elif session.get("role") == "admin" or session.get("user_id"):
                rows = conn.execute(
                    "SELECT * FROM complaints WHERE LOWER(name) LIKE ? ORDER BY id DESC",
                    (f"%{search_query.lower()}%",)
                ).fetchall()
            else:
                flash("Guests can view and track tickets by Complaint ID number. Please enter a valid ID.", "info")
                rows = []

            # Protect student identity for unauthorized viewers
            complaints = [mask_complaint_for_viewer(r) for r in rows]

        # Recent complaints for public viewing (student identities masked)
        recent_rows = conn.execute(
            "SELECT * FROM complaints ORDER BY id DESC LIMIT 6"
        ).fetchall()
        recent_complaints = [mask_complaint_for_viewer(r) for r in recent_rows]

    return render_template(
        "track.html",
        complaints=complaints,
        recent_complaints=recent_complaints,
        search_query=search_query,
        searched=searched
    )


@app.route("/admin")
@admin_required
def admin():
    """Administrator Dashboard with KPIs, recurring warnings, and complaint management."""
    filter_q = request.args.get("q", "").strip()
    filter_status = request.args.get("status", "").strip()
    filter_priority = request.args.get("priority", "").strip()

    with get_db_connection() as conn:
        query = "SELECT * FROM complaints WHERE 1=1"
        params = []

        if filter_q:
            query += " AND (LOWER(description) LIKE ? OR LOWER(name) LIKE ? OR LOWER(location) LIKE ?)"
            q_like = f"%{filter_q.lower()}%"
            params.extend([q_like, q_like, q_like])

        if filter_status:
            query += " AND status = ?"
            params.append(filter_status)

        if filter_priority:
            query += " AND priority = ?"
            params.append(filter_priority)

        query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, id DESC"

        complaints = conn.execute(query, params).fetchall()

        total = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Pending'").fetchone()[0]
        in_progress = conn.execute("SELECT COUNT(*) FROM complaints WHERE status = 'In Progress'").fetchone()[0]
        resolved = conn.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'").fetchone()[0]
        urgent = conn.execute("SELECT COUNT(*) FROM complaints WHERE priority = 'High' AND status != 'Resolved'").fetchone()[0]
        recurring = conn.execute("SELECT COUNT(*) FROM complaints WHERE is_recurring = 1").fetchone()[0]

        hotspot_rows = conn.execute("""
            SELECT location, category, COUNT(*) as count 
            FROM complaints 
            WHERE location IS NOT NULL AND location != ''
            GROUP BY LOWER(TRIM(location)), category 
            HAVING count >= 2 
            ORDER BY count DESC 
            LIMIT 5
        """).fetchall()

        recurring_hotspots = [dict(h) for h in hotspot_rows]

    stats = {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "urgent": urgent,
        "recurring": recurring
    }

    return render_template(
        "admin.html",
        complaints=complaints,
        stats=stats,
        recurring_hotspots=recurring_hotspots,
        filter_q=filter_q,
        filter_status=filter_status,
        filter_priority=filter_priority
    )


@app.route("/update_status/<int:complaint_id>", methods=["POST"])
@admin_required
def update_status(complaint_id):
    """Updates complaint status, priority, department, and resolution remarks."""
    status = request.form.get("status")
    department = request.form.get("department")
    priority = request.form.get("priority")
    remarks = request.form.get("remarks", "").strip()

    if status not in ["Pending", "In Progress", "Resolved"]:
        return "Invalid status", 400

    with get_db_connection() as conn:
        conn.execute("""
            UPDATE complaints 
            SET status = ?, department = ?, priority = ?, admin_remarks = ?
            WHERE id = ?
        """, (status, department, priority, remarks, complaint_id))
        conn.commit()

        # Retrieve updated record and synchronize with Firebase Cloud Firestore
        updated_row = conn.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,)).fetchone()
        if updated_row:
            sync_to_firestore_async(dict(updated_row))

    flash(f"Ticket #{complaint_id} status updated to '{status}'.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/sync_firebase", methods=["POST"])
@admin_required
def sync_firebase():
    """Bulk synchronizes all existing complaints from SQLite into Firebase Cloud Firestore."""
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM complaints").fetchall()
        count = len(rows)
        for r in rows:
            sync_to_firestore_async(dict(r))

    flash(f"Firestore Sync Dispatched: Pushing {count} tickets to Firebase Cloud Firestore.", "success")
    return redirect(url_for("admin"))


@app.route("/api/preview", methods=["POST"])
def api_preview():
    """AJAX endpoint for real-time classification preview & similarity alert."""
    data = request.get_json() or {}
    description = data.get("description", "").strip()
    location = data.get("location", "").strip()

    if not description:
        return jsonify({"error": "Empty description"}), 400

    ai_result = analyze_complaint(description)

    similar_match = None
    if len(description) >= 10:
        with get_db_connection() as conn:
            active_rows = conn.execute(
                "SELECT id, description, location, category, parent_id FROM complaints WHERE status != 'Resolved'"
            ).fetchall()
            active_list = [dict(r) for r in active_rows]
            similar_match = find_similar_complaints(description, location, active_list)

    return jsonify({
        "category": ai_result["category"],
        "priority": ai_result["priority"],
        "priority_reason": ai_result["priority_reason"],
        "department": ai_result["department"],
        "similar": similar_match
    })


@app.route("/api/analytics")
def api_analytics():
    """API endpoint providing dataset for Chart.js admin visualizations."""
    with get_db_connection() as conn:
        cat_rows = conn.execute("""
            SELECT category, COUNT(*) as count 
            FROM complaints 
            GROUP BY category 
            ORDER BY count DESC
        """).fetchall()

        high_cnt = conn.execute("SELECT COUNT(*) FROM complaints WHERE priority = 'High'").fetchone()[0]
        med_cnt = conn.execute("SELECT COUNT(*) FROM complaints WHERE priority = 'Medium'").fetchone()[0]
        low_cnt = conn.execute("SELECT COUNT(*) FROM complaints WHERE priority = 'Low'").fetchone()[0]

        loc_rows = conn.execute("""
            SELECT location, COUNT(*) as count 
            FROM complaints 
            WHERE location IS NOT NULL AND location != '' 
            GROUP BY location 
            ORDER BY count DESC 
            LIMIT 5
        """).fetchall()

    return jsonify({
        "categories": {
            "labels": [r["category"] for r in cat_rows],
            "data": [r["count"] for r in cat_rows]
        },
        "priority": {
            "high": high_cnt,
            "medium": med_cnt,
            "low": low_cnt
        },
        "locations": {
            "labels": [r["location"] for r in loc_rows],
            "data": [r["count"] for r in loc_rows]
        }
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
