🪞 Digital Habit Mirror
A Flask-based full-stack web application designed to help users track daily habits, analyze behavioral patterns, and gain productivity insights through data-driven analysis and burnout detection.
📌 Project Overview
Digital Habit Mirror acts as a reflection system for daily habits. Instead of only recording habits, the application analyzes long-term behavior to identify consistency, productivity trends, and early burnout risks.
This project demonstrates full-stack Python development, behavioral analytics, and real-world problem solving, making it suitable for college projects, placements, and portfolios.
🎯 Problem Statement
Most habit-tracking applications focus only on reminders and data storage. They do not analyze user behavior or detect burnout symptoms.
Digital Habit Mirror solves this problem by:
Tracking habits over time
Analyzing behavioral patterns
Calculating burnout indicators
Providing meaningful productivity insights
🚀 Features
🔐 User Registration & Authentication
📝 Daily Habit Creation & Logging
📊 Interactive Dashboard
📅 Weekly Habit Summaries
🧠 Behavioral Pattern Analysis
🔥 Burnout Score Calculation
📈 Productivity Insights
🔒 Secure Session Management
🛠️ Technology Stack
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
Database
SQLite
Deployment
PythonAnywhere
🏗️ System Architecture
The project follows the MVC (Model-View-Controller) architecture:
Model → Database schema and data handling
View → HTML templates and UI
Controller → Flask routes and business logic
This structure improves scalability, maintainability, and clarity.
🧠 Burnout Score Logic
Burnout score is calculated based on:
Habit completion frequency
Missed habits
Consistency patterns
Workload intensity
Higher scores indicate potential stress or overwork, helping users take early corrective action.
📁 Project Structure
Copy code

Digital-Habit-Mirror/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│
├── app.py
├── models.py
├── requirements.txt
├── README.md
⚙️ Installation & Setup
Clone the repository
Copy code
Bash
git clone https://github.com/your-username/Digital-Habit-Mirror.git
Navigate to the project folder
Copy code
Bash
cd Digital-Habit-Mirror
Create and activate a virtual environment
Copy code
Bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
Install dependencies
Copy code
Bash
pip install -r requirements.txt
Run the application
Copy code
Bash
flask run
Open in browser
Copy code

http://127.0.0.1:5000/
📊 Use Cases
Students tracking study habits
Professionals monitoring work-life balance
Personal productivity improvement
Wellness and burnout monitoring
✅ Advantages
Simple and user-friendly interface
Data-driven behavioral insights
Early burnout detection
Real-world applicability
Scalable and extensible design
⚠️ Limitations
Manual habit entry required
No AI/ML prediction currently
Limited data visualization
🔮 Future Enhancements
AI/ML-based habit prediction
Personalized habit recommendations
Mobile application integration
Email / notification reminders
Cloud database support
Advanced analytics dashboards
🧪 Testing
Manual testing
Functional testing
Input validation and error handling
📦 Deployment
The project is deployed on PythonAnywhere using Flask WSGI configuration and environment-based dependency management.
💼 Resume Description
Digital Habit Mirror – A Flask-based full-stack web application that tracks daily habits, analyzes behavioral patterns, and calculates burnout scores to provide productivity insights. Deployed on PythonAnywhere with secure authentication and interactive dashboards.
🏁 Conclusion
Digital Habit Mirror is a practical, real-world Python project that demonstrates:
Full-stack development skills
Backend logic and analytics
Deployment experience
Problem-solving ability
It is ideal for academic submission, placements, and technical interviews.
