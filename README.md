# 🏛️ CollegeCare AI: AI-Based College Complaint Management & Priority System

A full-stack, AI-powered campus grievance resolution platform built with **Flask**, **Scikit-learn (NLP)**, **Firebase Cloud Firestore**, **Firebase Authentication (Google Sign-In)**, **SQLite**, and **Chart.js**.

**🌐 Live Cloud URL:** [https://collegecare-ai.onrender.com](https://collegecare-ai.onrender.com)  
**📘 Complete Academic Documentation:** See [DOCUMENTATION.md](DOCUMENTATION.md) for full system architecture, algorithms, and viva defense guide.

---

## 🌟 Key Capabilities (Aligned with Institutional Specifications)

### 1. Complaint Categorization (NLP)
* Utilizes **TF-IDF Vectorization** and **Logistic Regression** trained on campus-specific grievance scenarios.
* Automatically classifies complaints into 7 distinct domains:
  - `IT & Lab Facilities` (Computers, projectors, WiFi, software, printers)
  - `Electrical & Power` (Wiring, power cuts, switchboards, lights, fans, AC)
  - `Classroom Facilities` (Benches, whiteboards, podiums, windows)
  - `Cleanliness & Sanitation` (Washroom hygiene, trash bins, corridors)
  - `Water Supply` (Drinking water coolers, pipe leakage, tap failure)
  - `Infrastructure & Campus` (Roads, lifts/elevators, stairs, canteen)
  - `Academic & Faculty` (Lecture attendance, lab practicals, curriculum)

### 2. Urgency & Priority Classification
* Automatically assigns priority levels: **High (Urgent)**, **Medium**, or **Low**.
* Evaluates safety hazards (e.g., electrical sparking, exposed wiring, chemical/lab hazards, flooding, lift stuck) and operational disruptions.
* Explains the classification reason on both student receipt and admin dashboard.

### 3. Duplicate & Similar Complaint Detection
* Employs **Cosine Similarity** on TF-IDF feature vectors across active, unresolved complaints.
* Detects when multiple students report the same problem (e.g., *"Projector not working in Room 115"*).
* Links duplicate tickets to a primary ticket and increments the `related_count` (e.g., *"4 reports grouped"*), automatically escalating priority when report thresholds are met.

### 4. Recurring Issue Detection & Hotspot Analytics
* Scans historical complaint patterns grouped by campus location and category.
* Flags facilities with $\ge 2$ repeat issues as **⚠️ Recurring Issues**.
* Highlights chronic problem areas on the Administrator Dashboard so college authorities can pursue permanent infrastructure fixes rather than repetitive patches.

### 5. Interactive Administrator Dashboard & Visualization
* Visualized using **Chart.js**:
  - Complaints by Category (Doughnut Chart)
  - Priority Breakdown (Urgent vs Medium vs Low Bar Chart)
  - Top Facility Hotspots by Location (Horizontal Bar Chart)
* Manage status (`Pending`, `In Progress`, `Resolved`), assign departments, add resolution remarks, and filter by status/priority/search keywords.

### 6. Student Portal & Live Status Tracking
* **Live AI Preview**: Real-time category and priority prediction as students type their description.
* **Photo Attachment**: Optional image upload (`static/uploads/`) for visual proof of facility damage.
* **Status Tracker**: Search by Complaint ID or student name with a 3-stage visual progress timeline.

---

## 🚀 Running the Project

### Prerequisites
Make sure you have Python 3.9+ installed with the following packages:
```bash
pip install flask scikit-learn
```

### Start the Application
Run the Flask server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 📁 Project Structure

```
CollegeComplaintAI/
├── app.py                      # Flask backend & API routes controller
├── ai_model.py                 # Scikit-learn NLP models, Priority & Similarity engines
├── complaints.db               # SQLite database with auto-migration
├── README.md                   # System documentation
├── static/
│   ├── css/
│   │   └── style.css           # Custom modern responsive styling & badges
│   └── uploads/                # Uploaded student complaint photos
└── templates/
    ├── base.html               # Shared layout & navigation
    ├── index.html              # Landing page & AI capability overview
    ├── complaint.html          # Student submission form with real-time AI preview
    ├── complaint_success.html  # Ticket receipt with similarity & recurrence alerts
    ├── track.html              # Complaint status tracking & visual timeline
    └── admin.html              # Executive admin dashboard with Chart.js charts
```

---

## 🔒 Privacy & Access Control Rules

1. **Guest Access**:
   * Guests (unregistered visitors) can **only view & track** complaints (`/track`).
   * Guests **cannot submit** complaints. Attempting to access `/complaint` directs them to the sign-in/registration page.
   * Guests can browse the **Public Campus Grievances Feed** on `/track` to see active maintenance work across the college.

2. **Student Identity Confidentiality**:
   * The name and student ID of the person who lodged a grievance is **strictly confidential**.
   * It is **only visible to**:
     1. **The Administrator** (on `/admin` and `/track`).
     2. **The specific User who lodged the complaint** (when logged in).
   * For all other users and unauthenticated guests, the student's name is automatically masked as:
     `🔒 Student Identity Protected (Only visible to filer & admin)`.

---

## 🔑 Default Sign-In Credentials

The system provides role-based authentication with pre-seeded accounts:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full access to Administrative Board, KPI Analytics, Status/Department Updates |
| **Student** | `student` | `student123` | Submit complaints, auto-filled name, personal grievance portal (`/my_complaints`) |

New students and faculty can also register their own accounts directly via the **Register** page (`/register`).

---

## 🔗 Main URLs

| URL Route | Access | Description |
| :--- | :--- | :--- |
| `/` | Public | Landing page with key statistics and quick action cards |
| `/login` | Public | Sign-in page with credential verification & 1-click demo buttons |
| `/register` | Public | Account creation for students and faculty |
| `/logout` | Authenticated | Clears session and logs out |
| `/complaint` | Public / Student | Grievance submission with real-time AI preview & photo upload |
| `/track` | Public | Complaint status lookup by reference ID or student name |
| `/my_complaints`| Logged In | Personal dashboard showing all grievances filed by the user |
| `/admin` | **Admin Only** | Executive Board with KPI cards, recurring alerts & Chart.js graphs |
