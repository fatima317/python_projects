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
    
    #score feedback
    if score == 5:
        st.success("Your password is strong!")
    elif score >= 3:
        st.warning("Your password is moderate. Consider making it stronger.")
    else:
        st.error("Your password is weak. Please make it stronger.")

    # improvement tips
    for tip in feedback:
        st.write(tip)
        
else:
    st.info("Please enter a password to check its strength.")


    


