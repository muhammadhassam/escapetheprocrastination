import os
import streamlit as st
import pyrebase

# Ensure setuptools is installed
try:
    import pkg_resources
except ModuleNotFoundError:
    os.system("pip install --upgrade setuptools")
    import pkg_resources  # Retry import

# Ensure pyrebase4 is installed
try:
    import pyrebase
except ModuleNotFoundError:
    os.system("pip install pyrebase4")
    import pyrebase  # Retry import after installation

# Firebase Configuration
firebase_config = {
    "apiKey": "AIzaSyBk4LNNe01m35jCVWNsFcLMde51XykSGKM",
    "authDomain": "escape-procrastination.firebaseapp.com",
    "databaseURL": "https://escape-procrastination-default-rtdb.firebaseio.com/",
    "projectId": "escape-procrastination",
    "storageBucket": "escape-procrastination.appspot.com",
    "messagingSenderId": "687402348295",
    "appId": "1:687402348295:web:da4602785acf1cb2a59fa2"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Streamlit Page Configuration
st.set_page_config(page_title="Escape Procrastination", page_icon="🔥", layout="wide")

# Sidebar Login/Sign Up
if "user" not in st.session_state:
    st.sidebar.title("🔑 Login / Sign Up")
    choice = st.sidebar.radio("Select an option", ["Login", "Sign Up"])
    
    email = st.sidebar.text_input("📧 Email", key="email_input")
    password = st.sidebar.text_input("🔑 Password", type="password", key="password_input")

    if choice == "Login":
        if st.sidebar.button("Login", use_container_width=True):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state["user"] = user
                st.session_state["user_id"] = user["localId"]
                st.sidebar.success("✅ Logged in successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.sidebar.error("Invalid credentials. Try again.")

    elif choice == "Sign Up":
        if st.sidebar.button("Sign Up", use_container_width=True):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.sidebar.success("✅ Account created! Please log in.")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

else:
    # Logout Option
    st.sidebar.write(f"👋 Welcome, {st.session_state['user']['email']}")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.pop("user")
        st.session_state.pop("user_id")
        st.experimental_rerun()

# Main Content - Streak Tracking
if "user" in st.session_state:
    st.title("🔥 Escape the Procrastination - Streak Progress")

    # Retrieve or Initialize User Streak Data
    user_id = st.session_state["user"]["localId"]
    user_data = db.child("streaks").child(user_id).get().val()

    if not user_data:
        user_data = {
            "streak_day_1": 0,
            "streak_day_2": 0,
            "streak_day_3": 0,
            "streak_day_4": 0,
            "streak_day_5": 0
        }
        db.child("streaks").child(user_id).set(user_data)

    # Display Checkboxes for Streak
    st.subheader("✅ Track Your Streak Progress")
    tasks = [
        "🔥 Day 1: 5-Minute Start",
        "📅 Day 2: Prioritize 3 Tasks",
        "⏳ Day 3: Pomodoro Sprint",
        "🐸 Day 4: Eat the Frog",
        "🎯 Day 5: Full Productivity"
    ]

    streak_status = {}
    for i, task in enumerate(tasks, start=1):
        streak_status[f"streak_day_{i}"] = st.checkbox(task, user_data[f"streak_day_{i}"])

    # Save Progress Button
    if st.button("Save Progress"):
        for i in range(1, 6):
            user_data[f"streak_day_{i}"] = int(streak_status[f"streak_day_{i}"])
        db.child("streaks").child(user_id).update(user_data)
        st.success("✅ Progress saved!")

    # Show Current Progress
    completed_tasks = sum(user_data[f"streak_day_{i}"] for i in range(1, 6))
    st.progress(completed_tasks / 5)

    if completed_tasks == 5:
        st.success("🎉 Congratulations! You completed the 5-Day Streak Challenge! 🚀")
    elif completed_tasks > 0:
        st.info(f"Keep going! You're {completed_tasks}/5 days into the challenge! 💪")
    else:
        st.warning("Let's get started! Check off your first task today! 🔥")

