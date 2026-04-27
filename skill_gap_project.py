import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText



# ---------------- EMAIL FUNCTION ---------------- #
def send_email(student_name, weak_skills):
    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"
    hod_email = "hod_email@gmail.com"

    subject = "⚠️ Student Performance Alert"

    body = f"""
    Dear HOD,

    This is to inform you that the student {student_name} is underperforming.

    Weak Skills:
    {weak_skills.to_string(index=False)}

    Please take necessary action.

    Regards,
    Skill Gap Analysis System
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = hod_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("📧 Email sent successfully to HOD!")
    except Exception as e:
        print("❌ Error sending email:", e)

# ---------------- MAIN PROGRAM ---------------- #
# Load dataset
data = pd.read_csv("student_skills.csv")

# Input student name
student_name = input("Enter student name (Student1 / Student2): ")

# Filter data
student_data = data[data["Student"] == student_name]

if student_data.empty:
    print("❌ Student not found!")
    exit()

# Calculate skill gap
student_data["Skill_Gap"] = student_data["Required_Level"] - student_data["Student_Level"]

# Display table
print(f"\n--- Skill Gap Analysis for {student_name} ---\n")
print(student_data[["Skill", "Skill_Gap"]])

# Performance summary
min_gap = student_data["Skill_Gap"].min()
max_gap = student_data["Skill_Gap"].max()

print("\nPerformance Summary:")

if min_gap == max_gap:
    print("All skills are balanced.")
else:
    best_skill = student_data.loc[student_data["Skill_Gap"].idxmin()]
    weak_skill = student_data.loc[student_data["Skill_Gap"].idxmax()]

    print(f"Strongest Skill : {best_skill['Skill']} (Gap = {best_skill['Skill_Gap']})")
    print(f"Weakest Skill   : {weak_skill['Skill']} (Gap = {weak_skill['Skill_Gap']})")

# ---------------- WEAK DETECTION ---------------- #
threshold = 3

weak_skills = student_data[student_data["Skill_Gap"] >= threshold]

if not weak_skills.empty:
    print("\n⚠️ ALERT: Student is weak in following skills:\n")
    print(weak_skills[["Skill", "Skill_Gap"]])

    # Send email
    send_email(student_name, weak_skills)
else:
    print("\n✅ Student performance is satisfactory.")

# ---------------- GRAPH ---------------- #
colors = []
for gap in student_data["Skill_Gap"]:
    if gap == min_gap:
        colors.append("green")
    elif gap == max_gap:
        colors.append("red")
    else:
        colors.append("blue")

plt.bar(student_data["Skill"], student_data["Skill_Gap"], color=colors)
plt.xlabel("Skills")
plt.ylabel("Skill Gap")
plt.title(f"Skill Gap Analysis - {student_name}")
plt.show()