# create_db.py
import sqlite3

conn = sqlite3.connect("careerrec.db")
cur = conn.cursor()

# users table with optional skills column (comma-separated)
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password_hash TEXT,
    skills TEXT DEFAULT ''   -- store skills like "Python,SQL,TensorFlow"
);
""")

# jobs table (skills_required as comma-separated)
cur.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    skills_required TEXT
);
""")

# applications table
cur.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    job_id INTEGER,
    status TEXT,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);
""")

# Seed some jobs if none exist
cur.execute("SELECT COUNT(*) FROM jobs")
count = cur.fetchone()[0]
if count == 0:
    jobs = [
        ("Data Science Intern","QuantumLeap Inc.","Python,SQL,Machine Learning"),
        ("Web Developer Intern","TechFlow","HTML,CSS,JavaScript"),
        ("AI/ML Intern","InnovateX","Python,TensorFlow"),
        ("DevOps Intern","CloudWorks","Linux,Docker,Kubernetes"),
        ("SQL Data Analyst","DataInsight","SQL,Excel,Tableau")
    ]
    cur.executemany("INSERT INTO jobs (title, company, skills_required) VALUES (?, ?, ?)", jobs)
    print("Seeded jobs.")

conn.commit()
conn.close()
print("DB created/ready: careerrec.db")
