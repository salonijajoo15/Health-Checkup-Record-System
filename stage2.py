import sqlite3
from flask import Flask, jsonify
import os
if os.path.exists("health.db"):
    os.remove("health.db")

conn = sqlite3.connect("health.db")
cursor = conn.cursor()

# Patients Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_of_birth DATE,
    gender TEXT,
    email TEXT
)
""")

# Doctors Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_name TEXT NOT NULL,
    specialty TEXT,
    hospital TEXT
)
""")

# Checkup Types Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS CheckupTypes (
    checkup_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
""")

# Checkups Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Checkups (
    checkup_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    checkup_type_id INTEGER,
    date DATE,
    doctor_notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (checkup_type_id) REFERENCES CheckupTypes(checkup_type_id)
)
""")

# Insert dummy Patients
cursor.executemany("""
INSERT INTO Patients (name, date_of_birth, gender, email)
VALUES (?, ?, ?, ?)
""", [
    ('Saloni Jajoo', '2004-10-15', 'Female', 'saloni@example.com'),
    ('Bob Smith', '1987-09-21', 'Male', 'bob@example.com'),
    ('Alice Johnson', '1990-03-12', 'Female', 'alice@example.com'),
    ('Tom Clark', '1985-06-22', 'Male', 'tom@example.com'),
    ('Nina Brown', '2000-11-30', 'Female', 'nina@example.com'),
    ('John Doe', '1975-02-14', 'Male', 'john@example.com'),
    ('Emma White', '1999-08-01', 'Female', 'emma@example.com'),
    ('David Green', '1988-12-10', 'Male', 'david@example.com'),
    ('Sara Lee', '1995-09-17', 'Female', 'sara@example.com'),
    ('Leo King', '1992-05-25', 'Male', 'leo@example.com')
])

# Insert dummy Doctors
cursor.executemany("""
INSERT INTO Doctors (doctor_name, specialty, hospital)
VALUES (?, ?, ?)
""", [
    ('Dr. Sarah Lee', 'General Physician', 'City Health Center'),
    ('Dr. Mike Patel', 'Dentist', 'Downtown Dental'),
    ('Dr. Aisha Khan', 'Eye Specialist', 'Vision Plus Clinic'),
    ('Dr. Henry Ford', 'Cardiologist', 'Metro Hospital'),
    ('Dr. Lisa Ray', 'Neurologist', 'Neuro Care'),
    ('Dr. Tom Blake', 'Dermatologist', 'Skin Solutions'),
    ('Dr. Rita Paul', 'Pediatrician', 'Child First Clinic'),
    ('Dr. Neil Zee', 'ENT Specialist', 'Hear Well Hospital'),
    ('Dr. Emily Chan', 'Orthopedic', 'Bone & Joint Center'),
    ('Dr. Omar Nash', 'General Physician', 'Health Bridge')
]
)

# Insert dummy CheckupTypes
cursor.executemany("""
INSERT INTO CheckupTypes (name, description)
VALUES (?, ?)
""", [
    ('General', 'Routine health examination'),
    ('Dental', 'Teeth cleaning and checkup'),
    ('Vision', 'Eye test and vision health'),
    ('Cardio', 'Heart and blood pressure checkup'),
    ('Neuro', 'Neurological evaluation'),
    ('Skin', 'Skin and dermatology consultation'),
    ('Pediatrics', 'Child health checkup'),
    ('ENT', 'Ear, Nose, and Throat'),
    ('Orthopedic', 'Bone and joint health'),
    ('Wellness', 'General wellness and lifestyle')
]
)

# Insert dummy Checkups
cursor.executemany("""
INSERT INTO Checkups (patient_id, doctor_id, checkup_type_id, date, doctor_notes)
VALUES (?, ?, ?, ?, ?)
""", [
    (1, 1, 1, '2025-01-15', 'Vitals normal.'),
    (2, 2, 2, '2025-01-20', 'Cavity found.'),
    (3, 3, 3, '2025-01-25', 'Glasses prescribed.'),
    (4, 4, 4, '2025-02-01', 'Heart healthy.'),
    (5, 5, 5, '2025-02-05', 'Neurological baseline recorded.'),
    (6, 6, 6, '2025-02-10', 'Skin rash diagnosed.'),
    (7, 7, 7, '2025-02-15', 'Routine child checkup.'),
    (8, 8, 8, '2025-02-20', 'ENT infection noticed.'),
    (9, 9, 9, '2025-02-25', 'Knee joint strain.'),
    (10, 10, 10, '2025-03-01', 'Lifestyle improvement recommended.')
]
)

cursor.execute("CREATE INDEX IF NOT EXISTS idx_checkups_type_date ON Checkups(checkup_type_id, date)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_checkups_patient_id ON Checkups(patient_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_checkups_type ON Checkups(checkup_type_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_checkups_doctor_id ON Checkups(doctor_id)")

# Drop view if it already exists
cursor.execute("DROP VIEW IF EXISTS CheckupStats")

cursor.executescript("""
CREATE VIEW CheckupStats AS
SELECT
    checkup_type_id,
    COUNT(*) AS count,
    MIN(date) AS first_checkup,
    MAX(date) AS last_checkup
FROM Checkups
GROUP BY checkup_type_id;
""")
for row in cursor.execute("SELECT * FROM CheckupStats"):
    print(row)

