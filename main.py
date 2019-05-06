from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    res = "This page is HOME!"
    return res

@app.route('/login')
def login():
    res = "This page is Login page!"
    return res

@app.route('/create')
def createContest():
    res = "This page is for creating contest!"
    return res

@app.route('/history')
def history():
    res = "This page is for history of participated contest!"
    return res

@app.route('/contest/<contestID>', methods=["GET","POST"])
def contest(contestID):
    return render_template("contest.html", title=contestID,id=contestID)

if __name__ == "__main__":
    app.run(debug=True)