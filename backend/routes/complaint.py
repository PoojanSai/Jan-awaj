import os
import shutil
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form

from database import SessionLocal
from models import Complaint

from services.speech_to_text import transcribe_audio
from services.department_ai import identify_department
from services.location_service import reverse_geocode
from services.letter_generator import generate_letter
from services.email_service import send_email
from utils.fallback import fallback_text

router = APIRouter()


@router.post("/complaint")
async def submit_complaint(
    lat: float = Form(...),
    lon: float = Form(...),
    text: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None)
):
    """
    Accepts complaints via:
    - Text input
    - Voice recording
    - Audio upload

    Robust against:
    - Empty audio field
    - Speech-to-text failure
    """

    complaint_text = None

    # ----------------------------
    # 1️⃣ TEXT HAS HIGHEST PRIORITY
    # ----------------------------
    if text and text.strip():
        complaint_text = text.strip()

    # ----------------------------
    # 2️⃣ AUDIO (ONLY IF VALID FILE)
    # ----------------------------
    elif audio and audio.filename:
        file_path = f"temp_{audio.filename}"

        try:
            with open(file_path, "wb") as f:
                shutil.copyfileobj(audio.file, f)

            complaint_text = transcribe_audio(file_path)

        except Exception as e:
            print("Audio processing error:", e)
            complaint_text = None

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    # ----------------------------
    # 3️⃣ FALLBACK (ALWAYS SAFE)
    # ----------------------------
    complaint_text = fallback_text(complaint_text)

    # ----------------------------
    # 4️⃣ IDENTIFY DEPARTMENT
    # ----------------------------
    department = identify_department(complaint_text)

    # ----------------------------
    # 5️⃣ REVERSE GEOCODE LOCATION
    # ----------------------------
    district, state = reverse_geocode(lat, lon)

    # ----------------------------
    # 6️⃣ GENERATE FORMAL LETTER
    # ----------------------------
    letter = generate_letter(
        complaint_text,
        department,
        district,
        state
    )

    # ----------------------------
    # 7️⃣ STORE IN DATABASE
    # ----------------------------
    db = SessionLocal()
    complaint = Complaint(
        text=complaint_text,
        department=department,
        district=district,
        state=state,
        email_sent_to="TEST"
    )
    db.add(complaint)
    db.commit()
    db.close()

    # ----------------------------
    # 8️⃣ SEND EMAIL (TEST MODE)
    # ----------------------------
    try:
        send_email(letter)
    except Exception as e:
        # Email failure should NOT break complaint flow
        print("Email error:", e)

    # ----------------------------
    # 9️⃣ RESPONSE
    # ----------------------------
    return {
        "status": "Complaint submitted successfully"
    }
