from flask import *
from sqlalchemy.sql import func

import hashlib
import datetime
import problem as pm
import user as usr
from setting import session

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
        problems_url = request.form.getlist("problem_url")

        print(contest_name)
        print(start_date)
        print(start_time)
        print(end_date)
        print(end_time)
        for url in problems_url:
            print(url)
        
        pr = session.query(pm.Problem).all()
        

        res_mx = session.query(func.max(pm.Problem.contestID).label("max_contestid")).one()
        max_contestID = res_mx.max_contestid
        print(max_contestID)
        max_contestID += 1

        
        for url in problems_url:
            pr = pm.Problem()
            pr.problemURL = url
            pr.problem = url.split('/')[5] + url.split('/')[6]
            pr.contest = contest_name
            pr.contestID = max_contestID
            pr.participant = "springroll"
            pr.start_time = start_date +" "+ start_time + ":00"
            pr.end_time = end_date +" "+ end_time + ":00"
            pr.penalty = 0

            session.add(pr)
            session.commit()

            print(pr.contestID)
        
            

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