from dotenv import load_dotenv
load_dotenv()
import os

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TEST_EMAIL = os.getenv("TEST_EMAIL", "test@example.com")
