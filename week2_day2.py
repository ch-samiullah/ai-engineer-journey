# =============================================
# MINI PROJECT — Contact Book using JSON
# =============================================
import json
import os

FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_contacts(contacts):
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)

def add_contact(name, phone, email):
    contacts = load_contacts()
    contacts[name] = {
        "phone": phone,
        "email": email
    }
    save_contacts(contacts)
    print(f"Contact '{name}' saved!")

def view_contacts():
    contacts = load_contacts()
    if not contacts:
        print("No contacts yet.")
        return
    print("\n--- CONTACT BOOK ---")
    for name, info in contacts.items():
        print(f"Name  : {name}")
        print(f"Phone : {info['phone']}")
        print(f"Email : {info['email']}")
        print("-" * 20)

def delete_contact(name):
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print(f"'{name}' deleted!")
    else:
        print("Contact not found.")

def search_contact(name):
    contacts = load_contacts()
    if name in contacts:
        print(f"\nFound: {name}")
        print(f"Phone: {contacts[name]['phone']}")
        print(f"Email: {contacts[name]['email']}")
    else:
        print("Contact not found.")

# --- RUN ---
print("=" * 30)
print("   JSON CONTACT BOOK")
print("=" * 30)

add_contact("Samiullah", "0300-1234567", "sami@email.com")
add_contact("Ali", "0311-9876543", "ali@email.com")
add_contact("Ahmed", "0333-5555555", "ahmed@email.com")

view_contacts()
search_contact("Ali")
delete_contact("Ahmed")

print("\nAfter deleting Ahmed:")
view_contacts()