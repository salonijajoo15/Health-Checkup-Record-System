# 🩺 Health Checkup Record System

This is a personal health record management app built using **Flask** and **SQLite**. It allows users to record, edit, and analyze medical checkups such as general, dental, and vision appointments.

---

## 📦 Features

- ✅ Add / edit / delete checkup records
- 📁 Store patient, doctor, and checkup type info
- 📊 Generate reports filtered by date and checkup type
- 📐 View summary stats:
  - Total checkups
  - First and most recent dates
  - Average time between checkups
- 💾 Uses prepared statements and a stored procedure (via view)

---

## 🖥️ Requirements

- Python 3.9+
- Flask
- SQLite (comes bundled with Python)

You can install dependencies via:

```bash
pip install Flask

