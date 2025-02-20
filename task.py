import streamlit as st
import pandas as pd
import os
import yaml
import time

USER_FILE = "users.yaml"
EXCEL_FILE = "survey_data.xlsx"
ADMIN_CREDENTIALS = {"admin": "admin123"}  # Hardcoded admin login

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return yaml.safe_load(file) or {}
    return {}

def save_users(users):
    with open(USER_FILE, "w") as file:
        yaml.safe_dump(users, file)

def load_survey_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame(columns=["Name", "Gender"])

def save_survey_data(name, gender):
    df = load_survey_data()
    new_data = pd.DataFrame({"Name": [name], "Gender": [gender]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

def signup():
    st.title("Sign Up")
    st.markdown("<h3 style='color: #4CAF50;'>Create a new account</h3>", unsafe_allow_html=True)
    
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    
    if st.button("Sign Up"):
        users = load_users()
        if new_username in users or new_username == "admin":
            st.error("Username already exists. Choose a different one.")
        else:
            users[new_username] = new_password
            save_users(users)
            st.success("✅ Account created successfully! Please log in.")
            time.sleep(2)  # Pause for 2 seconds to show success message
            st.rerun()

def login():
    st.title("Welcome to the Survey App")
    st.markdown("<h3 style='color: #4CAF50;'>Please log in to continue</h3>", unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        login_button = st.button("Login", use_container_width=True)
    
    if login_button:
        users = load_users()
        if (username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password) or (username in users and users[username] == password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

def user_dashboard():
    st.title("User Dashboard")
    st.subheader("Fill out the Survey Form")
    
    with st.form(key="survey_form"):
        name = st.text_input("Enter your name")
        gender = st.radio("Select Gender", options=["Male", "Female", "Others"])
        submit_button = st.form_submit_button("Submit Survey")
        
        if submit_button:
            if name and gender:
                save_survey_data(name, gender)
                st.success("Survey submitted successfully! Thank you for your input.")
            else:
                st.error("Both fields are required to submit the survey.")
    
    if st.button("Log out"):
        logout()

def admin_dashboard():
    st.title("Admin Dashboard")
    st.subheader("View Survey Data")
    
    df = load_survey_data()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        if st.button("Download Survey Data (Excel)"):
            st.download_button(
                label="Download Excel",
                data=df.to_excel(index=False),
                file_name="survey_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No survey data available yet.")
    
    if st.button("Log out"):
        logout()

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    
    menu = ["Login", "Sign Up"] if not st.session_state.logged_in else ["Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if not st.session_state.logged_in:
        if choice == "Login":
            login()
        elif choice == "Sign Up":
            signup()
    else:
        if st.session_state.username == "admin":
            admin_dashboard()
        else:
            user_dashboard()

if __name__ == "__main__":
    main()