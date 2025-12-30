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
    Accepts complaint via:
    - Text input
    - Voice recording
    - Audio upload
    """

    complaint_text = None

    # 1️⃣ If text is provided, use it directly
    if text and text.strip():
        complaint_text = text.strip()

    # 2️⃣ Else if audio is provided, transcribe
    elif audio:
        file_path = f"temp_{audio.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        complaint_text = transcribe_audio(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)

    # 3️⃣ Fallback (if speech fails or nothing provided)
    complaint_text = fallback_text(complaint_text)

    # 4️⃣ Identify department
    department = identify_department(complaint_text)

    # 5️⃣ Reverse geocode location
    district, state = reverse_geocode(lat, lon)

    # 6️⃣ Generate formal letter
    letter = generate_letter(
        complaint_text,
        department,
        district,
        state
    )

    # 7️⃣ Store in database
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

    # 8️⃣ Send email (test mode)
    send_email(letter)

    return {
        "status": "Complaint submitted successfully"
    }
