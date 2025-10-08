# Productivity Hub

A beautiful and intuitive web application to track your tasks, build habits, and boost your productivity.

## Features

- Task Management - Create, complete, and track your daily tasks
- Habit Tracking - Build streaks and maintain consistency
- Dashboard Analytics - Monitor your productivity score and progress
- Celebration Rewards - Get motivated with achievement celebrations
- User Authentication - Secure login and registration system
- Personal Data - Each user has their own private workspace

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone or download the project

2. Install dependencies
```bash
pip install flask flask-sqlalchemy apscheduler werkzeug
```

3. Run the application
```bash
python app.py
```

4. Open your browser
```
http://localhost:5000
```

## Project Structure

```
productivity-hub/
├── app.py                 # Main Flask application
├── templates/
│   ├── login.html        # Login/Registration page
│   └── index2.html       # Dashboard page
└── productivity.db       # SQLite database (auto-created)
```

## How to Use

### 1. Register/Login
- Open the app and create a new account
- Or login with existing credentials

### 2. Add Tasks
- Type your task in the Tasks section
- Press Enter or click the plus button
- Check off tasks when completed

### 3. Build Habits
- Add habits you want to track daily
- Click Mark Done each day
- Watch your streak grow

### 4. Track Progress
- View your productivity score
- Monitor completed tasks
- See your total streak days
- Track active habits

## Tech Stack

- Backend: Flask, SQLAlchemy
- Frontend: HTML, CSS, JavaScript, jQuery
- Database: SQLite
- Styling: Bootstrap 5, Font Awesome
- Scheduler: APScheduler (for daily resets)

## Database Schema

The app uses 5 main tables:
- Users - User accounts and authentication
- Tasks - User tasks with status and due dates
- Habits - Daily habits with streak tracking
- DailyStreaks - Overall streak records
- UserSettings - User preferences

## Security

- Passwords are hashed using Werkzeug security
- Session-based authentication
- Protected API routes
- User data isolation

## Features Breakdown

### Dashboard Stats
- Productivity Score: Based on completed tasks and streaks
- Tasks Completed: Shows completion ratio
- Total Streak Days: Consecutive days with all habits done
- Active Habits: Number of habits being tracked

### Task Features
- Create unlimited tasks
- Mark tasks as complete
- Delete tasks
- Automatic timestamps

### Habit Features
- Daily habit tracking
- Streak counter
- Visual progress bar
- Done Today status
- Automatic streak reset if missed


## Future Enhancements

- Add task priorities and categories
- Weekly/monthly habit tracking
- Export data to CSV
- Dark mode toggle
- Email notifications
- Mobile app

