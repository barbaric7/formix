import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeB0xY2LFDRSohoHx3dYy7PVxHd-uoigHHEPBq9TG9m0mw54Q/viewform?usp=send_form"

PRIMARY_MODEL = "openai/gpt-3.5-turbo"
SECONDARY_MODEL = "meta-llama/llama-3.1-8b-instruct"

EDGE_PROFILE_PATH = r"C:\Users\Hp\AppData\Local\Microsoft\Edge\SeleniumProfile"

STUDENT_DETAILS = {
    "email": "aaditya.kalmekh24@vit.edu",
    "full name": "Aaditya Rakesh Kalmekh",
    "college": "Vishwakarma Institute of Technology",
    "year": "Year II",
    "roll number": "11",
    "prn": "12411536",
    "branch-division": "CSSE-B"
}