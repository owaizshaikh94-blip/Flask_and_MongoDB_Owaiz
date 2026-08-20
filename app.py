from flask import Flask, jsonify, request, render_template_string, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["flask_assignment"]
collection = db["submissions"]


# Task 1: API route
@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Task 2: Frontend form
@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            collection.insert_one({
                "name": name,
                "email": email,
                "message": message
            })

            return redirect(url_for("success"))

        except Exception as e:
            error = str(e)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MongoDB Submission Form</title>
    </head>
    <body>
        <h1>Submit Data</h1>

        {% if error %}
            <p style="color:red;">Error: {{ error }}</p>
        {% endif %}

        <form method="POST">
            <label>Name:</label><br>
            <input type="text" name="name" required><br><br>

            <label>Email:</label><br>
            <input type="email" name="email" required><br><br>

            <label>Message:</label><br>
            <textarea name="message" required></textarea><br><br>

            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """, error=error)


# Success page
@app.route("/success")
def success():
    return """
    <h1>Data submitted successfully.</h1>
    """


if __name__ == "__main__":
    app.run(debug=True)