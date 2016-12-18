from flask import Flask, jsonify, render_template, url_for
import sqlite3

app = Flask(__name__)

dbname = "humidity.sqlite3"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    result = {};
    labels = [];
    data = [];
    conn = sqlite3.connect(dbname)
    cur = conn.cursor();
    for row in cur.execute("select * from data;"):
        data.append(row[1]);
        labels.append(row[2]);
    result["labels"] = labels
    result["datasets"] = [];
    result["datasets"].append({});
    result["datasets"][0]["data"] = data

    return jsonify(ResultSet=result);

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
