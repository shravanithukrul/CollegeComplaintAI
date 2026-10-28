"""
AI Engine for College Complaint Management and Priority System
Covers:
1. Category Classification (NLP: TF-IDF + Classifier)
2. Priority Classification (Urgency/Severity Scoring + NLP)
3. Similar & Duplicate Complaint Detection (TF-IDF + Cosine Similarity)
4. Recurring Issue Detection (Historical Frequency & Location Analytics)
5. Department Recommendation
"""

import re
import sqlite3
from typing import Dict, List, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------
# 1. Training Dataset for Category Classification
# ---------------------------------------------------------
TRAINING_DATA = [
    # IT & Lab Facilities
    ("Computer is not booting up in Lab 3", "IT & Lab Facilities"),
    ("Lab computers are extremely slow and lagging", "IT & Lab Facilities"),
    ("Projector is not turning on in seminar hall", "IT & Lab Facilities"),
    ("Projector display is blurred and flickering in Room 115", "IT & Lab Facilities"),
    ("Campus WiFi is disconnected and not connecting", "IT & Lab Facilities"),
    ("Internet is not working in the digital library", "IT & Lab Facilities"),
    ("Keyboards and mouse missing from computer lab 2", "IT & Lab Facilities"),
    ("LAN cables damaged near workstation 14", "IT & Lab Facilities"),
    ("Printer in computer lab has paper jam and error code", "IT & Lab Facilities"),
    ("Software required for coding lab is not installed", "IT & Lab Facilities"),
    ("Monitor screen flickering and showing vertical lines", "IT & Lab Facilities"),
    ("Smart board touch sensors not responding in smart room", "IT & Lab Facilities"),

    # Electrical & Power
    ("Sparks coming out of switchboard in classroom 204", "Electrical & Power"),
    ("Exposed wires hanging dangerously near the corridor switch", "Electrical & Power"),
    ("Ceiling fan not spinning and making loud buzzing sound", "Electrical & Power"),
    ("Tube lights are burnt out in Room 302", "Electrical & Power"),
    ("Power socket is broken and sparking when plugged in", "Electrical & Power"),
    ("Frequent power tripping in the electronics wing", "Electrical & Power"),
    ("Air conditioner is blowing warm air and not cooling", "Electrical & Power"),
    ("AC in lecture hall 1 is leaking water and not working", "Electrical & Power"),
    ("Corridor is pitch dark because all bulbs are fused", "Electrical & Power"),
    ("Electric switchboard has loose wiring and gave mild shock", "Electrical & Power"),
    ("Exhaust fan in chemistry lab is not working", "Electrical & Power"),

    # Classroom Facilities
    ("Broken wooden bench in Room 115 with sharp exposed nail", "Classroom Facilities"),
    ("Desks are broken and rocking in classroom 102", "Classroom Facilities"),
    ("Whiteboard is cracked and cannot be written on", "Classroom Facilities"),
    ("Podium microphone is not catching audio in auditorium", "Classroom Facilities"),
    ("Classroom window glass broken and draft coming inside", "Classroom Facilities"),
    ("Door lock is jammed and students got stuck inside", "Classroom Facilities"),
    ("Curtains are torn and sunlight reflecting on the board", "Classroom Facilities"),
    ("Chairs in lecture room 3 are broken and unstable", "Classroom Facilities"),
    ("Notice board glass is shattered in main corridor", "Classroom Facilities"),

    # Cleanliness & Sanitation
    ("Dustbins overflowing with trash on the second floor", "Cleanliness & Sanitation"),
    ("Washroom is extremely filthy and needs urgent cleaning", "Cleanliness & Sanitation"),
    ("Stinking smell coming from third floor restroom", "Cleanliness & Sanitation"),
    ("Garbage dumped behind the canteen building", "Cleanliness & Sanitation"),
    ("Classroom floor has spilled juice and sticky dirt", "Cleanliness & Sanitation"),
    ("Corridors have not been swept for three days", "Cleanliness & Sanitation"),
    ("Insects and pests spotted in classroom corners", "Cleanliness & Sanitation"),
    ("Washroom basin has food particles and spit stains", "Cleanliness & Sanitation"),
    ("Sanitary disposal bins in girls washroom are full", "Cleanliness & Sanitation"),

    # Water Supply
    ("Drinking water cooler on 1st floor is empty and dry", "Water Supply"),
    ("Water purifier dispensing dirty brownish contaminated water", "Water Supply"),
    ("No running water in any washroom of the main building", "Water Supply"),
    ("Water tap leaking continuously and flooding the restroom", "Water Supply"),
    ("Flush tank in washroom broken and water overflowing", "Water Supply"),
    ("Low water pressure in washbasin taps on 3rd floor", "Water Supply"),
    ("Drinking water filter is leaking and making puddle", "Water Supply"),
    ("Water tank pipe burst causing continuous leakage", "Water Supply"),

    # Infrastructure & Campus
    ("Deep potholes on the main college entrance road", "Infrastructure & Campus"),
    ("Staircase railing is loose and shaking dangerously", "Infrastructure & Campus"),
    ("College lift/elevator stuck between floors", "Infrastructure & Campus"),
    ("Roof is leaking during rain in the library top floor", "Infrastructure & Campus"),
    ("Tiles broken and loose on the main staircase", "Infrastructure & Campus"),
    ("Canteen seating tables broken and wobbly", "Infrastructure & Campus"),
    ("Campus parking gate hinge broken and falling", "Infrastructure & Campus"),
    ("Boundary wall plaster peeling and falling off", "Infrastructure & Campus"),
    ("Drainage line blocked outside mechanical workshop", "Infrastructure & Campus"),

    # Academic & Faculty
    ("Professor has been absent for a week without substitute", "Academic & Faculty"),
    ("Faculty not taking scheduled practical lab sessions", "Academic & Faculty"),
    ("Syllabus incomplete and no extra classes arranged", "Academic & Faculty"),
    ("Lab instructor not explaining experiments properly", "Academic & Faculty"),
    ("Lecture cancelled without prior announcement or notice", "Academic & Faculty"),
    ("Study materials and question banks not provided by teacher", "Academic & Faculty"),
]

