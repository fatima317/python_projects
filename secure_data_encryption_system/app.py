import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

DATA_FILE = "secure_data.json"
SALT = b"secure_salt_value"
LOCKOUT_DURATION = 60

#login details
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0

# data loading
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def generate_key(passkey):
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)
    return urlsafe_b64encode(key)

def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000).hex()

def encrypt_text(text, key):
    cipher = Fernet(generate_key(key))
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypt_text, key):
    try:
        cipher = Fernet(generate_key(key))
        return cipher.decrypt(encrypt_text.encode()).decode()
    except Exception as e:
        st.error("Decryption failed. Please check your key.")
        return None
    
stored_data = load_data()

st.title("🔐 Secure Data Encryption System")
menu = ["Home", "Login", "Register", "Store Data", "Retrieve Data"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("Welcome to the Secure Data Encryption System")
    st.write("This application allows you to securely store and retrieve data using encryption.")
    st.write("Please log in or register to get started.")

elif choice == "Register":
    st.subheader("Register a New User")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            if username in stored_data:
                st.warning("Username already exists. Please choose a different one.")
            else:
                stored_data[username] = {
                    "password": hash_password(password),
                    "data": []
                }
                save_data(stored_data)
                st.success("User registered successfully! You can now log in.")
        else:
            st.error("Please enter both username and password.")

elif choice == "Login":
    st.subheader("User Login")
    
    if time.time() < st.session_state.lockout_time:
        remaining_time = int(st.session_state.lockout_time - time.time())
        st.warning(f"Too many failed login attempts. Please wait {remaining_time} seconds before trying again.")
        st.stop()
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in stored_data and stored_data[username]["password"] == hash_password(password):
            st.session_state.authenticated_user = username
            st.session_state.login_attempts = 0
            st.success(f"Welcome, {username}!")
        else:
            st.session_state.login_attempts += 1
            remaining = 3 - st.session_state.login_attempts
            st.warning(f"Incorrect username or password. You have {remaining} attempts left.")

            if st.session_state.login_attempts >= 3:
                st.session_state.lockout_time = time.time() + LOCKOUT_DURATION
                st.error("Too many failed login attempts. You are locked out for 60 seconds.")
                st.stop()

elif choice == "Store Data":
    if not st.session_state.authenticated_user:
        st.warning("Please log in to store data.")
    else:
        st.subheader("Store Encrypted Data")
        data = st.text_area("Data to store")
        passkey = st.text_input("Encryption Key", type="password")

        if st.button("Encrypt And Store Data"):
            if data and passkey:
                encrypted_data = encrypt_text(data, passkey)
                stored_data[st.session_state.authenticated_user]["data"].append(encrypted_data)
                save_data(stored_data)
                st.success("Data encrypted and stored successfully!")
            else:
                st.error("Please enter both data and encryption key.")

elif choice == "Retrieve Data":
    if not st.session_state.authenticated_user:
        st.warning("Please log in to retrieve data.")
    else:
        st.subheader("Retrieve Data")
        user_data = stored_data.get(st.session_state.authenticated_user, {}).get("data", [])

        if not user_data:
            st.info("No data found for the user.")
        else:
            st.write("Encrypted Data:")
            for i, item in enumerate(user_data):
                st.code(item, language="text")

            encrypted_input = st.text_area("Enter Encrypted Text")
            passkey = st.text_input("Decryption Key", type="password")

            if st.button("Decrypt Data"):
                result = decrypt_text(encrypted_input, passkey)
                if result:
                    st.success(f"Decrypted Data: {result}")
                else:
                    st.error("Decryption failed. Please check your key.")
        