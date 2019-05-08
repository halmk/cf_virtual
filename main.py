from flask import *

import hashlib
import datetime
import problem as pm
import user as usr

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('template.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/create', methods=["GET", "POST"])
def createContest():
    print("create contest page.")
    if request.method == "GET":
        return render_template("create.html")
    else:
        contest_name = request.form["contest_name"]
        start_date = request.form["start_date"]
        start_time = request.form["start_time"]
        end_date = request.form["end_date"]
        end_time = request.form["end_time"]
        problems_url = request.form["problem_url"]

        print(contest_name)
        print(start_date)
        print(start_time)
        print(end_date)
        print(end_time)
        print(problems_url)

        return render_template("create.html")

@app.route('/history')
def history():
    res = "This page is for history of participated contest!"
    return res

@app.route('/contest/<contestID>', methods=["GET","POST"])
def contest(contestID):
    return render_template("contest.html", title=contestID,id=contestID)

if __name__ == "__main__":
    app.run(debug=True)