# Train Category Pipeline
category_texts = [item[0] for item in TRAINING_DATA]
category_labels = [item[1] for item in TRAINING_DATA]

category_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), stop_words="english", lowercase=True)),
    ("clf", LogisticRegression(max_iter=1000, random_state=42))
])
category_pipeline.fit(category_texts, category_labels)

# Department Mapping
CATEGORY_DEPARTMENT_MAP = {
    "IT & Lab Facilities": "IT Support & Computing Systems",
    "Electrical & Power": "Electrical & Maintenance Dept",
    "Classroom Facilities": "Estate & Campus Facilities",
    "Cleanliness & Sanitation": "Housekeeping & Sanitation",
    "Water Supply": "Plumbing & Water Services",
    "Infrastructure & Campus": "Civil Works & Infrastructure",
    "Academic & Faculty": "Academic Affairs & Dean Office"
}

# ---------------------------------------------------------
# 2. Priority Classification Engine
# ---------------------------------------------------------
HIGH_PRIORITY_KEYWORDS = [
    "spark", "sparking", "shock", "electric shock", "exposed wire", "fire",
    "smoke", "hazard", "dangerous", "danger", "burst", "stuck between floors",
    "elevator stuck", "lift stuck", "no water", "contaminated", "flooding",
    "urgent", "blackout", "shattered glass", "broken glass", "injury",
    "falling", "burst", "emergency", "nail", "short circuit"
]

MEDIUM_PRIORITY_KEYWORDS = [
    "not working", "broken", "flickering", "leaking", "overflowing", "ac",
    "air conditioner", "projector", "wifi", "internet", "fan", "computer",
    "slow", "damaged", "dirty", "smell", "stinking", "jammed", "unstable",
    "absent", "cancelled", "exam"
]

