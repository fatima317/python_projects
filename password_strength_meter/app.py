import streamlit as st
import regex as re

st.set_page_config(page_title="Password Strength Checker", page_icon="🔒")
st.title(" 🔒 Password Strength Checker")
st.write("Check the strength of your password and get tips to make it stronger.")
st.write("Enter your password below:")

password = st.text_input("Enter your Password", type="password")

feedback = []

score = 0

if password:
    # Check length
    if len(password) < 8:
        feedback.append("Password should be at least 8 characters long.")
    else:
        score += 1

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    # Check for digits
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Password should contain at least one digit.")

    # Check for special characters
    if re.search(r'[@$!%*?&]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one special character (@, $, !, %, *, ?, &).")
    
    # score feedback
    if score == 0:
        feedback.append("Password is very weak.")
    elif score == 1:
        feedback.append("Password is weak.")
    elif score == 2:
        feedback.append("Password is moderate.")
    elif score == 3:
        feedback.append("Password is strong.")
    elif score == 4:
        feedback.append("Password is very strong.")
    else:
        feedback.append("Password is extremely strong.")
    
    # improvement tips
    st.write("### Improvement Tips:")
    for tip in feedback:
        st.write(tip)

else:
    st.info("Please enter a password to check its strength.")


    


