from flask import Flask, render_template, request, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')                # head-less backend
import matplotlib.pyplot as plt
import os, logging

app = Flask(__name__)

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.DEBUG)

# ── Data Load & Cleaning ───────────────────────────────────────────────────
try:
    df = pd.read_csv('data.csv')                         # raw headers e.g. “Student ID”
    df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_')
                  for c in df.columns]                   # → snake_case
    for col in ['student_id', 'course_id', 'marks']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    logging.info('CSV loaded. Shape %s', df.shape)
except FileNotFoundError:
    logging.error('data.csv not found')
    df = pd.DataFrame()

# ── Routes ────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_type  = request.form.get('ID')
        id_value = request.form.get('id_value', '').strip()

        if not id_type or not id_value:
            return render_template('error.html',
                                   message="Please select an ID type and enter a value.")

        # ---------- Student ID ----------
        if id_type == 'student_id':
            try:
                sid = int(id_value)
            except ValueError:
                return render_template('error.html', message="Invalid Student ID format.")
            sub = df[df['student_id'] == sid].copy()
            if sub.empty:
                return render_template('error.html',
                                       message=f"No records found for Student ID {sid}.")
            total_marks = int(sub['marks'].sum())
            return render_template('student_details.html',
                                   student_id=sid,
                                   records=sub.to_dict(orient='records'),
                                   total_marks=total_marks)

        # ---------- Course ID ----------
        elif id_type == 'course_id':
            try:
                cid = int(id_value)
            except ValueError:
                return render_template('error.html', message="Invalid Course ID format.")
            sub = df[df['course_id'] == cid].copy()
            if sub.empty:
                return render_template('error.html',
                                       message=f"No records found for Course ID {cid}.")
            marks = sub['marks'].dropna()
            avg_marks = round(float(marks.mean()), 2)
            max_marks = int(marks.max())

            os.makedirs('static', exist_ok=True)
            img_file = f"hist_{cid}.png"
            plt.figure(figsize=(8,5))
            plt.hist(marks, bins=10, edgecolor='black', color='skyblue')
            plt.title(f'Histogram of Marks for Course {cid}')
            plt.xlabel('Marks'); plt.ylabel('Frequency')
            plt.tight_layout()
            plt.savefig(os.path.join('static', img_file), dpi=150)
            plt.close()

            return render_template('course_details.html',
                                   course_id=cid,
                                   average_marks=avg_marks,
                                   maximum_marks=max_marks,
                                   histogram_url=url_for('static', filename=img_file))

        # ---------- Unexpected ----------
        return render_template('error.html', message="Unexpected selection.")
    # GET
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
