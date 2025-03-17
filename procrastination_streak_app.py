import streamlit as st

# App Title
st.title("🔥 5-Day Procrastination Streak Challenge")

# Description
st.write("Welcome to the **5-Day Procrastination Streak Challenge!** 🚀 Track your progress, stay accountable, and build momentum.")

# Task List
tasks = {
    "🔥 Day 1": "⏳ Pick a procrastinated task & work on it for 5 minutes",
    "📅 Day 2": "📝 Write tomorrow’s to-do list & highlight 3 key tasks",
    "⏳ Day 3": "⏲️ Use the Pomodoro method (25 min focus, 5 min break)",
    "🐸 Day 4": "🐸 Start with your hardest task first, no avoiding it",
    "🎯 Day 5": "🔍 Look back—what worked? What didn’t?"
}

# Streak Progress
st.subheader("✅ Track Your Streak Progress")

# Checkbox for each task
streak_status = {}
for day, task in tasks.items():
    streak_status[day] = st.checkbox(f"{day}: {task}")

# Show progress
completed_tasks = sum(streak_status.values())
st.progress(completed_tasks / len(tasks))

# Motivation Message
if completed_tasks == len(tasks):
    st.success("🎉 Congratulations! You completed the 5-Day Streak Challenge! 🚀")
elif completed_tasks > 0:
    st.info(f"Keep going! You're {completed_tasks}/5 days into the challenge! 💪")
else:
    st.warning("Let's get started! Check off your first task today! 🔥")

# Footer
st.write("Made with ❤️ for productivity. Let's beat procrastination together!")
