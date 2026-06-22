from flask import Blueprint, render_template, redirect, request, session, url_for, flash, send_file
import sqlite3, datetime
from utils.excel_export import export_to_excel
from utils.ai_attendance import get_low_attendance_students

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
DB = "database/attendance.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login.login'))
    conn = get_db()
    cur = conn.cursor()
    today = datetime.date.today().strftime("%Y-%m-%d")
    cur.execute("""
        SELECT s.*, a.status AS today_status 
        FROM students s
        LEFT JOIN attendance a ON s.roll_no = a.roll_no AND a.date = ?
    """, (today,))
    students = cur.fetchall()
    low_attendance = get_low_attendance_students()
    return render_template('admin_dashboard.html', students=students, low_attendance=low_attendance)

@admin_bp.route('/add_student', methods=['POST'])
def add_student():
    if 'admin' not in session:
        return redirect(url_for('login.login'))
    data = (
        request.form['name'],
        request.form['roll_no'],
        request.form['department'],
        request.form['mobile'],
        request.form['password']
    )
    conn = get_db()
    try:
        conn.execute("INSERT INTO students (name, roll_no, department, mobile, password) VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        flash("Student added successfully!", "success")
    except sqlite3.IntegrityError:
        flash("Student with this Roll Number already exists!", "danger")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'admin' not in session:
        return redirect(url_for('login.login'))

    today = datetime.date.today().strftime("%Y-%m-%d")
    conn = get_db()
    cur = conn.cursor()

    # Clear today's previous records to allow updates and avoid duplication
    cur.execute("DELETE FROM attendance WHERE date=?", (today,))

    # Fetch all students to ensure everyone is accounted for
    cur.execute("SELECT roll_no FROM students")
    all_students = [row['roll_no'] for row in cur.fetchall()]
    
    present_students = request.form.getlist('attendance')

    for roll_no in all_students:
        status = 'Present' if roll_no in present_students else 'Absent'
        cur.execute("INSERT INTO attendance (roll_no, date, status) VALUES (?, ?, ?)", (roll_no, today, status))

    conn.commit()
    flash("Attendance marked successfully!", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/export_excel')
def export_excel():
    export_to_excel()
    return send_file(
        "Attendance_Report.xlsx",
        as_attachment=True,
        download_name="Attendance_Report.xlsx"
    )
