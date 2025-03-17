import streamlit as st
import pyrebase

# Firebase Configuration
firebase_config = {
    "apiKey": "YOUR_FIREBASE_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Streamlit UI
st.title("🔥 Escape the Procrastination - Login")

# Login/Register Toggle
choice = st.selectbox("Login or Sign Up", ["Login", "Sign Up"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if choice == "Sign Up":
    if st.button("Create Account"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("✅ Account created! Please log in.")
        except Exception as e:
            st.error(f"Error: {e}")

if choice == "Login":
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state["user"] = user
            st.success("✅ Logged in successfully! 🚀")
        except Exception as e:
            st.error("Invalid credentials. Try again.")

# Show streak tracking after login
if "user" in st.session_state:
    st.write(f"Welcome, {st.session_state['user']['email']}!")

    # Retrieve or Initialize User Streak Data
    user_id = st.session_state["user"]["localId"]
    user_data = db.child("streaks").child(user_id).get().val()

    if not user_data:
        user_data = {"streak_day_1": 0, "streak_day_2": 0, "streak_day_3": 0, "streak_day_4": 0, "streak_day_5": 0}
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
