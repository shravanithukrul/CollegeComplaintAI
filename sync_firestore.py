"""
Firebase Firestore One-Click Sync Utility
Synchronizes all records from complaints.db into Firebase Cloud Firestore.
"""

import sqlite3
import json
import urllib.request
import time

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


def sync_all():
    conn = sqlite3.connect("complaints.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM complaints").fetchall()
    print(f"Found {len(rows)} local complaints in database. Pushing to Firebase Firestore...")

    success = 0
    for r in rows:
        cid = r["id"]
        doc_id = f"ticket_{cid}"
        url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/complaints/{doc_id}"

        payload_data = {
            "id": r["id"],
            "name": r["name"],
            "category": r["category"],
            "priority": r["priority"],
            "priority_reason": r["priority_reason"] or "",
            "location": r["location"],
            "description": r["description"],
            "department": r["department"] or "",
            "status": r["status"] or "Pending",
            "admin_remarks": r["admin_remarks"] or "",
            "is_recurring": bool(r["is_recurring"]),
            "created_at": r["created_at"] or time.strftime("%Y-%m-%d %H:%M:%S")
        }

        payload = json.dumps({"fields": format_firestore_fields(payload_data)}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="PATCH")
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status in (200, 201):
                    print(f"  [OK] Ticket #{cid} synced: {r['category']} ({r['priority']})")
                    success += 1
        except Exception as e:
            print(f"  [Error] Ticket #{cid}: {e}")

    print(f"\nSync finished: {success}/{len(rows)} complaints stored in Firebase Cloud Firestore.")


if __name__ == "__main__":
    sync_all()
