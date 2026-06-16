import uuid
from collections import Counter
from datetime import datetime, timezone

import requests

from firebase_config import (
    FIREBASE_API_KEY,
    FIREBASE_AUTH_URL,
    FIREBASE_PROJECT_ID,
    FIREBASE_TOKEN_URL,
    get_firebase_credentials,
    is_firebase_configured,
)

_firebase_app = None
_firestore_db = None


def _get_firestore():
    global _firebase_app, _firestore_db

    if _firestore_db is not None:
        return _firestore_db

    if not is_firebase_configured():
        return None

    import firebase_admin
    from firebase_admin import credentials, firestore

    service_account_info = get_firebase_credentials()

    if not service_account_info:
        return None

    if not firebase_admin._apps:
        cred = credentials.Certificate(
            service_account_info
        )

        _firebase_app = firebase_admin.initialize_app(
            cred,
            {
                "projectId": FIREBASE_PROJECT_ID
            }
        )
    else:
        _firebase_app = firebase_admin.get_app()

    _firestore_db = firestore.client()

    return _firestore_db


def _auth_request(endpoint, payload):
    if not FIREBASE_API_KEY:
        return None, "Firebase API key is not configured."

    response = requests.post(
        f"{FIREBASE_AUTH_URL}:{endpoint}?key={FIREBASE_API_KEY}",
        json=payload,
        timeout=15
    )
    data = response.json()

    if response.status_code != 200:
        error = data.get("error", {})
        message = error.get("message", "Authentication request failed.")
        return None, _friendly_auth_error(message)

    return data, None


def _friendly_auth_error(message):
    mapping = {
        "EMAIL_EXISTS": "An account with this email already exists.",
        "EMAIL_NOT_FOUND": "No account found with this email.",
        "INVALID_PASSWORD": "Incorrect password. Please try again.",
        "INVALID_LOGIN_CREDENTIALS": "Invalid email or password.",
        "WEAK_PASSWORD": "Password should be at least 6 characters.",
        "INVALID_EMAIL": "Please enter a valid email address.",
        "USER_DISABLED": "This account has been disabled.",
        "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts. Try again later.",
    }
    return mapping.get(message, message.replace("_", " ").capitalize())


