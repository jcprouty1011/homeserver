from flask import Flask, g, request, jsonify
# TODO As homeserver increases in complexity, transition to an ORM (SQLAlchemy)
import sqlite3
import json
app = Flask(__name__)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("homedata.db")
    return db

def query(sql, replacements=None):
    cur = get_db().cursor()
    cur.execute(sql, replacements)
    get_db().commit()
    return cur.fetchall()

def result_to_list(result):
    return list(map(lambda x: x[0], result))

@app.route("/")
def hello():
  return "Hello World! Homeserver is running."

@app.route("/maja-toothbrush-timestamps", methods=["GET", "POST"])
def maja_toothbrush_timestamps():
    if request.method == "POST":
        # TODO Add option to send a timestamp in the request body
        query("INSERT INTO maja_toothbrush_timestamps VALUES (datetime('now'))")
        return "Success", 203 # CREATED
    else:
        result = query("SELECT * FROM maja_toothbrush_timestamps")
        return jsonify({"timestamps": result_to_list(result)})

@app.route("/maja-toothbrush-timestamps/latest")
def latest():
    result = query('''SELECT * FROM maja_toothbrush_timestamps
                      ORDER BY timestamp DESC''')
    # TODO improve efficiency
    return jsonify({"timestamp": result_to_list(result)[0]})

@app.route("/health", methods=["POST"])
def health():
    if request.json is None:
        return "The Content-Type must be application/json", 400 # BAD REQUEST
    data = json.dumps(request.json)
    query("INSERT INTO health_data VALUES (?, datetime('now'))", (data,))
    return "Success", 200 # OK
