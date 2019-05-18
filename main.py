from flask import *
from sqlalchemy.sql import func
from sqlalchemy import distinct
from sqlalchemy import desc

import hashlib
import datetime
import problem as pm
import user as usr
from setting import session
import json
import requests
from datetime import datetime, date
import time

app = Flask(__name__)

# CFのSubmissionAPIから最新20件のSubmissionを取得します #
def getSubmissionInfo():
    sub_url = "https://codeforces.com/api/user.status?handle=springroll&from=1&count=20"
    response = requests.get(sub_url)
    sub_data = json.loads(response.text)
    return sub_data["result"]

# ホームページのURLが指定されたとき #
@app.route('/')
def home():
    return render_template('template.html')

# ログインページのURLが指定されたとき #
@app.route('/login')
def login():
    return render_template('login.html')

# コンテスト作成ページのURLが指定されたとき #
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
            pr.last_updated = start_date +" "+ start_time + ":00"

            session.add(pr)
            session.commit()

            print(pr.contestID)
        
        return redirect(url_for('contest', contestID=max_contestID))

# コンテスト履歴ページのURLが指定されたとき #
@app.route('/history', methods=["GET","POST"])
def history():
    if request.method == "POST":
        contest_ID = request.form["del"]
        contest_ID = int(contest_ID)
        print(contest_ID)
        session.query(pm.Problem).filter(pm.Problem.contestID==contest_ID).delete()
        session.commit()
        print("delete finish.")
    
    contests = session.query(pm.Problem.contest,pm.Problem.contestID,pm.Problem.start_time,pm.Problem.end_time)\
            .distinct(pm.Problem.contest).order_by(desc(pm.Problem.contestID)).all()

    return render_template("history.html", cont=contests)


# あるIDのコンテストページが指定されたとき #
@app.route('/contest/<contestID>', methods=["GET","POST"])
def contest(contestID):
    contest_ID = contestID
    print("Getting Submmision data...")
    sub_data = getSubmissionInfo()
    print(" -> Finish.")
    crt = time.time()
    loc = datetime.fromtimestamp(crt)
    last_updateds = session.query(pm.Problem.last_updated).filter(pm.Problem.contestID==contest_ID).all()
    if len(last_updateds)==0:
        return redirect(url_for('history'))
    
    last_max = "1997-12-03 00:00:00"
    for last_update in last_updateds:
        lustr = last_update[0].strftime('%Y-%m-%d %H:%M:%S')
        if last_max < lustr:
            last_max = lustr

    print(last_max)
    start_t = session.query(pm.Problem.start_time).filter(pm.Problem.contestID==contest_ID).first()

    print(start_t)
    start_epoch = int(start_t[0].timestamp())
    
    for sub in sub_data:
        sub_epochtime = sub["creationTimeSeconds"]
        sub_time = datetime.fromtimestamp(sub_epochtime)
        sub_time = sub_time.strftime('%Y-%m-%d %H:%M:%S')
        if sub_time > last_max:
            print(sub_time)
            problem = str(sub["contestId"])+sub["problem"]["index"]
            update_pr = session.query(pm.Problem).filter(pm.Problem.contestID==contest_ID, pm.Problem.problem==problem).first()
            if update_pr is None:
                continue
            print(update_pr)
            for key, value in sub.items():
                print(str(key) +" "+ str(value))
            if sub["passedTestCount"] == 0:
                continue
                
            update_pr.last_updated = loc
            if sub["verdict"] == "OK":
                ac_diff = sub_epochtime - start_epoch
                ac_tm = "{:02}:{:02}".format(ac_diff//60, ac_diff%60)
                update_pr.ac_time = ac_tm
            else:
                update_pr = session.query(pm.Problem).filter(pm.Problem.contestID==contest_ID, pm.Problem.problem==problem).first()
                update_pr.penalty = update_pr.penalty + 1
            
            session.commit()

    content = session.query(pm.Problem).filter(pm.Problem.contestID==contest_ID).all()
    max_time = 0
    sum_penalty = 0
    for con in content:
        if con.ac_time is not None:
            max_time = max(max_time,int(con.ac_time.split(':')[0])*60+int(con.ac_time.split(':')[1]))
        sum_penalty += con.penalty
    
    max_time = "{:02}:{:02}".format(max_time//60, max_time%60)

    print("Complete.")
    return render_template('contest.html', cont=content, sum_time=max_time, sum_penalty=sum_penalty)

# コンテストの編集ページのURLが指定されたとき #
@app.route('/modify/<contestID>', methods=["GET","POST"])
def modify(contestID):
    contest_ID = contestID

    print("modify contest page.")
    if request.method == "GET":
        contents = session.query(pm.Problem).filter(pm.Problem.contestID==contest_ID).all()
        return render_template("modify.html", cont=contents)

    else:
        print("modify this contest.")
        session.query(pm.Problem).filter(pm.Problem.contestID==contest_ID).delete()
        session.commit()

        contest_name = request.form["contest_name"]
        start_date = request.form["start_date"]
        start_time = request.form["start_time"]
        end_date = request.form["end_date"]
        end_time = request.form["end_time"]
        problems_url = request.form.getlist("problem_url")
        pr = session.query(pm.Problem).all()
                
        for url in problems_url:
            if len(url) == 0:
                continue

            pr = pm.Problem()
            pr.problemURL = url
            pr.problem = url.split('/')[5] + url.split('/')[6]
            pr.contest = contest_name
            pr.contestID = contest_ID
            pr.participant = "springroll"
            pr.start_time = start_date +" "+ start_time + ":00"
            pr.end_time = end_date +" "+ end_time + ":00"
            pr.penalty = 0
            pr.last_updated = start_date +" "+ start_time + ":00"

            print(url)

            session.add(pr)
            session.commit()

        return redirect(url_for('contest', contestID=contest_ID))


# 実行 #
if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=False, host='0.0.0.0')