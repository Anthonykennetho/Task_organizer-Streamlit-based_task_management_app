import streamlit as st
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import plotly.express as px
from config import DATABASE_URI

# Attempt to establish database connection with error handling
try:
    engine = create_engine(DATABASE_URI)  # Create database engine
    connection = engine.raw_connection()  # Get raw connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    
    # Ensure users table exists with email as unique identifier
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    
    # Ensure tasks table exists with correct user_id reference
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            task_description TEXT NOT NULL,
            due_date DATE NOT NULL,
            status VARCHAR(50) DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    connection.commit()
except Exception as e:
    st.error(f"Database connection failed: {e}")  # Display error message if connection fails
    st.stop()  # Stop execution if database connection is not established

# Configure Streamlit app interface with theme and layout settings
st.set_page_config(page_title="Task Organizer", layout="wide", page_icon="📌", initial_sidebar_state="expanded")
st.title("📌 Task Organizer")  # Set main title
st.markdown("---")  # Add a horizontal line for visual separation

# Sidebar navigation with options for different pages
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("Use the menu to navigate through different sections.")
page = st.sidebar.radio("Go to", ["📝 Sign Up", "🔑 Login", "➕ Add Task", "📋 View Tasks", "📊 Task Analysis"])  # Sidebar menu

# Protect pages that require authentication
if page in ["➕ Add Task", "📋 View Tasks", "📊 Task Analysis"]:
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("⚠️ Please log in first to access this page.")
        st.stop()

# User Registration
if page == "📝 Sign Up":
    st.subheader("📝 Create an Account")
    new_username = st.text_input("Choose a Username")
    new_email = st.text_input("Enter Your Email")
    new_password = st.text_input("Choose a Password", type="password")
    signup_button = st.button("Sign Up")
    
    if signup_button:
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (new_username, new_email, new_password))
            connection.commit()
            st.success("✅ Account created successfully! You can now log in.")
        except Exception as e:
            st.error(f"Failed to create account: {e}")

# User Authentication
elif page == "🔑 Login":
    st.subheader("🔑 User Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    # Initialize session state for error message
    if "login_error" not in st.session_state:
        st.session_state["login_error"] = ""

    if login_button:
        cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        
        if user:
            st.session_state["user_id"] = user[0]
            st.session_state["authenticated"] = True
            st.session_state["login_error"] = ""  # Clear error message
            st.success("✅ Login successful!")
            st.rerun()  # Refresh page after successful login
        else:
            st.session_state["login_error"] = "Invalid email or password"

    if st.session_state["login_error"]:
        st.error(st.session_state["login_error"])

# Page for adding a new task
elif page == "➕ Add Task":
    st.subheader("➕ Add a New Task")
    with st.form("task_form"):
        task_description = st.text_area("Task Description")  # Input field for task details
        due_date = st.date_input("Due Date")  # Date input field for task deadline
        submit = st.form_submit_button("Add Task")  # Submit button
        