def predict_priority(description: str, category: str) -> Tuple[str, str]:
    """
    Evaluates urgency, severity, safety, and operational impact.
    Returns: (Priority: 'High' | 'Medium' | 'Low', Reason: str)
    """
    desc_lower = description.lower()

    # Rule 1: Safety & Urgent Hazards
    for kw in HIGH_PRIORITY_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", desc_lower) or kw in desc_lower:
            return "High", f"Flagged High Priority due to critical safety/operational hazard: '{kw}'."

    # Rule 2: Water Supply or Electrical issues with leakage/failure
    if category in ["Electrical & Power", "Water Supply"]:
        if any(w in desc_lower for w in ["leak", "outage", "off", "no water", "spark", "smell"]):
            return "High", f"Critical utility ({category}) disruption detected."

    # Rule 3: Medium Priority indicators
    for kw in MEDIUM_PRIORITY_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", desc_lower) or kw in desc_lower:
            return "Medium", f"Flagged Medium Priority due to disruption indicator: '{kw}'."

    # Default to Low for routine or aesthetic reports
    return "Low", "Routine issue with low immediate safety or operational impact."

# ---------------------------------------------------------
# 3. Main Predictor Function
# ---------------------------------------------------------
def analyze_complaint(description: str) -> Dict[str, str]:
    """
    Predicts category, recommended department, and priority.
    """
    clean_desc = description.strip()
    category = str(category_pipeline.predict([clean_desc])[0])
    priority, priority_reason = predict_priority(clean_desc, category)
    department = CATEGORY_DEPARTMENT_MAP.get(category, "Administration")

    return {
        "category": category,
        "priority": priority,
        "priority_reason": priority_reason,
        "department": department
    }

# ---------------------------------------------------------
# 4. Similar & Duplicate Complaint Detection (Cosine Similarity)
# ---------------------------------------------------------
def find_similar_complaints(
    new_description: str,
    new_location: str,
    existing_complaints: List[dict],
    threshold: float = 0.55
) -> Optional[dict]:
    """
    Compares a new complaint against active existing complaints.
    Uses TF-IDF and Cosine Similarity.
    Matches with location weighting.
    Returns the most similar existing complaint if similarity >= threshold, else None.
    """
    if not existing_complaints:
        return None

    norm_new_loc = (new_location or "").strip().lower()

    # Filter candidates: prefer matching or near location, or same unresolved status
    candidate_descriptions = [c["description"] for c in existing_complaints]

    all_texts = [new_description] + candidate_descriptions
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    except Exception:
        # Fallback if text has only stop words
        return None

    best_idx = int(similarities.argmax())
    best_score = float(similarities[best_idx])
    matched_complaint = existing_complaints[best_idx]
    norm_matched_loc = (matched_complaint.get("location") or "").strip().lower()

    # If same location, allow a lower threshold (0.45)
    adjusted_threshold = threshold
    if norm_new_loc and norm_matched_loc and (norm_new_loc in norm_matched_loc or norm_matched_loc in norm_new_loc):
        adjusted_threshold = max(0.40, threshold - 0.15)
        # boost score for same location
        best_score = min(1.0, best_score + 0.10)

    if best_score >= adjusted_threshold:
        return {
            "matched_id": matched_complaint["id"],
            "matched_description": matched_complaint["description"],
            "matched_location": matched_complaint.get("location", ""),
            "matched_category": matched_complaint.get("category", ""),
            "similarity_score": round(best_score * 100, 1),
            "parent_id": matched_complaint.get("parent_id") or matched_complaint["id"]
        }

    return None

# ---------------------------------------------------------
# 5. Recurring Issue Detection
# ---------------------------------------------------------
def check_recurring_issue(
    location: str,
    category: str,
    db_path: str = "complaints.db",
    threshold: int = 2
) -> Tuple[bool, int, str]:
    """
    Checks historical complaint logs for the given location and category.
    If occurrences >= threshold, marks as recurring problem.
    Returns: (is_recurring: bool, total_count: int, message: str)
    """
    norm_loc = (location or "").strip().lower()
    if not norm_loc:
        return False, 0, "No location specified."

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Count existing complaints at this location
        cursor.execute(
            """
            SELECT COUNT(*) FROM complaints 
            WHERE LOWER(TRIM(location)) = ? AND category = ?
            """,
            (norm_loc, category)
        )
        count = cursor.fetchone()[0]

    # If count + 1 (including the current complaint) exceeds threshold
    total_after_this = count + 1
    if total_after_this >= threshold:
        return (
            True,
            total_after_this,
            f"Recurring Issue detected: {total_after_this} reports recorded at '{location}' for {category}."
        )

    return False, total_after_this, "Standard frequency."

# Backwards compatibility helper for existing imports
def predict_category(description: str) -> str:
    return analyze_complaint(description)["category"]
