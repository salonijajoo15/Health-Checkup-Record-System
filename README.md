# 🩺 Health Checkup Record System

This is a web-based application built using **Flask** and **SQLite** that allows clinics or users to manage patient checkups, including CRUD operations, dynamic report generation, and statistical summaries.

---

## 📂 Features

### ✅ Requirement 1: Manage Checkups
- Add, Edit, Delete checkup records.
- Dropdowns dynamically populated using database queries (for Patients, Doctors, Checkup Types).
- Built with prepared statements for secure data handling.

### 📊 Requirement 2: Generate Report
- Select date range and checkup type to view:
  - Total number of checkups
  - First and latest checkup dates
  - Average time between checkups (in days)
- Report supports filtering and is backed by a **stored procedure** (view).

---

## 💻 Technologies Used
- **Python 3.10+**
- **Flask**
- **SQLite**
- **HTML (Jinja2 templates)**
- **Git + GitHub**

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/salonijajoo15/health-checkup-record-system.git
cd health-checkup-record-system

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with dummy data
python stage2.py

# Run the app
python main.py
