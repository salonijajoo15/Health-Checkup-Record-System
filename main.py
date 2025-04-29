from flask import Flask, render_template, redirect, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('health.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/checkups')
def show_checkups():
    conn = get_db_connection()
    checkups = conn.execute('''
        SELECT c.checkup_id, c.date, c.doctor_notes, 
               p.name AS patient_name, 
               d.doctor_name, 
               t.name AS type_name
        FROM Checkups c
        JOIN Patients p ON c.patient_id = p.patient_id
        JOIN Doctors d ON c.doctor_id = d.doctor_id
        JOIN CheckupTypes t ON c.checkup_type_id = t.checkup_type_id
    ''').fetchall()
    conn.close()
    return render_template('checkups.html', checkups=checkups)

@app.route('/')
def index():
    return redirect('/checkups')


@app.route('/checkups/new', methods=['GET', 'POST'])
def new_checkup():
    conn = get_db_connection()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        checkup_type_id = request.form['checkup_type_id']
        date = request.form['date']
        notes = request.form['doctor_notes']

        conn.execute('''
            INSERT INTO Checkups (patient_id, doctor_id, checkup_type_id, date, doctor_notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, doctor_id, checkup_type_id, date, notes))

        conn.commit()
        conn.close()
        return redirect('/checkups')

    # Fetch dropdown options for GET request
    patients = conn.execute('SELECT patient_id, name FROM Patients').fetchall()
    doctors = conn.execute('SELECT doctor_id, doctor_name FROM Doctors').fetchall()
    types = conn.execute('SELECT checkup_type_id, name FROM CheckupTypes').fetchall()
    conn.close()

    return render_template('new_checkup.html', patients=patients, doctors=doctors, types=types)


@app.route('/checkups/edit/<int:checkup_id>', methods=['GET', 'POST'])
def edit_checkup(checkup_id):
    conn = get_db_connection()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        checkup_type_id = request.form['checkup_type_id']
        date = request.form['date']
        doctor_notes = request.form['doctor_notes']

        conn.execute('''
            UPDATE Checkups
            SET patient_id = ?, doctor_id = ?, checkup_type_id = ?, date = ?, doctor_notes = ?
            WHERE checkup_id = ?
        ''', (patient_id, doctor_id, checkup_type_id, date, doctor_notes, checkup_id))

        conn.commit()
        conn.close()
        return redirect('/checkups')

    # GET request - fetch record and dropdown values
    checkup = conn.execute('SELECT * FROM Checkups WHERE checkup_id = ?', (checkup_id,)).fetchone()
    patients = conn.execute('SELECT patient_id, name FROM Patients').fetchall()
    doctors = conn.execute('SELECT doctor_id, doctor_name FROM Doctors').fetchall()
    types = conn.execute('SELECT checkup_type_id, name FROM CheckupTypes').fetchall()
    conn.close()

    return render_template('edit_checkup.html', checkup=checkup, patients=patients, doctors=doctors, types=types)

@app.route('/checkups/delete/<int:checkup_id>', methods=['GET'])
def delete_checkup(checkup_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Checkups WHERE checkup_id = ?', (checkup_id,))
    conn.commit()
    conn.close()
    return redirect('/checkups')

@app.route('/report', methods=['GET', 'POST'])
def checkup_report():
    conn = get_db_connection()
    checkup_types = conn.execute("SELECT * FROM CheckupTypes").fetchall()

    report_data = None
    average_gap = None  # Declare it early

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        type_id = request.form['checkup_type_id']

        # Basic stats
        report_data = conn.execute('''
            SELECT * FROM CheckupStats WHERE checkup_type_id = ?
        ''', (type_id,)).fetchone()

        # Get all checkup dates to compute average gap
        dates = conn.execute('''
            SELECT date FROM Checkups
            WHERE checkup_type_id = ? AND date BETWEEN ? AND ?
            ORDER BY date
        ''', (type_id, start_date, end_date)).fetchall()

        from datetime import datetime

        if len(dates) >= 2:
            parsed_dates = [datetime.strptime(row['date'], '%Y-%m-%d') for row in dates]
            total_gap = sum((parsed_dates[i+1] - parsed_dates[i]).days for i in range(len(parsed_dates)-1))
            average_gap = total_gap / (len(parsed_dates) - 1)

    conn.close()
    return render_template(
        'report.html',
        checkup_types=checkup_types,
        report=report_data,
        average_gap=average_gap,
        start_date=start_date if request.method == 'POST' else '',
        end_date=end_date if request.method == 'POST' else '',
        selected_type_id=int(type_id) if request.method == 'POST' else None
    )


if __name__ == '__main__':
    app.run(debug=True)