def sign_up(email, password, display_name):
    payload, error = _auth_request("signUp", {
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    if error:
        return None, error

    user = {
        "uid": payload["localId"],
        "email": payload.get("email", email),
        "display_name": display_name or email.split("@")[0],
        "id_token": payload["idToken"],
        "refresh_token": payload["refreshToken"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    _upsert_user_profile(user)
    return user, None


def sign_in(email, password):
    payload, error = _auth_request("signInWithPassword", {
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    if error:
        return None, error

    uid = payload["localId"]
    profile = get_user_profile(uid) or {}

    return {
        "uid": uid,
        "email": payload.get("email", email),
        "display_name": profile.get(
            "name",
            email.split("@")[0]
        ),
        "id_token": payload["idToken"],
        "refresh_token": payload["refreshToken"],
        "created_at": profile.get("created_at")
    }, None


def refresh_session(refresh_token):
    if not FIREBASE_API_KEY:
        return None, "Firebase API key is not configured."

    response = requests.post(
        f"{FIREBASE_TOKEN_URL}?key={FIREBASE_API_KEY}",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        },
        timeout=15
    )
    data = response.json()

    if response.status_code != 200:
        error = data.get("error", {})
        message = error.get("message", "Session expired. Please log in again.")
        return None, message

    uid = data["user_id"]
    profile = get_user_profile(uid) or {}

    return {
        "uid": uid,
        "email": profile.get("email", ""),
        "display_name": profile.get(
            "name",
            profile.get("email", "").split("@")[0]
        ),
        "id_token": data["id_token"],
        "refresh_token": data["refresh_token"],
        "created_at": profile.get("created_at")
    }, None


def send_password_reset(email):
    payload, error = _auth_request("sendOobCode", {
        "requestType": "PASSWORD_RESET",
        "email": email
    })
    if error:
        return False, error
    return True, payload.get("email", email)


def _upsert_user_profile(user):
    db = _get_firestore()
    if db is None:
        return

    doc_ref = db.collection("users").document(user["uid"])
    existing = doc_ref.get()

    profile_data = {
        "email": user["email"],
        "name": user["display_name"],
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    if not existing.exists:
        profile_data["created_at"] = user.get(
            "created_at",
            datetime.now(timezone.utc).isoformat()
        )
    else:
        profile_data["created_at"] = existing.to_dict().get(
            "created_at",
            datetime.now(timezone.utc).isoformat()
        )

    doc_ref.set(profile_data, merge=True)


def get_user_profile(uid):
    db = _get_firestore()
    if db is None:
        return None

    doc = db.collection("users").document(uid).get()
    if not doc.exists:
        return None
    return doc.to_dict()


def save_resume_analysis(uid, analysis_data):
    db = _get_firestore()
    if db is None:
        return None

    report_id = str(uuid.uuid4())
    uploaded_at = datetime.now(timezone.utc).isoformat()

    record = {
        "file_name": analysis_data.get("file_name", "resume.pdf"),
        "uploaded_at": uploaded_at,
        "role": analysis_data.get("role", ""),
        "resume_score": analysis_data.get("resume_score", 0),
        "ats_score": analysis_data.get("ats_score", 0),
        "match_score": analysis_data.get("match_score", 0),
        "matched_skills": analysis_data.get("matched_skills", []),
        "missing_skills": analysis_data.get("missing_skills", []),
        "suggestions": analysis_data.get("suggestions", []),
        "career_insights": analysis_data.get("career_insights", {}),
        "ats_strengths": analysis_data.get("ats_strengths", []),
        "ats_weaknesses": analysis_data.get("ats_weaknesses", []),
        "ats_suggestions": analysis_data.get("ats_suggestions", []),
        "readiness": analysis_data.get("readiness", ""),
    }

    db.collection("users").document(uid).collection(
        "resume_history"
    ).document(report_id).set(record)

    return report_id


def get_resume_history(uid, limit=50):
    db = _get_firestore()
    if db is None:
        return []

    docs = (
        db.collection("users")
        .document(uid)
        .collection("resume_history")
        .order_by("uploaded_at", direction="DESCENDING")
        .limit(limit)
        .stream()
    )

    history = []
    for doc in docs:
        entry = doc.to_dict()
        entry["id"] = doc.id
        history.append(entry)
    return history


def get_resume_report(uid, report_id):
    db = _get_firestore()
    if db is None:
        return None

    doc = (
        db.collection("users")
        .document(uid)
        .collection("resume_history")
        .document(report_id)
        .get()
    )
    if not doc.exists:
        return None

    data = doc.to_dict()
    data["id"] = doc.id
    return data


def get_analytics_summary(uid):
    history = get_resume_history(uid, limit=100)

    if not history:
        return {
            "total_uploads": 0,
            "recent_uploads": [],
            "ats_trend": [],
            "resume_trend": [],
            "roles_tried": [],
            "missing_skill_counts": {},
            "best_role": None
        }

    ats_trend = []
    resume_trend = []
    roles = []
    missing_counter = Counter()
    role_scores = {}

    for entry in reversed(history):
        label = entry.get("uploaded_at", "")[:10]
        ats_trend.append({
            "date": label,
            "score": entry.get("ats_score", 0)
        })
        resume_trend.append({
            "date": label,
            "score": entry.get("resume_score", 0)
        })
        role = entry.get("role", "Unknown")
        roles.append(role)
        role_scores.setdefault(role, []).append(
            entry.get("match_score", 0)
        )
        for skill in entry.get("missing_skills", []):
            missing_counter[skill] += 1

    best_role = None
    if role_scores:
        best_role = max(
            role_scores,
            key=lambda role: sum(role_scores[role]) / len(role_scores[role])
        )

    return {
        "total_uploads": len(history),
        "recent_uploads": history[:5],
        "ats_trend": ats_trend,
        "resume_trend": resume_trend,
        "roles_tried": list(dict.fromkeys(roles)),
        "missing_skill_counts": dict(missing_counter.most_common(10)),
        "best_role": best_role
    }
