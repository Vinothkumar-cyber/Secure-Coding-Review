# Task 3 - Fixed App (Secure Coding)
# Author: Vinoth Kumar
# Purpose: Safe implementation with fixes for SQL injection and command injection

import sqlite3
from flask import Flask, request, abort
import subprocess
import shlex

app = Flask(__name__)

# Secure DB access using parameterized queries
@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    if not username or not password:
        return "Missing credentials", 400
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Fixed: use parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    result = cursor.fetchall()
    conn.close()
    
    if result:
        return "Login successful!"
    else:
        return "Invalid credentials"

# Secure ping implementation: validate input and avoid shell=True
@app.route("/ping", methods=["GET"])
def ping():
    ip = request.args.get("ip", "")
    if not ip:
        return "Missing IP", 400
    
    # Simple validation: allow only digits, dots, and letters for IPv4/hostnames
    import re
    if not re.match(r'^[A-Za-z0-9\.\-]+$', ip):
        return "Invalid IP/hostname", 400
    
    # Use subprocess with list args (no shell) to avoid command injection
    try:
        completed = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True, timeout=5)
        return f"Ping return code: {completed.returncode}\nOutput:\n{completed.stdout}"
    except Exception as e:
        return f"Error executing ping: {e}", 500

if __name__ == "__main__":
    app.run(debug=False)
