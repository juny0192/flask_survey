from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz

app = Flask(__name__)

app.config['SECRET_KEY'] = 'juny0192'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

session_key = 'responses'

@app.route('/')
def survey_info():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/survey_start', methods=["POST"])
def survey_start():
    session[session_key] = []

    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def save_answer():
    ans = request.form['ans']

    responses = session[session_key]
    responses.append(ans)
    session[session_key] = responses
    
    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route(f'/questions/<int:q_num>')
def show_survey(q_num):
    responses = session.get(session_key)

    
    if(responses is None):
        return redirect("/")
    
    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")

    if (len(responses) != q_num):
        flash("Invalid question number! Redirected you to current survey.", "error")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[q_num]
    return render_template("survey.html", question_num=q_num, question=question)

@app.route("/complete")
def complete():
    return render_template("complete.html")