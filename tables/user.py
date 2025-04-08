import random
import string
import csv
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# ---------------------------
# Encryption Functions
# ---------------------------

# Generate a key (do this once and store the key securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encode_password(password: str) -> str:
    """
    Encrypts the password so it can be later decrypted.
    """
    token = cipher_suite.encrypt(password.encode('utf-8'))
    return token.decode('utf-8')

def decode_password(token: str) -> str:
    """
    Decrypts the previously encrypted password.
    """
    decrypted = cipher_suite.decrypt(token.encode('utf-8'))
    return decrypted.decode('utf-8')

# ---------------------------
# Utility Functions
# ---------------------------

def random_date(start: datetime, end: datetime) -> datetime:
    """
    Generate a random datetime between two datetime objects.
    """
    delta = end - start
    random_days = random.randrange(delta.days + 1)
    random_seconds = random.randrange(86400)  # seconds in a day
    return start + timedelta(days=random_days, seconds=random_seconds)

def generate_user(u_id: int, gender: str, first_names: list, family_names: list, 
                  email_domains: list, dob_start: datetime, dob_end: datetime, 
                  created_start: datetime, created_end: datetime, username_set: set) -> dict:
    """
    Generate a single user record with encrypted password.
    """
    # Pick a first and last name
    first = random.choice(first_names)
    last = random.choice(family_names)
    full_name = f"{first} {last}"
    
    # Generate a unique username (first name + random three-digit number)
    username = f"{first.lower()}{random.randint(100, 999)}"
    while username in username_set:
        username = f"{first.lower()}{random.randint(100, 999)}"
    username_set.add(username)
    
    # Create email using the last name and username
    email = f"{last.lower()}{username}@{random.choice(email_domains)}"
    
    # Generate a random plain text password and encrypt it
    plain_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    encrypted_password = encode_password(plain_password)
    
    # Generate a random date of birth and account creation date
    dob = random_date(dob_start, dob_end).date()
    date_created = random_date(created_start, created_end)
    
    return {
        "u_id": u_id,
        "username": username,
        "email": email,
        "password": encrypted_password,
        "name": full_name,
        "dob": dob.strftime("%Y-%m-%d"),
        "gender": gender,
        "date_created": date_created.strftime("%Y-%m-%d %H:%M:%S")
    }

# ---------------------------
# Configuration & Data Setup
# ---------------------------

male_names = [
    'Alexander', 'Benjamin', 'Caleb', 'Carter', 'Daniel', 'David', 'Dylan', 'Elias', 
    'Elijah', 'Enzo', 'Ethan', 'Ezra', 'Gabriel', 'Grayson', 'Henry', 'Hudson',
    'Isaac', 'Jack', 'Jacob', 'James', 'Jaxon', 'Joseph', 'Joshua', 'Kai',
    'Leo', 'Liam', 'Logan', 'Luca', 'Lucas', 'Mason', 'Michael', 'Noah',
    'Oliver', 'Roman', 'Rowan', 'Samuel', 'Sebastian', 'Theo', 'Theodore', 'Thomas',
    'Willian', 'Walker', 'Wesley', 'Weston'
]

female_names = [
    'Abigail', 'Adeline', 'Alyssa', 'Amelia', 'Aria', 'Aubrey', 'Aurora', 'Autumn',
    'Bella', 'Brielle', 'Brooklyn', 'Camila', 'Charlotte', 'Chloe', 'Clara', 'Ella',
    'Emily', 'Emma', 'Eva', 'Everly', 'Grace', 'Hannah', 'Harper', 'Hazel',
    'Isabella', 'Ivy', 'Lily', 'Luna', 'Mia', 'Nora', 'Olivia', 'Penelope',
    'Piper', 'Scarlett', 'Sienna', 'Sophia', 'Stella', 'Violet', 'Willow'
]

family_names = [
    'Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans',
    'Thomas', 'Johnson', 'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White'
]

# Use a fixed list of email domains
email_domains = ["example.com", "mail.com"]

# Define date ranges
dob_start = datetime(1980, 1, 1)
dob_end = datetime(2004, 12, 31)
created_start = datetime(2025, 1, 1)
created_end = datetime.now()

# Define the number of users to generate for each gender
male_users_count = 15
female_users_count = 25
other_users_count = 10

# ---------------------------
# Main User Generation Process
# ---------------------------

users = []         # List that will hold all user records
username_set = set()  # Set to ensure username uniqueness
current_id = 1     # Starting user ID

# Generate Male Users
for _ in range(male_users_count):
    user = generate_user(
        u_id=current_id,
        gender="Male",
        first_names=male_names,
        family_names=family_names,
        email_domains=email_domains,
        dob_start=dob_start,
        dob_end=dob_end,
        created_start=created_start,
        created_end=created_end,
        username_set=username_set
    )
    users.append(user)
    current_id += 1

# Generate Female Users
for _ in range(female_users_count):
    user = generate_user(
        u_id=current_id,
        gender="Female",
        first_names=female_names,
        family_names=family_names,
        email_domains=email_domains,
        dob_start=dob_start,
        dob_end=dob_end,
        created_start=created_start,
        created_end=created_end,
        username_set=username_set
    )
    users.append(user)
    current_id += 1

# Generate Users with 'Other' Gender
# For "Other", we use a combined list of male and female names.
combined_names = male_names + female_names
for _ in range(other_users_count):
    user = generate_user(
        u_id=current_id,
        gender="Other",
        first_names=combined_names,
        family_names=family_names,
        email_domains=email_domains,
        dob_start=dob_start,
        dob_end=dob_end,
        created_start=created_start,
        created_end=created_end,
        username_set=username_set
    )
    users.append(user)
    current_id += 1
    
# ---------------------------
# Shuffle and Reset Index
# ---------------------------

# Randomly shuffle the user records
random.shuffle(users)

# Reset the u_id for each user based on the new random order
for idx, user in enumerate(users, start=1):
    user["u_id"] = idx

# ---------------------------
# Save to CSV
# ---------------------------

csv_filename = "data/users.csv"
fieldnames = ["u_id", "username", "email", "password", "name", "dob", "gender", "date_created"]

with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(users)

print(f"Successfully generated {len(users)} users and stored them in '{csv_filename}'.")
