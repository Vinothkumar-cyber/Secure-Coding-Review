# Task 3 - Sample Vulnerable App
# Author: Vinoth Kumar
# Purpose: Example code to demonstrate common vulnerabilities for Secure Coding Review

import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# ❌ SQL Injection Vulnerability (unsafe string formatting)
@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Vulnerable: directly using user input in SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    
    if result:
        return "Login successful!"
    else:
        return "Invalid credentials"

# ❌ Command Injection Vulnerability (using os.system with user input)
@app.route("/ping", methods=["GET"])
def ping():
    ip = request.args.get("ip")
    os.system(f"ping -c 1 {ip}")  # dangerous: allows command injection
    return "Ping executed"

if __name__ == "__main__":
    app.run(debug=True)
