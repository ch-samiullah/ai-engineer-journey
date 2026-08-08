# =============================================
# MINI PROJECT — User Registration Simulator
# =============================================
import requests
import json
from datetime import datetime

def register_user(name, email, skills):
    url     = "https://httpbin.org/post"
    payload = {
        "name"       : name,
        "email"      : email,
        "skills"     : skills,
        "registered" : datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status"     : "active"
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        print(f"\n{'='*40}")
        print(f"  REGISTRATION SUCCESSFUL!")
        print(f"{'='*40}")
        print(f"  Name   : {data['json']['name']}")
        print(f"  Email  : {data['json']['email']}")
        print(f"  Skills : {', '.join(data['json']['skills'])}")
        print(f"  Time   : {data['json']['registered']}")
        print(f"{'='*40}")
        return True

    except Exception as e:
        print(f"Registration failed: {e}")
        return False

def get_user_input():
    print("=" * 40)
    print("   USER REGISTRATION SYSTEM")
    print("=" * 40)

    name   = input("Full name: ").strip()
    email  = input("Email: ").strip()

    print("Enter skills (comma separated):")
    skills_input = input("Skills: ").strip()
    skills = [s.strip() for s in skills_input.split(",")]

    if not name or not email:
        print("Name and email required!")
        return

    register_user(name, email, skills)

get_user_input()