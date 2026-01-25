from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta
from analysis.pattern_engine import generate_insights, burnout_score

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE =================
def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            study INTEGER,
            phone INTEGER,
            sleep INTEGER,
            mood TEXT,
            date TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            user_id INTEGER PRIMARY KEY,
            daily_goal INTEGER,
            weekly_goal INTEGER
        )
    """)

    conn.close()

# ================= STREAK =================
def calculate_streak(dates):
    if not dates:
        return 0, 0

    dts = sorted({datetime.strptime(d, "%Y-%m-%d").date() for d in dates})
    longest = streak = 1

    for i in range(1, len(dts)):
        if dts[i] == dts[i-1] + timedelta(days=1):
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 1

    today = datetime.now().date()
    current = 0
    if dts[-1] in (today, today - timedelta(days=1)):
        current = 1
        i = len(dts) - 1
        while i > 0 and dts[i] == dts[i-1] + timedelta(days=1):
            current += 1
            i -= 1

    return current, longest

# ================= FOCUS SCORE =================
def calculate_focus_score(data):
    if not data:
        return 0

    score = 0
    for d in data:
        study, phone, sleep = d[0], d[1], d[2]
        score += min(study * 5, 40)
        if sleep >= 7:
            score += 30
        elif sleep >= 6:
            score += 20
        elif sleep >= 5:
            score += 10
        score -= min(phone * 5, 30)

    return max(0, min(100, score // len(data)))

# ================= GOAL PROGRESS =================
def calculate_goal_progress(weekly, daily_goal, weekly_goal):
    today_study = weekly[-1][0] if weekly else 0
    weekly_total = sum(d[0] for d in weekly)

    return {
        "today_study": today_study,
        "weekly_study": weekly_total,
        "daily_done": daily_goal and today_study >= daily_goal,
        "weekly_done": weekly_goal and weekly_total >= weekly_goal
    }

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        conn = get_db()
        existing = conn.execute(
            "SELECT id, password FROM users WHERE username=?",
            (user,)
        ).fetchone()

        if existing:
            if existing[1] != pwd:
                conn.close()
                return render_template("login.html", error="❌ Incorrect password")
            session["user_id"] = existing[0]
        else:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user, pwd)
            )
            conn.commit()
            session["user_id"] = conn.execute(
                "SELECT id FROM users WHERE username=?",
                (user,)
            ).fetchone()[0]

        conn.close()
        return redirect("/dashboard")

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    uid = session["user_id"]
    conn = get_db()

    habits = conn.execute("""
        SELECT study, phone, sleep, mood, date
        FROM habits WHERE user_id=?
        ORDER BY date DESC
    """, (uid,)).fetchall()

    weekly = conn.execute("""
        SELECT study, phone, sleep, mood, date
        FROM habits
        WHERE user_id=?
        AND date >= date('now','-6 day')
        ORDER BY date
    """, (uid,)).fetchall()

    dates = conn.execute("SELECT date FROM habits WHERE user_id=?", (uid,)).fetchall()

    goal_row = conn.execute(
        "SELECT daily_goal, weekly_goal FROM goals WHERE user_id=?",
        (uid,)
    ).fetchone()

    conn.close()

    daily_goal = goal_row[0] if goal_row else 0
    weekly_goal = goal_row[1] if goal_row else 0
    goal_progress = calculate_goal_progress(weekly, daily_goal, weekly_goal)

    summary = None
    if weekly:
        summary = {
            "total_study": sum(d[0] for d in weekly),
            "avg_phone": round(sum(d[1] for d in weekly)/len(weekly), 1),
            "avg_sleep": round(sum(d[2] for d in weekly)/len(weekly), 1),
            "mood": max([d[3] for d in weekly], key=[d[3] for d in weekly].count)
        }

    current_streak, longest_streak = calculate_streak([d[0] for d in dates])
    focus_score = calculate_focus_score(weekly)

    return render_template(
        "dashboard.html",
        habits=habits,
        summary=summary,
        current_streak=current_streak,
        longest_streak=longest_streak,
        focus_score=focus_score,
        chart_dates=[d[4] for d in weekly],
        study_data=[d[0] for d in weekly],
        phone_data=[d[1] for d in weekly],
        sleep_data=[d[2] for d in weekly],
        daily_goal=daily_goal,
        weekly_goal=weekly_goal,
        goal_progress=goal_progress
    )

# ================= SET GOALS =================
@app.route("/goals", methods=["GET", "POST"])
def goals():
    if "user_id" not in session:
        return redirect("/")

    uid = session["user_id"]
    conn = get_db()

    if request.method == "POST":
        daily = int(request.form["daily_goal"])
        weekly = int(request.form["weekly_goal"])
        conn.execute("""
            INSERT INTO goals (user_id, daily_goal, weekly_goal)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET daily_goal=?, weekly_goal=?
        """, (uid, daily, weekly, daily, weekly))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    conn.close()
    return render_template("goals.html")

# ================= LOG HABIT =================
@app.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        conn = get_db()
        conn.execute("""
            INSERT INTO habits (user_id, study, phone, sleep, mood, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            int(request.form["study"]),
            int(request.form["phone"]),
            int(request.form["sleep"]),
            request.form["mood"],
            datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    return render_template("log.html")

# ================= INSIGHTS =================
@app.route("/insights")
def insights():
    if "user_id" not in session:
        return redirect("/")

    uid = session["user_id"]
    conn = get_db()

    data = conn.execute("""
        SELECT study, phone, sleep, mood
        FROM habits
        WHERE user_id=?
    """, (uid,)).fetchall()

    conn.close()

    # ---- Mood distribution (SAFE) ----
    moods = {
        "Happy": 0,
        "Neutral": 0,
        "Sad": 0,
        "Stressed": 0
    }

    for d in data:
        if d[3] in moods:
            moods[d[3]] += 1

    return render_template(
        "insights.html",
        insights=generate_insights(data),
        score=burnout_score(data),
        moods=moods
    )



# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
